# AI Quality Engineering Copilot

An AI-powered Quality Engineering platform that uses **RAG (Retrieval-Augmented Generation)** and **LLMs** to assist with requirement analysis, risk identification, test design, API automation generation, regression-impact analysis, defect summarization, log analysis, and end-to-end traceability.

The project is designed as a portfolio-grade engineering solution that combines **Quality Engineering, distributed systems, Generative AI, Python, FastAPI, AWS, and automation**.

---

## 1. Problem Statement

Modern QA teams work across multiple disconnected sources of information:

- Jira requirements and defects
- Confluence documentation
- API specifications
- Test repositories
- Git changes
- Application logs
- Release and regression information

Understanding the complete testing impact of a change often requires significant manual effort.

**AI Quality Engineering Copilot** creates a contextual QA knowledge layer over these engineering artifacts and uses RAG + LLMs to provide grounded, traceable Quality Engineering assistance.

---

## 2. Key Capabilities

The platform is intended to support the following workflows:

### Requirement Analysis

Analyze Jira requirements using related technical and product documentation.

Outputs may include:

- Requirement summary
- Ambiguities
- Dependencies
- Assumptions
- Missing information
- Testability concerns

### Missing Acceptance Criteria

Identify acceptance criteria that may be missing from a requirement.

Example:

```text
Requirement:
Device shall retry registration when the server is unavailable.

Possible missing acceptance criteria:
- Maximum retry count
- Retry interval
- Backoff strategy
- Expected state after retry exhaustion
```

### Risk Identification

Identify potential quality risks such as:

- Functional risks
- Integration risks
- Reliability risks
- Performance risks
- Data consistency risks
- Dependency risks
- Failure recovery risks

### Test Scenario Generation

Generate structured:

- Positive scenarios
- Negative scenarios
- Boundary cases
- Integration scenarios
- Failure scenarios
- Recovery scenarios

### API Test Skeleton Generation

Generate automation skeletons from:

- Requirements
- OpenAPI specifications
- Existing framework conventions
- Generated test scenarios

Initial targets:

- JavaScript + k6
- Python + pytest

### Regression Impact Analysis

Analyze engineering changes and identify potentially impacted:

- Services
- Components
- Requirements
- APIs
- Test cases
- Automation suites

### Defect Summarization

Summarize defects using:

- Jira defect description
- Comments
- Status history
- Related requirements
- Related failures

### Log / Root-Cause Assistant

Analyze logs and historical defects to generate:

- Probable causes
- Supporting evidence
- Contradicting evidence
- Confidence level
- Additional evidence required

The system should assist investigation rather than claim an unsupported root cause.

### Traceability

Maintain relationships such as:

```text
Requirement
   |
   +-- Acceptance Criteria
   |
   +-- Risks
   |
   +-- Architecture Components
   |
   +-- API Endpoints
   |
   +-- Test Scenarios
   |       |
   |       +-- Automation Tests
   |
   +-- Defects
```

---

## 3. High-Level Architecture

```text
                  +----------------------+
                  |     Data Sources     |
                  |----------------------|
                  | Jira                 |
                  | Confluence           |
                  | OpenAPI              |
                  | Git / GitHub         |
                  | Test Repository      |
                  | Logs                 |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  |   Ingestion Layer    |
                  |----------------------|
                  | Connectors           |
                  | Normalization        |
                  | Chunking             |
                  | Metadata Extraction  |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  |   Embedding Layer    |
                  |----------------------|
                  | Amazon Titan /       |
                  | other embeddings     |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  |  RAG Knowledge Base  |
                  |----------------------|
                  | pgvector /           |
                  | OpenSearch           |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  | Retrieval + Rerank   |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  |    AI Orchestrator   |
                  |----------------------|
                  | Requirement Analyst  |
                  | Risk Analyst         |
                  | Test Designer        |
                  | Regression Analyst   |
                  | Defect Analyst       |
                  | Log Analyst          |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  |      LLM Layer       |
                  |----------------------|
                  | Amazon Bedrock /     |
                  | pluggable LLM API    |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  |       FastAPI        |
                  +----------------------+
```

---

## 4. Technology Stack

### Backend

- Python
- FastAPI
- Pydantic
- pytest

### AI / RAG

- LlamaIndex
- Amazon Bedrock
- Amazon Titan Embeddings
- Retrieval-Augmented Generation
- Structured LLM output
- Prompt engineering

### Data / Vector Storage

Local development:

- PostgreSQL
- pgvector

AWS deployment options:

- Amazon Aurora PostgreSQL + pgvector
- Amazon OpenSearch Serverless

### Integrations

- Jira REST API
- Confluence REST API
- Git / GitHub APIs
- OpenAPI / Swagger
- CloudWatch / ELK logs

### DevOps / Cloud

- Docker
- Docker Compose
- AWS
- Amazon ECR
- Amazon ECS / Fargate
- AWS Secrets Manager
- Amazon CloudWatch
- Terraform

---

## 5. Project Structure

```text
ai-quality-copilot/
|
+-- README.md
+-- .env.example
+-- .gitignore
+-- pyproject.toml
+-- requirements.txt
+-- Dockerfile
+-- docker-compose.yml
|
+-- app/
|   |
|   +-- main.py
|   +-- config.py
|   +-- dependencies.py
|   +-- logging_config.py
|   +-- exceptions.py
|   |
|   +-- api/
|   |   +-- router.py
|   |   +-- routes/
|   |   |   +-- health.py
|   |   |   +-- ingestion.py
|   |   |   +-- requirements.py
|   |   |   +-- tests.py
|   |   |   +-- regression.py
|   |   |   +-- defects.py
|   |   |   +-- logs.py
|   |   |   +-- traceability.py
|   |   |
|   |   +-- schemas/
|   |
|   +-- connectors/
|   |   +-- base.py
|   |   +-- jira_connector.py
|   |   +-- confluence_connector.py
|   |   +-- github_connector.py
|   |   +-- openapi_connector.py
|   |   +-- log_connector.py
|   |
|   +-- ingestion/
|   |   +-- document_loader.py
|   |   +-- normalizer.py
|   |   +-- chunker.py
|   |   +-- metadata_builder.py
|   |   +-- ingestion_service.py
|   |
|   +-- rag/
|   |   +-- embeddings.py
|   |   +-- vector_store.py
|   |   +-- retriever.py
|   |   +-- reranker.py
|   |   +-- context_builder.py
|   |   +-- citation_builder.py
|   |
|   +-- llm/
|   |   +-- client.py
|   |   +-- bedrock_client.py
|   |   +-- structured_outputs.py
|   |   +-- prompts/
|   |
|   +-- agents/
|   |   +-- requirement_analyst.py
|   |   +-- risk_analyst.py
|   |   +-- test_designer.py
|   |   +-- api_test_generator.py
|   |   +-- regression_analyst.py
|   |   +-- defect_analyst.py
|   |   +-- log_analyst.py
|   |
|   +-- services/
|   |
|   +-- models/
|   |
|   +-- repositories/
|   |
|   +-- generators/
|   |   +-- k6_generator.py
|   |   +-- pytest_generator.py
|   |
|   +-- graph/
|   |
|   +-- evaluation/
|   |
|   +-- utils/
|
+-- data/
|   +-- synthetic/
|   |   +-- jira/
|   |   +-- confluence/
|   |   +-- openapi/
|   |   +-- defects/
|   |   +-- logs/
|   |   +-- git/
|   |
|   +-- evaluation/
|
+-- scripts/
|   +-- ingest_sample_data.py
|   +-- rebuild_index.py
|   +-- seed_database.py
|   +-- run_evaluation.py
|
+-- tests/
|   +-- unit/
|   +-- integration/
|   +-- api/
|
+-- infra/
|   +-- terraform/
|
+-- docs/
    +-- architecture.md
    +-- rag-flow.md
    +-- api-design.md
    +-- evaluation-strategy.md
    +-- demo-scenarios.md
```

---

## 6. Core Data Model

All external sources are normalized into a common `SourceDocument`.

```python
from datetime import datetime
from pydantic import BaseModel, Field


class SourceDocument(BaseModel):
    id: str
    source_type: str
    title: str
    content: str

    project: str | None = None
    component: str | None = None

    source_url: str | None = None
    version: str | None = None
    updated_at: datetime | None = None

    labels: list[str] = Field(default_factory=list)
    relationships: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
```

Examples of `source_type`:

```text
jira_requirement
jira_defect
confluence_page
architecture_document
openapi_spec
git_change
test_case
automation_test
application_log
```

This keeps the retrieval pipeline independent from individual source systems.

---

## 7. Request Flow

A typical requirement-analysis request follows this path:

```text
Jira Connector
      |
      v
SourceDocument
      |
      v
Normalizer
      |
      v
Chunker
      |
      v
Embeddings
      |
      v
Vector Store
      |
      v
Retriever
      |
      v
Context Builder
      |
      v
Requirement Analyst
      |
      v
LLM
      |
      v
Structured Response
      |
      v
FastAPI
```

---

## 8. API Design

The application exposes task-oriented APIs instead of relying only on a generic chat endpoint.

```text
POST /api/v1/ingestion/jira
POST /api/v1/ingestion/confluence

POST /api/v1/requirements/analyze
POST /api/v1/requirements/missing-ac
POST /api/v1/requirements/risks

POST /api/v1/tests/generate
POST /api/v1/tests/api-skeleton

POST /api/v1/regression/impact

POST /api/v1/defects/summarize
POST /api/v1/logs/analyze

GET  /api/v1/traceability/{requirement_id}

GET  /health
```

---

## 9. Example Requirement Analysis

### Request

```json
{
  "requirement_id": "QE-101"
}
```

### Example Response

```json
{
  "requirement_id": "QE-101",
  "summary": "Device registration must retry when the registration server is unavailable.",
  "ambiguities": [
    "Maximum retry count is undefined",
    "Retry interval is undefined",
    "Expected behavior after retry exhaustion is undefined"
  ],
  "missing_acceptance_criteria": [
    "Define maximum retry attempts",
    "Define retry interval",
    "Define terminal device state"
  ],
  "risks": [
    {
      "risk": "Retry storm across a large device population",
      "severity": "HIGH",
      "reason": "Devices may retry simultaneously when the server recovers"
    }
  ],
  "suggested_tests": [
    "Server unavailable during initial registration",
    "Server becomes available during retry",
    "Maximum retry attempts exceeded",
    "Registration succeeds after transient failure"
  ],
  "sources": [
    "QE-101",
    "Device Registration Architecture"
  ]
}
```

---

## 10. Example Generated k6 Test Skeleton

```javascript
import http from 'k6/http';
import { check } from 'k6';

export default function () {
    const response = http.get(
        `${__ENV.BASE_URL}/v1/devices/${__ENV.DEVICE_ID}`
    );

    check(response, {
        'status is 200': (r) => r.status === 200,
        'firmware version exists': (r) =>
            r.json('firmwareVersion') !== null,
    });
}
```

The generator can use:

- OpenAPI specification
- Requirement context
- Existing framework conventions
- Authentication details
- Generated test scenarios

to create more contextual automation skeletons.

---

## 11. RAG Strategy

The RAG pipeline should perform:

```text
Document
   |
   v
Normalization
   |
   v
Semantic Chunking
   |
   v
Metadata Enrichment
   |
   v
Embedding Generation
   |
   v
Vector Storage
   |
   v
Similarity Retrieval
   |
   v
Metadata Filtering
   |
   v
Optional Reranking
   |
   v
Context Construction
   |
   v
LLM
```

Useful metadata includes:

```text
project
component
requirement_id
source_type
version
labels
endpoint
service
updated_at
related_requirements
```

---

## 12. Traceability Model

Example:

```text
QE-101
  |
  +-- AC-101-01
  +-- AC-101-02
  |
  +-- Risk: Registration retry storm
  |
  +-- Component: Registration Service
  |
  +-- POST /registration
  |
  +-- TC-21
  +-- TC-22
       |
       +-- registration_retry.js
```

This enables questions such as:

```text
Which tests are impacted by a change to Registration Service?
```

or:

```text
Which requirements currently have no automated test coverage?
```

---

## 13. AI Safety and Grounding Principles

Generated results should be grounded in retrieved engineering context.

The system should:

- Return source references with AI output
- Clearly distinguish facts from inferred suggestions
- Avoid unsupported root-cause conclusions
- Expose confidence where appropriate
- Validate structured output using Pydantic
- Allow engineers to review generated test artifacts before execution
- Avoid automatically modifying production systems

For root-cause analysis, prefer:

```text
Probable Cause
      |
      +-- Supporting Evidence
      |
      +-- Contradicting Evidence
      |
      +-- Confidence
      |
      +-- Additional Evidence Required
```

---

## 14. Evaluation Strategy

A production-quality RAG application must be evaluated, not just demonstrated.

The project will maintain a golden evaluation dataset containing:

```text
Question
Expected source
Expected requirement
Expected risks
Expected test coverage
Expected answer characteristics
```

Potential metrics:

- Retrieval precision
- Retrieval recall
- Source correctness
- Citation correctness
- Groundedness
- Hallucination rate
- Structured-output validity
- Requirement coverage
- Risk-discovery quality
- Generated test usefulness

---

## 15. Local Development

### Prerequisites

Install:

- Python 3.11+
- Docker
- Docker Compose
- PostgreSQL / pgvector
- AWS CLI if using Amazon Bedrock

### Clone

```bash
git clone <your-repository-url>
cd ai-quality-copilot
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate it.

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Configuration

Copy:

```bash
cp .env.example .env
```

Example:

```env
APP_ENV=local

AWS_REGION=us-east-1

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/qepilot

VECTOR_STORE=pgvector

LLM_PROVIDER=bedrock
EMBEDDING_PROVIDER=bedrock

JIRA_BASE_URL=
JIRA_EMAIL=
JIRA_API_TOKEN=

CONFLUENCE_BASE_URL=
CONFLUENCE_EMAIL=
CONFLUENCE_API_TOKEN=
```

Never commit credentials to Git.

---

## 16. Start the Application

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

to access the FastAPI Swagger interface.

---

## 17. Docker

Build:

```bash
docker build -t ai-quality-copilot .
```

Run:

```bash
docker run -p 8000:8000 --env-file .env ai-quality-copilot
```

Or:

```bash
docker compose up --build
```

---

## 18. AWS Deployment

A later production deployment can use:

```text
FastAPI
   |
   v
Docker
   |
   v
Amazon ECR
   |
   v
Amazon ECS / Fargate
   |
   +--> Amazon Bedrock
   |
   +--> Aurora PostgreSQL + pgvector
   |       OR
   +--> OpenSearch Serverless
   |
   +--> Secrets Manager
   |
   +--> CloudWatch
```

Infrastructure can be managed using Terraform under:

```text
infra/terraform/
```

---

## 19. MVP Roadmap

### Phase 1 — Requirement Intelligence

- [ ] Create synthetic Jira requirements
- [ ] Create synthetic Confluence documents
- [ ] Implement `SourceDocument`
- [ ] Implement document ingestion
- [ ] Implement chunking
- [ ] Generate embeddings
- [ ] Store vectors
- [ ] Implement retrieval
- [ ] Integrate LLM
- [ ] Build `/requirements/analyze`
- [ ] Return grounded sources

### Phase 2 — Test Intelligence

- [ ] Missing acceptance-criteria detection
- [ ] Risk analysis
- [ ] Test-scenario generation
- [ ] OpenAPI ingestion
- [ ] k6 skeleton generation
- [ ] pytest skeleton generation

### Phase 3 — Engineering Intelligence

- [ ] Git change ingestion
- [ ] Regression-impact analysis
- [ ] Defect summarization
- [ ] Historical defect retrieval
- [ ] Log analysis
- [ ] Root-cause assistance

### Phase 4 — Traceability

- [ ] Requirement relationships
- [ ] Component relationships
- [ ] Test-to-requirement mapping
- [ ] Defect-to-requirement mapping
- [ ] Coverage queries
- [ ] Graph-based impact analysis

### Phase 5 — Productionization

- [ ] RAG evaluation framework
- [ ] Authentication
- [ ] Observability
- [ ] Docker deployment
- [ ] Terraform
- [ ] AWS deployment
- [ ] CI/CD

---

## 20. Recommended First Milestone

The first end-to-end slice should remain intentionally small:

```text
Synthetic Jira Requirement
        +
Synthetic Confluence Architecture
        |
        v
Document Ingestion
        |
        v
Embedding + Vector Store
        |
        v
RAG Retrieval
        |
        v
LLM
        |
        v
POST /api/v1/requirements/analyze
        |
        v
Structured + Cited Analysis
```

Once this pipeline works reliably, additional capabilities can reuse the same knowledge and retrieval layers.

---

## 21. Demo Dataset

The public repository should use fictional engineering data.

Example domain:

```text
Project: AutoConnect

Components:
- Device Registration
- OTA Campaign Service
- Device Management
- Notification Service
- Telemetry Service

Technologies:
- REST
- Kafka
- Redis
- IoT messaging
- AWS
```

Do **not** publish proprietary company/client requirements, architecture documents, logs, credentials, source code, or production data.

---

## 22. Future Enhancements

Possible extensions:

- GraphRAG
- Multi-agent orchestration
- Jira ticket creation from approved AI output
- Confluence knowledge synchronization
- GitHub pull-request impact analysis
- Automated traceability-matrix generation
- AI-assisted exploratory testing
- Self-healing automation experiments
- Test prioritization
- Release risk scoring
- Quality dashboards
- Human feedback loops
- Prompt/version evaluation
- Model comparison

---

## 23. Portfolio Positioning

This project demonstrates practical experience in:

- Generative AI application development
- Retrieval-Augmented Generation
- LLM integration
- Python backend engineering
- FastAPI
- AWS
- Vector databases
- Distributed-system quality engineering
- API automation
- Test architecture
- AI-assisted Quality Engineering
- RAG evaluation
- Traceability and impact analysis
- Docker and cloud deployment

---

## 24. Disclaimer

This is a learning and portfolio project.

All demo requirements, defects, logs, architecture documents, and system information should be **synthetic or publicly shareable**. The repository must not contain confidential information from any employer, client, or production environment.

---

## 25. License

Add an appropriate open-source license before publishing the repository.

A common choice for portfolio projects is the **MIT License**.
