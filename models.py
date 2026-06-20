from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ==========================
# User Table
# ==========================

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    mobile = db.Column(db.String(15), nullable=False)

    password = db.Column(db.String(255), nullable=False)
    
    profile_image = db.Column(db.String(255), default="default.png")

    about = db.Column(db.Text)

    address = db.Column(db.Text)

    github = db.Column(db.String(255))

    linkedin = db.Column(db.String(255))

    role = db.Column(db.String(20), default="client")

    status = db.Column(db.String(20), default="Active")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    projects = db.relationship(
    "Project",
    backref="user",
    lazy=True,
    cascade="all, delete-orphan"
)



# ==========================
# Project Table
# ==========================

class Project(db.Model):

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text, nullable=False)

    technology = db.Column(db.String(200))

    github = db.Column(db.String(300))

    live_demo = db.Column(db.String(300))

    image = db.Column(db.String(300))

    status = db.Column(db.String(20), default="Pending")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)