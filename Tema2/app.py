from flask import Flask, render_template, request, redirect, url_for, session
from db_connection import get_db_connection
import pymysql.err as pymysql_err

import hashlib

app = Flask(__name__, template_folder='template')
app.secret_key = 'mi_secreto'  # Cambia esto por un valor seguro

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Ruta para el dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

# Ruta para el Ignite Pod
@app.route('/ignite')
def ignite():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('ignite.html')

# Ruta para Waka Pod
@app.route('/waka')
def waka():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('waka.html')

# Ruta para Ayuda
@app.route('/help')
def help():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('help.html')

# Ruta para Suscripción
@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['last_name']
        email = request.form['email']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insertar datos de suscripción en la base de datos
        query = "INSERT INTO subscribers (name, last_name, email) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (name, last_name, email))
            conn.commit()
            cursor.close()
            conn.close()
            return render_template('subscribe.html', message="¡Gracias por suscribirte! Recibirás notificaciones pronto.")
        except pymysql_err.MySQLError as err:
            return render_template('subscribe.html', message=f"Error al suscribirse: {err}")
        except Exception as e:
            return render_template('subscribe.html', message=f"Error inesperado: {e}")

    return render_template('subscribe.html')

# Ruta para registro de usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash de la contraseña
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insertar usuario en la base de datos
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        try:
            cursor.execute(query, (username, hashed_password))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
        except pymysql_err.IntegrityError as err:
            if err.args[0] == 1062:
                return render_template('register.html', error_message="El nombre de usuario ya está registrado. Por favor, elige otro.")
            else:
                return render_template('register.html', error_message=f"Error de base de datos: {err.args[1]}")
        except Exception as e:
            return render_template('register.html', error_message=f"Error inesperado: {e}")

    return render_template('register.html')

# Ruta para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash de la contraseña
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar usuario y contraseña
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error_message="Usuario o contraseña incorrectos")

    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Para que sea accesible desde cualquier IPv4 en el puerto estándar de Flask (5000)
    app.run(host='0.0.0.0', debug=True)