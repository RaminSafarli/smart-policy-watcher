import os
from difflib import ndiff
from app.pipeline.preprocessor import preprocess_policy_html
from app.pipeline.aligner import compute_similarity_matrix, greedy_alignment
from app.pipeline.llm_filter import llm_meaningful_change_detect
from app.pipeline.summarizer import summarize_changes

def load_html_file(filepath: str) -> str:
    """Load raw HTML content from a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def print_diff(old_sentences, new_sentences):
    """Print side-by-side semantic-level diff between sentence lists."""
    print("\n🔍 Differences between old and new policy sentences:\n")
    diff = list(ndiff(old_sentences, new_sentences))
    for line in diff:
        if line.startswith("+ "):
            print(f"\033[92m{line}\033[0m")  # green = added
        elif line.startswith("- "):
            print(f"\033[91m{line}\033[0m")  # red = removed
        elif line.startswith("? "):
            continue  # skip metadata lines
        else:
            print(f"  {line}")

if __name__ == "__main__":
    # ==== INPUT FILES ====
    old_path = "./data/demo/2023-01.html"
    new_path = "./data/demo/2024-01.html"

    if not os.path.exists(old_path) or not os.path.exists(new_path):
        print("❌ Test HTML files not found.")
        exit(1)

    # ==== PREPROCESS ====
    old_html = load_html_file(old_path)
    new_html = load_html_file(new_path)

    old_sentences = preprocess_policy_html(old_html)
    new_sentences = preprocess_policy_html(new_html)

    print(f"🔍 Loaded {len(old_sentences)} old sentences and {len(new_sentences)} new sentences.")

    # ==== SENTENCE ALIGNMENT ====
    sim_matrix = compute_similarity_matrix(old_sentences, new_sentences)
    aligned, removed, added = greedy_alignment(old_sentences, new_sentences, sim_matrix)

    # ==== TEST PRINT TO SEE PAIRS ====
    print("\n🔗 Aligned Sentences:")
    for old, new, score in aligned:
        print(f"[{score:.2f}]")
        print(f"OLD: {old}")
        print(f"NEW: {new}\n")

    print("❌ Removed Sentences:")
    for s in removed:
        print(f"- {s}")

    print("➕ Added Sentences:")
    for s in added:
        print(f"+ {s}")
        
    print("################# MEANINGFUL DETECTION STARTS HERE #################")
    meaningful_changes = []
    for old, new, score in aligned:
        if 0.4 < score < 0.95:
            if llm_meaningful_change_detect(old, new):
                meaningful_changes.append((old, new, score))
                
    print("\n🔍 Meaningful Changes Detected:")
    for old, new, score in meaningful_changes:
        print("##############")
        print(f"OLD: {old}")
        print(f"NEW: {new}\n")
        print(score)
        print("##############")
        
        
    # ==== SUMMARIZATION STARTS ====
    summarize_changes(meaningful_changes, added, removed)