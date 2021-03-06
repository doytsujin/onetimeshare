import os
import uuid

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "onetimeshare.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

class Secret(db.Model):
    secret = db.Column(db.String(80), nullable=False)
    sid = db.Column(db.String(32), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Secret: {}>".format(self.secret)

@app.route("/", methods=["GET", "POST"])
def add_secret():
    sid = ""
    url = ""
    if request.form:
        sid = str(uuid.uuid4()).replace("-","")
        secret = Secret(secret=request.form.get("secret"), sid=sid)
        db.session.add(secret)
        db.session.commit()
        url = request.base_url
    
    return render_template("index.html", sid=sid, url=url)
  
@app.route("/<sid>", methods=["GET"])
def get_secret(sid):
    secret = Secret.query.filter_by(sid=sid).first()
    if secret is not None:
        db.session.delete(secret)
        db.session.commit()
    return render_template("get.html", secret=secret)  

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
