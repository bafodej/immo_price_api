# 🏠 API Estimation Immobilière

**API REST pour l'estimation automatisée des prix au m² d'un bien immobilier**

Cette API expose des modèles prédictifs entraînés pour estimer les prix immobiliers à Lille et Bordeaux, permettant un A/B testing des performances des modèles sur différentes villes.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#️-architecture)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Endpoints](#-endpoints)
- [Exemples d'utilisation](#-exemples-dutilisation)
- [Structure du projet](#-structure-du-projet)
- [Technologies utilisées](#-technologies-utilisées)
- [Méthodologie](#-méthodologie)

## ✨ Fonctionnalités

- **3 endpoints de prédiction** : Lille, Bordeaux et choix dynamique
- **Modèles pré-entraînés** : Réutilisation du modèle Lille pour Bordeaux (selon énoncé Phase 3)
- **A/B Testing** : Comparaison des performances sur différentes villes
- **Documentation interactive** : Interface Swagger UI automatique
- **Validation des données** : Schémas Pydantic avec validation
- **Gestion d'erreurs** : Messages explicites et codes de statut appropriés

## 🏗️ Architecture

```
API FastAPI
├── Endpoint /predict/lille      (Modèle entraîné sur Lille)
├── Endpoint /predict/bordeaux   (Modèle Lille appliqué à Bordeaux)
└── Endpoint /predict            (Choix dynamique de ville)
```

**Principe** : Un seul modèle entraîné sur les données de Lille est réutilisé pour faire des prédictions sur Bordeaux, permettant d'analyser la généralisation du modèle.

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### 1. Cloner le projet
```bash
git clone <url-du-repository>
cd immoprice-api
```

### 2. Créer un environnement virtuel
```bash
python -m venv immo_env
source immo_env/bin/activate  # Linux/Mac
# ou
immo_env\Scripts\activate     # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Vérifier la structure
Assurez-vous d'avoir les modèles dans le dossier `models/` :
```
immoprice-api/
├── models/
│   ├── lille_appartements.pkl
│   └── scaler_lille_apt.pkl
└── app/
```

## 💻 Utilisation

### Lancer l'API
```bash
uvicorn app.main:app --reload
```

L'API sera accessible sur : `http://127.0.0.1:8000`

### Documentation
- **Swagger UI** : `http://127.0.0.1:8000/docs`
- **ReDoc** : `http://127.0.0.1:8000/redoc`

## 🛠 Endpoints

### 1. Prédiction Lille
```http
POST /predict/lille
```

### 2. Prédiction Bordeaux  
```http
POST /predict/bordeaux
```

### 3. Prédiction Dynamique
```http
POST /predict
```

### Schéma des données d'entrée

#### Pour `/predict/lille` et `/predict/bordeaux`
```json
{
  "surface_bati": 75.0,
  "nombre_pieces": 3,
  "type_local": "Appartement",
  "surface_terrain": 0.0,
  "nombre_lots": 1
}
```



### Schéma de réponse
```json
{
  "prix_m2_estime": 3245.67,
  "ville_modele": "Lille",
  "model": "LinearRegression"
}
```

## 📝 Exemples d'utilisation



### Exemple  : Estimation Bordeaux
```bash
curl -X POST "http://127.0.0.1:8000/predict/bordeaux" \
     -H "Content-Type: application/json" \
     -d '{
       "surface_bati": 110,
       "nombre_pieces": 4,
       "type_local": "Maison",
       "surface_terrain": 300,
       "nombre_lots": 2
     }'
```



## 📁 Structure du projet

```
immoprice-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée FastAPI
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── route_lille.py       # Endpoints Lille
│   │   ├── route_bordeaux.py    # Endpoints Bordeaux
│   │   └── route_prediction.py  # Endpoint dynamique
│   └── schemas/
│       ├── __init__.py
│       └── prediction.py       # Schémas Pydantic
├── models/
│   ├── lille_appartements.pkl  # Modèle entraîné
│   └── scaler_lille_apt.pkl    # Scaler pour standardisation
├── requirements.txt
└── README.md
```

## 🔧 Technologies utilisées

- **FastAPI** : Framework web moderne et rapide
- **Pydantic** : Validation des données et sérialisation
- **scikit-learn** : Modèles de machine learning
- **pandas** : Manipulation des données
- **joblib** : Sérialisation des modèles
- **uvicorn** : Serveur ASGI

## 📊 Méthodologie

### Phase 1 : Entraînement (Lille)
- Modèle entraîné uniquement sur les données de Lille
- Sauvegarde du modèle et du scaler

### Phase 2 : Test de généralisation (Bordeaux)  
- Application du modèle Lille sur les données de Bordeaux
- **Pas de réentraînement** selon l'énoncé
- Calcul des métriques de performance (MSE)

### Phase 3 : API REST
- Exposition des modèles via 3 endpoints
- A/B Testing des performances
- Facilitation de l'intégration dans des services externes

## 🎯 A/B Testing

L'API permet de comparer facilement les performances du modèle Lille sur différentes villes :

- **Endpoint Lille** (`/predict/lille`) : Performance du modèle sur sa ville d'entraînement
- **Endpoint Bordeaux** (`/predict/bordeaux`) : Performance du même modèle sur une nouvelle ville
- **Comparaison** : Analyse de la généralisation du modèle

## 🔍 Validation des données

- **Surface bâtie** : 0 < surface ≤ 1000 m²
- **Nombre de pièces** : 1 ≤ pièces ≤ 20
- **Type de local** : "Appartement" ou "Maison"
- **Surface terrain** : ≥ 0 m²
- **Nombre de lots** : ≥ 1

## 🚧 Gestion d'erreurs

- **400** : Ville non supportée ou données invalides
- **500** : Modèle non chargé ou erreur de prédiction
- **422** : Erreur de validation Pydantic

## 📈 Développement futur

- [ ] Ajout de nouvelles villes
- [ ] Métriques de performance en temps réel
- [ ] Cache des prédictions
- [ ] Authentification API
- [ ] Tests unitaires
- [ ] Monitoring et logging


---

**🔗 Liens utiles :**
- Documentation interactive : `http://127.0.0.1:8000/docs`
- Statut de l'API : `http://127.0.0.1:8000/`