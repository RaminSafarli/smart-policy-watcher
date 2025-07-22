# from bs4 import BeautifulSoup, Comment
import spacy
from trafilatura import fetch_url, extract

nlp = spacy.load("en_core_web_trf")

def extract_policy_text_trafilatura_test(html_path: str) -> str:
    downloaded_html = fetch_url("https://web.archive.org/web/20250602171837/https://www.facebook.com/privacy/policy/")
    result = extract(downloaded_html)
    return result

def segment_sentences_test(text):
    # print("!!!!!!!Segmenting sentences...")
    # print(text)
    # print("!!!!!!!Segmented sentences...")
    
    """Split text into sentences using spaCy."""
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

def normalize_sentence_test(sentence: str) -> str:
    """Lowercase and remove excess whitespace (light normalization)."""
    return sentence.lower().strip()

def preprocess_policy_html_test(html_path: str) -> list:
    """Main preprocessing pipeline: HTML → clean, normalized sentences."""
    raw_text = extract_policy_text_trafilatura_test(html_path)
    sentences = segment_sentences_test(raw_text)
    return [normalize_sentence_test(s) for s in sentences]