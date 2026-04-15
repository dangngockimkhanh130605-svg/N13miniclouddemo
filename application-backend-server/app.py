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
    try:
        with open("students.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Tạo chuỗi HTML để hiển thị bảng có màu sắc
        html_content = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f9; }
                h2 { color: #4a4a8a; text-align: center; }
                table { width: 80%; margin: auto; border-collapse: collapse; box-shadow: 0 5px 15px rgba(0,0,0,0.1); background-color: white; }
                th { background-color: #6c5ce7; color: white; padding: 12px; text-align: left; }
                td { padding: 10px; border-bottom: 1px solid #ddd; }
                tr:nth-child(even) { background-color: #f2f2f2; }
                tr:hover { background-color: #e1dcf9; transition: 0.3s; }
                .gpa-high { color: #27ae60; font-weight: bold; }
            </style>
        </head>
        <body>
            <h2>Danh sách sinh viên (JSON Data)</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Họ và Tên</th>
                    <th>Chuyên ngành</th>
                    <th>GPA</th>
                </tr>
        """
        
        for s in data:
            html_content += f"""
                <tr>
                    <td>{s['id']}</td>
                    <td>{s['name']}</td>
                    <td>{s['major']}</td>
                    <td class="{"gpa-high" if s['gpa'] >= 3.5 else ""}">{s['gpa']}</td>
                </tr>
            """
            
        html_content += """
            </table>
        </body>
        </html>
        """
        return html_content
    except Exception as e:
        return f"<h3>Lỗi: {str(e)}</h3>", 500

def get_db_connection():
    return mysql.connector.connect(
        host="relational-database-server",
        user="root",
        password="root",
        database="studentdb"
    )

@app.get("/students-db") 
def get_students_from_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) 
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Tạo chuỗi HTML với màu sắc khác để phân biệt (màu xanh lá)
        html_content = """
        <html>
        <head>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f0fdf4; }
                h2 { color: #166534; text-align: center; }
                table { width: 85%; margin: auto; border-collapse: collapse; background-color: white; border: 1px solid #bbf7d0; }
                th { background-color: #22c55e; color: white; padding: 15px; text-align: left; }
                td { padding: 12px; border-bottom: 1px solid #f0fdf4; color: #1f2937; }
                tr:nth-child(even) { background-color: #f9fefb; }
                tr:hover { background-color: #dcfce7; }
            </style>
        </head>
        <body>
            <h2>Danh sách sinh viên (Truy vấn từ MariaDB)</h2>
            <table>
                <tr>
                    <th>#</th>
                    <th>Student ID</th>
                    <th>Fullname</th>
                    <th>DOB</th>
                    <th>Major</th>
                </tr>
        """
        for row in rows:
            html_content += f"""
                <tr>
                    <td>{row['id']}</td>
                    <td>{row['student_id']}</td>
                    <td>{row['fullname']}</td>
                    <td>{row['dob']}</td>
                    <td>{row['major']}</td>
                </tr>
            """
        html_content += "</table></body></html>"
        return html_content
    except Exception as e:
        return f"<h3>Lỗi kết nối Database: {str(e)}</h3>", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
