from flask import Flask, render_template
import sqlite3

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/', methods=['GET'])
def base():
    return render_template('base.html')

@app.route('/home', methods=['GET'])
def home():
    titulo = "esta es el html home como variable"
    return render_template('home.html', titulo=titulo)

@app.route('/posts', methods=['GET'])
def get_all_posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('post/post_list.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)