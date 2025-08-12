from __future__ import annotations
import re
import dataclasses
import spacy
from spacy.language import Language
from trafilatura import extract as trafi_extract, fetch_url

nlp = spacy.blank("en")
nlp.add_pipe("sentencizer")

@Language.component("newline_sentencizer")
def newline_sentencizer(doc):
    if not doc or len(doc) == 0:
        return doc
    for i, token in enumerate(doc[:-1]):
        if token.text in (".", "!", "?") and "\n" in token.whitespace_:
            doc[i + 1].is_sent_start = True
    text = doc.text
    char_idxs = {m.end() for m in re.finditer(r"\n\s*\n+", text)}
    for token in doc:
        if token.idx in char_idxs:
            token.is_sent_start = True
    return doc

nlp.add_pipe("newline_sentencizer", after="sentencizer")

def hard_newline_splits(text: str) -> str:
    return re.sub(r'([.!?])\s*\n+', r'\1\n\n', text)

def normalize_wraps(text: str) -> str:
    return re.sub(r'([^\n])\n(?!\n)([^\n])', r'\1 \2', text)

def normalize_sentence(sentence: str) -> str:
    return sentence.lower().strip()

def segment_sentences(text: str) -> list[str]:
    if not text:
        return []
    text = hard_newline_splits(normalize_wraps(text))
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

def extract_text_from_html(html: str) -> str:
    """Accept raw HTML string and return main text via Trafilatura."""
    return trafi_extract(html) or ""

def preprocess_policy_html_string(html: str) -> list[str]:
    """HTML string -> clean, normalized sentences."""
    raw_text = extract_text_from_html(html)
    sentences = segment_sentences(raw_text)
    return [normalize_sentence(s) for s in sentences]

def extract_policy_text_trafilatura(url: str) -> str:
    downloaded_html = fetch_url(url)
    result = trafi_extract(downloaded_html) 
    return result or ""

def preprocess_policy_html(url: str) -> list[str]:
    """URL -> clean, normalized sentences (legacy path using trafilatura.fetch_url)."""
    raw_text = extract_policy_text_trafilatura(url)
    sentences = segment_sentences(raw_text)
    return [normalize_sentence(s) for s in sentences]

