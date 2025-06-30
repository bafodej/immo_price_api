from fastapi import FastAPI
from .routes.route_lille import router as lille_router
from .routes.route_bordeaux import router as bordeaux_router  
from .routes.route_prediction import router as prediction_router

# Configuration de l'application
app = FastAPI(
    title=" API Estimation Immobilière",
    description="""
    API REST pour l'estimation automatisée des prix immobiliers.
    
    ## Fonctionnalités
    * Modèles prédictif pour Lille et Bordeaux
    * Prédictions en temps réel
    """,
    version="1.0.0"
)

# Inclure tous les routers
app.include_router(prediction_router, tags=[" Prédiction Dynamique"])
app.include_router(lille_router, tags=[" Lille"])
app.include_router(bordeaux_router, tags=[" Bordeaux"])

@app.get("/", tags=[" Général"])
def root(): 
    """Page d'accueil de l'API"""
    return {
        "message": " API Estimation Immobilière",
        "status": " Opérationnelle",
        "version": "1.0.0",
        "cities": ["Lille", "Bordeaux"],
        "endpoints": {
            "main": {
                "predict": "POST /predict",
                "models_status": "GET /models/status",
                "cities": "GET /cities"
            },
            "lille": {
                "predict": "POST /predict/lille",
                "health": "GET /lille/health"
            },
            "bordeaux": {
                "predict": "POST /predict/bordeaux", 
                "health": "GET /bordeaux/health"
            },
            "docs": "/docs"
        }
    }


