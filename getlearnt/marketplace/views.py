from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.forms.models import model_to_dict
from django.contrib.auth import hashers
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Skill,  Listing, Transaction, Tag, AuthToken, Review, Recommendation


import random
import string
import json

@csrf_exempt
def UserView(request, user_id):
    responseData = {
        'ok': 'False'
    }
    user = get_object_or_404(UserProfile, pk=user_id)
    if request.method == 'POST':
        #change fields
        if request.POST.get('username'):
            username = request.POST.get('username')
            user.username = username
            user.save()
        if request.POST.get('email'):
            email = request.POST.get('email')
            user.email = email
            user.save()
    responseData = {
        'ok':   'True',
        'result':
        {
            'user':model_to_dict(user)
        }
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def CreateUserView(request):
    responseData = {
        'ok':   'FALSE',
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        newUser = UserProfile.objects.create(username=username, email=email)
        newUser.save()
        responseData = {
            'ok':   'True',
            'result':
            {
                'username':username,
                'email':email,
            }
        }
    return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def DeleteUserView(request, user_id):
    user = get_object_or_404(UserProfile, pk=user_id)
    user.delete()
    responseData = {
        'ok':   'True',
        'result':
        {
            'user_id': user_id
        }
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def AllUsersView(request):
    userList = UserProfile.objects.all()
    userListFinal = []
    for user in userList:
        user = model_to_dict(user)
        userListFinal.append(user)

    responseData = {
        'ok':'True',
        'result':
        {
            'listings':userListFinal
        }
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")


#-------------- Skill views
@csrf_exempt
def SkillView(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    if request.method == 'POST':
        if request.POST.get('newTitle'):
            newTitle = request.POST.get('newTitle')
            skill.title = newTitle
            skill.save()
        if request.POST.get('newDescription'):
            newDescription = request.POST.get('newDescription')
            skill.description = newDescription
            skill.save()
    # Make JSON file here
    responseData = {
        'ok':   'True',
        'result':
        {
            'title':skill.title,
            'description':skill.description,
        }
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def CreateSkillView(request):
    responseData = {
        'ok':   'FALSE',
    }
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        #user = request.POST.get('user')
        #user = UserProfile.objects.get(pk=user)
        newSkill = Skill.objects.create(title=title, description=description)
        newSkill.save()
        responseData = {
            'ok':   'True',
            'result':
            {
                'title':title,
                'description':description,
            }
        }
    return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def DeleteSkillView(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    skill.delete()
    responseData = {
        'ok':   True,
        'result':
        {
            'skill_id': skill_id
        }
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def AllSkillsView(request):
    skillList = (Skill.objects.all().values('title', 'description'))
    jsonSkillList = json.dumps(list(skillList))
    return HttpResponse(jsonSkillList, content_type="application/json")

#------------------- Tag Views

@csrf_exempt
def TagView(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    if request.method == 'POST':
        if request.POST.get('newTagType'):
            newTagType = request.POST.get('newTagType')
            tag.tagType = newTagType
            tag.save()
        if request.POST.get('newSkill'):
            newSkill = request.POST.get('newSkill')
            tag.skill = Skill.objects.get(pk=newSkill)
            tag.save()

    responseData = {
        'ok':   'True',
        'result': { 'tagType':tag.tagType, 'skill':tag.skill.title }
    }

    return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def CreateTagView(request):
    if request.method == 'POST':
        skill = request.POST.get('skill')
        tagType = request.POST.get('tagType')
        newTag = Tag.objects.create(tagType=tagType, skill=Skill.objects.get(pk=skill))
        newTag.save()
    responseData = {
        'ok':   'True',
        'result':
        {
            'tagType':tagType,
            'skill':skill
        }
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def DeleteTagView(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    tag.delete()
    responseData = {
        'ok':   'True',
        'result':
        {
            'tag_id':tag_id
        }
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def AllTagsView(request):
    tagList = (Tag.objects.all().values('tagType', 'skill'))
    jsonTagList = json.dumps(list(tagList))
    return HttpResponse(jsonTagList, content_type="application/json")


#---------------- Transaction Views

@csrf_exempt
def TransactionView(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    responseData = {
        'ok':   'True',
        'result':
        {
            'buyer':transaction.buyer.username,
            'seller':transaction.seller.username,
            'price':transaction.price
        }
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def CreateTransactionView(request):
    if request.method=='POST':
        buyer = request.POST.get('buyer')
        seller = request.POST.get('seller')
        skillSold = request.POST.get('skillSold')
        price = request.POST.get('price')
        newTransaction = Transaction.objects.create(buyer=UserProfile.objects.get(pk=buyer), seller=UserProfile.objects.get(pk=seller), skillSold=Skill.objects.get(pk=skillSold), price=price)
        newTransaction.save()
    responseData = {
        'ok':   'True',
        'result':
        {
            'buyer':buyer,
            'seller':seller,
            'price':price
        }
    }

    return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def DeleteTransactionView(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    transaction.delete()
    responseData = {
        'ok':   'True',
        'result':
        {
            'transaction_id':transaction_id
        }
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def AllTransactionsView(request):
    transactionList = (Transaction.objects.all().values('buyer', 'seller', 'skillSold'))
    jsonTransactionList = json.dumps(list(transactionList))
    return HttpResponse(jsonTransactionList, content_type="application/json")

#---------------- Listing Views

@csrf_exempt
def ListingView(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == 'POST':
        if request.POST.get('skill'):
            newSkill = request.POST.get('skill')
            listing.skill = Skill.objects.get(pk=newSkill)
            listing.save()
        if request.POST.get('price'):
            newPrice = request.POST.get('price')
            listing.price = newPrice
            listing.save()
        if request.POST.get('description'):
            newDescription = request.POST.get('description')
            listing.description = newDescription
            listing.save()

    listingDict = model_to_dict(listing)
    listingDict['skill'] = model_to_dict(Skill.objects.get(pk=listingDict['skill']))
    responseData = {
        'ok':   'True',
        'result':
        {
            'listing':listingDict,
            'recommendations':getRecommendations(listing_id)
        }
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")

def getRecommendations(listing_id):
    if Recommendation.objects.filter(item_id=listing_id).exists():
        return Recommendation.objects.get(item_id=listing_id).recommended_items
    else:
        return "none"


@csrf_exempt
def CreateListingView(request):
    header = request.POST.get('header')
    skill = request.POST.get('skill')
    skill_description = request.POST.get('skill_description')
    newSkill = Skill.objects.create(title=skill, description=skill_description)
    newSkill.save()
    price = request.POST.get('price')
    description = request.POST.get('description')
    user = UserProfile.objects.get(pk=request.POST.get('user'))
    newListing = Listing.objects.create(header=header, skill=newSkill, price=price, description=description, user=user)
    newListing.save()

    listingDict = model_to_dict(newListing)
    listingDict['skill'] = model_to_dict(Skill.objects.get(pk=listingDict['skill']))
    responseData = {
        'ok':   'True',
        'result':
        {
            'listing':model_to_dict(newListing)
        },
        'pk': newListing.pk
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def DeleteListingView(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    listing.delete()
    responseData = {
        'ok':   'True',
        'result':
        {
            'listing_id':listing_id
        }
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def AllListingsView(request):
    listings = Listing.objects.all()
    listingList = []

    for listing in listings:
        listing = model_to_dict(listing)
        listing['skill'] = model_to_dict(Skill.objects.get(pk=listing['skill']))
        listingList.append(listing)

    responseData = {
        'ok':'True',
        'result':
        {
            'listings':listingList
        }
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")



#---------- Review
@csrf_exempt
def ReviewView(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        if request.POST.get('header'):
            newHeader = request.POST.get('header')
            review.header = newHeader
            review.save()
        if request.POST.get('text'):
            newText = request.POST.get('text')
            review.price = newText
            review.save()
        if request.POST.get('rating'):
            newRating = request.POST.get('rating')
            listing.rating = newRating
            review.save()

    reviewDict = model_to_dict(review)
    responseData = {
        'ok':   'True',
        'result':
        {
            'review':reviewDict
        }
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")


@csrf_exempt
def CreateReviewView(request):
    header = request.POST.get('header')
    text = request.POST.get('text')
    rating = request.POST.get('rating')
    user = request.POST.get('user')
    user = UserProfile.objects.get(pk=user)
    listing = Listing.objects.get(pk=request.POST.get('listing'))
    newReview = Review.objects.create(header=header, text=text, rating=rating, user=user, listing=listing)
    newReview.save()

    reviewDict = model_to_dict(newReview)
    responseData = {
        'ok':   'True',
        'result':
        {
            'review':reviewDict
        }
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def DeleteReviewView(request, review_id):
    try:
        review = get_object_or_404(Review, pk=review_id)
        review.delete()
        responseData = {
            'ok':   'True',
            'result':
            {
                'listing_id':review_id
            }
        }
        return HttpResponse(json.dumps(responseData), content_type="application/json")
    except Http404 as e:
        responseData = {
            'ok':'False',
            'error': 'id does not match existing review'
        }
        return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def AllReviewView(request, listing_id):
    reviews = Review.objects.filter(listing=listing_id)
    reviewList = []

    for review in reviews:
        review = model_to_dict(review)
        reviewList.append(review)


    responseData = {
        'ok':'True',
        'result':
        {
            'reviews':reviewList
        }
    }
    return HttpResponse(json.dumps(responseData), content_type="application/json")
#------------ Other Stuff
@csrf_exempt
def CreateAccount(request):
    if request.method=='POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            new_user = UserProfile.objects.create(username=username, password=hashers.make_password(password=password), email=email)
            new_user.save()
        except IntegrityError as e:
            return HttpResponse(json.dumps({"status":"A user with that email or username already exists"}), content_type="application/json")
        return HttpResponse(json.dumps({"status":"success"}), content_type="application/json")

    else:
        return HttpResponse(json.dumps({"status":"Error, must be a post request"}), content_type="application/json")

@csrf_exempt
def Login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if UserProfile.objects.filter(username=username).exists():
            user = UserProfile.objects.get(username=username)
            valid = hashers.check_password(password=password, encoded=user.password)
            if valid:
                #return an authentication token of some sort
                token = AuthToken.objects.create(token=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(256)))
                token.save()
                responseData = {
                    "status":"login successful",
                    "token":model_to_dict(token),
                    "user_id":user.id
                }
                return HttpResponse(json.dumps(responseData), content_type="application/json")

            else:
                #return an incorrect password message
                responseData = {"status":"Incorrect password"}
                return HttpResponse(json.dumps(responseData), content_type="application/json")

        else:
            responseData = {"status":"User not found"}
            return HttpResponse(json.dumps(responseData), content_type="application/json")
    else:
        responseData = {"status":"Error, must be a post request"}
        return HttpResponse(json.dumps(responseData), content_type="application/json")

@csrf_exempt
def Logout(request):
    if request.method=='POST':
        token = request.POST.get('token')
        db_token = AuthToken.objects.get(token=token)
        db_token.delete()
        return HttpResponse(json.dumps({"status":"Successfully logged out"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"status":"Error, must be a post request"}), content_type="application/json")

@csrf_exempt
def Authenticate(request):
    if request.method=='POST':
        token = request.POST.get('token')
        db_token = AuthToken.objects.get(token=token)

        if db_token:
            return HttpResponse(json.dumps({"status":"authenticated"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status":"failure"}), content_type="application/json")

    else:
        return HttpResponse(json.dumps({"status":"Error, must be a post request"}), content_type="application/json")
