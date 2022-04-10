from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from .models import Skill, Tag, Transaction, Listing, UserProfile
# Create your tests here.
# fixtures = ['db.json'] TODO: why does this not work
class userProfileModelTestCase(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        pass

    # def test_user_success_create(self):
    #     response = self.client.post(reverse('CreateUserView'), {'username':'TestUser', 'email':'test@test.com'})
    #     self.assertContains(response, 'TestUser')

    def test_user_success_valid_url(self):
        # Try to view first user in db
        response = self.client.get(reverse('UserView', args=[10]))
        # Make sure response contains a username
        self.assertContains(response, 'username')

    def test_user_success_update(self):
        # Get first listing in db
        response = self.client.post(reverse('UserView', kwargs={'user_id':10}), {'username':'test'})

        self.assertContains(response, 'test')

    def test_user_failure_invalid_url(self):
        #response = self.client.get(reverse('UserView')) TODO: this doesn't work for some reason
        response = self.client.get('/user/')
        self.assertEquals(response.status_code, 404)

    def test_user_failure_user_dne(self):
        response = self.client.get('/user/delete/', {'user_id':100000})
        self.assertEquals(response.status_code, 404)

    def test_user_success_get_all(self):
        response = self.client.get(reverse('AllUsersView'))
        self.assertContains(response, 'username')

    def tearDown(self):
        pass

class skillModelTestCase(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        pass

    def test_skill_success_create(self):
        # Create a new skill
        response = self.client.post(reverse('CreateSkillView'), {'title':'testing', 'description':'skill used for testing'})
        self.assertContains(response, 'testing')

    def test_skill_success_valid_url(self):
        # Try to view first skill in db
        response = self.client.get(reverse('SkillView', args=[1]))
        # Make sure response came back True
        self.assertContains(response, 'True')

    def test_skill_failure_invalid_url(self):
        response = self.client.get('/skill/')
        self.assertEquals(response.status_code, 404)

    def test_skill_failure_skill_dne(self):
        response = self.client.get('/skill/delete/', {'user_id':100000})
        self.assertEquals(response.status_code, 404)

    def test_skill_success_get_all(self):
        response = self.client.get(reverse('AllSkillsView'))
        self.assertContains(response, 'title')

    def tearDown(self):
        pass

class tagModelTestCase(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        pass

    def test_tag_success_create(self):
        # Create a new tag
        response = self.client.post(reverse('CreateTagView'), {'skill':1, 'tagType':'tag used for testing'})
        self.assertContains(response, 'tagType')

    def test_tag_success_valid_url(self):
        # Try to view first skill in db
        response = self.client.get(reverse('TagView', args=[1]))
        # Make sure response contains a username
        self.assertContains(response, 'True')

    def test_tag_failure_invalid_url(self):
        response = self.client.get('/tag/')
        self.assertEquals(response.status_code, 404)

    def test_tag_failure_skill_dne(self):
        response = self.client.get('/tag/delete/', {'user_id':100000})
        self.assertEquals(response.status_code, 404)

    def test_tag_success_get_all(self):
        response = self.client.get(reverse('AllTagsView'))
        self.assertContains(response, 'tagType')

    def tearDown(self):
        pass

class transactionModelTestCase(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        pass

    def test_transaction_success_create(self):
        # Create a new transaction
        response = self.client.post(reverse('CreateTransactionView'), {'buyer':10, 'seller':11, 'skillSold':1, 'price':22.02})
        self.assertContains(response, 'price')

    def test_transaction_success_valid_url(self):
        # Try to view first skill in db
        response = self.client.get(reverse('TransactionView', args=[2]))
        # Make sure response contains a username
        self.assertContains(response, 'price')


    def test_transaction_failure_invalid_url(self):
        response = self.client.get('/transaction/')
        self.assertEquals(response.status_code, 404)

    def test_transaction_failure_skill_dne(self):
        response = self.client.get('/transaction/', {'transaction_id':10000})
        self.assertEquals(response.status_code, 404)

    def test_transaction_success_get_all(self):
        response = self.client.get(reverse('AllTransactionsView'))
        self.assertContains(response, 'buyer')

    def test_transaction_tearDown(self):
        pass

class listingModelTestCase(TestCase):

    fixtures = ['db.json']

    def setUp(self):
        pass

    def test_listing_success_create(self):
        # Create a new listing
        response = self.client.post(reverse('CreateListingView'), {'header': 'ListingTitle', 'skill':'skillTitle', 'skill_description':'description of skill', 'price': 10.10, 'description':'listing used for testing', 'user':11})
        self.assertContains(response, 'ListingTitle')

    def test_listing_success_valid_url(self):
        # Try to view first listing in db
        response = self.client.get(reverse('ListingView', args=[8]))
        # Make sure response comes back true
        self.assertContains(response, 'True')

    def test_listing_success_update(self):
        # Change first listing in db
        newSkill = Skill.objects.create(title='skillTitleTest', description='description of skill')
        response = self.client.post('/listing/9/', {'skill':newSkill.id})
        self.assertContains(response, 'True')

    def test_listing_failure_invalid_url(self):
        response = self.client.get('/listing/')
        self.assertEquals(response.status_code, 404)

    def test_listing_failure_skill_dne(self):
        response = self.client.get('/listing/delete', {'skill_id':10000})
        self.assertEquals(response.status_code, 404)

    def test_listing_success_get_all(self):
        response = self.client.get(reverse('AllListingsView'))
        self.assertContains(response, 'skill')

    def tearDown(self):
        pass

class ReviewModelTestCase(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        pass

    def test_review_success_create(self):
        # Create a new review
        user = UserProfile.objects.get(pk=11)
        response = self.client.post(reverse('CreateReviewView'), {'header':'Test Review', 'text':'Test Text', 'rating':4, 'user':user.id, 'listing':8})
        self.assertContains(response, 'review')

    def test_review_success_valid_url(self):
        # Try to view first review in db
        response = self.client.get(reverse('ReviewView', args=[1]))
        # Make sure response comes back true
        self.assertContains(response, 'True')

    def test_review_failure_invalid_url(self):
        response = self.client.get('/review/')
        self.assertEquals(response.status_code, 404)

    def test_review_failure_dne(self):
        response = self.client.get('/review/delete', {'review_id':10000})
        self.assertEquals(response.status_code, 404)

    def test_listing_success_get_all(self):
        response = self.client.get('/review/all/8/')
        self.assertContains(response, 'review')

    def tearDown(self):
        pass

class AccountTestCase(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        pass

    def test_account_create(self):
        response = self.client.post(reverse('CreateAccount'), {'username':'TestUser', 'password':'passwordTest', 'email':'test@test.com'})
        self.assertContains(response, 'success')

    def test_account_create_usernameExists(self):
        response = self.client.post(reverse('CreateAccount'), {'username':'user', 'password':'password', 'email':'test2@test.com'})
        self.assertContains(response, 'A user with that email or username already exists')

    def test_account_loginTrue(self):
        response = self.client.post(reverse('Login'), {'username':'user', 'password':'password'})
        self.assertContains(response, 'login successful')

    def test_account_incorrectUsername(self):
        response = self.client.post(reverse('Login'), {'username':'TestUser', 'password':'passwordTest'})
        self.assertContains(response, 'User not found')

    def test_account_incorrectPassword(self):
        response = self.client.post(reverse('Login'), {'username':'user', 'password':'FAKE'})
        self.assertContains(response, 'Incorrect password')


    def tearDown(self):
        pass

class RecommendationTestCase(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        pass

    def test_recommendations_get(self):
        # Get recommendations for item 3 (should include item 4)
        pass

    def test_get_empty_recommendations(self):
        # Get recommendations for item 1 (should be empty)
        pass

    def tearDonw(self):
        pass
