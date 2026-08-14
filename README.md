# OmniPay Agentic Observability Platform

A cloud-native, distributed payment processing simulation engine designed to demonstrate the application of Agentic AI and Retrieval-Augmented Generation (RAG) in analyzing high-throughput transaction telemetry.

## Architecture

The platform is designed around a microservices architecture to simulate enterprise payment settlement:
- **Backend (Python/FastAPI):** Handles high-throughput transaction streaming and interfaces with the LLM API to perform simulated RAG on unstructured observability logs.
- **Frontend (React/Vite):** A dark-mode dashboard for visualizing live transaction streams, system telemetry, and agentic root cause analysis.
- **Databases:** Relational transaction data is modeled for PostgreSQL, while unstructured failure logs are targeted for document storage.
- **Infrastructure:** Containerized via Docker and orchestrated with Docker Compose for local development. CI/CD pipelines are managed through GitHub Actions.

## Key Features

- **Distributed Transaction Simulation:** Generates continuous synthetic payment data across various merchant gateways, simulating network latency and varied failure rates.
- **Agentic Root Cause Analysis:** When a transaction fails, the engine autonomously retrieves relevant error logs and prompts a Large Language Model (Gemini 2.5 Pro) to diagnose the root cause and recommend engineering actions.
- **Real-Time Observability Dashboard:** A React-based interface that polls telemetry data and presents both standard system metrics and AI-generated insights.
- **Continuous Integration:** Automated build and linting workflows integrated via GitHub Actions to maintain code reliability.

## Prerequisites

- Docker and Docker Compose
- Google GenAI API Key (for the Agentic workflow)

## Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/AryanAI0035/payment-observability-engine.git
   cd payment-observability-engine
   ```

2. Export your API key to the environment:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

3. Build and run the containers:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend Dashboard: `http://localhost:5173`
   - Backend API Docs: `http://localhost:8000/docs`

## Repository Structure

- `/backend`: FastAPI service, Pydantic models, and Agentic AI workflow logic.
- `/frontend`: React dashboard, styling, and Axios integrations.
- `.github/workflows`: CI/CD pipeline definitions.
- `docker-compose.yml`: Multi-container orchestration config.

## License

MIT License
