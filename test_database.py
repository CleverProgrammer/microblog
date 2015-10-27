#!/Users/Chesstastic/Anaconda/envs/microblog/bin/python3
from app import db, models
from unittest import TestCase


# Changed flask_sqlalchemy __init__.py in order to make this test run
# /Users/Chesstastic/Anaconda/lib/python3.4/site-packages/flask_alchemy
# Changed None to True on line 797
class TestDatabase(TestCase):
    def test_User_and_Posts(self):
        # create user 1
        u = models.User(nickname='john', email='john@email.com')
        # create user 2
        u = models.User(nickname='susan', email='susan@email.com')
        users = models.User.query.all()
        # Access everything
        self.assertEqual(str(users), "[<User 'john'>, <User 'susan'>]")
        # Access id
        self.assertEqual(users[0].id, 1, "john's id should be 1")
        # Access nickname
        self.assertEqual(users[0].nickname, 'john', 'john should be john')
        # Access email
        self.assertEqual(users[0].email, 'john@email.com', 'john should be john')

