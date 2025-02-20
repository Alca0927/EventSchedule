from flask import Flask, render_template, request, jsonify, abort, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, Event, members, mypage
from login_manager import login_manager
import secrets
from PIL import Image
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/pic')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secret_key'

def setup_routes(app):
    @login_manager.user_loader
    def load_members(members_id):
        return members.query.get(members_id)

    # 라우터
    # 홈페이지
    @app.route('/')
    def home():
        events = Event.query.all()
        return render_template('home.html',events=events)

    # 로그인 페이지
    @app.route('/login')
    def login():
        return render_template('signin.html')

    # 로그인/ 로그아웃 처리 라우트
    @app.route('/loginTry', methods=['GET', 'POST'])
    def loginTry():
        if request.method == 'POST':
            id = request.form['id']
            password = request.form['password']

            user = members.query.filter_by(id=id).first()
            
            if id != user.id:
                return render_template("signin.html", message="아이디를 확인하세요.")
            else:
                if password == user.password_hash:
                    login_user(user)
                    session['user_id'] = user.id
                    return redirect(url_for('home'))
                else:
                    return render_template("signin.html", message="패스워드가 다릅니다.")
        return redirect(url_for('home'))

    # 로그아웃 기능
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        session.pop('user_id', None)
        return redirect(url_for('home')) # 로그아웃 후 메인 페이지로 리다이렉트

    # 회원가입 페이지
    @app.route('/signup')
    def signup():
        return render_template('signup.html')

    # 회원가입 기능 라우트
    @app.route('/signupTry', methods=['GET', 'POST'])
    def signupTry() :
        if request.method == 'POST' :
            id = request.form['signupUserid']
            password = request.form['signupPassword']
            username = request.form['signupUsername']
            email = request.form['signupUseremail']
            
            # 회원가입 실패시 에러 메시지를 json형태로 반환(프런트앤드 페이지에서 해당 메시지를 기반으로 팝업을 띄움)
            existing_member = members.query.filter((members.username == username) | (members.email == email)).first()
            if existing_member :
                return jsonify({'error': '사용자 이름 또는 이메일이 이미 사용 중입니다.'}), 400
            member = members(id= id, password_hash=password, username=username, email=email)
            # members.set_password(password_hash)
            db.session.add(member)
            db.session.commit()

            return render_template('home.html')
        return redirect(url_for('home')) # 비정상 요청의 경우 리다이렉트

    @app.route('/mypage', methods=['GET'])
    @login_required
    def list_mypage():
        # 현재 로그인한 사용자의 id가 mypage 테이블의 id와 일치한다고 가정
        mypages = mypage.query.filter_by(id=current_user.id).all()
        events = []
        for mp in mypages:
            # 날짜 형식이 "YYYYMMDD"라면 "YYYY-MM-DD"로 변환, 이미 형식이 맞다면 그대로 사용
            if len(mp.my_startDate) == 8:
                start = f"{mp.my_startDate[:4]}-{mp.my_startDate[4:6]}-{mp.my_startDate[6:]}"
            else:
                start = mp.my_startDate
            if len(mp.my_endDate) == 8:
                end = f"{mp.my_endDate[:4]}-{mp.my_endDate[4:6]}-{mp.my_endDate[6:]}"
            else:
                end = mp.my_endDate

            events.append({
                "startDate": start,
                "endDate": end,
                "eventName": mp.my_eventName,   # 새로 추가된 이벤트 이름 사용
                "location": mp.my_location,
                "explain": mp.my_explain,
                "image": mp.my_image
            })
        return render_template('mypage.html', events=events, username=current_user.username)


    # 즐겨찾기 정보 생성
    @app.route('/mypage/create/<int:no>', methods=['POST'])
    @login_required
    def create_mypage(no):

        if request.method=='POST': 
            likes = request.form['likes']

        if likes == '즐겨찾기':

            user = members.query.filter_by(id=current_user.id).first()
            event = Event.query.filter_by(no=no).first()

            id = user.id
            name = user.username
            eventName = event.eventName
            startDate = event.startDate
            endDate = event.endDate
            explain = event.explain
            location = event.location
            image = event.image

            new_mypage= mypage(
                id=id,
                my_name=name,
                my_eventName=eventName,
                my_startDate=startDate,
                my_endDate=endDate,
                my_location=location,
                my_explain=explain,
                my_image=image
                )
            
            db.session.add(new_mypage)
            db.session.commit()
            return redirect(url_for('home'))

    # 즐겨찾기 삭제
    @app.route('/mypage/delete/<eventName>', methods=['POST'])
    @login_required
    def delete_mypage(eventName):
        my_page = mypage.query.filter_by(my_eventName=eventName, id=current_user.id).first() # 현재 로그인한 사용자의 메모만 선택 
        if my_page:
            db.session.delete(my_page)
            db.session.commit()
            return redirect(url_for('list_mypage'))
        else:
            abort(404, description="Memo not found or not authorized")
    
    # 상세 페이지 정보 가져오기
    @app.route('/detail/<int:no>', methods=['GET','POST'])
    def get_event(no):
        event = Event.query.filter_by(no=no).first()
        return render_template('detail.html', event=event, no=no)

    # 이벤트 업로드 페이지
    @app.route('/upload')
    def uploadPage():
        return render_template('upload.html')

    # 이벤트 업로드 하는 기능 구현
    @app.route('/upload/new', methods=['GET','POST'])
    def uploadNew():
        if request.method == 'POST':
            eventName = request.form['eventName']
            startDate = request.form['startDate']
            endDate = request.form['endDate']
            location = request.form['location']
            explain = request.form['explain']
            image = request.files['image']

            # date를 YYYY-MM-DD 문자열을 python날짜로 변환
            startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
            endDate = datetime.strptime(endDate, '%Y-%m-%d').date()
            
            # 이미지 저장 & 경로 저장
            if image:
                file_path = os.path.join(UPLOAD_FOLDER, image.filename)
                image.save(file_path)
            post = Event(eventName=eventName, startDate=startDate, endDate=endDate, location=location, explain=explain, image=image.filename)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('upload.html')
    
    # 이벤트 업로드 페이지
    @app.route('/detail/<int:no>/update',methods=['POST'])
    def updatePage(no):
        event = Event.query.filter_by(no=no).first()
        return render_template('event_UD.html', event=event, no=no)
    
    # 이벤트 업데이트 기능
    @app.route('/detail/<int:no>/updating',methods=['PUT','POST'])
    @login_required
    def update_event(no):
        event = Event.query.filter_by(no=no).first()
        if event:
            event.eventName = request.form['eventName']
            startDate = request.form['startDate']
            endDate = request.form['endDate']
            event.location = request.form['location']
            event.explain = request.form['explain']
            image = request.files['image']
            # date를 YYYY-MM-DD 문자열을 python날짜로 변환
            event.startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
            event.endDate = datetime.strptime(endDate, '%Y-%m-%d').date()
            
            # 이미지 저장 & 경로 저장
            if image:
                file_path = os.path.join(UPLOAD_FOLDER, image.filename)
                image.save(file_path)
            event.image = image.filename
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('home.html')
    
    # 이벤트 삭제 기능
    @app.route('/detail/<int:no>/delete',methods=['POST'])
    @login_required
    def delete_event(no):
        event = Event.query.filter_by(no=no).first()
        if event:
            db.session.delete(event)
            db.session.commit()
            return redirect(url_for('home'))
        return redirect(url_for('home'))
    
    #회원가입 아이디 증복 확인 기능
    @app.route('/checkDup', methods=['POST'])
    def check_dup():
        data = request.get_json()
        user_id = data.get('userId')
        if not user_id:
            return jsonify({'exists': False})
        # members 테이블에서 id가 존재하는지 확인
        exists = members.query.filter_by(id=user_id).first() is not None
        return jsonify({'exists': exists})
   

