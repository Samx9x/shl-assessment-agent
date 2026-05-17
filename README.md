# SHL Assessment Recommendation Agent

AI-powered conversational recommendation system for SHL assessments.

## Features

- Conversational hiring assistant
- Multi-turn clarification flow
- SHL catalog-grounded recommendations
- Semantic retrieval with ChromaDB
- Gemini-powered reasoning layer
- Recommendation validation
- Comparison and explanation support
- FastAPI REST API

---

## API Endpoints

### POST /chat

Request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Frontend React developer"
    }
  ]
}
```

---

### GET /health

Returns service health status.

---

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## Deployment

Dockerized and deployable on Render.
