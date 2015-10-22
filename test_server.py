import server
from test_facebook import test_token


def test_session():
    server.app.debug = True
    client = server.app.test_client()
    response = client.get('/reach?access_token='+test_token)
    return response.data

