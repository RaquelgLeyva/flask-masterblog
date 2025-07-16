from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_posts():
    with open('posts.json') as f:
        return json.load(f)

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = load_posts()
        new_post = {
            "id": max([post["id"] for post in blog_posts] or [0]) + 1,
            "author": request.form.get("author"),
            "title": request.form.get("title"),
            "content": request.form.get("content")
        }
        blog_posts.append(new_post)

        # Save in posts.json
        with open('posts.json', 'w') as f:
            json.dump(blog_posts, f, indent=4)

        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    posts = load_posts()
    posts = [post for post in posts if post['id'] != post_id]

    # Save new list in posts.json
    with open('posts.json', 'w') as f:
        json.dump(posts, f, indent=4)

    return redirect(url_for('index'))

def save_posts(posts):
    with open('posts.json', 'w') as f:
        json.dump(posts, f, indent=4)

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_posts()
    # Buscar el post por id
    post = next((p for p in posts if p['id'] == post_id), None)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Actualizar con los datos del formulario
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')

        save_posts(posts)
        return redirect(url_for('index'))

    # Si es GET, mostrar el formulario con datos actuales
    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)

