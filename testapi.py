from fastapi import APIRouter, HTTPException, status
from app.schemas.prediction import (
    PredictionInput, 
    PredictionInputDynamic, 
    PredictionOutput, 
    ErrorResponse
)
from app.models.model_loader import model_manager
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/predict", tags=["Prédictions"])

@router.post(
    "/lille",
    response_model=PredictionOutput,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Prédiction avec modèle Lille",
    description="Estime le prix au m² d'un bien immobilier en utilisant le modèle entraîné sur les données de Lille"
)
async def predict_lille(data: PredictionInput):
    """Prédiction avec le modèle Lille"""
    try:
        # Conversion en dict pour le gestionnaire de modèles
        features_dict = {
            "surface_bati": data.surface_bati,
            "nombre_pieces": data.nombre_pieces,
            "type_local": data.type_local.value,
            "surface_terrain": data.surface_terrain,
            "nombre_lots": data.nombre_lots
        }
        
        # Prédiction
        result = model_manager.predict("lille", features_dict)
        
        return PredictionOutput(**result)
        
    except ValueError as e:
        logger.error(f"Erreur de validation Lille: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "ValidationError",
                "message": str(e),
                "details": {"ville": "lille", "data": features_dict}
            }
        )
    
    except Exception as e:
        logger.error(f"Erreur prédiction Lille: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "PredictionError",
                "message": "Erreur lors de la prédiction",
                "details": {"error_type": type(e).__name__}
            }
        )

@router.post(
    "/bordeaux",
    response_model=PredictionOutput,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Prédiction avec modèle Bordeaux",
    description="Estime le prix au m² d'un bien immobilier en utilisant le modèle entraîné sur les données de Bordeaux"
)
async def predict_bordeaux(data: PredictionInput):
    """Prédiction avec le modèle Bordeaux"""
    try:
        # Conversion en dict pour le gestionnaire de modèles
        features_dict = {
            "surface_bati": data.surface_bati,
            "nombre_pieces": data.nombre_pieces,
            "type_local": data.type_local.value,
            "surface_terrain": data.surface_terrain,
            "nombre_lots": data.nombre_lots
        }
        
        # Prédiction
        result = model_manager.predict("bordeaux", features_dict)
        
        return PredictionOutput(**result)
        
    except ValueError as e:
        logger.error(f"Erreur de validation Bordeaux: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "ValidationError",
                "message": str(e),
                "details": {"ville": "bordeaux", "data": features_dict}
            }
        )
    
    except Exception as e:
        logger.error(f"Erreur prédiction Bordeaux: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "PredictionError",
                "message": "Erreur lors de la prédiction",
                "details": {"error_type": type(e).__name__}
            }
        )

@router.post(
    "",
    response_model=PredictionOutput,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Prédiction dynamique",
    description="Estime le prix au m² en choisissant dynamiquement la ville du modèle à utiliser"
)
async def predict_dynamic(data: PredictionInputDynamic):
    """Prédiction avec choix dynamique de la ville"""
    try:
        # Conversion en dict pour le gestionnaire de modèles
        features_dict = {
            "surface_bati": data.features.surface_bati,
            "nombre_pieces": data.features.nombre_pieces,
            "type_local": data.features.type_local.value,
            "surface_terrain": data.features.surface_terrain,
            "nombre_lots": data.features.nombre_lots
        }
        
        # Prédiction avec la ville choisie
        result = model_manager.predict(data.ville.value, features_dict)
        
        return PredictionOutput(**result)
        
    except ValueError as e:
        logger.error(f"Erreur de validation dynamique: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "ValidationError",
                "message": str(e),
                "details": {"ville": data.ville.value, "data": features_dict}
            }
        )
    
    except Exception as e:
        logger.error(f"Erreur prédiction dynamique: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "PredictionError",
                "message": "Erreur lors de la prédiction",
                "details": {"error_type": type(e).__name__}
            }
        )

@router.get(
    "/models",
    summary="Modèles disponibles",
    description="Liste les modèles et scalers chargés"
)
async def get_available_models():
    """Retourne les modèles disponibles"""
    try:
        return model_manager.get_available_models()
    except Exception as e:
        logger.error(f"Erreur récupération modèles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "SystemError",
                "message": "Erreur lors de la récupération des modèles"
            }
        )

@router.get(
    "/health",
    summary="Statut de santé",
    description="Vérifie l'état des modèles"
)
async def health_check():
    """Health check des modèles"""
    try:
        return model_manager.health_check()
    except Exception as e:
        logger.error(f"Erreur health check: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "HealthCheckError",
                "message": "Erreur lors du health check"
            }
        )