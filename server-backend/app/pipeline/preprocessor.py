# from bs4 import BeautifulSoup, Comment
import spacy
from trafilatura import extract, fetch_url

nlp = spacy.load("en_core_web_trf")

def extract_policy_text_trafilatura(html_path: str) -> str:
    downloaded_html = fetch_url(html_path)
    result = extract(downloaded_html)
    return result

def segment_sentences(text: str) -> list:
    # print("Segmenting test sentences...")
    # print(text)
    # print("Segmented test sentences...")
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