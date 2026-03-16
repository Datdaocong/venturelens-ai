from ai_modules.data_loader import load_startup_clean, validate_startup_dataframe
from ai_modules.preprocessing import preprocess_idea
from ai_modules.retrieval import retrieve_similar_startups
from ai_modules.scoring import score_idea
from ai_modules.generator import build_analysis_report


def analyze_startup_idea(idea_text: str) -> dict:
    df = load_startup_clean()
    validate_startup_dataframe(df)

    idea_profile = preprocess_idea(idea_text)
    similar_startups = retrieve_similar_startups(df, idea_profile, top_k=5)
    scores = score_idea(idea_profile, similar_startups)

    report = build_analysis_report(
        idea_text=idea_text,
        idea_profile=idea_profile,
        similar_startups=similar_startups,
        scores=scores
    )

    return report