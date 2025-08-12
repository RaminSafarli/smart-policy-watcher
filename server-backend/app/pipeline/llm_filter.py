from app.pipeline.llm_instance import llm, YESNO_GRAMMAR
import re

YES = re.compile(r'^\s*yes\s*$', re.IGNORECASE)
NO  = re.compile(r'^\s*no\s*$', re.IGNORECASE)

def _call_yes_no(prompt: str) -> str:
    kwargs = dict(
        max_tokens=2,
        temperature=0.0,
        top_p=0.9,
        top_k=40,
        repeat_penalty=1.18,
        stop=["</s>", "[/INST]", "\n"],
    )
    # Try grammar; fallback if unsupported
    # 1️⃣ Check grammar loaded
    assert YESNO_GRAMMAR is not None, "YESNO_GRAMMAR is None — not being applied!"
    try:
        if YESNO_GRAMMAR is not None:
            print("YESNO_GRAMMAR WORKED LLM FILTER")
            out = llm(prompt, grammar=YESNO_GRAMMAR, **kwargs)
        else:
            out = llm(prompt, **kwargs)
    except (TypeError, AttributeError):
        out = llm(prompt, **kwargs)
    return out["choices"][0]["text"].strip()

def llm_meaningful_change_detect(old_sentence: str, new_sentence: str) -> bool:
    old_sentence = (old_sentence or "")[:1000].strip()
    new_sentence = (new_sentence or "")[:1000].strip()

    prompt = f"""[INST] <<SYS>>
        Output ONLY one word: yes or no.
        A meaningful change affects collection, storage, sharing, retention, security, or user rights.
        Stylistic/grammatical edits without policy effect are not meaningful.
        No explanations.
        <</SYS>>
        OLD: {old_sentence}
        NEW: {new_sentence}
        Meaningful change? yes or no
        [/INST]"""

    resp = _call_yes_no(prompt)
    if YES.match(resp): return True
    if NO.match(resp):  return False

    # # One ultra-strict retry
    # retry = f"""[INST] <<SYS>>Output EXACTLY one word: yes or no.<</SYS>>
    #     OLD: {old_sentence}
    #     NEW: {new_sentence}
    #     [/INST]"""
    # resp = _call_yes_no(retry)
    # if YES.match(resp): return True
    # if NO.match(resp):  return False
    return False

