from fastapi import APIRouter, HTTPException
import joblib
import pandas as pd
import os
from ..schemas.prediction import PredictionInput, PredictionOutput

router = APIRouter()

# Variables globales pour les modèles Bordeaux
bordeaux_model = None
bordeaux_scaler = None

@router.on_event("startup")
async def load_bordeaux_models():
    """Charger les modèles Bordeaux au démarrage"""
    global bordeaux_model, bordeaux_scaler
    
    try:
        # Chargement du modèle Bordeaux (même modèle Lille)
        model_path = "models/lille_appartements.pkl"
        if os.path.exists(model_path):
            bordeaux_model = joblib.load(model_path)
            print(" Modèle Bordeaux chargé")
        else:
            print(f" Modèle Bordeaux non trouvé: {model_path}")
        
        # Chargement du scaler Bordeaux (même scaler Lille)
        scaler_path = "models/scaler_lille_apt.pkl"
        if os.path.exists(scaler_path):
            bordeaux_scaler = joblib.load(scaler_path)
            print(" Scaler Bordeaux chargé")
        else:
            print(f" Scaler Bordeaux non trouvé: {scaler_path}")
            
    except Exception as e:
        print(f" Erreur chargement Bordeaux: {e}")


async def predict_bordeaux_internal(data: PredictionInput) -> PredictionOutput:
    """Fonction interne de prédiction Bordeaux (utilise le modèle Lille)"""
    
    if bordeaux_model is None:
        raise HTTPException(
            status_code=500, 
            detail="Modèle Bordeaux non chargé"
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
        if bordeaux_scaler is not None:
            features_scaled = bordeaux_scaler.transform(features)
        else:
            features_scaled = features.values
        
        # Prédiction
        prediction = bordeaux_model.predict(features_scaled)[0]
        
        return PredictionOutput(
            prix_m2_estime=round(float(prediction), 2),
            ville_modele="Bordeaux",
            model=bordeaux_model.__class__.__name__
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur prédiction Bordeaux: {str(e)}"
        )

# Endpoint public (maintenant utilise la fonction interne)
@router.post("/predict/bordeaux", response_model=PredictionOutput)
async def predict_bordeaux(data: PredictionInput):
    """Prédiction prix immobilier pour Bordeaux"""
    return await predict_bordeaux_internal(data)

