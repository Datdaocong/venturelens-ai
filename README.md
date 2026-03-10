# VentureLens AI

VentureLens AI is an AI-powered startup idea analysis system that evaluates startup concepts, identifies risks, and simulates possible future scenarios.

## Features
- Structure raw startup ideas
- Score business ideas across key criteria
- Identify major risks and hidden assumptions
- Simulate best-case, realistic-case, and worst-case scenarios
- Recommend next validation steps

## Tech Stack
- Python
- Streamlit
- OpenAI API

## Project Structure
```bash
venturelens-ai/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .env.example
├── README.md
│
├── ai_modules/
│   ├── idea_structurer.py
│   ├── scoring_engine.py
│   ├── risk_analyzer.py
│   ├── scenario_simulator.py
│   └── recommendation_engine.py
│
├── prompts/
│
└── utils/
    └── openai_client.py