from flask import Flask, request
from users import User

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcomes to the magic making server"


@app.route("/reach",methods=['GET'])
def reach():

    session_token = request.args.get('access_token')
    user = User(session_token)
    return "{\n\t'reach' : " + str(user.reach) + "\n}"
    try:
        user = User(session_token)
        return "{\n\t'reach' : " + str(user.reach) + "\n}"
    except Exception as e:
        raise e


if __name__ == "__main__":
    app.run()


