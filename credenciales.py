import pyotp
import sqlite3  
import hashlib  
import uuid     
from flask import Flask, request

app = Flask(__name__)

db_name = 'credenciales.db' 
@app.route('/')
def index():
    return 'Sitio web de gestión de credenciales.'

######################################### Plain Text #########################################################
@app.route('/signup/v1', methods=['POST'])
def signup_v1():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_PLAIN
           (USERNAME  TEXT    PRIMARY KEY NOT NULL,
            PASSWORD  TEXT    NOT NULL);''')
    conn.commit()
    try:
        c.execute("INSERT INTO USER_PLAIN (USERNAME,PASSWORD) "
                  "VALUES ('{0}', '{1}')".format(request.form['username'], request.form['password']))
        conn.commit()
    except sqlite3.IntegrityError:
        return "El nombre de usuario ha sido registrado."
    print('username: ', request.form['username'], ' password: ', request.form['password'])
    return "REGISTRO EXITOSO"

def verify_plain(username, password):
    conn = sqlite3.connect('credenciales.db')
    c = conn.cursor()
    query = "SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = '{0}'".format(username)
    c.execute(query)
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == password

@app.route('/login/v1', methods=['GET', 'POST'])

@app.route('/login/v1', methods=['POST'])
def login_v1():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if verify_plain(username, password):
            return 'Inicio de sesión exitoso para {}'.format(username)
        else:
            return 'Nombre de usuario o contraseña incorrectos', 401
    else:
        return 'Método no válido', 405

    return error



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')


