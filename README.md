# Employee AI Assistant

An AI-powered employee assistant that answers natural-language questions about employee information and company policies using Gemini tool calling, PostgreSQL, and Retrieval-Augmented Generation (RAG).

## Overview

The application combines structured employee data with semantically retrieved company policy information. Gemini chooses backend tools based on the question, and then generates a natural-language response from the returned results.

## Features

- Natural-language questions about employee records and company policies
- Gemini function calling to select backend tools
- Employee lookups and salary analytics using PostgreSQL
- Semantic policy retrieval using ChromaDB and Gemini embeddings
- Combined questions that require employee data and policy information
- Angular and TypeScript frontend with a Python FastAPI backend

## Architecture

Angular frontend → FastAPI REST API → Gemini model/tool calling → backend tools

Employee tools query PostgreSQL. The policy tool retrieves relevant text from ChromaDB, a vector database. The model uses tool results to compose the response.

## Technology Stack

- Frontend: Angular, TypeScript
- Backend: Python, FastAPI, Uvicorn
- LLM and tool calling: Google Gemini, Google GenAI SDK
- Relational database: PostgreSQL
- Vector database: ChromaDB
- Embeddings: `gemini-embedding-001`

## Example Questions

- What is Rahul Sharma's current salary?
- How many active employees are there?
- What is the average salary by department?
- What is the company's work-from-home policy?
- Can Rahul Sharma work from home, and what is his current salary?

The employee and policy details in this project are demonstration data. Do not use real employee information in a public demo.

## Getting Started

### Prerequisites

- Python 3.10 or later
- Node.js and npm compatible with the Angular project
- PostgreSQL
- A Google Gemini API key

### 1. Clone the repository

```bash
git clone https://github.com/snake0507/employee-ai-assistant.git
cd employee-ai-assistant
```

### 2. Configure environment variables

Create a virtual environment and install backend dependencies:

```bash
python -m venv venv
```

On Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and replace the placeholder values with your own credentials.

On Windows Command Prompt:

```cmd
copy .env.example .env
```

Required variables:

- `GEMINI_API_KEY`
- `POSTGRES_HOST` (defaults to `localhost` in the example)
- `POSTGRES_PORT` (defaults to `5432`)
- `POSTGRES_DB` (defaults to `employee_analytics`)
- `POSTGRES_USER` (defaults to `postgres`)
- `POSTGRES_PASSWORD`

Never commit your real `.env` file or share API keys/passwords.

### 3. Prepare PostgreSQL

Start PostgreSQL and create the `employee_analytics` database and an `employees` table with the columns expected by the backend: `id`, `full_name`, `department`, `salary`, and `active`. Add synthetic demonstration records before asking employee questions.

### 4. Initialize the policy vector collection

From the repository root, run the ingestion script:

```bash
python ingest_policies.py
```

The script reads policy sections from `employee_policies.txt`, creates Gemini embeddings, and stores the sections in the persistent ChromaDB collection named `company_policies`. You can rerun it after editing the policy file; it replaces the collection's current entries with the updated sections.

This step requires a valid `GEMINI_API_KEY` in your local `.env` file. Run ingestion before starting the backend because the policy search module expects the collection to exist.

### 5. Start the backend

From the repository root:

```bash
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`. API health check: `http://127.0.0.1:8000/api/health`.

### 6. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm start
```

Open `http://localhost:4200` in your browser. The frontend API URL is currently configured for `http://127.0.0.1:8000/api`.

## Current Status

This is a learning-focused project demonstrating LLM tool calling, SQL-backed data retrieval, semantic policy search, and a full-stack chat interface. It is not a production-ready HR system. Possible next steps include automated evaluation, improved error handling, and observability.

## Security

- Keep API keys and database passwords in environment variables.
- Use synthetic or authorized data only.
- If a credential has ever been committed to Git, rotate it; deleting it from the latest version does not remove it from Git history.

## Author

**Mohit Ajay Patil**

- GitHub: https://github.com/snake0507
