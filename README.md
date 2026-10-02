# HR Tier-0 Agent

A self-hosted HR Tier-0 employee assistant built with **Google ADK**, **LiteLLM**, **Ollama**, **Qwen3 8B**, **Qdrant**, and **Docker Compose**.

The application is designed to answer employee HR questions, retrieve information from an employee data source, and use RAG to answer questions from official HR policy documents.

---

## 1. What is this application?

The HR Tier-0 Agent is an AI-powered employee assistant that provides a single conversational interface for common HR queries.

At a high level:

```text
Employee
   |
   v
ADK Web / Application
   |
   v
HR Root Agent
   |
   +--------------------+
   |                    |
   v                    v
Employee DB Tool      HR Policy RAG
   |                    |
   v                    v
Employee Data         Qdrant
                        |
                        v
                   Policy Documents

              +----------------+
              |    Ollama      |
              |   Qwen3 8B     |
              +----------------+
```

The current implementation runs completely locally using Docker.

---

# 2. Main Features

The current project contains the following capabilities:

### Employee authorization

Before the agent processes the request, an authorization callback checks the employee identity.

The current prototype uses the ADK `user_id` and validates it against the employee authorization logic.

```text
User
 |
 v
Authorization Callback
 |
 +---- Authorized ----> Continue to Agent
 |
 +---- Not Authorized -> Access Denied
```

### Employee information

The `get_employee_details` tool retrieves employee-specific information from:

```text
hr_assistant/data/employees/employees.json
```

This is currently a JSON-based prototype data source.

For a production implementation, this can later be replaced with PostgreSQL or an enterprise HR system without changing the overall agent architecture.

### HR Policy RAG

The application can search official HR policy documents.

The RAG pipeline is:

```text
HR Policy PDFs
     |
     v
PDF Text Extraction
     |
     v
Chunking
     |
     v
nomic-embed-text
     |
     v
Qdrant
     |
     v
Semantic Search
     |
     v
HR Agent
```

The current implementation uses:

- PDF extraction: `pypdf`
- Chunk size: approximately 800 characters
- Chunk overlap: 150 characters
- Embedding model: `nomic-embed-text`
- Vector database: Qdrant
- Similarity: Cosine
- Retrieval: Top 5 results

The current policy index contains approximately **81 chunks**.

### Local LLM

The application uses:

```text
Ollama
   |
   +-- Qwen3 8B
   |
   +-- nomic-embed-text
```

Qwen3 8B is the current chat/inference model.

`nomic-embed-text` is used for generating embeddings for the RAG pipeline.

---

# 3. Architecture

The current Docker architecture is:

```text
                    Your Computer
                         |
                  Docker Desktop
                         |
       +-----------------+-----------------+
       |                 |                 |
       v                 v                 v
  +---------+       +---------+       +---------+
  |hr-agent |       | Ollama  |       | Qdrant  |
  | :8000   |------>| :11434  |       | :6333   |
  +---------+       +---------+       +---------+
       |                 |
       |                 v
       |              Qwen3 8B
       |
       +---------------------> Qdrant
```

Important:

Inside Docker, services communicate using their Docker Compose service names.

Therefore:

```text
Correct:
http://ollama:11434
http://qdrant:6333
```

Do **not** use:

```text
http://localhost:11434
http://localhost:6333
```

from inside the `hr-agent` container.

However, from your Mac/browser, the ADK Web UI is accessed through:

```text
http://localhost:8000
```

---

# 4. Technology Stack

| Component | Technology |
|---|---|
| Agent Framework | Google ADK |
| LLM abstraction | LiteLLM |
| LLM Runtime | Ollama |
| Chat Model | Qwen3 8B |
| Embedding Model | nomic-embed-text |
| Vector Database | Qdrant |
| Backend Language | Python |
| Python Version | Python 3.14 |
| PDF Processing | pypdf |
| Containerization | Docker |
| Orchestration | Docker Compose |
| Development UI | ADK Web |

---

# 5. Project Structure

```text
HR_Agent/
│
├── hr_assistant/
│   │
│   ├── __init__.py
│   ├── agent.py
│   │
│   ├── prompt/
│   │   └── instruction.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── employee_db_tool.py
│   │   └── rag_tool.py
│   │
│   ├── callbacks/
│   │   ├── __init__.py
│   │   └── authorization_callback.py
│   │
│   ├── guardrails/
│   │   ├── __init__.py
│   │   └── authorization.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── ingestion.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── state.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   │
│   └── data/
│       ├── employees/
│       │   └── employees.json
│       │
│       └── policies/
│           └── HR policy PDFs
│
├── evals/
├── scripts/
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .dockerignore
```

---

# 6. Prerequisites

Before running the application, install the following:

## Docker Desktop

Install Docker Desktop for your operating system.

After installation, verify:

```bash
docker --version
```

and:

```bash
docker compose version
```

Also verify Docker is running:

```bash
docker info
```

You should see information about CPUs and available memory.

---

# 7. Recommended System Resources

The current project uses a local LLM, so RAM is important.

The development environment used for this project has:

```text
CPU:    10
Memory: 7.75 GiB Docker memory
```

Qwen3 8B successfully runs in this environment.

The earlier Gemma 4 12B model did not run successfully under the same memory allocation.

For a smoother local deployment, more RAM is recommended.

A practical target for a dedicated machine is:

```text
CPU:    4+ cores
RAM:    16 GB+
SSD:    100 GB+
OS:     Linux/macOS
Docker: Supported
```

---

# 8. Download the Application

There are two common ways to obtain the project.

## Option A — Git repository

If the project is stored in Git:

```bash
git clone <YOUR_REPOSITORY_URL>
```

Then:

```bash
cd HR_Agent
```

Example:

```bash
git clone https://github.com/<your-org>/<your-repository>.git
cd HR_Agent
```

Replace `<YOUR_REPOSITORY_URL>` with the actual repository URL.

## Option B — Download ZIP

If the project is provided as a ZIP:

1. Download the project ZIP.
2. Extract it.
3. Open Terminal.
4. Navigate to the extracted directory.

Example:

```bash
cd ~/Downloads/HR_Agent
```

Verify:

```bash
ls
```

You should see files such as:

```text
Dockerfile
docker-compose.yml
requirements.txt
hr_assistant
```

---

# 9. Configuration

The application uses environment variables for configuration.

The important settings are:

```text
MODEL
EMBEDDING_MODEL
OLLAMA_HOST
QDRANT_URL
COMPANY_NAME
```

Current Docker configuration:

```yaml
MODEL: "ollama_chat/qwen3:8b"
EMBEDDING_MODEL: "nomic-embed-text"
OLLAMA_HOST: "http://ollama:11434"
QDRANT_URL: "http://qdrant:6333"
COMPANY_NAME: "LALA Company"
```

### Important

Do not change:

```text
OLLAMA_HOST=http://ollama:11434
```

to:

```text
OLLAMA_HOST=http://localhost:11434
```

when running inside Docker.

`localhost` inside the `hr-agent` container refers to the `hr-agent` container itself.

---

# 10. Build and Start the Application

From the project root:

```bash
docker compose up -d --build
```

This command:

1. Builds the `hr-agent` Docker image.
2. Starts the `hr-agent` container.
3. Starts the Ollama container.
4. Starts the Qdrant container.
5. Creates the Docker network.
6. Creates named volumes if they don't already exist.

Check the containers:

```bash
docker compose ps
```

Expected services:

```text
hr-agent
ollama
qdrant
```

All should show a running/healthy state where applicable.

---

# 11. Verify the LLM

Check the models available inside Ollama:

```bash
docker compose exec ollama ollama list
```

You should have:

```text
qwen3:8b
nomic-embed-text
```

If Qwen3 is missing:

```bash
docker compose exec ollama ollama pull qwen3:8b
```

If the embedding model is missing:

```bash
docker compose exec ollama ollama pull nomic-embed-text
```

Test Qwen3 directly:

```bash
docker compose exec ollama ollama run qwen3:8b "Say hello in one sentence."
```

Expected behavior is a normal response such as:

```text
Hello! How can I assist you today?
```

---

# 12. Verify the Application Configuration

Run:

```bash
docker compose exec hr-agent python -c "from hr_assistant.core.config import settings; print('MODEL:', settings.MODEL); print('OLLAMA_HOST:', settings.OLLAMA_HOST); print('QDRANT_URL:', settings.QDRANT_URL)"
```

Expected:

```text
MODEL: ollama_chat/qwen3:8b
OLLAMA_HOST: http://ollama:11434
QDRANT_URL: http://qdrant:6333
```

---

# 13. Verify Docker-to-Ollama Connectivity

Run:

```bash
docker compose exec hr-agent python -c "import urllib.request; print(urllib.request.urlopen('http://ollama:11434/api/tags').read().decode())"
```

If this succeeds, the `hr-agent` container can communicate with Ollama.

This is an important test because the browser uses:

```text
localhost:8000
```

while the application uses:

```text
ollama:11434
```

for internal Docker communication.

---

# 14. Verify Qdrant

Open Qdrant from your browser:

```text
http://localhost:6333
```

Or test it from the container:

```bash
docker compose exec hr-agent python -c "from qdrant_client import QdrantClient; c=QdrantClient(url='http://qdrant:6333'); print(c.get_collections())"
```

The application should contain the collection:

```text
hr_policies
```

---

# 15. Load HR Policy Documents

The HR policy PDFs are located in:

```text
hr_assistant/data/policies/
```

The ingestion process performs:

```text
PDF
 ↓
Text extraction
 ↓
Chunking
 ↓
Embedding
 ↓
Qdrant
```

Run the ingestion script:

```bash
docker compose exec hr-agent python -m hr_assistant.rag.ingestion
```

The script processes the PDFs and indexes them into Qdrant.

You should see output similar to:

```text
Processing: LALA Company - Document 1.pdf
Processing: LALA Company - Document 2.pdf
...
Indexed 81 chunks from HR policy documents.
```

The exact number can change if the policy files are changed.

---

# 16. Open the HR Agent

Once all containers are running, open:

```text
http://localhost:8000
```

This opens the ADK Web interface.

Select the HR assistant agent.

Create a new session and test a simple request.

For example:

```text
What is the leave policy?
```

The expected flow is:

```text
User
 ↓
ADK Web
 ↓
HR Root Agent
 ↓
Authorization Callback
 ↓
Qwen3
 ↓
search_hr_policies
 ↓
Qdrant
 ↓
Relevant policy chunks
 ↓
Qwen3
 ↓
Final answer
```

---

# 17. Test Employee Information

Try a request that requires employee-specific information.

For example:

```text
Show my employee details.
```

The expected flow is:

```text
User
 ↓
Authorization
 ↓
Root Agent
 ↓
get_employee_details
 ↓
employees.json
 ↓
Employee information
 ↓
Qwen3
 ↓
Response
```

The agent should use the authorized employee identity rather than allowing a user to freely access another employee's record.

---

# 18. Understanding Authorization

The current authorization flow is:

```text
ADK user_id
     |
     v
Authorization Callback
     |
     v
is_employee_authorized()
     |
     +------ No ------> Access Denied
     |
    Yes
     |
     v
state["employee_id"]
state["authorized"] = True
     |
     v
Continue to Agent
```

The important security principle is:

> The LLM should not be responsible for deciding whether an employee is authorized to access HR data.

Authorization should happen outside the model's reasoning.

---

# 19. RAG Query Flow

When the employee asks:

```text
What is the leave policy?
```

the system does approximately:

```text
Question
   |
   v
search_hr_policies()
   |
   v
Generate query embedding
   |
   v
Qdrant similarity search
   |
   v
Top 5 chunks
   |
   v
Return source + text
   |
   v
Qwen3
   |
   v
Grounded answer
```

The vector database does not generate the answer.

It retrieves relevant information.

Qwen3 generates the natural-language answer using the retrieved context.

---

# 20. Starting the Application Again

After shutting down your computer, the containers stop.

The Docker volumes remain available unless they are explicitly deleted.

After restarting your computer:

```bash
cd HR_Agent
```

Then:

```bash
docker compose up -d
```

You do not normally need to download Qwen3 or recreate the Qdrant collection every time.

Then open:

```text
http://localhost:8000
```

---

# 21. Important Docker Volume Warning

Use:

```bash
docker compose down
```

when you want to stop/remove the containers.

This normally preserves named volumes.

Be careful with:

```bash
docker compose down -v
```

The `-v` option removes the named volumes.

That can delete:

```text
Ollama model storage
Qdrant vector database storage
```

Therefore, do not use `down -v` unless you intentionally want to reset the application's persistent Docker data.

---

# 22. Useful Commands

## Start

```bash
docker compose up -d
```

## Start and rebuild

```bash
docker compose up -d --build
```

## Stop

```bash
docker compose down
```

## Check status

```bash
docker compose ps
```

## View all logs

```bash
docker compose logs --tail=100
```

## ADK logs

```bash
docker compose logs hr-agent --tail=100
```

## Ollama logs

```bash
docker compose logs ollama --tail=100
```

## Qdrant logs

```bash
docker compose logs qdrant --tail=100
```

## Follow logs

```bash
docker compose logs -f hr-agent
```

## Check models

```bash
docker compose exec ollama ollama list
```

## Run Qwen3

```bash
docker compose exec ollama ollama run qwen3:8b
```

## Open a shell in the ADK container

```bash
docker compose exec hr-agent bash
```

## Open a shell in Ollama

```bash
docker compose exec ollama bash
```

---

# 23. Troubleshooting

## Problem: ADK cannot connect to Ollama

Look for:

```text
Cannot connect to host localhost:11434
```

Inside Docker this is usually incorrect.

Verify:

```bash
docker compose exec hr-agent python -c "from hr_assistant.core.config import settings; print(settings.OLLAMA_HOST)"
```

Expected:

```text
http://ollama:11434
```

Also verify Ollama:

```bash
docker compose ps
```

and:

```bash
docker compose logs ollama --tail=100
```

---

## Problem: Qwen3 does not respond

Test Ollama directly:

```bash
docker compose exec ollama ollama run qwen3:8b "Say hello"
```

If this fails, the issue is at the Ollama/model layer rather than the ADK layer.

---

## Problem: Qdrant collection is missing

Check:

```bash
docker compose exec hr-agent python -c "from qdrant_client import QdrantClient; c=QdrantClient(url='http://qdrant:6333'); print(c.get_collections())"
```

If `hr_policies` is missing, run ingestion:

```bash
docker compose exec hr-agent python -m hr_assistant.rag.ingestion
```

---

## Problem: RAG returns no results

Check:

1. Policy PDFs exist.
2. PDFs contain extractable text.
3. Ingestion completed.
4. Qdrant is running.
5. `hr_policies` exists.
6. `nomic-embed-text` is available.

Check models:

```bash
docker compose exec ollama ollama list
```

---

## Problem: Agent uses the wrong model

Check:

```bash
docker compose exec hr-agent python -c "from hr_assistant.core.config import settings; print(settings.MODEL)"
```

Expected:

```text
ollama_chat/qwen3:8b
```

---

# 24. Application Lifecycle

The complete lifecycle is:

```text
1. Start Docker
       |
       v
2. Start hr-agent
       |
       v
3. Start Ollama
       |
       v
4. Start Qdrant
       |
       v
5. Load Qwen3 / embeddings
       |
       v
6. Load Qdrant collection
       |
       v
7. Open ADK Web
       |
       v
8. Employee submits question
       |
       v
9. Authorization
       |
       v
10. Agent reasoning
       |
       v
11. Tool / RAG execution
       |
       v
12. LLM response
       |
       v
13. Employee receives answer
```

---

# 25. Current Implementation vs Future Enhancements

The current project is a working local prototype/foundation.

Future enhancements can include:

### Database

Replace:

```text
employees.json
```

with:

```text
PostgreSQL
```

### Authentication

Replace the development identity mechanism with:

```text
SSO / OIDC / Identity Provider
```

### Specialized Agents

Add:

```text
Root Agent
   |
   +-- HR Policy Agent
   |
   +-- Employee Data Agent
   |
   +-- HR Case Agent
   |
   +-- Escalation Agent
```

### Orchestrator

Introduce a dedicated orchestration layer for multi-step workflows.

### Guardrails

Add:

```text
Input Guardrail
Authorization Guardrail
Tool Guardrail
RAG Grounding Guardrail
Output Guardrail
Escalation Guardrail
```

### Observability

Add:

```text
Structured Logging
Metrics
Tracing
Audit Logs
```

### Evaluation

Create automated tests for:

```text
Planner accuracy
Tool selection
RAG retrieval
Groundedness
Authorization
Safety
Escalation
End-to-end answer quality
```

---

# 26. Recommended Development Order

For someone continuing development on this repository, the recommended sequence is:

```text
Phase 1
Current Docker + ADK + Qwen3
        |
        v
Phase 2
Employee DB + RAG stabilization
        |
        v
Phase 3
Authentication + Authorization
        |
        v
Phase 4
Specialized Agents
        |
        v
Phase 5
Orchestrator
        |
        v
Phase 6
Guardrails
        |
        v
Phase 7
Evaluation
        |
        v
Phase 8
Observability
        |
        v
Phase 9
Production API / Frontend
```

---

# 27. Quick Start

For an experienced developer, the shortest path is:

```bash
# 1. Download repository
git clone <YOUR_REPOSITORY_URL>

# 2. Enter project
cd HR_Agent

# 3. Start application
docker compose up -d --build

# 4. Verify services
docker compose ps

# 5. Verify models
docker compose exec ollama ollama list

# 6. Test Qwen3
docker compose exec ollama ollama run qwen3:8b "Say hello"

# 7. Ingest HR policies if required
docker compose exec hr-agent python -m hr_assistant.rag.ingestion

# 8. Open application
open http://localhost:8000
```

On Linux, if `open` is unavailable, simply open the URL manually in your browser.

---

# 28. Summary

The HR Tier-0 Agent is a self-hosted agentic HR assistant built around Google ADK.

The current runtime consists of:

```text
Google ADK
    +
LiteLLM
    +
Ollama / Qwen3 8B
    +
Qdrant
    +
HR Policy RAG
    +
Employee Authorization
    +
Employee Data Tool
    +
Docker Compose
```

The application can run entirely on a local computer without requiring a cloud deployment.

The main entry point for users during development is:

```text
http://localhost:8000
```

The key internal Docker endpoints are:

```text
Ollama:
http://ollama:11434

Qdrant:
http://qdrant:6333
```

The project can later be extended with PostgreSQL, SSO, specialized agents, orchestration, stronger guardrails, evaluation, logging, and a dedicated frontend/API.

---

## License

Add the project's applicable license here.

## Maintainer

Add the project owner/team information here.
