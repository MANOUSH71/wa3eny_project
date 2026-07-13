from fastapi import APIRouter, HTTPException
from app.models.scenario import ScenarioRequest, ScenarioResponse, ClassificationRequest, ClassificationResult
from app.services.ai_service import generate_scenario, DEPARTMENTS, SECTORS

router = APIRouter()

@router.post("/generate", response_model=ScenarioResponse)
async def create_scenario(request: ScenarioRequest):
    label = DEPARTMENTS.get(request.department) or SECTORS.get(request.sector, "General")
    try:
        return await generate_scenario(label, request.difficulty)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/classify", response_model=ClassificationResult)
async def classify(request: ClassificationRequest):
    return ClassificationResult(
        correct_classification=True,
        score=85,
        feedback="Good job!",
        flag_analysis={"correct": 2, "wrong": 0, "missed": 1, "total": 3}
    )
