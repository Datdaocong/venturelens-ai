from src.retrieval.similarity_search import StartupSimilarityEngine

engine = StartupSimilarityEngine()

idea = """
AI platform helping fashion brands predict demand
and optimize inventory using machine learning
"""

results = engine.find_similar_startups(idea)

print(results[[
    "startup_name",
    "industry",
    "business_model",
    "similarity"
]])