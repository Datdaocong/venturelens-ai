from ai_modules.data_loader import load_ai_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_engine = None
_df = None
_vectorizer = None
_matrix = None

def _init_engine():
    global _df, _vectorizer, _matrix

    _df = load_ai_dataset()

    texts = _df["search_text"].fillna("").astype(str)

    _vectorizer = TfidfVectorizer(max_features=5000)
    _matrix = _vectorizer.fit_transform(texts)


def retrieve_similar_startups(user_idea, top_k=5):

    global _df, _vectorizer, _matrix

    if _vectorizer is None:
        _init_engine()

    query_vec = _vectorizer.transform([user_idea])

    sims = cosine_similarity(query_vec, _matrix).flatten()

    top_idx = sims.argsort()[-top_k:][::-1]

    results = _df.iloc[top_idx].copy()
    results["similarity"] = sims[top_idx]

    return results.to_dict("records")