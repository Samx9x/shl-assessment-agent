import chromadb

from chromadb.config import (
    Settings,
)

from app.catalog.loader import (
    catalog_data,
)

from app.retrieval.embedder import (
    embedding_model,
)

from app.core.config import (
    CHROMA_DB_DIR,
)


client = chromadb.PersistentClient(
    path=CHROMA_DB_DIR,
    settings=Settings(
        anonymized_telemetry=False
    ),
)


collection = client.get_or_create_collection(
    name="shl_catalog_v2"
)


def build_document(item):

    return f"""
    Name: {item.get('name', '')}

    Description:
    {item.get('description', '')}

    Categories:
    {', '.join(item.get('keys', []))}

    Job Levels:
    {', '.join(item.get('job_levels', []))}
    """


def build_metadata(item):

    return {

        "name": item.get(
            "name",
            "",
        ),

        "url": item.get(
            "link",
            "",
        ),

        "test_type": (
            item.get(
                "keys",
                ["Unknown"],
            )[0]
        ),

        "categories": ",".join(
            item.get(
                "keys",
                [],
            )
        ),
    }


def initialize_vector_store():

    existing = collection.count()

    if existing > 0:

        return

    documents = []

    metadatas = []

    ids = []

    for item in catalog_data:

        documents.append(
            build_document(item)
        )

        metadatas.append(
            build_metadata(item)
        )

        ids.append(
            item["entity_id"]
        )

    embeddings = (
        embedding_model.encode(
            documents
        ).tolist()
    )

    collection.add(

        documents=documents,

        embeddings=embeddings,

        metadatas=metadatas,

        ids=ids,
    )


def semantic_search(
    query,
    top_k=15,
):

    embedding = (
        embedding_model.encode(
            query
        ).tolist()
    )

    return collection.query(

        query_embeddings=[
            embedding
        ],

        n_results=top_k,
    )