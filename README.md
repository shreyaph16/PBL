# Sentiment Analysis Platform for tech products

A full-stack AI-driven application that leverages advanced Machine Learning and Large Language Models (LLMs) to perform sophisticated sentiment analysis and reasoning on product reviews.

## 🌟 Key Features

- **Interactive Dashboard**: A modern, responsive frontend built with React 19, Vite, and Tailwind CSS. Features dynamic data visualization using Recharts and smooth micro-animations via Framer Motion.
- **Robust API Backend**: A lightning-fast FastAPI server handling RESTful endpoints for real-time individual text analysis and batch CSV processing.
- **Advanced ML & Agentic Pipeline**: 
  - **Base Classification**: Utilizes a locally loaded RoBERTa model via Hugging Face Transformers for highly accurate baseline sentiment classification (Positive/Negative/Neutral).
  - **Agentic Reasoning**: Integrates a powerful LangGraph workflow combined with Google's **Gemini 2.0 Flash** (via LangChain). This agentic engine not only classifies but also provides deep reasoning, summarizes trends, and extracts actionable insights from batch datasets.
- **Data Persistence**: Configured to use PostgreSQL (via Docker) or SQLite locally, orchestrated smoothly using SQLAlchemy ORM.
- **Containerized Architecture**: A complete `docker-compose.yml` is provided for seamless, one-click deployment of the database, backend API, and frontend client.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Node.js** (v18 or higher)
- **Python** (v3.11 or higher)
- **Docker & Docker Compose** (Optional, but highly recommended for easy setup)
- **Google Gemini API Key** (Required for the LangGraph reasoning engine)

---

## 🚀 Getting Started

### 1. Environment Setup

First, configure your environment variables. Copy the provided example file:

```bash
cp .env.example .env
```

Open the newly created `.env` file and insert your Gemini API Key:
```env
# .env
DATABASE_URL=postgresql://user:password@db:5432/reviews_db
GEMINI_API_KEY=your_actual_api_key_here
VITE_API_BASE_URL=http://localhost:8000
```

### 2. Running with Docker (Recommended)

You can launch the entire stack (Database, Backend, Frontend) concurrently with a single command:

```bash
docker-compose up --build
```

Once the containers are successfully built and running, you can access:
- **Frontend App**: [http://localhost:5173](http://localhost:5173)
- **Backend API Docs (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Database**: PostgreSQL mapped to port `5432`

### 3. Running Locally (Manual Setup)

If you prefer to run the services without Docker, follow these steps:

#### Backend Setup
```bash
# Navigate to the backend directory (optional if you run from root, but ensure paths are correct)
cd backend

# Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Return to root directory and start the backend server
cd ..
uvicorn backend.main:app --reload --port 8000
```

#### Frontend Setup
```bash
# Navigate to the frontend directory
cd frontend

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
```

---

## 📦 Project Requirements & Tech Stack

The project's dependencies are cleanly separated into frontend and backend ecosystems.

### Backend (`backend/requirements.txt`)
- **FastAPI** & **Uvicorn**: High-performance asynchronous web framework and ASGI server.
- **SQLAlchemy** & **Pydantic**: Database ORM and robust data validation/settings management.
- **Pandas** & **NumPy**: Foundational data manipulation and analysis libraries.
- **Transformers** & **Torch**: Hugging Face ecosystem for running the local RoBERTa model.
- **LangGraph** & **LangChain (Google GenAI)**: Frameworks orchestrating the multi-agent reasoning workflow and communicating with the Gemini API.

### Frontend (`frontend/package.json`)
- **React 19** & **React DOM**: Component-based UI library.
- **Vite**: Next-generation, blazing-fast frontend tooling.
- **Tailwind CSS**: Utility-first CSS framework for rapid UI styling.
- **Recharts**: Composable charting library for rendering sentiment distributions.
- **Framer Motion**: Production-ready animation library for React.
- **Axios**: Promise-based HTTP client for API communication.
- **Lucide React**: Beautiful, consistent icon toolkit.
