from bs4 import BeautifulSoup, Comment
import spacy
import trafilatura

nlp = spacy.load("en_core_web_sm")

def extract_policy_text_trafilatura(html: str) -> str:
    return trafilatura.extract(html)

# def extract_text_from_html(html_content: str) -> str:
#     """
#     Extracts text from HTML content using BeautifulSoup.
    
#     Args:
#         html_content (str): The HTML content as a string.
        
#     Returns:
#         str: The extracted text.
#     """
#     # soup = BeautifulSoup(html_content, "html.parser")   
    
#     # all_text_nodes = soup.find_all(string=True)
#     # visible_texts = filter(is_visible_text, all_text_nodes)

#     # cleaned = [str(t).strip() for t in visible_texts if str(t).strip()]
#     # return " ".join(cleaned)
#     soup = BeautifulSoup(html_content, "html.parser")

#     # Remove script/style/head/meta tags
#     for tag in soup(["script", "style", "head", "meta", "noscript", "iframe", "footer", "nav"]):
#         tag.decompose()

#     # Get clean visible text
#     text = soup.get_text(separator=' ')
#     return text.strip()

# def is_visible_text(elem):
#     """
#     Return False for strings we don’t want.
#     """
#     if elem.parent.name in (
#         "style",    
#         "script",   
#         "head",     
#         "title",    
#         "meta",
#         "a",     
#         "[document]"
#     ):
#         return False

#     if isinstance(elem, Comment):
#         return False

#     return True

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