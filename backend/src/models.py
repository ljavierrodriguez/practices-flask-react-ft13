import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    users = db.relationship('User', cascade="all, delete", secondary='roles_users')


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }    

    def serialize_with_users(self):
        return {
            "id": self.id,
            "name": self.name,
            "users": self.get_users() # [] de usuarios
        }

    def get_users(self):
        return list(map(lambda user: user.serialize(), self.users))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    posts = db.relationship('Post', cascade="all,delete", backref='category')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }  

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()   


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    roles = db.relationship('Role',  cascade="all, delete", secondary='roles_users')
    profile = db.relationship('Profile', cascade="all, delete", backref='user', uselist=False)
    posts = db.relationship('Post', cascade="all, delete")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "active": self.active,
            "profile": {
                "name": self.profile.name,
                "lastname": self.profile.lastname,
                "instagram": self.profile.instagram,
                "biography": self.profile.biography,
                "facebook": self.profile.facebook,
                "twitter": self.profile.twitter,
                "linkedin": self.profile.linkedin,
                "github": self.profile.github
            }
        }

    def serialize_with_roles(self):
        return {
            "id": self.id,
            "email": self.email,
            "active": self.active,
            "profile": {
                "name": self.profile.name,
                "lastname": self.profile.lastname,
                "instagram": self.profile.instagram,
                "biography": self.profile.biography,
                "facebook": self.profile.facebook,
                "twitter": self.profile.twitter,
                "linkedin": self.profile.linkedin,
                "github": self.profile.github
            },
            "roles": self.get_roles()
        }

    def get_roles(self):
        return list(map(lambda role: role.serialize(), self.roles))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    instagram = db.Column(db.String(120))
    biography = db.Column(db.Text)
    facebook = db.Column(db.String(120))
    twitter = db.Column(db.String(120))
    linkedin = db.Column(db.String(120))
    github = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "instagram": self.instagram,
            "biography": self.biography,
            "facebook": self.facebook,
            "twitter": self.twitter,
            "linkedin": self.linkedin,
            "github": self.github
        }  

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class RoleUser(db.Model):
    __tablename__ = 'roles_users'
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    slug = db.Column(db.String(250), nullable=False, unique=True)
    content = db.Column(db.Text)
    image = db.Column(db.String(120))
    status = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    comments = db.relationship('Comment', backref='post')

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "content": self.content,
            "image": self.image,
            "status": self.status,
            "user": self.user.serialize(),
            "category": self.category.serialize(),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }  


    def serialize_with_comment(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "content": self.content,
            "image": self.image,
            "status": self.status,
            "user": self.user.serialize(),
            "category": self.category.serialize(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "comments": list(map(lambda comment: comment.serialize(), self.comments))
        }  

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "created_at": self.created_at
        }  

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()