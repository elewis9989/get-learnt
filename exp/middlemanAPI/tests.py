from django.test import TestCase, Client
from django.core.urlresolvers import reverse
# Create your tests here.

class userProfileModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_user_success_create(self):
        response = self.client.post(reverse('user', {'username':'TestUser', 'email':'test@test.com'}))
        self.assertContains(response, 'TestUser')

    def test_user_success_valid_url(self):
        # Try to view first user in db
        response = self.client.get(reverse('user', kwargs={'user_id':1}))
        # Make sure response contains a username
        self.assertContains(response, 'username')

    def test_user_failure_invalid_url(self):
        response = self.client.get(reverse('user'))
        self.assertEquals(response.status_code, 404)

    def test_user_failure_user_dne(self):
        response = self.client.get(reverse('user', kwargs={'user_id':10000}))
        self.assertEquals(response.status_code, 404)

    def tearDown(self):
        pass

class skillModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_skill_success_create(self):
        # Create a new skill
        response = self.client.post('skill', {'title':'testing', 'description':'skill used for testing', 'user':1})
        self.assertContains(response, 'testing')

    def test_skill_success_valid_url(self):
        # Try to view first skill in db
        response = self.client.get(reverse('skill', kwargs={'skill_id':1}))
        # Make sure response came back True
        self.assertContains(response, 'True')

    def test_skill_failure_invalid_url(self):
        response = self.client.get(reverse('skill'))
        self.assertEquals(response.status_code, 404)

    def test_skill_failure_skill_dne(self):
        response = self.client.get(reverse('skill', kwargs={'skill_id':10000}))
        self.assertEquals(response.status_code, 404)

    def tearDown(self):
        pass

class tagModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_tag_success_valid_url(self):
        # Try to view first skill in db
        response = self.client.get(reverse('tag', kwargs={'model_id':1}))
        # Make sure response contains a username
        self.assertContains(response, 'True')

    def test_tag_failure_invalid_url(self):
        response = self.client.get(reverse('tag'))
        self.assertEquals(response.status_code, 404)

    def test_tag_failure_skill_dne(self):
        response = self.client.get(reverse('tag', kwargs={'tag':10000}))
        self.assertEquals(response.status_code, 404)

    def tearDown(self):
        pass

class transactionModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_transaction_success_valid_url(self):
        # Try to view first skill in db
        response = self.client.get(reverse('transaction', kwargs={'transaction_id':1}))
        # Make sure response contains a username
        self.assertContains(response, 'True')


    def test_transaction_failure_invalid_url(self):
        response = self.client.get(reverse('transaction'))
        self.assertEquals(response.status_code, 404)

    def test_transaction_failure_skill_dne(self):
        response = self.client.get(reverse('transaction', kwargs={'transaction_id':10000}))
        self.assertEquals(response.status_code, 404)

    def test_transaction_tearDown(self):
        pass

class listingModelTestCase(TestCase):
    def setUp(self):

        pass

    def test_listing_success_valid_url(self):
        # Try to view first skill in db
        response = self.client.get(reverse('listing', kwargs={'listing_id':1}))
        # Make sure response comes back true
        self.assertContains(response, 'True')

    def test_listing_success_update(self):
        # Get first listing in db
        response = self.client.post('listing/1', {'skill':'test'})
        self.assertContains(response, 'test')

    def test_listing_failure_invalid_url(self):
        response = self.client.get(reverse('listing'))
        self.assertEquals(response.status_code, 404)

    def test_listing_failure_skill_dne(self):
        response = self.client.get(reverse('listing', kwargs={'skill_id':10000}))
        self.assertEquals(response.status_code, 404)

    def tearDown(self):
        pass
