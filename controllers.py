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
            
            if password == user.password_hash:
                login_user(user)
                session['user_id'] = user.id
                return redirect(url_for('home'))
            return jsonify({'error': '아이디가 없거나 패스워드가 다릅니다.'}), 400
        return redirect(url_for('home'))

    # 로그아웃 기능
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        session.pop['user_id', None]
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

    # 개인 상세페이지 조회 (로그인 성공하면 기존 자신의 즐겨찾기 저장 된 페이지(favorite))
    @app.route('/mypage', methods=['GET'])
    @login_required
    def list_mypage() :
        mypages = mypage.query.filter_by(user_id=current_user.id).all() # 현재 로그인한 사용자의 즐겨찾기 저장된 것만 조회
        return render_template('mypage.html', mypages=mypages, username=current_user.username) # 사용자별 즐겨찾기 저장된 정보 표시 렌더링 

    # 즐겨찾기 정보 생성
    @app.route('/mypage/create', methods=['POST'])
    @login_required
    def create_mypage():
        event = Event.query.filter_by(no=event.no).first() # 이벤트 Table 검색, event 선택 
        if event:
            Event.eventName = request.json['eventName']
            Event.startDate = request.json['startDate']
            Event.endDate = request.json['endDate']
            Event.location = request.json['location']
            Event.explain = request.json['explain']
            Event.image = request.json['image']
        
            new_mypage = mypage(user_id=current_user.id, mypageName=members.Name) # 현재 로그인한 사용자의 ID추가
            db.session.add(new_mypage)
            db.session.commit()
            return jsonify({'message': 'Mypage created'}), 201

    # mypage 삭제
    @app.route('/mypage/delete/<int:id>', methods=['DELETE'])
    @login_required
    def delete_mypage(id):
        mypage = mypage.query.filter_by(mypage_id=current_user.id, eventName=mypage.eventName).first() # 현재 로그인한 사용자의 메모만 선택 
        if mypage:
            db.session.delete(mypage)
            db.session.commit()
            return jsonify({'message': 'Mypage one record deleted'}), 200
        else:
            abort(404, decription="Memo not found or not authorized")
    
    # 상세 페이지 정보 가져오기
    @app.route('/detail/<int:no>', methods=['GET','POST'])
    def get_event(no):
        event = Event.query.filter_by(no=no).first()
        return render_template('detail.html', event=event)

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
    

    # 이벤트 업데이트 기능
    @app.route('/detail/<int:no>/update',methods=['PUT','POST'])
    @login_required
    def update_event(no):
        event = Event.query.filter_by(no=no).first()
        if event:
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
            return redirect(url_for('detail'))
        return render_template('home.html')
    
    # 이벤트 삭제 기능
    @app.route('/delete/<int:no>',methods=['DELETE'])
    @login_required
    def delete_event(no):
        event = Event.query.filter_by(no=no).first()
        if event:
            db.session.delete(event)
            db.session.commit()
            return redirect(url_for('detail'))
        return redirect(url_for('detail'))