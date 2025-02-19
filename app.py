# 모든 라우터 등의 정보가 들어갑니다.
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user
import pymysql

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/EventSchedule'
db = SQLAlchemy(app)

# 데이터 모델 정의 (행사 정보)
class Event(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(30), nullable=False)
    startDate = db.Column(db.String(30), nullable=False)
    endDate = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(30), nullable=False)
    explain = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(30))

    def __repr__(self):
        return f'<Event {self.eventName}>'

with app.app_context():
    db.create_all()

# 라우트
@app.route('/')
def home():
    events = Event.query.filter(Event.eventName).all()
    return render_template('home.html',events=events)

@app.route('/upload')
def uploadPage():
    return render_template('upload.html')

# 업로드 하는 기능 구현
@app.route('/upload/new', methods=['POST'])
def uploadNew():
    if request.method == "POST":
        eventName = request.form['eventName']
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        location = request.form['location']
        explain = request.form['explain']
        image = request.form['image']

        post = Event(eventName=eventName, startDate=startDate, endDate=endDate, location=location, explain=explain, image=image)
        db.session.add(post)
        db.session.commit()
        return render_template('home.html')
    return render_template('upload.html')
  
# 상세 페이지 정보 가져오기
@app.route('/detail', methods=['GET'])
def get_detail():
    events = Event.query.all()
    return jsonify([
        {
            "id": event.no,
            "eventName": event.eventName,
            "startDate": event.startDate,
            "endDate": event.endDate,
            "location": event.location,
            "explain": event.explain,
            "image": event.image
        }
        for event in events
    ])

@app.route('/logout')
def logout():
    logout_user()
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

