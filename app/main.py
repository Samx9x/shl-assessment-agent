from fastapi import FastAPI

from app.models.schemas import (
    ChatRequest,
)

from app.graph.workflow import (
    workflow,
)

from app.retrieval.vector_store import (
    initialize_vector_store,
)


app = FastAPI()

@app.on_event("startup")
def startup_event():

    initialize_vector_store()

    print(
        "\nVector store initialized.\n"
    )

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    state = {
        "messages": [
            msg.model_dump()
            for msg in request.messages
        ],

        "hiring_context": None,

        "intent": "",

        "ambiguity_detected": False,

        "ambiguity_reason": "",

        "retrieval_query": "",

        "retrieved_results": [],

        "final_recommendations": [],

        "final_response": {},

        "refusal_reason": "",
    }

    result = workflow.invoke(state)

    return result["final_response"]