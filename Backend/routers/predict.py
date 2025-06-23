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
    # Test model to ensure it's working
    test_input = np.array([[5,1,1,1,2,1,3,1,1]])
    test_pred = model.predict(test_input)
    print(f"Model test prediction: {test_pred}")
except Exception as e:
    raise RuntimeError(f"Error loading model: {str(e)}")

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
    try:
        prediction = model.predict(features)
        # Handle both 1D and 2D output formats
        if prediction.ndim == 2 and prediction.shape[0] == 1:
            pred_class = int(prediction[0][0])
        else:
            pred_class = int(prediction[0])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

    # Create database record
    record = models.User_data(
        Clump_Thickness=data.Clump_Thickness, # type: ignore
        Uniformity_of_Cell_Size=data.Uniformity_of_Cell_Size, # type: ignore
        Uniformity_of_Cell_Shape=data.Uniformity_of_Cell_Shape, # type: ignore
        Marginal_Adhesion=data.Marginal_Adhesion, # type: ignore
        Single_Epithelial_Cell_Size=data.Single_Epithelial_Cell_Size, # type: ignore
        Bare_Nuclei=data.Bare_Nuclei, # type: ignore
        Bland_Chromatin=data.Bland_Chromatin, # type: ignore
        Normal_Nucleoli=data.Normal_Nucleoli, # type: ignore
        Mitoses=data.Mitoses # type: ignore
    )

    # Save to database
    db.add(record)
    db.commit()
    db.refresh(record)

    return schemas.PredictResponse(
        id=record.id,
        result=pred_class
    )