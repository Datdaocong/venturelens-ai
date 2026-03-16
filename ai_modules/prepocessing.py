import re


SECTOR_KEYWORDS = {
    "fintech": ["finance", "fintech", "payment", "bank", "wallet", "credit"],
    "healthtech": ["health", "clinic", "medical", "doctor", "hospital"],
    "edtech": ["education", "learning", "student", "course", "school"],
    "ecommerce": ["shop", "store", "ecommerce", "retail", "marketplace"],
    "saas": ["software", "platform", "dashboard", "workflow", "automation"],
    "ai": ["ai", "artificial intelligence", "machine learning", "llm", "model"]
}

BUSINESS_MODEL_KEYWORDS = {
    "b2b": ["business", "company", "enterprise", "team", "organization"],
    "b2c": ["consumer", "user", "customer", "individual", "people"],
    "marketplace": ["marketplace", "connect buyers and sellers", "two-sided"],
    "subscription": ["subscription", "monthly", "annual", "recurring"],
    "transactional": ["commission", "fee per transaction", "take rate"]
}


def normalize_text(text: str) -> str:
    text = str(text).lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def extract_keywords(text: str) -> list[str]:
    text = normalize_text(text)
    tokens = re.findall(r"[a-zA-Z]{3,}", text)
    stopwords = {
        "the", "and", "for", "with", "that", "this", "from", "have",
        "will", "your", "into", "about", "their", "helps", "using"
    }
    return [t for t in tokens if t not in stopwords]


def infer_sector(text: str) -> list[str]:
    text = normalize_text(text)
    matched = []

    for sector, keywords in SECTOR_KEYWORDS.items():
        if any(k in text for k in keywords):
            matched.append(sector)

    return matched or ["general"]


def infer_business_model(text: str) -> list[str]:
    text = normalize_text(text)
    matched = []

    for model, keywords in BUSINESS_MODEL_KEYWORDS.items():
        if any(k in text for k in keywords):
            matched.append(model)

    return matched or ["unknown"]


def preprocess_idea(text: str) -> dict:
    norm_text = normalize_text(text)

    return {
        "raw_text": text,
        "normalized_text": norm_text,
        "keywords": extract_keywords(norm_text),
        "sectors": infer_sector(norm_text),
        "business_models": infer_business_model(norm_text),
    }