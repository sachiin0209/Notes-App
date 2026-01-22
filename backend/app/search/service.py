# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
from app.notes.services import get_notes_for_user

# Load model once (global)
# model = SentenceTransformer('all-MiniLM-L6-v2')
model = None

def semantic_search(user_id, query):
    """Return notes whose content is semantically similar to query."""
    notes = get_notes_for_user(user_id)
    if not notes:
        return []

    return []

    # Compute embeddings
    # query_emb = model.encode(query)
    # contents = [note['content'] for note in notes]
    # content_embs = model.encode(contents)

    # # Compute cosine similarities
    # sims = cosine_similarity([query_emb], content_embs)[0]
    
    # # Pair scores with notes, filter by a threshold or sort
    # results = []
    # for score, note in sorted(zip(sims, notes), reverse=True, key=lambda x: x[0]):
    #     if score > 0.5:  # threshold for relevance
    #         results.append({'note': note, 'score': float(score)})
    # return results
