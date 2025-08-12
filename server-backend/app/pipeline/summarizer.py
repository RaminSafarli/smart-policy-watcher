# #########################################
# from app.pipeline.llm_instance import llm, SUMMARY_GRAMMAR

# def build_chunks_from_text_blocks(blocks, max_chars=7000):  # ~ safer vs 4k tokens
#     current_chunk, current_len = [], 0
#     for block in blocks:
#         blen = len(block)
#         if current_len and current_len + blen > max_chars:
#             yield current_chunk
#             current_chunk, current_len = [block], blen
#         else:
#             current_chunk.append(block)
#             current_len += blen
#     if current_chunk:
#         yield current_chunk

# def summarize_changes(aligned_sentences, added_sentences, removed_sentences) -> str:
#     all_blocks = []

#     # Keep ordering stable for determinism
#     if aligned_sentences:
#         for old, new, _ in aligned_sentences:
#             all_blocks.append(f"- EDIT:\n  OLD: {old}\n  NEW: {new}\n")

#     if added_sentences:
#         for s in added_sentences:
#             all_blocks.append(f"- ADD:\n  TEXT: {s}\n")

#     if removed_sentences:
#         for s in removed_sentences:
#             all_blocks.append(f"- REMOVE:\n  TEXT: {s}\n")

#     summaries = []
#     for chunk in build_chunks_from_text_blocks(all_blocks, max_chars=7000):
#         prompt = (
#             "[INST] <<SYS>>\n"
#             "You write concise, neutral change summaries of privacy policies for end users.\n"
#             "Return ONLY JSON\n"
#             "1) Short summary - Most important update in privacy policy\n"
#             "2) Details — details of changes, not too long, in plain, understandable languge\n"
#             "No legal advice, no speculation, no marketing language. Keep it under ~150–200 words per chunk.\n"
#             "<</SYS>>\n"
#             "CHANGES:\n" + "\n".join(chunk) + "\n\n"
#             "Write the summary now.\n[/INST]"
#         )

#         result = llm(
#             prompt,
#             max_tokens=500,          
#             temperature=0.2,
#             grammar=SUMMARY_GRAMMAR,
#             top_p=0.9,
#             top_k=40,
#             repeat_penalty=1.18,
#             mirostat_mode=2, mirostat_tau=5.0, mirostat_eta=0.1,
#             stop=["</s>", "[/INST]"]
#         )
#         summaries.append(result["choices"][0]["text"].strip())

#     return "\n\n".join(summaries)

#################

# from app.pipeline.llm_instance import llm

# def build_chunks_from_text_blocks(blocks, max_chars=7000):
#     current_chunk, current_len = [], 0
#     for block in blocks:
#         blen = len(block)
#         if current_len and current_len + blen > max_chars:
#             yield current_chunk
#             current_chunk, current_len = [block], blen
#         else:
#             current_chunk.append(block)
#             current_len += blen
#     if current_chunk:
#         yield current_chunk

# def summarize_changes(aligned_sentences, added_sentences, removed_sentences) -> str:
#     all_blocks = []

#     # Stable ordering for reproducible output
#     if aligned_sentences:
#         for old, new, _ in aligned_sentences:
#             all_blocks.append(f"- EDIT:\n  OLD: {old}\n  NEW: {new}\n")
#     if added_sentences:
#         for s in added_sentences:
#             all_blocks.append(f"- ADD:\n  TEXT: {s}\n")
#     if removed_sentences:
#         for s in removed_sentences:
#             all_blocks.append(f"- REMOVE:\n  TEXT: {s}\n")

#     summaries = []
#     for chunk in build_chunks_from_text_blocks(all_blocks, max_chars=7000):
#         prompt = (
#             "[INST] <<SYS>>\n"
#             "You are an assistant that summarizes privacy policy changes for a browser extension.\n"
#             "Return ONLY valid JSON, no other text. The JSON schema is:\n"
#             "{\n"
#             "  \"headline\": string (not too long),\n"
#             "  \"details\": {\n"
#             "    \"Collection\": [string...],\n"
#             "    \"Use/Sharing\": [string...],\n"
#             "    \"Retention\": [string...],\n"
#             "    \"Security\": [string...],\n"
#             "    \"User Rights\": [string...],\n"
#             "    \"Other\": [string...]\n"
#             "  }\n"
#             "}\n"
#             "Follow these rules:\n"
#             "- Keep bullets short, accurate, plain language.\n"
#             "- Skip categories with no changes (return empty array).\n"
#             "- Never add extra commentary.\n"
#             "<</SYS>>\n"
#             "CHANGES:\n" + "\n".join(chunk) + "\n"
#             "[/INST]"
#         )


#         result = llm(
#             prompt,
#             max_tokens=400,
#             temperature=0.2,
#             top_p=0.9,
#             top_k=40,
#             repeat_penalty=1.18,
#             mirostat_mode=2, mirostat_tau=5.0, mirostat_eta=0.1,
#             stop=["</s>", "[/INST]"]
#         )
#         summaries.append(result["choices"][0]["text"].strip())

#     return "\n\n".join(summaries)

# app/pipeline/summarizer.py

import json
import re
from typing import Optional, List
from app.pipeline.llm_instance import llm, SUMMARY_GRAMMAR

# ---------------------------
# Helpers (kept lightweight)
# ---------------------------

def build_chunks_from_text_blocks(blocks: List[str], max_chars: int = 7000):
    current_chunk, current_len = [], 0
    for block in blocks:
        blen = len(block)
        if current_len and current_len + blen > max_chars:
            yield current_chunk
            current_chunk, current_len = [block], blen
        else:
            current_chunk.append(block)
            current_len += blen
    if current_chunk:
        yield current_chunk

def _safe_json_from_text(text: str) -> Optional[dict]:
    """
    Extract first {...} and parse.
    """
    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        try:
            return json.loads(text)
        except Exception:
            pass
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end+1])
        except Exception:
            return None
    return None

def _choose_short_summary(candidates: List[str], detailed_fallback: str) -> str:
    """
    Pick the first non-empty, <= 140 chars if possible; otherwise trim.
    """
    for c in candidates:
        if isinstance(c, str):
            s = c.strip()
            if s:
                return s if len(s) <= 140 else (s[:137] + "…")
    # fallback from detailed
    df = (detailed_fallback or "").strip()
    if not df:
        return "Changes detected in the privacy policy"
    # take first sentence-ish
    first = re.split(r"(?<=[.!?])\s+", df, maxsplit=1)[0]
    return first if len(first) <= 140 else (first[:137] + "…")

def _join_detailed(parts: List[str]) -> str:
    cleaned = [p.strip() for p in parts if isinstance(p, str) and p.strip()]
    if not cleaned:
        return ""
    # Merge with a blank line; keep total length reasonable (~1200 chars)
    merged = "\n\n".join(cleaned)
    return merged[:1200]


# ---------------------------
# Main entry
# ---------------------------

def summarize_changes(aligned_sentences, added_sentences, removed_sentences) -> str:
    """
    Produces a minimal, structured summary:
    {
      "short_summary": "one sentence, ≤140 chars",
      "detailed_summary": "1–4 sentences or brief bullets in plain language"
    }
    """
    # Build blocks from your existing pipeline (order preserved)
    all_blocks = []
    if aligned_sentences:
        for old, new, _ in aligned_sentences:
            all_blocks.append(f"- EDIT:\n  OLD: {old}\n  NEW: {new}\n")
    if added_sentences:
        for s in added_sentences:
            all_blocks.append(f"- ADD:\n  TEXT: {s}\n")
    if removed_sentences:
        for s in removed_sentences:
            all_blocks.append(f"- REMOVE:\n  TEXT: {s}\n")

    # If somehow nothing came in, return a neutral summary
    if not all_blocks:
        return json.dumps({
            "short_summary": "No meaningful changes detected",
            "detailed_summary": "The latest version appears equivalent to the previous one."
        }, ensure_ascii=False)

    # Simple guidance for the model
    SYSTEM_RULES = (
        "You summarize privacy policy changes for a browser extension.\n"
        "Return ONLY a single JSON object with exactly two fields:\n"
        "{\n"
        "  \"short_summary\": string,   // one sentence, ≤140 chars, plain language, state the most important change\n"
        "  \"detailed_summary\": string // 1–4 sentences or brief bullets; explain what changed and why it matters\n"
        "}\n"
        "Rules:\n"
        "- Use plain language. No legalese, no citations.\n"
        "- If wording-only or neutral, skip it.\n"
        "- If unsure where to focus, pick the change with the biggest impact on users (sharing/collection/retention/rights).\n"
        "- Output MUST be valid JSON. No extra text or code fences.\n"
    )

    short_candidates = []
    detailed_parts = []

    # Process by chunks to stay within context limits
    for chunk in build_chunks_from_text_blocks(all_blocks, max_chars=7000):
        prompt = (
            "[INST] <<SYS>>\n" +
            SYSTEM_RULES +
            "<</SYS>>\n" +
            "CHANGES:\n" + "\n".join(chunk) + "\n" +
            "[/INST]"
        )

        kwargs = dict(
            max_tokens=600,
            temperature=0.2,
            top_p=0.9,
            top_k=40,
            repeat_penalty=1.18,
            mirostat_mode=2, mirostat_tau=5.0, mirostat_eta=0.1,
            stop=["</s>", "[/INST]"]
        )

        # Enforce structure via grammar when available
        try:
            if SUMMARY_GRAMMAR is not None:
                result = llm(prompt, grammar=SUMMARY_GRAMMAR, **kwargs)
            else:
                result = llm(prompt, **kwargs)
        except (TypeError, AttributeError):
            result = llm(prompt, **kwargs)

        text = result["choices"][0]["text"].strip()
        obj = _safe_json_from_text(text) or {}

        short = obj.get("short_summary", "") if isinstance(obj, dict) else ""
        detailed = obj.get("detailed_summary", "") if isinstance(obj, dict) else ""
        short_candidates.append(short)
        detailed_parts.append(detailed)

    # Merge multi-chunk outputs
    detailed_merged = _join_detailed(detailed_parts)
    short_final = _choose_short_summary(short_candidates, detailed_merged)

    # Safe fallback if model gave absolutely nothing useful
    if not detailed_merged:
        detailed_merged = "Changes were detected, but the summary could not be formatted. Please review the highlighted edits."

    return json.dumps({
        "short_summary": short_final,
        "detailed_summary": detailed_merged
    }, ensure_ascii=False)
