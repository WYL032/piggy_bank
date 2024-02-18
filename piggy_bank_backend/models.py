from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint
from datetime import datetime
from enum import Enum
from sqlalchemy.orm import relationship


class TransactionType(Enum):
    INCOME = 0
    EXPENSE = 1


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    hash = db.Column(db.String(100), nullable=False)



class CategorySection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sectionName = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    # createId = db.Column(db.Integer, nullable=False)
    createTime = db.Column(db.DateTime, nullable=False, default=func.now())
    # modifyId = db.Column(db.Integer)
    modifyTime = db.Column(db.DateTime)

    def validate_type(self, key, type):
        type = int(type)
        if any(type == item.value for item in TransactionType):
            raise ValueError("invalid type")
        return type

    def validate_sectionName(self, key, sectionName):
        if not isinstance(sectionName, str) or len(sectionName) > 100:
            raise ValueError("invalid sectionName")
        return sectionName

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sectionId = db.Column(db.Integer, db.ForeignKey(CategorySection.id), nullable=False)
    categoryName = db.Column(db.String(100), nullable=False)
    # createId = db.Column(db.Integer, nullable=False)
    createTime = db.Column(db.DateTime, nullable=False, default=func.now())
    # modifyId = db.Column(db.Integer)
    modifyTime = db.Column(db.DateTime)

    categorySection = db.relationship('CategorySection')

    @validates('sectionId')
    def validate_sectionId(self, key, sectionId):
        if not CategorySection.query.get(sectionId):
            raise ValueError(f"CategorySection with id {sectionId} does not exist.")
        return sectionId

    @validates("categoryName")
    def validate_categoryName(self, key, categoryName):
        if not isinstance(categoryName, str) or len(categoryName) > 100:
            raise ValueError("invalid categoryName")
        return categoryName

class TransLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transDate = db.Column(db.DateTime, nullable=False)
    categoryId = db.Column(db.Integer, db.ForeignKey(Category.id), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    memo = db.Column(db.String(100), nullable=False)
    # createId = db.Column(db.Integer, nullable=False)
    createTime = db.Column(db.DateTime, nullable=False, default=func.now())
    # modifyId = db.Column(db.Integer)
    modifyTime = db.Column(db.DateTime, onupdate=func.now())

    category = db.relationship('Category', backref=db.backref('trans_logs', lazy=True))

    @validates('categoryId')
    def validate_category_id(self, key, id):
        if not Category.query.get(id):
            raise ValueError(f"Category with id {id} does not exist.")
        return id

    @validates("amount")
    def validate_amount(self, key, amount):
        amount = int(amount)
        if amount <= 0:
            raise ValueError("invalid amount")
        return amount

    @validates("transDate")
    def validate_transDate(self, key, date):
        return datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')

    @validates("memo")
    def validate_memo(self, key, memo):
        if not isinstance(memo, str) or len(memo) > 100:
            raise ValueError("invalid memo")
        return memo