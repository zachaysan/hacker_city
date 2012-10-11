import riak
from copy import copy

from models.github_id import GithubId
from datetime import datetime
from dateutil import parser

BUCKET_NAME = 'github_user'
client = riak.RiakClient()
bucket = client.bucket(BUCKET_NAME)

class GithubUser(object):

    @staticmethod
    def find(id):
        riak_user = bucket.get(str(id))
        if not riak_user._exists:
            raise Exception, "No such user"
        data = riak_user.get_data()
        return GithubUser(data=data)
    
    @staticmethod
    def delete(id):
        r_github_user = bucket.get(str(id))
        r_github_user_data = r_github_user.get_data()
        assert r_github_user_data['id'] == str(id)
        login = r_github_user_data['login']
        GithubId.delete(login)
        r_github_user.delete()

    def destroy(self):
        GithubUser.delete(self.id)

    def __init__(self, user=None, data=None):
        if user and not data:
            data = self.get_data_from_user_attrs(user)
        elif not data:
            err = "Expect either user or data needed"
            raise TypeError, err
        self.ensure_proper_github_user_type(data)
        self.set_attrs_from_data(data)

    def ensure_proper_github_user_type(self, data):
        err = "Expects a User, not Company or Organization"
        if 'type' in data and data['type'] != 'User':
            raise TypeError, err

    def get_data_from_user_attrs(self, user):
        data = copy(user._attrs)
        data["count_followers"] = data["followers"]
        data["count_following"] = data["following"]
        data["count_public_gists"] = data["public_gists"]
        data["count_public_repos"] = data["public_repos"]
        del(data['followers'])
        del(data['following'])
        del(data['public_gists'])
        del(data['public_repos'])
        return data

    def set_attrs_from_data(self, data):
        self.set_created_at(data)
        self.id = int(data['id'])

        self.avatar_url = data['avatar_url']
        self.bio = data['bio']
        self.blog = data['blog']
        self.company = data['company']
        self.email = data['email']
        self.count_followers = data['count_followers']
        self.count_following = data['count_following']
        self.gravatar_id =  data['gravatar_id']
        self.hireable = data['hireable']
        self.html_url = data['html_url']
        self.location = data['location']
        self.login = data['login']
        self.name = data['name']
        self.count_public_gists = data['count_public_gists']
        self.count_public_repos = data['count_public_repos']
        self.url = data['url']
        
        del(data)
    
    def save(self):
        data = {"id": str(self.id),
                "created_at": str(self.created_at),

                "avatar_url": self.avatar_url,
                "bio": self.bio,
                "blog": self.blog,
                "company": self.company,
                "email": self.email,
                "count_followers": self.count_followers,
                "count_following": self.count_following,
                "gravatar_id": self.gravatar_id,
                "hireable": self.hireable,
                "html_url": self.html_url,
                "location": self.location,
                "login": self.login,
                "name": self.name,
                "count_public_gists": self.count_public_gists,
                "count_public_repos": self.count_public_repos,
                "url": self.url}
        return bucket.new(str(self.id), data=data).store()

    def set_created_at(self, data):
        created_at = data['created_at']
        if type(created_at) != datetime:
            self.created_at = parser.parse(created_at)
        else:
            self.created_at = created_at
