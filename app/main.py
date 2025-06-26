from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import os
from app.schemas.prediction import PredictionInput, PredictionOutput

# Configuration de l'application
app = FastAPI(
    title=" API Estimation Lille",
    description="API pour estimer les prix immobiliers à Lille",
    version="1.0.0"
)

# Variables globales pour les modèles
lille_model = None
lille_scaler = None

@app.on_event("startup")
async def load_models():
    """Charger les modèles au démarrage"""
    global lille_model, lille_scaler
    
    try:
        # Chargement du modèle Lille
        model_path = "models/lille_appartements.pkl"
        if os.path.exists(model_path):
            lille_model = joblib.load(model_path)
            print(" Modèle Lille chargé")
        else:
            print(f" Modèle non trouvé: {model_path}")
        
        # Chargement du scaler Lille
        scaler_path = "models/scaler_lille_apt.pkl"
        if os.path.exists(scaler_path):
            lille_scaler = joblib.load(scaler_path)
            print(" Scaler Lille chargé")
        else:
            print(f" Scaler non trouvé: {scaler_path}")
            
    except Exception as e:
        print(f" Erreur chargement: {e}")

@app.get("/")  # route acceuil de l'api 
async def root():
    """Page d'accueil"""
    return {
        "message": " API Estimation Lille",
        "status": " Opérationnelle",
        "endpoint": "/predict/lille",
        "docs": "/docs"
    }

@app.post("/predict/lille", response_model=PredictionOutput) # Route predict 
async def predict_lille(data: PredictionInput):
    """Prédiction prix immobilier Lille"""
    
    # Vérifier que le modèle est chargé
    if lille_model is None:
        raise HTTPException(
            status_code=500, 
            detail="Modèle Lille non chargé"
        )
    
    try:
        # Préparer les features
        type_local_encoded = 1 if data.type_local == 'Appartement' else 0
        
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
            detail=f"Erreur lors de la prédiction: {str(e)}"
        )

@app.get("/health") # Routes pour verifier que l'api fonctionne 
async def health_check():
    """Vérification de l'état"""
    return {
        "status": "healthy",
        "models": {
            "lille_model": lille_model is not None,
            "lille_scaler": lille_scaler is not None
        }
    }