from fastapi import APIRouter, HTTPException
import mlflow.sklearn  
import pandas as pd
import os
from ..schemas.prediction import PredictionInput, PredictionOutput

# Configuration MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "file:./notebooks/mlruns")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Run ID du modèle Lille
LILLE_APT_RUN_ID = "cc34f04d13ee4fd3b984a7d16ad7d919"

router = APIRouter()

# Variables globales pour les modèles Lille
lille_model = None
lille_scaler = None

@router.on_event("startup")
async def load_lille_models():
    """Charger les modèles Lille depuis MLflow au démarrage"""
    global lille_model, lille_scaler
    
    try:
        print("Chargement modele Lille depuis MLflow...")
        lille_model = mlflow.sklearn.load_model(f"runs:/{LILLE_APT_RUN_ID}/model")
        lille_scaler = mlflow.sklearn.load_model(f"runs:/{LILLE_APT_RUN_ID}/scaler")
        print("Modele Lille charge avec succes")
    except Exception as e:
        print(f"Erreur chargement Lille: {e}")


async def predict_lille_internal(data: PredictionInput) -> PredictionOutput:
    """Fonction interne de prédiction Lille"""
    
    if lille_model is None:
        raise HTTPException(
            status_code=500, 
            detail="Modèle Lille non chargé"
        )
    
    try:
        # Préparer les features
        features = pd.DataFrame({
            'Surface reelle bati': [data.surface_bati],
            'Nombre pieces principales': [data.nombre_pieces],
            'Surface terrain': [data.surface_terrain],
            'Nombre de lots': [data.nombre_lots]
        })
        
        # Standardisation si scaler disponible
        if lille_scaler is not None:
            features_scaled = lille_scaler.transform(features)
        else:
            features_scaled = features.values
        
        # Prédiction
        prediction = lille_model.predict(features_scaled)[0]
        
        return PredictionOutput(
            prix_m2_estime=round(float(prediction), 2),
            ville_modele="Lille",
            model=lille_model.__class__.__name__
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur prédiction Lille: {str(e)}"
        )

# Endpoint public 
@router.post("/predict/lille", response_model=PredictionOutput)
async def predict_lille(data: PredictionInput):
    """Prédiction prix immobilier pour Lille"""
    return await predict_lille_internal(data)
