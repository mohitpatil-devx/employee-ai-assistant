# Employee AI Assistant

An AI-powered employee assistant that answers natural-language questions about employee information and company policies using Gemini function calling, PostgreSQL, and Retrieval-Augmented Generation (RAG).

## Overview

The Employee AI Assistant combines structured employee data with company policy documents to provide contextual answers through a conversational interface.

Instead of relying on hardcoded keywords, the system uses an LLM to determine which tools are appropriate for a question, retrieve relevant information, and generate a natural-language response.

## Features

- **Natural-language interaction:** Ask questions about employee information and company policies.
- **AI tool calling:** Uses Gemini function calling to select and invoke relevant backend tools.
- **Employee analytics:** Retrieves employee counts, salary summaries, individual employee records, and salary-based search results.
- **Policy search with RAG:** Uses ChromaDB for semantic retrieval of company policy information.
- **Combined queries:** Handles questions that require both employee data and policy information.
- **Full-stack interface:** Angular frontend connected to a Python FastAPI backend.

## Architecture

Angular Frontend → FastAPI Backend → Gemini AI Agent → Backend Tools

The tools retrieve structured employee information from PostgreSQL and relevant policy information through ChromaDB-based retrieval. The retrieved results are passed back to the model to generate a response.

## Technology Stack

- **Frontend:** Angular, TypeScript
- **Backend:** Python, FastAPI
- **LLM and tool calling:** Google Gemini, Google GenAI SDK
- **Database:** PostgreSQL
- **Vector database:** ChromaDB
- **Embeddings:** Gemini Embedding model (`gemini-embedding-001`)
- **API:** REST

## Example Questions

- What is Rahul Sharma's current salary?
- How many active employees are there?
- What is the average salary by department?
- What is the company's work-from-home policy?
- Can Rahul Sharma work from home, and what is his current salary?

The assistant uses employee data and policy retrieval tools as needed to answer these questions.

## Getting Started

### Prerequisites

- Python
- Node.js and npm
- PostgreSQL
- A Google Gemini API key

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/snake0507/employee-ai-assistant.git
   cd employee-ai-assistant
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python -m venv venv
   ```

   On Windows:

   ```bash
   venv\Scripts\activate
   ```

3. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the required environment variables for the Gemini API and PostgreSQL connection. Keep credentials in a local `.env` file and never commit secrets.

5. Ensure PostgreSQL is running and the required database and employee table are configured.

6. Start the backend using the appropriate entry point for your project. If `main.py` contains the FastAPI application:

   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Open a separate terminal and navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the Angular development server:

   ```bash
   ng serve
   ```

4. Open `http://localhost:4200` in your browser.

Ensure the frontend API URL matches the address of the running backend.

## Current Status

This project is a learning-focused implementation of an LLM-powered application integrating function calling, structured database queries, semantic policy retrieval, and a web interface. Further improvements can include automated agent evaluation, robust retry handling, observability, and persistent conversation state.

## Security

API keys, database credentials, and other secrets should be stored in environment variables and excluded from version control. Use only synthetic or authorized employee data.

## Author

**Mohit Ajay Patil**

- GitHub: https://github.com/snake0507
