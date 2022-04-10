from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class UserProfile(models.Model):
	username = models.CharField(max_length=45, unique=True)
	email = models.CharField(max_length=100, default='EMAIL')
	password = models.CharField(max_length=500, default='SOME STRING')

	def __str__(self):
		return self.username

class Skill(models.Model):
	title = models.CharField(max_length=30)
	description=models.TextField()

	def __str__(self):
		return self.title

class Tag(models.Model):
	tagType = models.CharField(max_length=25)
	skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

	def __str__(self):
		return self.tagType

class Transaction(models.Model):
	buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='transaction_as_buyer')
	seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='transaction_as_seller')
	skillSold = models.ForeignKey(Skill, on_delete=models.CASCADE)
	price = models.FloatField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '' + self.buyer.username + ' bought from ' + self.seller.username

class Listing(models.Model):
	skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
	price = models.FloatField()
	listDate = models.DateTimeField(auto_now_add=True)
	description = models.TextField()
	header = models.CharField(max_length=75, default="No Header")
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

	def __str__(self):
		return self.header

class Review(models.Model):
	header = models.CharField(max_length=30)
	text = models.TextField()
	rating = models.IntegerField()
	user = models.ForeignKey(UserProfile)
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

	def __str__(self):
		return self.header


class AuthToken(models.Model):
	token=models.CharField(max_length=500)

class Recommendation(models.Model):
	item_id = models.CharField(default=None, max_length=200, unique=True)
	recommended_items = models.CharField(default=None, max_length=200)
