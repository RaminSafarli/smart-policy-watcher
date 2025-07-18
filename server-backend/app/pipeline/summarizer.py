import os
from llama_cpp import Llama

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../models/llama-2-7b-chat.Q5_K_M.gguf"))
llm = Llama(model_path=model_path, n_ctx=2048)

def summarize_changes(aligned_sentences, added_sentences, removed_sentences) -> str:
    prompt_parts = []
    
    if aligned_sentences:
        prompt_parts.append("Aligned sentences changes: ")
        for old, new, score in aligned_sentences:
            prompt_parts.append(f"- OLD: {old}\n  NEW: {new}\n")

    if added_sentences:
        prompt_parts.append("Added sentences:")
        for sentence in added_sentences:
            prompt_parts.append(f"- {sentence}\n")
            
    if removed_sentences:
        prompt_parts.append("Removed sentences:")
        for sentence in removed_sentences:
            prompt_parts.append(f"- {sentence}\n")
            
    full_prompt = "[INST] <<SYS>>\nYou are a helpful assistant that summarizes changes in privacy policies. " \
                  "Write a clear, concise summary of what has changed in the data handling, retention, or sharing terms.\n<</SYS>>\n"
                  
    full_prompt += "\n".join(prompt_parts)
    full_prompt += "\n\nSummarize these changes in 3–5 sentences:\n[/INST]"
    
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Prompt for summarization:", full_prompt)  # Debugging line
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
