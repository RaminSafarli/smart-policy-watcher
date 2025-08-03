from llama_cpp import Llama
import os

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../models/llama-2-7b-chat.Q5_K_M.gguf"))
llm = Llama(model_path=model_path, n_ctx=4096)