from flask import Flask, jsonify, request
import time, requests, os, json
from jose import jwt
import mysql.connector

ISSUER   = os.getenv("OIDC_ISSUER", "http://localhost:8081/realms/realm_sv001")
AUDIENCE = os.getenv("OIDC_AUDIENCE", "account")
JWKS_URL = os.getenv(
    "OIDC_JWKS_URL",
    "http://authentication-identity-server:8080/realms/realm_sv001/protocol/openid-connect/certs"
)

_JWKS = None; _TS = 0
def get_jwks():
    global _JWKS, _TS
    now = time.time()
    if not _JWKS or now - _TS > 600:
        _JWKS = requests.get(JWKS_URL, timeout=5).json()
        _TS = now
    return _JWKS

app = Flask(__name__)

@app.get("/hello")
def hello(): return jsonify(message="Hello from App Server!")

@app.get("/secure")
def secure():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify(error="Missing Bearer token"), 401

    token = auth.split(" ", 1)[1]

    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        jwks = get_jwks()
        rsa_key = None

        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                rsa_key = {
                    "kty": key.get("kty"),
                    "kid": key.get("kid"),
                    "use": key.get("use"),
                    "n": key.get("n"),
                    "e": key.get("e"),
                }
                break

        if rsa_key is None:
            return jsonify(error="Unable to find appropriate key"), 401

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=ISSUER
        )

        return jsonify(
            message="Secure resource OK",
            preferred_username=payload.get("preferred_username")
        )
    except Exception as e:
        return jsonify(error=str(e)), 401
    
@app.get("/student")
def student(): 
    with open("students.json") as f:
        data = json.load(f)
    return jsonify(data)

def get_db_connection():
    return mysql.connector.connect(
        host="relational-database-server",
        user="root",
        password="admin",
        database="studentdb"
    )

@app.get("/student-db") 
def get_students_from_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) 
        
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
