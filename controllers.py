from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, Event, members, mypage
from login_manager import login_manager

def setup_routes(app):
    @login_manager.members_loader
    def load_members(members_id):
        return members.query.get(int(members_id))

    # 기존 라우터
    @app.route('/')
    def home():
        return render_template('Home.html')

    @app.route('/about')
    def about():
        return '이것은 이벤트 정보 소개 페이지입니다.'

    # 로그인/ 로그아웃 처리 라우트
    @app.route('/login', methods=['GET', 'POST'])
    def login():
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

    # 회원가입 기능 라우트
    @app.route('/signup', methods=['GET', 'POST'])
    def signup() :
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
            