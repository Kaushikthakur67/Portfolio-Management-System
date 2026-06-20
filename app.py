import os

from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Project

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

# Create folders automatically
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["PROFILE_FOLDER"], exist_ok=True)
os.makedirs(app.config["RESUME_FOLDER"], exist_ok=True)
os.makedirs(app.config["CERTIFICATE_FOLDER"], exist_ok=True)
os.makedirs(app.config["PROJECT_FOLDER"], exist_ok=True)


# ==========================
# Public Pages
# ==========================

@app.route("/")
def home():
    return render_template("public/index.html")


@app.route("/about")
def about():
    return render_template("public/about.html")


@app.route("/contact")
def contact():
    return render_template("public/contact.html")


# ==========================
# Client Registration
# ==========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        password = request.form["password"]

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for("register"))

        # Encrypt Password
        hashed_password = generate_password_hash(password)

        new_user = User(
            full_name=full_name,
            email=email,
            mobile=mobile,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful!", "success")

        return redirect(url_for("register"))

    return render_template("client/register.html")


# ==========================
# login
# ==========================

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        user=User.query.filter_by(email=email).first()

        if user:

            if check_password_hash(user.password,password):

                session["user_id"]=user.id
                session["name"]=user.full_name

                flash("Login Successful!")

                return redirect(url_for("client_dashboard"))

        flash("Invalid Email or Password")

    return render_template("client/login.html")

# ==========================
# Client Dashboard
# ==========================

@app.route("/client_dashboard")
def client_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    total_projects = Project.query.filter_by(
        user_id=session["user_id"]
    ).count()

    return render_template(
        "client/dashboard.html",
        name=session["name"],
        total_projects=total_projects
    )
    
# ==========================
# Create
# ==========================

@app.route("/profile",methods=["GET","POST"])
def profile():

    if "user_id" not in session:

        return redirect(url_for("login"))

    user=User.query.get(session["user_id"])

    if request.method=="POST":

        user.full_name=request.form["full_name"]

        user.mobile=request.form["mobile"]

        user.about=request.form["about"]

        user.address=request.form["address"]

        user.github=request.form["github"]

        user.linkedin=request.form["linkedin"]

        image=request.files["profile_image"]

        if image.filename!="":

            filename=secure_filename(image.filename)

            image.save(os.path.join(app.config["PROFILE_FOLDER"],filename))

            user.profile_image=filename

        db.session.commit()

        flash("Profile Updated Successfully")

        return redirect(url_for("profile"))

    return render_template("client/profile.html",user=user)

# ==========================
# Add Project
# ==========================

@app.route("/add_project", methods=["GET", "POST"])
def add_project():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        technology = request.form["technology"]
        github = request.form["github"]
        live_demo = request.form["live_demo"]

        image = request.files["image"]

        filename = ""

        if image and image.filename != "":
            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config["PROJECT_FOLDER"],
                    filename
                )
            )

        project = Project(
            title=title,
            description=description,
            technology=technology,
            github=github,
            live_demo=live_demo,
            image=filename,
            user_id=session["user_id"],
            status="Pending"
        )

        db.session.add(project)
        db.session.commit()

        flash("Project Added Successfully!", "success")

        return redirect(url_for("my_projects"))

    return render_template("client/add_project.html")

# ==========================
# My Projects
# ==========================

@app.route("/my_projects")
def my_projects():

    if "user_id" not in session:
        return redirect(url_for("login"))

    projects = Project.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "client/my_projects.html",
        projects=projects
    )

# ==========================
# Edit Project
# ==========================

@app.route("/edit_project/<int:id>", methods=["GET", "POST"])
def edit_project(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    project = Project.query.filter_by(
        id=id,
        user_id=session["user_id"]
    ).first_or_404()

    if request.method == "POST":

        project.title = request.form["title"]
        project.description = request.form["description"]
        project.technology = request.form["technology"]
        project.github = request.form["github"]
        project.live_demo = request.form["live_demo"]

        image = request.files["image"]

        if image and image.filename != "":

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config["PROJECT_FOLDER"],
                    filename
                )
            )

            project.image = filename

        db.session.commit()

        flash("Project Updated Successfully!", "success")

        return redirect(url_for("my_projects"))

    return render_template(
        "client/edit_project.html",
        project=project
    )
    
# ==========================
# Delete Project
# ==========================

@app.route("/delete_project/<int:id>")
def delete_project(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    project = Project.query.filter_by(
        id=id,
        user_id=session["user_id"]
    ).first_or_404()

    db.session.delete(project)

    db.session.commit()

    flash("Project Deleted Successfully!", "success")

    return redirect(url_for("my_projects"))


# ==========================
# logout 
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logout Successfully")

    return redirect(url_for("login"))


# ==========================
# Create Database
# ==========================

with app.app_context():
    db.create_all()


# ==========================
# Run Application
# ==========================

if __name__ == "__main__":
    app.run(debug=True)