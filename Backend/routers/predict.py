from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database, models, schemas
from typing import List, Optional
import numpy as np
import joblib
from pathlib import Path

router = APIRouter(tags=['predict'])

# Get the absolute path to the model file
current_dir = Path(__file__).parent  # Backend/routers
project_root = current_dir.parent.parent  # Project root (Fastapi_ML directory)
model_path = project_root / "ML" / "Trained_model" / "mapicx_pipeline.pkl"

# Load the model
try:
    model = joblib.load(model_path)
except FileNotFoundError:
    raise RuntimeError(f"Model file not found at {model_path}. "
                       "Please ensure the file exists in the repository.")

@router.post("/predict", response_model=schemas.PredictResponse)
def predict_cancer(data: schemas.PredictInput, db: Session = Depends(database.get_db)):
    features = np.array([[
        data.Clump_Thickness,
        data.Uniformity_of_Cell_Size,
        data.Uniformity_of_Cell_Shape,
        data.Marginal_Adhesion,
        data.Single_Epithelial_Cell_Size,
        data.Bare_Nuclei,
        data.Bland_Chromatin,
        data.Normal_Nucleoli,
        data.Mitoses
    ]])

    # Get prediction
    prediction = model.predict(features)
    pred_class = int(prediction[0])  # Directly get the prediction

    # Create database record
    record = models.User_data(
        Clump_Thickness=data.Clump_Thickness,
        Uniformity_of_Cell_Size=data.Uniformity_of_Cell_Size,
        Uniformity_of_Cell_Shape=data.Uniformity_of_Cell_Shape,
        Marginal_Adhesion=data.Marginal_Adhesion,
        Single_Epithelial_Cell_Size=data.Single_Epithelial_Cell_Size,
        Bare_Nuclei=data.Bare_Nuclei,
        Bland_Chromatin=data.Bland_Chromatin,
        Normal_Nucleoli=data.Normal_Nucleoli,
        Mitoses=data.Mitoses
    )

    # Save to database
    db.add(record)
    db.commit()
    db.refresh(record)

    return schemas.PredictResponse(
        id=record.id,
        result=pred_class
    )