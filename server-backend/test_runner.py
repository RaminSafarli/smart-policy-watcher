import os
import time
from difflib import ndiff
from app.pipeline.preprocessor import preprocess_policy_html
from app.pipeline.aligner import compute_similarity_matrix, greedy_alignment
from app.pipeline.llm_filter import  batch_llm_meaningful_change_detect, llm_meaningful_change_detect
from app.pipeline.summarizer import summarize_changes
from app.pipeline.test_prep import preprocess_policy_html_test

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
    
    start = time.time()
    
    # ==== INPUT FILES ====
    # old_path = "./data/demo/2023-01.html"
    # new_path = "./data/demo/2024-01.html"
    old_path = "./data/7-april-fb.html"
    new_path = "./data/16-june-fb.html"

    if not os.path.exists(old_path) or not os.path.exists(new_path):
        print("❌ Test HTML files not found.")
        exit(1)

    # ==== PREPROCESS ====
    old_html = load_html_file(old_path)
    new_html = load_html_file(new_path)

    old_sentences = preprocess_policy_html("https://web.archive.org/web/20240928153923/https://telegram.org/privacy")
    new_sentences = preprocess_policy_html("https://web.archive.org/web/20250724132406/https://telegram.org/privacy")

    print(f"🔍 Loaded {len(old_sentences)} old sentences and {len(new_sentences)} new sentences.")
    print("🔍 Old sentences sample!!!!!!!!!!!!!!!!!")
    for i, s in enumerate(old_sentences):
        print(f"{i+1}. {s}")
    print("END!!!!!!!!!!!!!!!!")
    print("!!!!!NEW SENTENCES SAMPLE!!!!!!!!!!!!!!!!!")
    for i, s in enumerate(new_sentences):
        print(f"{i+1}. {s}")    
    print("END!!!!!!!!!!!!!!!!")
    # print("🔍 Old sentences sample!!!!!!!!!!!!!!!!!")
    # for i, s in enumerate(old_sentences):
    #     print(f"{i+1}. {s}")
    # print("END!!!!!!!!!!!!!!!!")

    # ==== SENTENCE ALIGNMENT ====
    sim_matrix = compute_similarity_matrix(old_sentences, new_sentences)
    aligned, removed, added = greedy_alignment(old_sentences, new_sentences, sim_matrix)

    # print(f"🔗 Aligned {len(aligned)} sentence pairs, {len(removed)} removed, and {len(added)} added sentences.")
    # for old, new, score in aligned:
    #     print(f"🔗 Aligned Pair:")
    #     print(f"[{score:.2f}]")
    #     print(f"OLD: {old}")
    #     print(f"NEW: {new}\n")
    
    # for s in removed:
    #     print(f"❌ Removed: {s}")
        
    # for s in added:
    #     print(f"✔ Added: {s}")    
    
    
    # ==== TEST PRINT TO SEE PAIRS ====
    # print("\n🔗 Aligned Sentences:")
    # for old, new, score in aligned:
    #     print(f"[{score:.2f}]")
    #     print(f"OLD: {old}")
    #     print(f"NEW: {new}\n")

    # print("❌ Removed Sentences:")
    # for s in removed:
    #     print(f"- {s}")

    # print("➕ Added Sentences:")
    # for s in added:
    #     print(f"+ {s}")
        
    print("################# MEANINGFUL DETECTION STARTS HERE #################")
    meaningful_changes = []
    for old, new, score in aligned:
        if 0.4 < score < 0.95:
            if llm_meaningful_change_detect(old, new):
                meaningful_changes.append((old, new, score))
    # # Step 1: Filter by similarity score first
    # to_check = [(old, new, score) for old, new, score in aligned if 0.4 < score < 0.95]
    # sentence_pairs = [(old, new) for old, new, _ in to_check]

    # # Step 2: Run LLM in batches
    # results = batch_llm_meaningful_change_detect(sentence_pairs, batch_size=10)

    # # Step 3: Keep only meaningful ones
    # meaningful_changes = [
    #     (old, new, score) for (old, new, score), is_meaningful in zip(to_check, results) if is_meaningful
    # ]

                
    print("\n🔍 Meaningful Changes Detected:")
    print("#################")
    print(f"Found {len(meaningful_changes)} meaningful changes out of {len(aligned)} aligned pairs.")
    for old, new, score in meaningful_changes:
        print(f"[{score:.2f}]")
        print(f"OLD: {old}")
        print(f"NEW: {new}\n")
    print("#################")
    
    print("@@@@@@@@@@@@@")
    for word in removed:
        print(f"❌ Removed: {word}")
    print("@@@@@@@@@@@@@")
    print("@@@@@@@@@@@@@")
    for word in added:
        print(f"✔ Removed: {word}")
    print("@@@@@@@@@@@@@")

        
    # ==== SUMMARIZATION STARTS ====
    summary = summarize_changes(meaningful_changes, added, removed)
    print("\n📄 Summary of Changes:"
          f"\n{summary}\n")
    
    end = time.time()
    print(f"⏱️ Total time taken: {end - start:.2f} seconds")
    
    