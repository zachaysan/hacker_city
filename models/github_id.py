import riak

client = riak.RiakClient()
bucket = client.bucket('login_to_id')

class GithubId(object):
    
    @staticmethod
    def check_exists(r_github_id):
        if not r_github_id._exists:
            err = "No such login"
            raise Exception, err
    
    @staticmethod
    def find(login):
        r_github_id = bucket.get(login)
        GithubId.check_exists(r_github_id)
        data = r_github_id.get_data()
        return GithubId(login, **data)

    @staticmethod
    def delete(login):
        r_github_id = bucket.get(login)
        GithubId.check_exists(r_github_id)
        r_github_id.delete()

    def __init__(self, login, id):
        self.login = login
        self.id = id
    
    def save(self):
        data = {"id": self.id}
        return bucket.new(self.login, data=data).store()
