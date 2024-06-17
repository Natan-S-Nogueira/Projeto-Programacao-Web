from flask import Flask, render_template, request, redirect, url_for, session # type: ignore
from flask_bcrypt import Bcrypt # type: ignore
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Defina uma chave secreta forte para usar em produção
bcrypt = Bcrypt()

# Configuração do banco de dados
DATABASE = 'biblioteca.db'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash da senha
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insere no banco de dados
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (username, email, password_hash) VALUES (?, ?, ?)', (username, email, hashed_password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[3], password):
            session['user_id'] = user[0]
            return redirect(url_for('index'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
