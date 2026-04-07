# fake news detector

## prerequis

- docker desktop (avec docker compose)
- python 3.11 (si lancement sans docker)
- visual studio code + extension python + extension jupyter (pour le notebook)

## lancement notebook

Le notebook ecf_fake_news.ipynb contient les traitements et recherches sur les modèles. Avant de lancer jupyter, il peut 
être nécessaire de lancer la commande suivante :

```powershell
 python -m spacy download en_core_web_sm
```

Relancer le notebook va overrider les modèles sauvegardés et distribués avec le repo.

## lancement de l'api

### option 1 - docker (recommande)

Depuis la racine du projet :

```powershell
docker compose up -d --build
```

Verifier les logs :

```powershell
docker compose logs -f api
```

Arreter :

```powershell
docker compose down
```

### option 2 - sans docker

Depuis la racine du projet :

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## swagger

Une fois l'api demarree :

- swagger ui : http://127.0.0.1:8000/docs
- health check : `GET /health`
- prediction unitaire : `POST /predict`
- prediction batch : `POST /predict/batch`

### exemples de body

Pour `POST /predict` :

```json
{
  "title": "central bank raises interest rates by 0.25 points"
}
```

Pour `POST /predict/batch` :

```json
{
  "titles": [
    "parliament votes on new environmental legislation",
    "you will not believe what this celebrity did last night"
  ]
}
```

## fichiers modeles attendus

L'api charge ces fichiers :

- `models/best_model.keras`
- `models/vectorizer.pkl`
