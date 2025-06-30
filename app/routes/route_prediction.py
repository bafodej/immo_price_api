from fastapi import APIRouter, HTTPException
from ..schemas.prediction import DynamicPredictionInput, PredictionOutput

router = APIRouter()

@router.post("/predict", response_model=PredictionOutput)
async def predict_dynamic(data: DynamicPredictionInput):
    """
    Endpoint avec choix dynamique de la ville
    
    Permet de choisir entre Lille et Bordeaux dans le payload
    """
    
    ville = data.ville.lower()
    
    if ville == "lille":
        # Importer et utiliser la fonction de prédiction Lille
        from .route_lille import predict_lille_internal
        return await predict_lille_internal(data.features)
        
    elif ville == "bordeaux":
        # Importer et utiliser la fonction de prédiction Bordeaux
        from .route_bordeaux import predict_bordeaux_internal
        return await predict_bordeaux_internal(data.features)
        
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Ville '{ville}' non supportée. Villes disponibles: lille, bordeaux"
        )
