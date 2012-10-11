import pygithub3

class Github(object):
    def __init__(self):
        self.gh = pygithub3.Github()
        
    def crawl_from_user(self,
                        username,
                        location,
                        max_requests=None):
        
        user = self.gh.users.get(username)
        yield user
        max_requests -= 1
        for page in self.gh.users.followers.list(username):
            if max_requests < 1:
                break
            for user in page:
                yield user

        
