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
        # Step 1: Preprocess the HTML content to extract sentences
        old_sentences = preprocess_policy_html(req.old_html)
        new_sentences = preprocess_policy_html(req.new_html)
        
        # Step 2: Align sentences between old and new versions
        sim_matrix = compute_similarity_matrix(old_sentences, new_sentences)
        aligned_pairs, unmatched_old, unmatched_new = greedy_alignment(old_sentences, new_sentences, sim_matrix)
        
        # Step 3: Filter out non-meaningful changes
        filtered_pairs = []
        for old, new, score in aligned_pairs:
            if llm_meaningful_change_detect(old, new):
                filtered_pairs.append((old, new, score))
                
        # THERE SHOULD BE A CHECK FOR UNMATCHED SENTENCES (NEED TO BE OPTIMIZED)
        added_meaningful = [s for s in unmatched_new if llm_meaningful_change_detect("", s)]
        removed_meaningful = [s for s in unmatched_old if llm_meaningful_change_detect(s, "")]
        
        # Step 4: Summarize the meaningful changes
        if not filtered_pairs:
            return AnalyzeChangeResponse(is_meaningful=False, summary="No meaningful changes detected.")
        
        summary = summarize_changes(aligned_sentences=filtered_pairs, added_sentences=unmatched_new, removed_sentences=unmatched_old)

        return AnalyzeChangeResponse(is_meaningful=True, summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))