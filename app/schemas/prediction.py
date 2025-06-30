from pydantic import BaseModel, Field
from typing import Literal

class PredictionInput(BaseModel):
    """Schéma pour les données d'entrée - Version Lille/Bordeaux"""
    surface_bati: float = Field(
        ..., 
        gt=0, 
        le=1000,
        description="Surface bâtie en m²"
    )
    nombre_pieces: int = Field(
        ..., 
        ge=1, 
        le=20,
        description="Nombre de pièces"
    )
    type_local: Literal["Appartement", "Maison"] = Field(
        ...,
        description="Type de local"
    )
    surface_terrain: float = Field(
        default=0,
        ge=0,
        description="Surface du terrain en m²"
    )
    nombre_lots: int = Field(
        default=1,
        ge=1,
        description="Nombre de lots"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "surface_bati": 75,
                "nombre_pieces": 3,
                "type_local": "Appartement",
                "surface_terrain": 0,
                "nombre_lots": 1
            }
        }

class DynamicPredictionInput(BaseModel):
    """Schéma pour l'endpoint dynamique /predict"""
    ville: Literal["lille", "bordeaux"] = Field(
        ...,
        description="Ville pour laquelle faire la prédiction"
    )
    features: PredictionInput = Field(
        ...,
        description="Caractéristiques du bien immobilier"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "ville": "bordeaux",
                "features": {
                    "surface_bati": 110,
                    "nombre_pieces": 4,
                    "type_local": "Maison",
                    "surface_terrain": 300,
                    "nombre_lots": 2
                }
            }
        }

class PredictionOutput(BaseModel):
    """Schéma pour la réponse"""
    prix_m2_estime: float = Field(
        ...,
        description="Prix estimé au m² en euros"
    )
    ville_modele: str = Field(
        ...,
        description="Ville du modèle utilisé"
    )
    model: str = Field(
        ...,
        description="Type de modèle"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "prix_m2_estime": 3245.67,
                "ville_modele": "Lille",
                "model": "LinearRegression"
            }
        }