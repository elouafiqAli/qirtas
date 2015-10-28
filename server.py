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
    answer = '{'
    answer += "\n\t'reach' : " + str(user.reach)
    answer += '\n}'

    return answer


@app.route("/posts", methods=['GET'])
def posts():
    session_token = request.args.get('access_token')
    limit = request.args.get('limit')
    user = users.User(session_token)
    top_posts = user.top_posts(limit)

    answer = '{'
    for post in top_posts:
        answer += "\n\t'" + post.id + "'"
        answer += " : "
        answer += "'" + post.reach + "'"
        answer += ","
    answer.pop()
    answer += '\n}'
    return answer


if __name__ == "__main__":
    app.run()


