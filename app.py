# 모든 라우터 등의 정보가 들어갑니다.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from login_manager import login_manager
from controllers import setup_routes

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/EventSchedule'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

# 데이터베이스 및 로그인 관리자 초기화
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# 라우트 설정
setup_routes(app)

with app.app_context():
    db.create_all()

    
if __name__ == '__main__':
    app.run(debug=True)

