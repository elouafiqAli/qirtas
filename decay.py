from flask import Flask, request
from user import User

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcomes to the magic making server"


@app.route("/reach",methods=['GET'])
def reach():

    session_token = request.args.get('access_token')
    try:
        user = User(session_token)
        return "{\n\t'reach' : " + str(user.reach) + "\n}"
    except Exception as e:
        return "{\n\t'error' : '" + e.message + "'\n}"


if __name__ == "__main__":
    app.run()


