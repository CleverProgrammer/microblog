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
        db.session.add(u)
        # create user 2
        u = models.User(nickname='susan', email='susan@email.com')
        db.session.add(u)
        users = models.User.query.all()
        # Access everything
        self.assertEqual(users.__repr__(), "[<User 'Rafeh'>, <User 'john'>, <User 'susan'>]")

        # -------------- CHECK JOHN ---------------------------
        # Access john's id
        self.assertEqual(users[1].id, 2, "john's id should be 1")
        # Access john's nickname
        self.assertEqual(users[1].nickname, 'john', 'john should be john')
        # Access john's email
        self.assertEqual(users[1].email, 'john@email.com', 'john should be john')

        # -------------- CHECK SUSAN ---------------------------
        # Access susan's id
        self.assertEqual(users[2].id, 3, "susan's id should be 1")
        # Access susan's nickname
        self.assertEqual(users[2].nickname, 'susan', 'susan should be susan')
        # Access susan's email
        self.assertEqual(users[2].email, 'susan@email.com', 'susan should be susan')

        # Get users with id
        u = models.User.query.get(2)
        self.assertEqual(u.__repr__(), "<User 'john'>")
        susan = models.User.query.get(3)
        self.assertEqual(susan.__repr__(), "<User 'susan'>")

        # Get all posts from Susan
        post = models.Post(body='my first post!', timestamp=datetime.datetime.utcnow(), author=susan)
        db.session.add(post)
        posts = susan.posts.all()
        self.assertEqual(posts.__repr__(), "[<Post 'my first post!'>]")

        # obtain author of each post
        for post in posts:
            print(post.id, post.author.nickname)
            self.assertEqual(post.id, 1)
            self.assertEqual(post.author.nickname, 'susan')
            self.assertEqual(post.body, "my first post!")
            pass

        # get all users in reverse alphabetical order
        nicknames_desc = models.User.query.order_by('nickname desc').all()
        expected = "[<User 'susan'>, <User 'john'>, <User 'Rafeh'>]"
        self.assertEqual(nicknames_desc.__repr__(), expected)
