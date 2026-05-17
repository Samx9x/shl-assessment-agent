from typing import TypedDict
from typing import List
from typing import Optional


class HiringContext:

    def __init__(self):

        self.role = None

        self.seniority = None

        self.skills = []

        self.behavioral_traits = []

        self.languages = []

        self.constraints = []

        self.refinement_requests = []

        self.assessment_dimensions = {
            "technical": False,
            "personality": False,
            "cognitive": False,
            "situational_judgment": False,
            "simulation": False,
            "leadership": False,
            "communication": False,
            "safety": False,
        }

        self.preferred_test_types = []

        self.excluded_test_types = []

        self.has_recommended = False

        self.conversation_stage = (
            "discovery"
        )


class GraphState(TypedDict):

    messages: list

    hiring_context: HiringContext

    intent: str

    ambiguity_detected: bool

    ambiguity_reason: str

    retrieval_query: str

    retrieved_results: list

    llm_plan: dict

    battery_plan: list

    final_recommendations: list

    final_response: dict

    refusal_reason: str

    candidate_results: list

    