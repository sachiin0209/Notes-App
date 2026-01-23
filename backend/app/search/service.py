from app.notes.services import get_notes_for_user

# Toggle this when you actually wire embeddings
NLP_ENABLED = False

try:
    if NLP_ENABLED:
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity

        model = SentenceTransformer("all-MiniLM-L6-v2")
        print("DEBUG: NLP model loaded successfully", flush=True)
    else:
        model = None
        print("DEBUG: NLP disabled, using keyword fallback", flush=True)

except Exception as e:
    print(f"DEBUG: Failed to load NLP model: {e}", flush=True)
    model = None
    NLP_ENABLED = False


def semantic_search(user_id, query):
    """Return notes whose content is semantically similar to query."""
    print(f"DEBUG: Semantic search called for user_id={user_id}, query='{query}'", flush=True)

    if not isinstance(query, str) or not query.strip():
        print("DEBUG: Empty or invalid query", flush=True)
        return []

    notes = get_notes_for_user(user_id)
    if not notes:
        print("DEBUG: No notes found for user", flush=True)
        return []

    # -----------------------
    # Fallback: keyword search
    # -----------------------
    if not NLP_ENABLED or model is None:
        q = query.lower()
        results = []

        for note in notes:
            content = (note.get("content") or "").lower()
            title = (note.get("title") or "").lower()

            if q in content or q in title:
                results.append({
                    "note": note,
                    "score": 1.0
                })

        print(f"DEBUG: Keyword search matched {len(results)} notes", flush=True)
        return results

    # -----------------------
    # Real semantic search (future)
    # -----------------------
    try:
        contents = [note.get("content", "") for note in notes]

        query_emb = model.encode(query)
        content_embs = model.encode(contents)

        sims = cosine_similarity([query_emb], content_embs)[0]

        results = []
        for score, note in sorted(zip(sims, notes), reverse=True, key=lambda x: x[0]):
            if score > 0.5:
                results.append({
                    "note": note,
                    "score": float(score)
                })

        print(f"DEBUG: Semantic search matched {len(results)} notes", flush=True)
        return results

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"DEBUG: Semantic search failed, falling back to keyword search: {e}", flush=True)

        # Last-resort fallback
        q = query.lower()
        results = []

        for note in notes:
            content = (note.get("content") or "").lower()
            title = (note.get("title") or "").lower()

            if q in content or q in title:
                results.append({
                    "note": note,
                    "score": 1.0
                })

        return results
