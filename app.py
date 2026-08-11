import json

from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


def load_posts():
    with open("blog_posts.json", "r") as file:
        return json.load(file)


@app.route("/")
def index():
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        content = request.form["content"]
        blog_post = {
            "id": get_next_id(),
            "author": author,
            "title": title,
            "content": content,
        }
        add_post(blog_post)
        return redirect(url_for("index"))
    return render_template("add.html")


def get_next_id():
    last_id = load_posts()[-1]["id"]
    return last_id + 1


def add_post(blog_post):
    blog_posts = load_posts()
    blog_posts.append(blog_post)
    with open("blog_posts.json", "w") as posts:
        json.dump(blog_posts, posts)


@app.route("/delete/<int:post_id>")
def delete(post_id):
    delete_post(post_id)
    return redirect(url_for("index"))


def delete_post(post_id):
    blog_posts = load_posts()  # Hier: alle Posts laden (load_posts())
    blog_posts = [
        post for post in blog_posts if post["id"] != post_id
    ]  # Hier: neue Liste ohne den Post mit passender id bauen
    with open(
            "blog_posts.json", "w"
    ) as file:  # Hier: Datei im Schreibmodus öffnen und mit json.dump() zurückschreiben
        json.dump(blog_posts, file)


def fetch_post_by_id(post_id):
    blog_posts = load_posts()
    for post in blog_posts:
        if post["id"] == post_id:
            return post
    return None


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        post["author"] = request.form["author"]
        post["title"] = request.form["title"]
        post["content"] = request.form["content"]

        blog_posts = load_posts()
        for index, p in enumerate(blog_posts):
            if p["id"] == post_id:
                blog_posts[index] = post

        with open("blog_posts.json", "w") as file:
            json.dump(blog_posts, file)

        return redirect(url_for("index"))

    return render_template("update.html", post=post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
