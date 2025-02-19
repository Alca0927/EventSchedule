from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, Event, members, mypage
from login_manager import login_manager
import secrets
from PIL import Image
import os

app = Flask(__name__)

def setup_routes(app):
    @login_manager.user_loader
    def load_members(members_id):
        return members.query.get(int(members_id))

    # 기존 라우터
    @app.route('/')
    def home():
        events = Event.query.all()
        return render_template('home.html',events=events)

    @app.route('/login')
    def login():
        return render_template('signin.html')
            
    # 로그인/ 로그아웃 처리 라우트
    @app.route('/loginTry', methods=['GET', 'POST'])
    def loginTry():
        if request.method == 'POST':
            user = members.query.filter_by(username=request.form['username']).first()
            if user and user.check_password(request.form['password']):
                login_user(user)
                return jsonify({'message': '로그인에 성공하였습니다. 이벤트 정보 상세 페이지로 이동합니다.'}), 200
            return jsonify({'error': '아이디가 없거나 패스워드가 다릅니다.'}), 400
        return redirect(url_for('home'))

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home')) # 로그아웃 후 메인 페이지로 리다이렉트

    @app.route('/signup')
    def signup():
        return render_template('signup.html')

    # 회원가입 기능 라우트
    @app.route('/signupTry', methods=['GET', 'POST'])
    def signupTry() :
        if request.method == 'POST' :
            userid = request.form['userid']
            password = request.form['password']
            username = request.form['username']
            email = request.form['email']
            
            # 회원가입 실패시 에러 메시지를 json형태로 반환(프런트앤드 페이지에서 해당 메시지를 기반으로 팝업을 띄움)
            existing_member = members.query.filter((members.username == username) | (members.email == email)).first()
            if existing_member :
                return jsonify({'error': '사용자 이름 또는 이메일이 이미 사용 중입니다.'}), 400
            members = members(userid= userid, username=username, email=email)
            members.set_password(password)
            db.session.add(members)
            db.session.commit()

            return jsonify({'message': '회원가입이 성공하였습니다. 기입한 아이디와 패스워드로 로그인할 수 있습니다.'}), 201
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
    @app.route('/detail', methods=['GET','POST'])
    def get_event():
        events = Event.query.all()
        return render_template('detail.html', events=events)

    @app.route('/upload')
    def uploadPage():
        return render_template('upload.html')

    # 업로드 하는 기능 구현
    @app.route('/upload/new', methods=['POST'])
    def uploadNew():

        data = request.form
        files = request.files

        eventName = data.get('eventName')
        startDate = data.get('startDate')
        endDate = data.get('endDate')
        location = data.get('location')
        explain = data.get('explain')
        if files:
            picFileName = savePic(files['image'], eventName)
    
        post = Event(eventName=eventName, startDate=startDate, endDate=endDate, location=location, explain=explain, image=picFileName)
        db.session.add(post)
        db.session.commit()
        return render_template('home.html')

# 첨부 이미지 파일 저장 함수
def savePic(pic, eventName):
    randHex = secrets.token_hex(8)
    _, fExt = os.path.splitext(pic.filename)
    picFileName = randHex + fExt
    picDir = os.path.join(app.static_folder, 'pics', eventName)
    picPath = os.path.join(picDir, picFileName)
    os.makedirs(picDir, exist_ok=True)

    with Image.open(pic) as image:
        image.save(picPath)

    return picFileName
