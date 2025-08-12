from llama_cpp import Llama, LlamaGrammar
import os

try:
    from llama_cpp import LlamaGrammar
    _HAS_GRAMMAR = True
except Exception:
    LlamaGrammar = None
    _HAS_GRAMMAR = False

def _compile_grammar(grammar_str: str):
    if not _HAS_GRAMMAR:
        return None
    try:
        return LlamaGrammar.from_string(grammar_str)
    except Exception:
        return None

YESNO_GRAMMAR_STR = r"""
root ::= "yes" | "no"
"""
SUMMARY_GRAMMAR_STR = r'''
root ::= object
object ::= "{" ws "\"short_summary\"" ws ":" ws string ws "," ws "\"detailed_summary\"" ws ":" ws string ws "}"
string ::= "\"" chars "\""
chars ::= char*
char ::= [^"\\] | escape
escape ::= "\\" ["\\/bfnrt] | "\\u" hex hex hex hex
hex ::= [0-9a-fA-F]
ws ::= [ \t\n\r]*
'''

YESNO_GRAMMAR = _compile_grammar(YESNO_GRAMMAR_STR)
SUMMARY_GRAMMAR = _compile_grammar(SUMMARY_GRAMMAR_STR)


# ---- Singleton LLM instance ----
_model = None

def get_llm():
    global _model
    if _model is None:
        model_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "../../models/llama-2-7b-chat.Q5_K_M.gguf"
        ))
        _model = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_gpu_layers=0,
        )
    return _model

llm = get_llm()

