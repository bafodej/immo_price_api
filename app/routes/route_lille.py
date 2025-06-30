from fastapi import APIRouter, HTTPException
import joblib
import pandas as pd
import os
from ..schemas.prediction import PredictionInput, PredictionOutput

router = APIRouter()

# Variables globales pour les modèles Lille
lille_model = None
lille_scaler = None

@router.on_event("startup")
async def load_lille_models():
    """Charger les modèles Lille au démarrage"""
    global lille_model, lille_scaler
    
    try:
        # Chargement du modèle Lille
        model_path = "models/lille_appartements.pkl"
        if os.path.exists(model_path):
            lille_model = joblib.load(model_path)
            print(" Modèle Lille chargé")
        else:
            print(f" Modèle Lille non trouvé: {model_path}")
        
        # Chargement du scaler Lille
        scaler_path = "models/scaler_lille_apt.pkl"
        if os.path.exists(scaler_path):
            lille_scaler = joblib.load(scaler_path)
            print(" Scaler Lille chargé")
        else:
            print(f" Scaler Lille non trouvé: {scaler_path}")
            
    except Exception as e:
        print(f" Erreur chargement Lille: {e}")

 
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
