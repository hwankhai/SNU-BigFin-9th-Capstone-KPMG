from pydantic import BaseModel

class HallucinationInput(BaseModel):
    question: str
    knowledge: str
    answer: str

class HallucinationResponse(BaseModel):
    has_hallucination: bool
    explanation: str
    details: dict
