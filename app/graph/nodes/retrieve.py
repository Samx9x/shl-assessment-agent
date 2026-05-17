from app.retrieval.reasoning.query_builder import (
    build_query,
)

from app.retrieval.reasoning.battery_planner import (
    build_battery_plan,
)

from app.retrieval.reasoning.role_scorer import (
    compute_role_score,
)

from app.retrieval.vector_store import (
    semantic_search,
)

from app.retrieval.composition.diversifier import (
    diversify_results,
)

from app.retrieval.reasoning.policy_scorer import (
    compute_policy_score,
)

from app.retrieval.reasoning.dimension_queries import (
    build_dimension_queries,
)


def retrieve_node(state):

    context = state[
        "hiring_context"
    ]

    query = build_query(
        context
    )

    battery_plan = (
        build_battery_plan(
            context
        )
    )

    dimension_queries = (
        build_dimension_queries(
            context,
            state["llm_plan"],
        )
    )

    all_results = []

    for dq in dimension_queries:

        results = semantic_search(

            query=dq["query"],

            top_k=8,
        )

        for idx, doc in enumerate(
            results["documents"][0]
        ):

            metadata = (
                results["metadatas"][0][idx]
            )

            role_score = (
                compute_role_score(

                    role=context.role,

                    document_text=doc,
                )
            )

            policy_score = (
                compute_policy_score(

                    role=context.role,

                    metadata=metadata,
                )
            )

            semantic_score = abs(

                results["distances"][0][idx]
            )

            final_score = (

                role_score

                + policy_score

                - semantic_score
            )

            all_results.append(

                {

                    "document": doc,

                    "metadata": metadata,

                    "role_score": role_score,

                    "policy_score": policy_score,

                    "semantic_score": semantic_score,

                    "final_score": final_score,

                    "dimension":
                    dq["dimension"],
                }
            )

    scored_results = all_results

    deduped = {}

    for item in scored_results:

        name = item[
            "metadata"
        ]["name"]

        if (
            name not in deduped
        ):

            deduped[name] = item

        else:

            if (
                item["final_score"]
                >
                deduped[name][
                    "final_score"
                ]
            ):

                deduped[name] = item

    scored_results = list(
        deduped.values()
    )

    scored_results = sorted(

        scored_results,

        key=lambda x: x[
            "final_score"
        ],

        reverse=True,
    )

    print(
        "\nTOP SCORED RESULTS:\n"
    )

    for item in scored_results[:10]:

        print(

            item["metadata"]["name"],

            " --> ",

            item["final_score"]
        )

    print("\n")

    role_lower = ""

    if context.role:

        role_lower = (
            context.role.lower()
        )

    # FORCE SPECIALIZED MATCHES

    if "react" in role_lower:

        react_results = [

            item

            for item in scored_results

            if (
                "react"
                in
                item["metadata"][
                    "name"
                ].lower()
            )
        ]

        for react_item in react_results:

            if react_item not in scored_results[:5]:

                scored_results.insert(
                    0,
                    react_item,
                )

    if "java" in role_lower:

        java_results = [

            item

            for item in scored_results

            if (
                "java"
                in
                item["metadata"][
                    "name"
                ].lower()
            )
        ]

        for java_item in java_results:

            if java_item not in scored_results[:5]:

                scored_results.insert(
                    0,
                    java_item,
                )

    balanced_results = (
        diversify_results(

            results=scored_results,

            battery_plan=battery_plan,

            limit=5,
        )
    )

    state[
        "retrieval_query"
    ] = query

    state["candidate_results"] = (
        scored_results
    )

    state[
        "retrieved_results"
    ] = balanced_results

    state[
        "battery_plan"
    ] = battery_plan

    return state