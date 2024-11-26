from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import HallucinationInput, HallucinationResponse
from .evaluator import HallucinationEvaluator
import json
import traceback

app = FastAPI(title="KnowHalu API")

# CORS 설정
origins = [
    "http://localhost:3000",  # React 개발 서버
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

evaluator = HallucinationEvaluator()

@app.post("/evaluate", response_model=HallucinationResponse)
async def evaluate_hallucination(input_data: HallucinationInput):
    try:
        result = await evaluator.evaluate(
            input_data.question,
            input_data.knowledge,
            input_data.answer
        )
        
        # String to dict if needed
        if isinstance(result, str):
            result = json.loads(result)
            
        return result
    except Exception as e:
        print(f"Error in /evaluate endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during evaluation: {str(e)}"
        )

@app.post("/evaluate-batch")
async def evaluate_batch(inputs: list[HallucinationInput]):
    try:
        results = []
        for input_data in inputs:
            result = await evaluator.evaluate(
                input_data.question,
                input_data.knowledge,
                input_data.answer
            )
            results.append(json.loads(result) if isinstance(result, str) else result)
        return results
    except Exception as e:
        print(f"Error in /evaluate-batch endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during batch evaluation: {str(e)}"
        )
