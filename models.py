from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# database 모델 정의
class Event(db.Model) :   # 이벤트 목록
    no = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(50), nullable=False) 
    startDate = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    explain = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.String(1000))

    def __repr__(self):
        return f'<Event {self.title}>'

class mypage(UserMixin, db.Model):   # Mypage
    id = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    my_name = db.Column(db.String(50), nullable=False) 
    my_eventName = db.Column(db.String(50),nullable=False)
    my_startDate = db.Column(db.String(20), nullable=False)
    my_endDate = db.Column(db.String(20), nullable=False)
    my_location = db.Column(db.String(100), nullable=False)
    my_explain = db.Column(db.String(1000), nullable=False)
    my_image = db.Column(db.String(1000))

class members(UserMixin, db.Model):    # 회원 Master
    id = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(512))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
