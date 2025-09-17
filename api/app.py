from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Caminho do banco
DB_PATH = os.path.join(os.path.dirname(__file__), 'banco.db')

# Criação automática da tabela
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pessoas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        ''')
        conn.commit()
init_db()
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        nome = request.form.get("nome")
        if nome:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO pessoas (nome) VALUES (?)", (nome,))
                conn.commit()
        return redirect("/")

    return render_template("index.html")

@app.route("/lista")
def lista():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pessoas")
        pessoas = cursor.fetchall()
    return render_template("lista.html", pessoas=pessoas)

if __name__ == "__main__":
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



