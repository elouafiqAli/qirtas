from user import User

test_token = 'CAACEdEose0cBALKXp9tpyDrftZAWOFLZAB0go51N6O9qgCAyliSPsfNv93XiFGEmbsmMmXf7SOTWaeaPUwjhB6fBmCVJKqlx3H3mL2GASEnCUWqNhT8YZBE20piyadejU2eTVpOHVhpZAUpih1KrS7M6sRcqbZAyVexdkSstjG6OMBI4lYg4JJyTEZBpeF3wv9uftSTd5jeQZDZD'


def test_session():
    print ' -- initalizing user'
    test_user = User(test_token)

    print test_user.reach


if __name__ == '__main__':
    test_session()