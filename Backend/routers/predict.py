# routers/cancer.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database, models, schemas
from pathlib import Path
import joblib
import numpy as np

router = APIRouter(tags=["predict"])

# 1) Build the absolute path to your pickled pipeline
current_dir = Path(__file__).parent          # e.g. Backend/routers
project_root = current_dir.parent.parent     # e.g. Fastapi_ML
model_path = project_root / "ML" / "Trained_model" / "mapicx_pipeline.pkl"

# 2) Load the model once, at startup
try:
    model = joblib.load(model_path)
    # Quick sanity check
    test_input = np.array([[5, 1, 1, 1, 2, 1, 3, 1, 1]])
    test_out = model.predict(test_input)
    print(f"[cancer.py] Model loaded, test prediction: {test_out}")
except Exception as e:
    # Fail fast if we can’t load the .pkl
    raise RuntimeError(f"Could not load model from {model_path!s}: {e}")

@router.post("/predict", response_model=schemas.PredictResponse)
def predict_cancer(
    data: schemas.PredictInput,
    db: Session = Depends(database.get_db)
):
    # 3) Turn incoming JSON into a 2D numpy array of features
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

    # 4) Run the pipeline’s predict (which in your first snippet returned a 2D array of class probabilities)
    try:
        probs = model.predict(features)  
        # pick the highest-probability class:
        pred_class = int(np.argmax(probs, axis=1)[0])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {e}"
        )

    # 5) Persist the raw inputs to your User_data table
    record = models.User_data(
        Clump_Thickness=data.Clump_Thickness, # type: ignore
        Uniformity_of_Cell_Size=data.Uniformity_of_Cell_Size,# type: ignore
        Uniformity_of_Cell_Shape=data.Uniformity_of_Cell_Shape,# type: ignore
        Marginal_Adhesion=data.Marginal_Adhesion,# type: ignore
        Single_Epithelial_Cell_Size=data.Single_Epithelial_Cell_Size,# type: ignore
        Bare_Nuclei=data.Bare_Nuclei,# type: ignore
        Bland_Chromatin=data.Bland_Chromatin,# type: ignore
        Normal_Nucleoli=data.Normal_Nucleoli,# type: ignore
        Mitoses=data.Mitoses# type: ignore
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    # 6) Return both the predicted class and the new row’s ID
    return schemas.PredictResponse(
        result=pred_class,
        id=record.id
    )
