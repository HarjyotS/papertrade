import flask
from auth.register import register
from auth.login import login

# this is only for api calls, no serving html data

app = flask.Flask(__name__)

# register an account with the server
@app.route("/register", methods=["POST"])
def register_account():
    # get form-data from the request
    c = flask.request.form
    print(c["email"], c["id"], c["password"])
    re = register(email=c["email"], id=c["id"], password=c["password"])
    if re is True:
        return {"status": "success"}, 200
    else:
        return {"status": "failure"}, 400


@app.route("/login", methods=["POST"])
def login_account():
    c = flask.request.get_json()
    re = login(id=c["id"], password=c["password"])
    if re is not False:
        return {"status": "success", "token": re}, 200
    else:
        return {"status": "failure"}, 400


app.run()
