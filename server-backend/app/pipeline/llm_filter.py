import os
from llama_cpp import Llama

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../models/llama-2-7b-chat.Q5_K_M.gguf"))
llm = Llama(model_path=model_path, n_ctx=2048)

def llm_meaningful_change_detect(old_sentence: str, new_sentence: str) -> bool:
    prompt = f"""[INST] <<SYS>>
    You are a helpful assistant focused on analyzing changes in privacy policies. Answer with one word only.
    <</SYS>>
    OLD: {old_sentence}
    NEW: {new_sentence}

    Is this a meaningful change that affects user privacy? Answer with one word: yes or no.
    [/INST]"""  
    

    output = llm(prompt, max_tokens=10)
    response = output["choices"][0]["text"].strip().lower()
    # print("***************LLM Analysis:")
    # print("old: " + old_sentence)
    # print("new: " + new_sentence)
    # print(f"LLM Response: {response}")  # Debugging output
    # print("***************")
    return "yes" in response
