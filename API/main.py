# main.py
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import bcrypt

app = FastAPI()

# Autoriser les requêtes depuis Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en dev, "*" suffit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connexion MySQL
def get_db():
    return mysql.connector.connect(
        host="localhost",       # ou IP de ton serveur MySQL
        user="root",            # utilisateur MySQL
        password="",
        database="app_login"      # nom de ta base
    )

# ==================== TEST ROOT ====================
@app.get("/")
async def root():
    return {"message": "FastAPI fonctionne ✅"}

# ==================== REGISTER ====================
@app.post("/register")
async def register(email: str = Form(...), password: str = Form(...)):
    db = get_db()
    cursor = db.cursor()

    # Vérifie si l'email existe déjà
    cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
    if cursor.fetchone():
        return {"success": False, "message": "Email déjà utilisé ❌"}

    # Hash du mot de passe
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_pw))
    db.commit()

    return {"success": True, "message": "Compte créé avec succès ✅"}

# ==================== LOGIN ====================
@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return {"success": False, "message": "Utilisateur non trouvé ❌"}

    # Vérifie le mot de passe
    if bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')): # type: ignore
        return {"success": True, "message": "Connexion réussie 🎉"}
    else:
        return {"success": False, "message": "Mot de passe incorrect ❌"}


# python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000