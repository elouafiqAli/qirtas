import decay

test_token = 'CAACEdEose0cBAAZC5hZBuURm5uyR0D553JUJKMAkr6rB59PSq1qk8s7oZBOfc29xCBnnGiqeRdUVEaJY9scn8UjZA6mzXiEvtcY47I6zA0VIyizXgBwOE0IFUN6ByZCinI3K4ZAfGLs0ZAKNfBxfNHyEEjpvpN4oYrl3xpL04QEh02OSh7XbuTNSLmSPV61KwB5nTx8t57nRgZDZD'


def test_session(test_token):
    decay.app.debug = True
    client = decay.app.test_client()
    response = client.get('/reach?access_token='+test_token)
    print response.data

if __name__ == '__main__':
    test_session(test_token)