# from bs4 import BeautifulSoup, Comment
import spacy
import trafilatura

nlp = spacy.load("en_core_web_trf")

def extract_policy_text_trafilatura(html: str) -> str:
    return trafilatura.extract(html)

def segment_sentences(text: str) -> list:
    """Split text into sentences using spaCy."""
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

def normalize_sentence(sentence: str) -> str:
    """Lowercase and remove excess whitespace (light normalization)."""
    return sentence.lower().strip()

def preprocess_policy_html(html: str) -> list:
    """Main preprocessing pipeline: HTML → clean, normalized sentences."""
    raw_text = extract_policy_text_trafilatura(html)
    sentences = segment_sentences(raw_text)
    return [normalize_sentence(s) for s in sentences]