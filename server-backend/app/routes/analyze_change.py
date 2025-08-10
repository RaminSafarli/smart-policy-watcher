from fastapi import APIRouter, HTTPException

from app.models.schemas import AnalyzeChangeRequest, AnalyzeChangeResponse
from app.pipeline.preprocessor import preprocess_policy_html
from app.pipeline.aligner import compute_similarity_matrix, greedy_alignment
from app.pipeline.llm_filter import llm_meaningful_change_detect
from app.pipeline.summarizer import summarize_changes



router = APIRouter()

@router.post("/analyze_change", response_model=AnalyzeChangeResponse)
def analyze_change(req: AnalyzeChangeRequest):
    try:
        old_sentences = req.old_sentences
        new_sentences = req.new_sentences
        
        sim_matrix = compute_similarity_matrix(old_sentences, new_sentences)
        aligned_pairs, unmatched_old, unmatched_new = greedy_alignment(old_sentences, new_sentences, sim_matrix)
        
        filtered_pairs = []
        for old, new, score in aligned_pairs:
            if 0.4 < score < 0.95:
                if llm_meaningful_change_detect(old, new):
                    filtered_pairs.append((old, new, score))

        added_meaningful = [s for s in unmatched_new if llm_meaningful_change_detect("", s)]
        removed_meaningful = [s for s in unmatched_old if llm_meaningful_change_detect(s, "")]

        if not (filtered_pairs or added_meaningful or removed_meaningful):
            return AnalyzeChangeResponse(is_meaningful=False, summary="No meaningful changes detected.")
        
        summary = summarize_changes(aligned_sentences=filtered_pairs, added_sentences=added_meaningful, removed_sentences=removed_meaningful)

        return AnalyzeChangeResponse(is_meaningful=True, summary=summary)
        # return AnalyzeChangeResponse(is_meaningful=True, summary="OKAY")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
