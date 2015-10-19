from user import User

test_token = 'CAACEdEose0cBAM2mct5BixCE8tTQrAWNiwCZACAyibwepuZA3L1ll5sUJHnbBBjjmqkct8cX2TAQYV2QwIlZATy3O4txVPePS5T94cpy1oCffL4EJ6JVUj0zqorV1ZCOfnlgUfKXb52JZCAjiblTLSZAMX9pt0o9HZA47AtOrLqIpZAImYWSIHGfEezfdMyyA58iRBnaMQ2QDgZDZD'

def test_session():
    print '-- initilizing user'
    test_user = User(test_token)
    print '-- getting posts'
    posts = test_user.posts
    print '-- computing reach for each post'
    reach_list = [post.reach for post in posts]
    print '-- sorting the list'
    sorted_posts = sorted( reach_list , reverse = True)
    for r in sorted_posts:
        print ' :: ' , r

if __name__ == '__main__':
    test_session()