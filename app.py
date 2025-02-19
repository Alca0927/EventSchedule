# 모든 라우터 등의 정보가 들어갑니다.
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

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
    image = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<Event {self.eventName}>'

with app.app_context():
    db.create_all()

# 라우트
@app.route('/')
def home():
    return render_template('home.html')

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
        pic = request.form['pic']

        post = Event(eventName=eventName, startDate=startDate, endDate=endDate, location=location, explain=explain, pic=pic)
        db.session.add(post)
        db.session.commit()
        return jsonify({'message':'게시물을 업로드되었습니다.'})
    return redirect(url_for('home'))