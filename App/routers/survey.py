from datetime import datetime
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status

from ..database import SessionLocal
from pydantic import BaseModel, Field
from ..models import Survey, SurveyStatus, Question, QuestionOption

from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/survey',
    tags=['survey']
)


def get_db():
    """
    Abre uma nova conexão com o banco de dados e a retorna (yield)
    Após o fim do escopo em que a função get_db é chamada, a conexão é fechada
    """

    db = SessionLocal()
    try: yield db
    finally: db.close()


db_dependency = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory="App/templates")


class SurveyStatusRequest(BaseModel):
    survey_status: str = Field(min_length=5)
    

class SurveyRequest(BaseModel):
    name: str = Field(min_length=5)
    description: str = Field(min_length=5, max_length=100)
    start_date: datetime 
    end_date: Optional[datetime] = None
    min_responses: int = Field(min=0)
    max_responses: int = Field(min=1)


### PAGES ###

@router.get("/city/{survey_id}")
async def render_restaurant_code_page( request: Request, survey_id: int):

    return templates.TemplateResponse("city.html", {"request": request})

@router.get("/fill/{survey_id}")
async def render_survey_response_page(request: Request,
        db: db_dependency, survey_id: int):
    
    question_model = db.query(Question).filter(Question.survey_id == survey_id).order_by(Question.order).all()
    
    question_opt_list = []
    for question in question_model:
        question_opt_list.append(
            db.query(QuestionOption).filter(QuestionOption.question_id == question.question_id).order_by(QuestionOption.order).all()
        )
    question_opt_list = [x for _ in question_opt_list for x in _]
    
    return templates.TemplateResponse("response.html", {"request": request,
            "questions": question_model, "questions_opt": question_opt_list})


### ENDPOINTS ###

@router.get("/status", status_code=status.HTTP_200_OK)
async def get_all_survey_status(db: db_dependency):
    return db.query(SurveyStatus).all()


@router.post("/status/create", status_code=status.HTTP_201_CREATED)
async def create_survey_status(db: db_dependency, survey_status_request: SurveyStatusRequest):
    
    # pesquisa criada automaticamente com status_id = 0
    survey_status_model = SurveyStatus(**survey_status_request.model_dump())
    db.add(survey_status_model)
    db.commit()


@router.delete("/status/delete/{survey_status_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_survey_status(db: db_dependency, survey_status_id: int = Path(gt=0)):
    
    survey_status_model = db.query(SurveyStatus).filter(SurveyStatus.survey_status_id == survey_status_id).first()
    if survey_status_model is None: raise HTTPException(status_code=404, detail="Survey status not found.")
    
    db.query(SurveyStatus).filter(SurveyStatus.survey_status_id == survey_status_id).first().delete()
    db.commit()


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_surveys(db: db_dependency):
    return db.query(Survey).all()


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_survey(db: db_dependency, survey_request: SurveyRequest):
    
    # pesquisa criada automaticamente com status_id = 0
    survey_model = Survey(**survey_request.model_dump(), survey_status_id = 1)
    db.add(survey_model)
    db.commit()


@router.delete("/delete/{survey_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_survey(db: db_dependency, survey_id: int = Path(gt=0)):
    
    survey_model = db.query(Survey).filter(Survey.survey_id == survey_id).first()
    if survey_model is None: raise HTTPException(status_code=404, detail="Survey not found.")
    
    db.query(Survey).filter(Survey.survey_id == survey_id).first().delete()
    db.commit()
