# Traffic Agent Documentation

## Overview
The Traffic Agent is an application that allows users to optimize urban traffic parameters through an interactive chatbot. The system consists of a frontend developed in React with TypeScript and a backend in FastAPI that integrates an AI agent based on LangChain. The agent can now utilize two different optimization tools: a Standard Optimizer and a Dynamic Optimizer.

## Project Structure
```
traffic-agent-project/
├── backend/
│   ├── app/
│   │   ├── agent.py         # Agent communication logic
│   │   ├── agent_logic.py   # Traffic agent implementation (with dual tool support)
│   │   └── main.py          # FastAPI API
│   ├── .env                 # Environment variables (production)
│   ├── .env.example         # Example environment variables
│   └── requirements.txt     # Python dependencies
└── frontend/
    ├── src/
    │   ├── components/
    │   │   └── Chatbot.tsx  # Main chatbot component
    │   ├── App.tsx          # Main application component
    │   └── main.tsx         # Application entry point
    ├── .env                 # Environment variables (production)
    ├── .env.example         # Example environment variables
    └── package.json         # Node.js dependencies
```

## Implemented Features
- Natural language interpretation for traffic optimization.
- Support for English language.
- Session management to maintain conversation context.
- Visual loading indicators during requests.
- Proper formatting of responses with line breaks.
- Robust error handling.
- Integration with two optimization services on Render:
    - Standard Optimizer: `https://fastapi-traffic-agent-v2.onrender.com`
    - Dynamic Optimizer: `https://fastapi2-traffic-agent-v1.onrender.com`
- Contextual selection between Standard and Dynamic optimization tools based on user input.

## Access URLs (Previous Deployment - May Need Redeployment for New Features)
- Frontend: http://5173-iuarg9qxnf6kd0ddoi6lq-adaa25d4.manus.computer
- Backend API: http://8000-iuarg9qxnf6kd0ddoi6lq-adaa25d4.manus.computer

## How to Use
1. Access the frontend via the provided URL (or local setup).
2. Type your optimization request. The agent will decide which optimizer to use:
   - **For Standard Optimization**: Provide weights or priorities for the standard parameters.
     - Example: "I want to give high priority to public transport and low priority to emissions"
     - Example: "Optimize public transport to 0.7, congestion to 0.2, emissions to 0.05 and operational cost to 0.05"
   - **For Dynamic Optimization**: Include the keyword "dynamic" in your request along with weights or priorities.
     - Example: "Perform a dynamic optimization with high priority for public transport."
     - Example: "Dynamic optimization: set emissions to 0.1 and operational cost to 0.6."
3. The agent will process your request and display the optimization results.

## Output Formats
- **Standard Optimizer Results**: Displayed as percentage changes in KPIs.
  - Example: "The KPI 'Congestion' improves by 15%."
- **Dynamic Optimizer Results**: Displayed as direct values for specific KPIs.
  - Example: "The value for 'Income' is 5000."
  - Example: "The value for 'Congestion inside' is 0.3."

## Local Installation Instructions

### Backend
1. Navigate to the backend directory: `cd backend`
2. Create a `.env` file based on `.env.example` and configure your OpenAI API key.
3. Install dependencies: `pip install -r requirements.txt`
4. Start the server: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Frontend
1. Navigate to the frontend directory: `cd frontend`
2. Create a `.env` file based on `.env.example` and configure the backend URL (e.g., `VITE_BACKEND_URL=http://localhost:8000/chat`).
3. Install dependencies: `npm install`
4. Start the development server: `npm run dev`

## Optimization Parameters (Input for both optimizers)
- **Public Transport** (weight_PublicTransport)
- **Congestion** (weight_Congestion)
- **Emissions** (weight_Emissions)
- **Operational Cost** (weight_OperationalCost)

## Dynamic Optimization Output Parameters
- **Income**
- **Congestion inside**
- **Congestion (Delay)**
- **Emissions** (Note: This is an output parameter for dynamic, and an input weight parameter for both)

## Implemented Improvements (Latest Update)
- Integrated a second "Dynamic Optimization" tool.
- Implemented logic in the agent to choose between "Standard" and "Dynamic" optimization based on user input (keyword "dynamic").
- Updated backend to call the respective API and format results accordingly.
- Ensured frontend can display results from both optimizers (as formatted text).

