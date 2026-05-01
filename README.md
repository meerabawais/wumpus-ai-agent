# 🧠 Wumpus World AI Agent

An AI agent that navigates a grid-based Wumpus World using propositional logic and resolution.

## 🚀 Features
- Dynamic grid size
- Random pits and Wumpus
- Breeze & Stench percepts
- Knowledge Base (CNF clauses)
- Resolution-based inference
- Gold detection (win condition)
- Interactive UI with React

## 🛠 Tech Stack
- Frontend: React + Tailwind CSS
- Backend: Flask (Python)
- AI Logic: Propositional Logic + Resolution

## ⚙️ How it Works
The agent:
1. Receives percepts (breeze/stench)
2. Updates knowledge base
3. Uses resolution to infer safe cells
4. Avoids hazards and searches for gold

## ▶️ Run Locally

### Backend
cd backend  
pip install -r requirements.txt  
python wumpus_agent.py  

### Frontend
cd frontend  
npm install  
npm start  

## 🌐 Deployment
- Frontend: Vercel
- Backend: Render

## 📸 Screenshots
<img width="863" height="478" alt="image" src="https://github.com/user-attachments/assets/86bc2841-12f5-4293-a773-eb8a06ecfc91" />
<img width="846" height="486" alt="image" src="https://github.com/user-attachments/assets/35ce1061-9faf-4ae4-bd94-4d0fa0c7185d" />
