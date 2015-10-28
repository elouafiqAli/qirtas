import server
from test_facebook import test_token

server.users.__caching__ = True
server.users.__cache_database__ = 'testing_users'
server.app.debug = True
client = server.app.test_client()

test_limit = 25


def test_session():
    response = client.get('/reach?access_token='+test_token)
    return response.data


def test_top_posts():
    response = client.get('/posts?access_token='+test_token+'&limit'+test_limit)
    return test_limit