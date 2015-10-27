#!/Users/Chesstastic/Anaconda/envs/microblog/bin/python3
from app import db, models
from unittest import TestCase


# Changed flask_sqlalchemy __init__.py in order to make this test run
# /Users/Chesstastic/Anaconda/lib/python3.4/site-packages/flask_alchemy
# Changed None to True on line 797
class TestModels(TestCase):
    def test_Users_and_Posts(self):
        import datetime
        # create user 1
        u = models.User(nickname='john', email='john@email.com')
        # create user 2
        u = models.User(nickname='susan', email='susan@email.com')
        users = models.User.query.all()
        # Access everything
        self.assertEqual(users.__repr__(), "[<User 'john'>, <User 'susan'>]")

        # -------------- CHECK JOHN ---------------------------
        # Access john's id
        self.assertEqual(users[0].id, 1, "john's id should be 1")
        # Access john's nickname
        self.assertEqual(users[0].nickname, 'john', 'john should be john')
        # Access john's email
        self.assertEqual(users[0].email, 'john@email.com', 'john should be john')

        # -------------- CHECK SUSAN ---------------------------
        # Access susan's id
        self.assertEqual(users[1].id, 2, "susan's id should be 1")
        # Access susan's nickname
        self.assertEqual(users[1].nickname, 'susan', 'susan should be susan')
        # Access susan's email
        self.assertEqual(users[1].email, 'susan@email.com', 'susan should be susan')

        # Get users with id
        u = models.User.query.get(1)
        self.assertEqual(u.__repr__(), "<User 'john'>")
        susan = models.User.query.get(2)
        self.assertEqual(susan.__repr__(), "<User 'susan'>")

        # Get all posts from a user
        post = models.Post(body='my first post!', timestamp=datetime.datetime.utcnow(), author=susan)
        posts = susan.posts.all()
        self.assertEqual(posts.__repr__(), "[<Post 'my first post!'>]")

        # obtain author of each post
        for post in posts:
            print(post.id, post.author.nickname, post.body)

