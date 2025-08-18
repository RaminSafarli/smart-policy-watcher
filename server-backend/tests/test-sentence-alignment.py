from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_similarity_matrix(old_sentences, new_sentences):
     """Return cosine similarity matrix between two lists of sentences."""
     old_embeddings = model.encode(old_sentences)
     new_embeddings = model.encode(new_sentences)
     return cosine_similarity(old_embeddings, new_embeddings)


def greedy_alignment(old_sentences, new_sentences, sim_matrix, sim_threshold=0.6):
    """Align sentences using greedy matching strategy."""
    aligned_pairs = []
    matched_old = set()
    matched_new = set()

    while True:
        max_sim = -1
        best_pair = (-1, -1)

        for i in range(len(old_sentences)):
            if i in matched_old:
                continue
            for j in range(len(new_sentences)):
                if j in matched_new:
                    continue
                sim = sim_matrix[i][j]
                if sim > max_sim:
                    max_sim = sim
                    best_pair = (i, j)

        if max_sim < sim_threshold:
            break

        i, j = best_pair
        aligned_pairs.append((old_sentences[i], new_sentences[j], max_sim))
        matched_old.add(i)
        matched_new.add(j)

    unmatched_old = [old_sentences[i] for i in range(len(old_sentences)) if i not in matched_old]
    unmatched_new = [new_sentences[j] for j in range(len(new_sentences)) if j not in matched_new]

    return aligned_pairs, unmatched_old, unmatched_new
 # <-- adjust if in same file

old_sentences = [
    "We may collect information about your device to improve application performance.",
    "Your data will be deleted within 60 days after account closure.",
    "We use your activity logs to recommend relevant content.",
]

new_sentences = [
    "To optimize how the app runs, we may gather details about the device you use.",   # paraphrase → ~0.74
    "After you close your account, your data will be erased within two months.",       # rephrased → ~0.76
    "Relevant suggestions are generated based on records of how you use the service.", # paraphrase → ~0.72
]




# Compute similarity matrix
model = SentenceTransformer("all-MiniLM-L6-v2")
sim_matrix = compute_similarity_matrix(old_sentences, new_sentences)

# Test different thresholds
# thresholds = [0.4, 0.6, 0.7, 0.8]
thresholds = [0.4]

for t in thresholds:
    aligned, un_old, un_new = greedy_alignment(old_sentences, new_sentences, sim_matrix, sim_threshold=t)
    print("\n" + "="*70)
    print(f"THRESHOLD = {t}")
    print(f"Aligned: {len(aligned)} | Unmatched old: {len(un_old)} | Unmatched new: {len(un_new)}\n")
    for old, new, score in aligned:
        print(f"[{score:.3f}]\n  OLD: {old}\n  NEW: {new}\n")
    if un_old:
        print("Unmatched OLD:") 
        for s in un_old: print("  -", s)
    if un_new:
        print("\nUnmatched NEW:")
        for s in un_new: print("  -", s)
