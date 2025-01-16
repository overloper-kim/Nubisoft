from connect_db import ConnectMysql
from flask import Flask, make_response, render_template, request, redirect
from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)

template = env.get_template("index.html")

# 개인 환경에 따라 host 및 포트 정보 수정
HOST="127.0.0.1"
PORT=3308
USER="root"
PW="sad123"
DB="Nubisoft"

db = ConnectMysql()
conn, cur = db.mysql_create_session(HOST, PORT, USER, PW, DB)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
  print("Get 요청")
  return render_template('index.html', context='')

@app.route("/", methods=['POST'])
def post_home():
  print("post 요청")
  return "끝"

@app.route("/login", methods=['GET'])
def get_login():
  user_id = request.cookies.get("user")

  if(user_id):
    component_name = "로그인 완료 상태"
    resp = redirect("/")
    return component_name
  else: 
    component_name = 'login'
    return render_template('index.html', context=component_name)

@app.route("/login", methods=['POST'])
def post_login():

  try:
    email = request.form['email']
    pw = request.form['pw']

    query = "SELECT userPassword, userId FROM User WHERE userEmail = %s"
    cur.execute(query, email)
    data = cur.fetchone()  # 이메일로 단일 사용자 조회

    if data is None:
        return "존재하지 않는 이메일입니다."
    elif data[0] == pw:
        resp =  redirect("/")
        resp.set_cookie("user", str(data[1]))
        return resp
    else:
        return "잘못된 비밀번호입니다."

  except Exception as e:
    return f"Error : {e}"

@app.route("/signup")
def signup():
  component_name = 'signup'
  return render_template('index.html', context=component_name)

@app.route("/signup", methods=['POST'])
def post_signup():
  try:

    nickname = request.form['nickname']
    email = request.form['email']
    pw = request.form['pw']

    query = "SELECT userNickname FROM User WHERE userNickname = %s"
    cur.execute(query, nickname)
    nick_data = cur.fetchone()

    if nick_data is None:
      query = "SELECT userPassword FROM User WHERE userEmail = %s"
      cur.execute(query, email)
      email_data = cur.fetchone()

      if email_data is None:
        query = "INSERT INTO User (userEmail, userPassword, userNickname, userProfileImage) VALUES(%s, %s, %s, %s)"
        cur.execute(query, (email, pw, nickname, 1))
        result_data = cur.fetchall()
        
        if(result_data == []):
          cur.execute("commit;")
          return "회원가입 완료"
        else:
          print(result_data)
          return "회원가입 오류"

      elif email_data[0] == pw:
        return "이미 존재하는 사용자입니다."
    else:
      return "이미 존재하는 사용자입니다."

  except Exception as e:
    return f"Error : {e}"

@app.route("/logout", methods=['GET'])
def logout():
  resp = redirect("/")
  resp.delete_cookie("user")
  return resp

@app.route("/myaccount", methods=["GET"])
def get_user_info():
  user_id = request.cookies.get("user")

  query = "SELECT userEmail, userNickname from User where userId = %s"
  cur.execute(query, user_id)
  user_data = cur.fetchone()

  component_name = "editUser"
  return render_template("index.html", context=component_name, data={"email": user_data[0], "name": user_data[1]})

@app.route("/myaccount", methods=['POST'])
def post_user_info():
    user_id = request.cookies.get("user")

    nickname = request.form['nickname']
    email = request.form['email']

    query = "SELECT userNickname FROM User WHERE userNickname = %s"
    cur.execute(query, nickname)
    nick_data = cur.fetchone()

    if nick_data is None:
      query = "SELECT userPassword FROM User WHERE userEmail = %s"
      cur.execute(query, email)
      email_data = cur.fetchone()

      # update 문
      if email_data is None:
        query = "UPDATE User SET userEmail = %s, userNickname = %s where userId like %s"
        cur.execute(query, (email, nickname, user_id))
        result_data = cur.fetchall()
        
        if(result_data == []):
          cur.execute("commit;")
          return "회원수정 완료!"
        else:
          print(result_data)
          return "회원수정 오류"

      elif email_data[0] == pw:
        return "이미 사용하는 이메일 입니다."
    else:
      return "이미 사용하는 데이터 입니다."

    return ""

@app.route("/store")
def store():
  component_name = 'store'
  return render_template('index.html', context=component_name)

@app.route("/library")
def library():
   component_name = 'library'
   return render_template('index.html', component_name)

if __name__ == '__main__':
  app.run(port=8080, debug=True)