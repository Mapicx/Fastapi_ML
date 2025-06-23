from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from .. import database,models,schemas
from typing import List,Optional
import numpy as np
import joblib

router = APIRouter(tags=['predict'])
model = joblib.load(r"ML\Trained_model\mapicx_pipeline.pkl")



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

    probs = model.predict(features)
    pred_class = int(np.argmax(probs, axis=1)[0])


    record = models.User_data(
        Clump_Thickness=data.Clump_Thickness,  # type: ignore
        Uniformity_of_Cell_Size=data.Uniformity_of_Cell_Size,  # type: ignore
        Uniformity_of_Cell_Shape=data.Uniformity_of_Cell_Shape,  # type: ignore
        Marginal_Adhesion=data.Marginal_Adhesion,  # type: ignore
        Single_Epithelial_Cell_Size=data.Single_Epithelial_Cell_Size,  # type: ignore
        Bare_Nuclei=data.Bare_Nuclei,  # type: ignore
        Bland_Chromatin=data.Bland_Chromatin,  # type: ignore
        Normal_Nucleoli=data.Normal_Nucleoli,  # type: ignore
        Mitoses=data.Mitoses  # type: ignore
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return schemas.PredictResponse(
        id = record.id,
        result = pred_class
        
    )





