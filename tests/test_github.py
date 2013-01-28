import unittest
from crawlers.github import Github
from models.github_id import GithubId
from models.github_user import GithubUser
from datetime import datetime
from pprint import pprint

class Test_Github(unittest.TestCase):
    def gen_users(self):
        """ Generate users by crawling from 
        Zach Aysan, each successive next() call
        goes further and further out
        """

        g = Github()
        u = (u for u in g.crawl_from_user("zachaysan",
                                          "toronto",
                                          max_requests=100))
        return u

    def setUp(self):
        try:
            GithubUser.delete(222715)
        except:
            pass

    def test_init(self):
        g = Github()
        self.assertTrue(g)

    def test_zach(self):
        zach = next(self.gen_users())
        GithubId(zach.login, zach.id).save()
        GithubUser(zach).save()
        zachaysan_id = zach.id
        del(zach)
        zach = GithubUser.find(222715)
        self.assertEqual(zach.login, "zachaysan")
        zach.destroy()

    def test_retrieving_unknown_user(self):
        self.assertRaises(Exception,
                          GithubUser.find,
                          222715)

    def test_retrived_created_at_in_datetime(self):
        zach = next(self.gen_users())
        GithubId(zach.login, zach.id).save()
        GithubUser(zach).save()
        zach_id = zach.id
        del(zach)
        zach = GithubUser.find(zach_id)
        self.assertEqual(zach.login, "zachaysan")
        self.assertEqual(type(zach.created_at), datetime)
        
    def test_follower_retrival(self):
        zach = next(self.gen_users())
        zach = GithubUser(zach)
        self.assertEqual(len([f for f in zach.followers()]),
                         zach.count_followers)
    
    def test_followings_retrival(self):
        zach = next(self.gen_users())
        zach = GithubUser(zach)
        self.assertEqual(len([f for f in zach.followings()]),
                         zach.count_followings)
