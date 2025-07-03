from flask import Flask, render_template, abort, request, redirect, url_for, flash, jsonify

import post

app = Flask(__name__)

app.config['SECRET_KEY'] = 'clave_secreta'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/posts')
def get_all_posts():
    all_posts = post.get_all_posts()

    if request.args.get('format') == 'json':
        posts_as_dicts = [dict(p) for p in all_posts]
        return jsonify(posts_as_dicts)
    
    return render_template('post/post_list.html', posts=all_posts)

@app.route('/posts/<int:post_id>')
def get_one_post(post_id):
    one_post = post.get_post_by_id(post_id)
    if one_post is None:
        abort(404)

    if request.args.get('format') == 'json':
        return jsonify(dict(one_post))

    return render_template("post/post.html", post=one_post)

@app.route('/posts/create', methods=['GET', 'POST'])
def create_one_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

# Validación
        if not title or not content:
            flash("El título y el contenido son obligatorios :)")
            return render_template("post/create.html")

        post.create_post(title, content)
        flash("El Post ha sido creado correctamente :)")
        return redirect(url_for('get_all_posts'))

    return render_template("post/create.html")
    
@app.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_one_post(post_id):
    one_post = post.get_post_by_id(post_id)
    if one_post is None:
        abort(404)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

# Validación
        if not title or not content:
            flash("El título y el contenido son obligatorios :)")
            return render_template("post/edit.html", post=one_post)
        
        post.edit_post(post_id, title, content)
        flash("El Post ha sido actualizado correctamente :)")
        return redirect(url_for('get_all_posts'))
    
    return render_template("post/edit.html", post=one_post)

@app.route('/posts/delete/<int:post_id>', methods=['DELETE'])
def delete_one_post(post_id):
    post.delete_post(post_id)
    flash("El Post ha sido eliminado :)")
    return redirect(url_for('get_all_posts'))

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/api/new')
def new():
    datos = [{"nombre": "Jorge", "edad": 35, "trabaja": True}, {"nombre": "Jaime", "edad": 34, "trabaja": False}]
    return datos, 200

if __name__ == '__main__':
    app.run(debug=True)