from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from secrets import token_hex
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


# User model
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    google_id = db.Column(db.String(200), unique=True)
    apitoken = db.Column(db.String)
    
    # Relationships
    # goals = db.relationship('Goal', backref='user', lazy=True)
    # transactions = db.relationship('Transaction', backref='user', lazy=True)
    # challenges = db.relationship('Challenge', secondary='user_challenge_membership', backref='users', lazy=True)
    # groups = db.relationship('Group', secondary='user_group_membership', backref='users', lazy=True)
    # feed = db.relationship('User_Feed', backref='user', lazy=True)
    # post = db.relationship("Post", backref='author', lazy=True)
    # likes = db.relationship("Likes", lazy=True, cascade="all, delete")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username' : self.username,
            'email' : self.email,
            'apitoken' : self.apitoken
        }


# Income_Deduction model
class IncomeDeduction(db.Model):
    __tablename__ = 'income_deduction'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    trans_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __init__(self, title, amount, category, trans_date, user_id):
        self.title = title
        self.amount = amount
        self.category = category
        self.trans_date = trans_date
        self.user_id = user_id

    def is_income(self):
        return self.category == 'income'

    def is_deduction(self):
        return self.category == 'deduction'

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'amount': self.amount,
            'income_type': 'income' if self.is_income() else 'deduction',
            'trans_date': self.trans_date.isoformat() if self.trans_date else None,
            'user_id': self.user_id
        }




# Goal model
# class Goal(db.Model):
#     __tablename__ = 'goal'
#     goal_id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(20), nullable=False)
#     amount = db.Column(db.Float, nullable=False)
#     target_date = db.Column(db.Date, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
#     # Relationships
#     transactions = db.relationship('Transaction', backref='goal', lazy=True)

#     def __init__(self, title, amount, target_date, user_id):
#         self.title = title
#         self.amount = amount
#         self.target_date = target_date
#         self.user_id = user_id


#     def saveToDB(self):
#         db.session.add(self)
#         db.session.commit()

#     def to_dict(self):
#         return {
#             'goal_id': self.goal_id,
#             'title': self.title,
#             'amount' : self.amount,
#             'target_date' : self.target_date,
#             'user_id' : self.user_id
#         }


# Transaction model
# class Transaction(db.Model):
#     __tablename__ = 'transaction'
#     trans_id = db.Column(db.Integer, primary_key=True)
#     amount = db.Column(db.Float, nullable=False)
#     category = db.Column(db.String(20), nullable=False)
#     trans_date = db.Column(db.Date, nullable=False)
#     frequency = db.Column(db.String(20), nullable=False)
#     goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

#     def __repr__(self):
#         return f"Transaction('{self.amount}', '{self.category}', '{self.trans_date}')"


# Challenge model
# class Challenge(db.Model):
#     __tablename__ = 'challenge'
#     challenge_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     description = db.Column(db.String(200), nullable=False)
#     start_date = db.Column(db.Date, nullable=False)
#     end_date = db.Column(db.Date, nullable=False)

#     def __repr__(self):
#         return f"Challenge('{self.name}', '{self.description}', '{self.start_date}', '{self.end_date}')"


# Group model
# class Group(db.Model):
#     tablename = 'group'
#     group_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     description = db.Column(db.String(200), nullable=False)

#     def __repr__(self):
#         return f"Group('{self.name}', '{self.description}')"


# User_Challenge_Membership model
# class User_Challenge_Membership(db.Model):
#     __tablename__ = 'user_challenge_membership'
#     challenge_membership_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
#     challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.challenge_id'), nullable=False)
#     start_date = db.Column(db.Date, nullable=False)
#     end_date = db.Column(db.Date, nullable=True)

#     def __repr__(self):
#         return f"User_Challenge_Membership('{self.start_date}', '{self.end_date}')"


# User_Group_Membership model
# class User_Group_Membership(db.Model):
#     tablename = 'user_group_membership'
#     group_membership_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
#     group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'), nullable=False)
#     start_date = db.Column(db.Date, nullable=False)
#     end_date = db.Column(db.Date, nullable=True)

#     def __repr__(self):
#         return f"User_Group_Membership('{self.start_date}', '{self.end_date}')"





# Post model
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     caption = db.Column(db.String(1000))
#     date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     likes = db.relationship("Likes", lazy=True, cascade="all, delete")

#     def __init__(self, title, caption, user_id):
#         self.title = title
#         self.caption = caption
#         self.user_id = user_id
#     def saveToDB(self):
#         db.session.add(self)
#         db.session.commit()
#     def saveChanges(self):
#         db.session.commit()
#     def deleteFromDB(self):
#         db.session.delete(self)
#         db.session.commit()
#     def getLikeCounter(self):
#         return len(self.likes)


#     def to_dict(self):
#         return {
#             'id': self.id,
#             'title': self.title,
#             'caption': self.caption,
#             'date_created': self.date_created,
#             'user_id': self.user_id,
#             'author': self.author.username,
#             'like_counter': len(self.likes)
#         }


# Likes model
# class Likes(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

#     def __init__(self, user_id, post_id):
#         self.user_id = user_id
#         self.post_id = post_id
#     def saveToDB(self):
#         db.session.add(self)
#         db.session.commit()
#     def deleteFromDB(self):
#         db.session.delete(self)
#         db.session.commit()
        
        
# User_Feed model
# class User_Feed(db.Model):
#     tablename = 'user_feed'
#     feed_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)

#     def __repr__(self):
#         return f"User_Feed('{self.user_id}', '{self.post_id}')"