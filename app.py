# 모든 라우터 등의 정보가 들어갑니다.
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user
from io import BytesIO
import base64
import pymysql


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/EventSchedule'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# 데이터 모델 정의 (행사 정보)
class Event(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(30), nullable=False)
    startDate = db.Column(db.String(30), nullable=False)
    endDate = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(30), nullable=False)
    explain = db.Column(db.String(500), nullable=False)
    image = db.Column(db.LargeBinary)

    def __repr__(self):
        return f'<Event {self.eventName}>'

with app.app_context():
    db.create_all()

# 라우트
@app.route('/')
def home():
    events = Event.query.all()
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
        file = request.files["image"]

        if file:
            image_data = file.read()
        else:
            image_data = None

        post = Event(eventName=eventName, startDate=startDate, endDate=endDate, location=location, explain=explain, image=image_data)
        db.session.add(post)
        db.session.commit()
        return render_template('home.html')
    return render_template('upload.html')

@app.route('/image/<int:event_id>')
def get_image(event_id):
    event = Event.query.get(event_id)
    if event and event.image:
        return send_file(BytesIO(event.image), mimetype='image/png')  # 이미지 반환
    return "이미지 없음", 404
  
# 상세 페이지 정보 가져오기
@app.route('/detail', methods=['GET','POST'])
def get_event():
    events = Event.query.all()
    return render_template('detail.html', events=events)

@app.route('/logout')
def logout():
    logout_user()
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/mypage')
def myPage():
    return render_template('mypage.html')

if __name__ == '__main__':
    app.run(debug=True)

