import decay
from test_facebook import test_token


def test_session():
    decay.app.debug = True
    client = decay.app.test_client()
    response = client.get('/reach?access_token='+test_token)
    print response.data