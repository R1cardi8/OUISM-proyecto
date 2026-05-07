from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
import hashlib
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_connection():
    return mysql.connector.connect(
        host     = os.getenv('DB_HOST'),
        user     = os.getenv('DB_USER'),
        password = os.getenv('DB_PASS'),
        database = os.getenv('DB_NAME')
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ── REGISTRO ──
@app.route('/api/registro', methods=['POST'])
def registro():
    data = request.get_json()
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)',
            (data['nombre'], data['email'], hash_password(data['password']))
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({ 'id': new_id, 'message': 'Usuario registrado' })
    except mysql.connector.IntegrityError:
        return jsonify({ 'error': 'El email ya está registrado' }), 400
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500

# ── LOGIN ──
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM usuarios WHERE email = %s AND password = %s',
            (data['email'], hash_password(data['password']))
        )
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        if usuario:
            return jsonify({
                'id':     usuario['id'],
                'nombre': usuario['nombre'],
                'email':  usuario['email'],
                'rol':    usuario['rol']
            })
        else:
            return jsonify({ 'error': 'Email o contraseña incorrectos' }), 401
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500

# ── GET INCIDENTES ──
@app.route('/api/incidentes', methods=['GET'])
def get_incidentes():
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM incidentes ORDER BY fecha DESC')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500

# ── POST INCIDENTE ──
@app.route('/api/incidentes', methods=['POST'])
def create_incidente():
    data = request.get_json()
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO incidentes (usuario_id, titulo, descripcion, tipo, ubicacion, prioridad, foto) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (
                data.get('usuario_id'),
                data['titulo'],
                data['descripcion'],
                data['tipo'],
                data.get('ubicacion'),
                data['prioridad'],
                data.get('foto')
            )
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({ 'id': new_id, 'message': 'Incidente creado' })
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500

# ── DELETE INCIDENTE ──
@app.route('/api/incidentes/<int:id>', methods=['DELETE'])
def delete_incidente(id):
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM incidentes WHERE id = %s', (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({ 'message': 'Incidente eliminado' })
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)