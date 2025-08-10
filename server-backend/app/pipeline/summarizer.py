from app.pipeline.llm_instance import llm

def build_chunks_from_text_blocks(blocks, max_chars=12000):
    """Group text blocks into chunks without exceeding character limit."""
    current_chunk = []
    current_length = 0
    for block in blocks:
        block_length = len(block)
        if current_length + block_length > max_chars:
            yield current_chunk
            current_chunk = [block]
            current_length = block_length
        else:
            current_chunk.append(block)
            current_length += block_length
    if current_chunk:
        yield current_chunk


def summarize_changes(aligned_sentences, added_sentences, removed_sentences) -> str:
    all_blocks = []

    # Prepare semantically grouped blocks
    if aligned_sentences:
        for old, new, _ in aligned_sentences:
            all_blocks.append(f"- OLD: {old}\n  NEW: {new}\n")

    if added_sentences:
        for sentence in added_sentences:
            all_blocks.append(f"- ADDED: {sentence}\n")

    if removed_sentences:
        for sentence in removed_sentences:
            all_blocks.append(f"- REMOVED: {sentence}\n")

    # Group into token-safe chunks
    final_summary = []

    for chunk_blocks in build_chunks_from_text_blocks(all_blocks, max_chars=7000):
        full_prompt = (
        "[INST] <<SYS>>\n"
        "Summarize these privacy policy changes clearly for a non-technical audience.\n"
        "1) At a glance: 3–6 bullet points.\n"
        "2) Details: short grouped bullets under Collection, Sharing, Retention, Security, Rights, Other.\n"
        "No legal jargon. Stay under 200 words.\n<</SYS>>\n"
    )

        full_prompt += "\n".join(chunk_blocks)
        full_prompt += "\n\nWhat changed?\n[/INST]"

        result = llm(full_prompt,
        max_tokens=512,
        temperature=0.6,
        top_p=0.9,
        top_k=40,
        repeat_penalty=1.18,
        mirostat_mode=2, mirostat_tau=5.0, mirostat_eta=0.1,
        stop=["</s>", "[/INST]"])
        summary = result["choices"][0]["text"].strip()
        final_summary.append(summary)

    return "\n\n".join(final_summary)
