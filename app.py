from connect_db import ConnectMysql
from flask import Flask, render_template, request
from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)

template = env.get_template("index.html")

# 개인 환경에 따라 host 및 포트 정보 수정
HOST="127.0.0.1"
PORT=3306
USER="root"
PW="root"
DB="nubisoft"

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
  component_name = 'login'
  return render_template('index.html', context=component_name)

@app.route("/login", methods=['POST'])
def post_login():

  try:
    email = request.form['email']
    pw = request.form['pw']

    query = "SELECT userPassword FROM User WHERE userEmail = %s"
    cur.execute(query, email)
    data = cur.fetchone()  # 이메일로 단일 사용자 조회

    if data is None:
        return "존재하지 않는 이메일입니다."
    elif data[0] == pw:
        return "로그인 성공"
    else:
        return "잘못된 비밀번호입니다."

  except Exception as e:
    return f"Error : {e}"



  # email = request.form['email']
  # pw = request.form['pw']

  # cur.execute('SELECT * FROM User;')
  # data = cur.fetchall()
  # result = []
  # result.append([])
  # result[0].append('userEmail')
  # result[0].append('userPassword')
  
  # count = 1

  # for rowdata in data:
  #     result.append([])
  #     result[count].append(rowdata[1])
  #     result[count].append(rowdata[2])
  #     count += 1

  # for i in range(len(result) + 1):
  #   if (email in result[i][0] and pw == result[i][1]):
  #     print("로그인 성공")
  #     break

@app.route("/signup")
def signup():
  component_name = 'signup'
  return render_template('index.html', context=component_name)

@app.route("/store")
def store():
  component_name = 'store'
  return render_template('index.html', context=component_name)

if __name__ == '__main__':
  app.run(port=8080, debug=True)