import os
from llama_cpp import Llama

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../models/llama-2-7b-chat.Q5_K_M.gguf"))
llm = Llama(model_path=model_path, n_ctx=4096)

# def summarize_changes(aligned_sentences, added_sentences, removed_sentences) -> str:
#     prompt_parts = []
    
#     if aligned_sentences:
#         prompt_parts.append("Aligned sentences changes: ")
#         for old, new, score in aligned_sentences:
#             prompt_parts.append(f"- OLD: {old}\n  NEW: {new}\n")

#     if added_sentences:
#         prompt_parts.append("Added sentences:")
#         for sentence in added_sentences:
#             prompt_parts.append(f"- {sentence}\n")
            
#     if removed_sentences:
#         prompt_parts.append("Removed sentences:")
#         for sentence in removed_sentences:
#             prompt_parts.append(f"- {sentence}\n")
            
#     full_prompt = "[INST] <<SYS>>\nYou are a helpful assistant. Summarize how a website’s privacy policy has changed. " \
#               "Write in plain, user-friendly language that non-experts can understand. " \
#               "Focus on any changes that may affect how the user’s personal information is handled, what the company can do with their data, or any rights the user may gain or lose. " \
#               "Avoid legal or overly formal language.\n<</SYS>>\n"

#     full_prompt += "\n".join(prompt_parts)
#     full_prompt += "\n\nWhat changed?\n[/INST]"

    
#     # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#     # print("Prompt for summarization:", full_prompt)  # Debugging line
#     # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#     result = llm(full_prompt, max_tokens=512)
#     summary = result["choices"][0]["text"].strip()

#     return summary


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

    for chunk_blocks in build_chunks_from_text_blocks(all_blocks, max_chars=12000):
        full_prompt = "[INST] <<SYS>>\nYou are a helpful assistant. Summarize how a website’s privacy policy has changed. " \
                      "Write in plain, user-friendly language that non-experts can understand. " \
                      "Focus on any changes that may affect how the user’s personal information is handled, what the company can do with their data, or any rights the user may gain or lose. " \
                      "Avoid legal or overly formal language.\n<</SYS>>\n"

        full_prompt += "\n".join(chunk_blocks)
        full_prompt += "\n\nWhat changed?\n[/INST]"

        result = llm(full_prompt, max_tokens=512)
        summary = result["choices"][0]["text"].strip()
        final_summary.append(summary)

    return "\n\n".join(final_summary)
