from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.data.load_data import load_startup_data


class StartupSimilarityEngine:
    def __init__(self):
        self.df = load_startup_data().copy()

        required_cols = ["startup_name", "description", "industry", "business_model"]
        for col in required_cols:
            if col not in self.df.columns:
                self.df[col] = ""

        for col in required_cols:
            self.df[col] = self.df[col].fillna("").astype(str).str.strip().str.lower()

        self.df["combined_text"] = (
            self.df["description"] + " " +
            self.df["industry"] + " " +
            self.df["business_model"]
        ).str.strip()

        self.df = self.df[self.df["combined_text"] != ""].copy()

        if self.df.empty:
            raise ValueError("Dataset is empty after cleaning. Check data/processed/startups_clean.csv")

        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["combined_text"])

    def find_similar_startups(self, idea_text, top_k=10):
        idea_text = str(idea_text).strip().lower()
        if not idea_text:
            raise ValueError("idea_text is empty.")

        idea_vector = self.vectorizer.transform([idea_text])
        similarities = cosine_similarity(idea_vector, self.tfidf_matrix).flatten()

        results = self.df.copy()
        results["similarity"] = similarities

        return results.sort_values("similarity", ascending=False).head(top_k)[
            ["startup_name", "description", "industry", "business_model", "similarity"]
        ]