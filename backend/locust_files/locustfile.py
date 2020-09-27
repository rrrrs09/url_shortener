import string, random

from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):
    '''Imitation of user actions'''
    @task()
    def shorten_url(self):
        '''tests url shortening method using random urls and slugs'''
        use_slug = random.choice((True, False))
        data = {
            'url': 'https://www.{}.ru'.format(self.generate_str()),
            'slug': '' if not use_slug else self.generate_str()
        }
        self.client.post('/shorten/', json=data)

    def generate_str(self):
        '''returns random string containing chars and digits'''
        alphabet = string.ascii_lowercase + string.digits
        size = random.randint(3, 10)
        return ''.join(random.choice(alphabet) for _ in range(size))


class WebsiteUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [UserBehavior]