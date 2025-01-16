from connect_db import ConnectMysql
from flask import Flask, render_template, request
from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)

template = env.get_template("index.html")

# 개인 환경에 따라 host 및 포트 정보 수정
HOST="127.0.0.1"
PORT=3308
USER="root"
PW="sad123"
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
  email = request.form['email']
  pw = request.form['pw']
  print(email)
  print(pw)
  return "post 요청"

@app.route("/signup")
def signup():
  component_name = 'signup'
  return render_template('index.html', context=component_name)

@app.route("/game")
def game():
  component_name = 'game'
  return render_template('index.html', context=component_name)

if __name__ == '__main__':
  app.run(port=8080, debug=True)