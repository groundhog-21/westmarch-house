# 🏰 The Westmarch Household  
*A Humorous Aristocratic Multi-Agent Concierge*

This repository contains the code for **The Westmarch Household**, a multi-agent assistant developed as part of the **Google AI Agents Course Capstone Project**.

The system features four agents, each portrayed as a member of an eccentric English estate:

- **Jeeves** – Head Butler & Orchestrator  
- **Perkins** – Research Footman  
- **Miss Pennington** – Scribe & Archivist  
- **Lady Hawthorne** – Dowager Critic

## 📦 Project Status
This project is currently in **Phase 2 (Core Implementation)**:
- Project structure created  
- Git repository initialized  
- Virtual environment configured  
- Agent scaffolding implemented  
- Mock orchestration operational  
- Integration with Gemini + GPT in progress  

## 🚀 Running the Demo
After activating the virtual environment:

```bash
python -m westmarch.demos.cli_demo
```

## 🔧 Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a .env file:

GOOGLE_API_KEY="your-gemini-api-key"
OPENAI_API_KEY="your-openai-api-key"

## 🗂 Structure
westmarch-house/
│
├── westmarch/
│   ├── agents/
│   ├── core/
│   ├── orchestrator/
│   ├── demos/
│   └── data/   (future)
│
├── requirements.txt
├── .gitignore
└── README.md

## 🏗 Next Steps (Planned)
- Integrate real Gemini + GPT model calls
- Add local memory system
- Implement logging and observability
- Demo workflows for all MVP use cases