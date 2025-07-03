from database import get_db_connection

def get_all_posts():
    """Obtiene todos los posts"""
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY created DESC').fetchall()
    conn.close()
    return posts

def get_post_by_id(post_id):
    """Obtiene un solo post por su ID"""
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return post

def create_post(title, content):
    """Crea un nuevo post"""
    conn = get_db_connection()
    conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
    conn.commit()
    conn.close()

def edit_post(post_id, title, content):
    """Edita un post"""
    conn = get_db_connection()
    conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, post_id))
    conn.commit()
    conn.close()

def delete_post(post_id):
    """Elimina un post"""
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()