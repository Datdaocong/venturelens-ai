# 🚀 VentureLens Project Journal (English)

## 1. Initial Idea (VentureLens-1)

The original goal was simple:

> Build an AI tool that can analyze startup ideas.

At this stage, the system relied mostly on:
- prompting an LLM
- generating general startup advice

### ❌ Problem
The outputs looked good but had a major flaw:
- no grounding in real data
- answers were generic and sometimes unrealistic

### 💡 Insight
“If the system only uses LLM, it’s just a chatbot — not an analysis system.”

---

## 2. Transition to Data-Driven Approach (VentureLens-2)

Introduced real startup dataset:

- description
- industry
- funding
- success_score
- outcome_label

### Key shift

From:
Idea → LLM → Output

To:
Idea → Data → Signals → Output

---

## 3. Retrieval System (VentureLens-3)

Implemented TF-IDF similarity.

### What worked:
- system started referencing real startups

### ❌ Problems:
- noisy matches
- dataset bugs (empty columns, wrong formats)
- still relied on LLM

### Fix:
- data cleaning pipeline
- standardized schema

---

## 4. Full Pipeline Thinking (VentureLens-4)

Redesigned system as a pipeline:

Idea  
→ Retrieval  
→ Scoring  
→ Risk  
→ Scenario  
→ Recommendation  
→ Report  

### Insight:
Separate:
- data (retrieval)
- logic (rules)
- generation (language)

---

## 5. RAG System (VentureLens-5)

Added `rag_context_builder.py`

### Responsibilities:
- retrieve similar startups
- compute signals:
  - avg_success_score
  - success_ratio
  - failure_ratio
  - similarity

### Key idea:
LLM is no longer the brain, only the narrator.

---

## 6. Scoring System Evolution

### ❌ Problem:
Random ideas got very high scores.

### Root cause:
- weak penalties
- no caps
- overly optimistic aggregation

### ✅ Fix:
- penalty system
- similarity thresholds
- score caps

### Insight:
Scoring must be conservative, not optimistic.

---

## 7. Risk Analyzer

Rule-based instead of LLM:

Signals:
- failure_ratio
- similarity strength
- peer count

Outputs:
- risk_level
- risk_flags

---

## 8. Scenario Simulation

Upgraded from simple text → structured output:

Each scenario includes:
- title
- description
- why it happens
- trigger
- warning signs
- actions

---

## 9. UI (Streamlit)

Components:
- score + radar chart
- peer signals
- similar startups
- scenarios
- recommendations

### Insight:
UI must explain reasoning, not just output.

---

## 10. Final Architecture

ai_modules/
- data_loader.py
- similarity_bridge.py
- rag_context_builder.py
- scoring_engine.py
- risk_analyzer.py
- scenario_simulator.py
- recommendation_engine.py
- report_generator.py
- full_analysis.py
- radar_chart.py

---

## 11. Key Lessons

1. LLM without data = unreliable  
2. Retrieval quality is critical  
3. Scoring must be calibrated  
4. Structure > complexity  
5. Most bugs come from data mismatch  

---

## 12. Future Improvements

- Embeddings instead of TF-IDF  
- Industry baseline scoring  
- Percentile ranking  
- Better evaluation  
- Memory system  

---

## 🎯 Interview Summary

“I built a startup analysis system that moved from LLM-based guessing to a data-driven RAG pipeline with scoring, risk modeling, and structured scenario simulation.”