from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import uuid
import os
from uuid import UUID
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)

POSTS_FILE = "data/posts.json"

class PostEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Post):
            return obj.__dict__  # Convert Post object to a dictionary
        return super().default(obj)

# ...

def save_post_to_file(post):
    posts = read_posts_from_file()
    posts.append(post)

    with open('data/posts.json', 'w') as file:
        json.dump(posts, file, cls=PostEncoder)

def read_posts_from_file():
    try:
        with open('data/posts.json', 'r') as file:
            content = file.read()
            if content:
                posts = json.loads(content)
            else:
                posts = []
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []

    return posts


class Post:
    def __init__(self, id, title, content, timestamp, author):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp
        self.author = author
        self.comments = []

    def add_comment(self, comment):
        self.comments.append(comment)

    # def get_comment_count(self):
    #     return len(self.comments)
        
class Comment:
    def __init__(self, content, author, timestamp):
        self.content = content
        self.author = author
        self.timestamp = timestamp



def write_posts_to_file(posts):
    with open(POSTS_FILE, "w") as file:
        json.dump(posts, file, indent=2)

@app.route('/')
def home():
    posts = read_posts_from_file()

    # Sort posts by the latest timestamp
    posts.sort(key=lambda post: datetime.strptime(post['timestamp'], '%d %b %Y - %H:%M:%S'), reverse=True)

    # Calculate comment count for each post
    for post in posts:
        if 'comments' in post:
            post['comment_count'] = len(post['comments'])
        else:
            post['comment_count'] = 0

    return render_template('home.hbs', posts=posts or [])



@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        timestamp = datetime.now().strftime('%d %b %Y - %H:%M:%S')

        post = Post(id=str(uuid.uuid4()), title=title, content=content, timestamp=timestamp, author=author)
        post.likes = 0
        save_post_to_file(post)
        return redirect(url_for('home'))
    return render_template('create_post.hbs')


@app.route('/post/<string:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    posts = read_posts_from_file()
    post = None
    for post in posts:
        if 'comments' in post:
            post['comment_count'] = len(post['comments'])
        else:
            post['comment_count'] = 0
            
    for p in posts:
        if p['id'] == post_id:
            post = p
            break
    # if post is None:
    #     return render_template('post_not_found.hbs')

    

    if request.method == 'POST':
        if 'comment' in request.form:
            comment_text = request.form['comment']
            author_name = request.form.get('author', 'Anonymous')
            timestamp = datetime.now().strftime('%d %b %Y - %H:%M:%S')
            comment = {
                'author': author_name,
                'text': comment_text,
                'timestamp': timestamp
            }
            if 'comments' in post:
                post['comments'].append(comment)
            else:
                post['comments'] = [comment]

        elif 'like' in request.form:
            post['likes'] = post.get('likes', 0) + 1
        else:
            pass

        write_posts_to_file(posts)
        return redirect(url_for('view_post', post_id=post_id))
    else:
        return render_template('view_post.hbs', post=post)
    

if __name__ == "__main__":
    # Use WSGIRequestHandler to run the app using WSGI instead of Flask's development server
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)), debug=True)
    # app.run()
