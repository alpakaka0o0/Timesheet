from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("config.py")

from models import db
db.init_app(app)

@app.route('/')
def users():
    #users 데이터를 Json 형식으로 반환한다.
    return {"members": [{"id" : 1, "name" : "jihyun"},
                        {"id" : 2, "name" : "jerry"}]}




if __name__ == "__main__":
    app.run(debug = True)

