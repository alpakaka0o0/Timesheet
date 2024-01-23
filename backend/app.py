from flask import Flask
from models import db, Manager, Employee, Pay, Timesheet, Image

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
with app.app_context():
    db.create_all()

# app.config.from_pyfile("config.py")

# from models import db
# db.init_app(app)

@app.route('/')
def users():
    #users 데이터를 Json 형식으로 반환한다.
    return {"members": [{"id" : 1, "name" : "jihyun"},
                        {"id" : 2, "name" : "jerry"}]}


if __name__ == "__main__":
    app.run(debug = True)

