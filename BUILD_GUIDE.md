# Build Guide — MVP 1

## Goal

Build one complete vertical slice before adding more AI features:

```text
Synthetic requirement + architecture docs
        -> ingestion
        -> chunking
        -> embeddings
        -> retrieval
        -> requirement-analysis prompt
        -> structured LLM output
        -> FastAPI endpoint
```

## Step 1 — Understand the data model

Start with `app/models/source_document.py`.

Every Jira issue, Confluence page, OpenAPI document, Git change, defect, or log will eventually be normalized into a `SourceDocument`. This is what prevents the RAG layer from becoming coupled to Jira or Confluence.

## Step 2 — Run without an LLM

Use the default `.env.example` settings:

```env
EMBEDDING_PROVIDER=local
LLM_PROVIDER=mock
```

Then run:

```bash
pytest -q
python scripts/smoke_test.py
```

The local embedding is a deterministic hashing implementation. It exists only to let you build and test the architecture without model cost or credentials.

## Step 3 — Start FastAPI

```bash
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` and execute:

```json
{
  "requirement_id": "QE-101"
}
```

against:

```text
POST /api/v1/requirements/analyze
```

Trace the request through these files in order:

1. `app/api/routes/requirements.py`
2. `app/services/requirement_service.py`
3. `app/rag/retriever.py`
4. `app/llm/prompts.py`
5. `app/llm/client.py`

## Step 4 — Inspect retrieval

The first requirement should retrieve:

- `QE-101`
- `CONF-REGISTRATION-ARCH`
- `CONF-RETRY-STRATEGY`

This is important: before tuning prompts, verify that the correct evidence is retrieved.

## Step 5 — Switch embeddings to Bedrock

Configure AWS credentials, then set:

```env
EMBEDDING_PROVIDER=bedrock
AWS_REGION=us-east-1
BEDROCK_EMBEDDING_MODEL_ID=amazon.titan-embed-text-v2:0
```

Keep `LLM_PROVIDER=mock` initially. This lets you validate retrieval separately from generation.

## Step 6 — Switch generation to Bedrock

Once retrieval is good:

```env
LLM_PROVIDER=bedrock
BEDROCK_MODEL_ID=<model-or-inference-profile-available-to-your-account>
```

The Bedrock client uses the `Converse` interface and asks for JSON-only output.

## Step 7 — Your first enhancement

Do **not** add Jira API integration immediately.

First add a second capability:

```text
POST /api/v1/requirements/risks
```

Reuse the exact same retrieval layer and create a dedicated risk-analysis prompt/response model. This will teach you why capabilities should be separated instead of putting everything into `/chat`.

## Step 8 — After that

Recommended order:

1. PostgreSQL + pgvector
2. Jira connector
3. Confluence connector
4. OpenAPI ingestion
5. k6 test skeleton generation
6. regression-impact analysis
7. defects/log RCA
8. evaluation framework
9. AWS ECS/Fargate deployment

## What you should be able to explain in an interview

After MVP 1, practice explaining:

- Why normalize heterogeneous sources into one document model?
- Why separate retrieval from generation?
- Why return citations/source IDs?
- Why does RAG quality depend heavily on retrieval quality?
- Why use structured output instead of free-form text?
- Why mock the LLM during local tests?
- What changes when moving from an in-memory store to pgvector?
- How would you prevent confidential Jira/Confluence data from leaking into a public project?
