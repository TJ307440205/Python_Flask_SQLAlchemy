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

# 定义模型（注意：模型类需要继承自db.Model）
class User(db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        # return '<User {0!r}>'.format(self.username)
        # return '<User {0!s}>'.format(self.username)
        return '<User {0}>'.format(self.username)

with app.test_request_context():
    db.create_all()

with app.test_request_context():
    admin = User('admin', 'admin@qq.com')
    guest = User('guest', 'guest@cqzuxia.com')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()

with app.test_request_context():
    print(User.query.all())
    print(User.query.first())
    admin = User.query.filter_by(username='admin').first()
    print(admin)
    user_obj = User.query.filter(User.id > 3).first()
    if isinstance(user_obj, User):
        print(user_obj.name)
    else:
        print('查无此人')