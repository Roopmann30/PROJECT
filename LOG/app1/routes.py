from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from bson.objectid import ObjectId
from .models import User
from . import mongo, login_manager

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(user_data) if user_data else None

def save_user_to_db(user_data):
    mongo.db.users.insert_one(user_data)

def find_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

def find_post_by_id(post_id):
    return mongo.db.posts.find_one({"_id": ObjectId(post_id)})

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if find_user_by_email(email):
            flash("Email already registered!")
        else:
            save_user_to_db(User.create_user(username, email, password))
            flash("Registration successful! Please log in.")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_data = find_user_by_email(email)
        if user_data:
            user = User(user_data)
            if user.check_password(password):
                login_user(user)
                return redirect(url_for("dashboard"))
        flash("Invalid email or password.")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    posts = list(mongo.db.posts.find())
    return render_template("dashboard.html", posts=posts)

@app.route("/like/<post_id>", methods=["POST"])
@login_required
def like(post_id):
    post = find_post_by_id(post_id)
    if current_user.id not in post.get("liked_by", []):
        mongo.db.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$inc": {"likes": 1}, "$push": {"liked_by": current_user.id}},
        )
    return redirect(url_for("dashboard"))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        mongo.db.users.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$set": {"username": username, "email": email}},
        )
        flash("Profile updated successfully.")
    return render_template("profile.html", user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
