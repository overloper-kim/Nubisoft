import pymysql

class ConnectMysql:
  def __init__(self) -> None:
    pass

  # MySQL 연동
  def mysql_create_session(self, _HOST, _PORT, _USER, _PW, _DB):
    conn = pymysql.connect(host=_HOST, port=_PORT, user=_USER, password=_PW, db=_DB, charset='utf8')
    cur = conn.cursor()
    print("========== DATABASE CONNECTION SUCCESS ==========")
    return conn, cur