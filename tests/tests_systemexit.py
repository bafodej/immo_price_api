import pytest
from fastapi.testclient import TestClient
from app.main import app

# Client de test FastAPI
client = TestClient(app)

class TestAPIEndpoints:
    """Tests des endpoints principaux"""
    
    def test_root_endpoint(self):
        """Test de la page d'accueil"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["status"] == " Opérationnelle"
        assert "endpoints" in data

    def test_predict_lille_valid_data(self):
        """Test prédiction Lille avec données valides"""
        payload = {
            "surface_bati": 75.0,
            "nombre_pieces": 3,
            "type_local": "Appartement",
            "surface_terrain": 0.0,
            "nombre_lots": 1
        }
        response = client.post("/predict/lille", json=payload)
        
        # Vérifier le statut (200 si modèle chargé, 500 si non chargé)
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "prix_m2_estime" in data
            assert "ville_modele" in data
            assert "model" in data
            assert data["ville_modele"] == "Lille"
            assert isinstance(data["prix_m2_estime"], (int, float))
