from flask import Flask, request
import users

app = Flask(__name__)
users.__caching__ = True
users.__cache_database__ = 'cacheDB'

@app.route("/")
def index():
    return "Welcomes to the magic making server"


@app.route("/reach",methods=['GET'])
def reach():

    session_token = request.args.get('access_token')
    user = users.User(session_token)
    return "{\n\t'reach' : " + str(user.reach) + "\n}"
    try:
        user = User(session_token)
        return "{\n\t'reach' : " + str(user.reach) + "\n}"
    except Exception as e:
        raise e


if __name__ == "__main__":
    app.run()


