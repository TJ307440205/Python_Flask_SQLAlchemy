from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# URI 配置: https://docs.sqlalchemy.org/en/latest/core/engines.html
# 数据库URI配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
# 干掉那个警告信息
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 显示SQLAlchemy的操作（用于调试）
app.config['SQLALCHEMY_ECHO'] = False
# 实例化数据库操作对象
db = SQLAlchemy(app)

class Category(db.Model):
    """分类类"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)

    def __init__(self, title):
        self.title = title
    
    def __repr__(self):
        return '<Category {0!r}>'.format(self.title)

class Post(db.Model):
    """文章类"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    category = db.relationship(
        Category,
        backref=db.backref('posts', lazy='dynamic')
    )

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category
        
    def __repr__(self):
        return '<Post {0!r}>'.format(self.title)

with app.test_request_context():
    db.create_all()

with app.test_request_context():
    py = Category('Python')
    p = Post('Hello Python!', 'Python is pretty cool', py)
    db.session.add(p)
    db.session.add(py)
    db.session.commit()

with app.test_request_context():
    py = Category.query.filter_by(title='Python').first()
    print(py.posts.all())
    print(Post.query.filter_by(category_id=py.id).all())

    p = Post.query.filter(Post.title.like('%Hello Python%')).first()
    print(p.category)
    print(Category.query.filter_by(id=p.category_id).first())