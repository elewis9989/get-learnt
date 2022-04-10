from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from kafka import KafkaProducer
from elasticsearch import Elasticsearch
import urllib.request
import urllib.parse
import urllib
import json
import requests


# Create your views here.

#-------------- USER
@csrf_exempt
def UserView(request, user_id):
    if(request.method == "GET"): #do I need this if?
        req = urllib.request.Request('http://models-api:8000/user/' + user_id + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle POST'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def CreateUserView(request):
    if (request.method == "POST"):
        # get username and email
        username = request.POST.get('username')
        email = request.POST.get('email')
        #send to models container
        post_data = {'username': username, 'email': email}
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        #get info back from models container
        req = urllib.request.Request('http://models-api:8000/user/create/', data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        #return
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle GET'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def DeleteUserView(request, user_id):
    if (request.method == "POST"):
        req = urllib.request.Request('http://models-api:8000/user/delete/' + user_id + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle GET'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def AllUsersView(request):
    if(request.method == "GET"):
        req = urllib.request.Request('http://models-api:8000/user/all/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle POST'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")



#-------------- SKILL
@csrf_exempt
def SkillView(request, skill_id):
    if(request.method == "GET"):
        req = urllib.request.Request('http://models-api:8000/skill/' + skill_id + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle POST'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def CreateSkillView(request):
    if(request.method == 'POST'):
        # get info
        title = request.POST.get('title')
        description = request.POST.get('description')
        #user = request.POST.get('user')
        # send to containers model
        post_data = {'title': title, 'description': description}
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        #get info back from models container
        req = urllib.request.Request('http://models-api:8000/skills/create/', data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        #return
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle POST'
        }
    }

    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def DeleteSkillView(request, skill_id):
    if (request.method == "POST"):
        req = urllib.request.Request('http://models-api:8000/skill/delete/' + skill_id + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle GET'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def AllSkillsView(request):
    if(request.method == "GET"):
        req = urllib.request.Request('http://models-api:8000/skill/all/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle POST'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

#-------------- TAG
@csrf_exempt
def TagView(request, tag_id):
    if(request.method == "GET"):
        req = urllib.request.Request('http://models-api:8000/tag/' + tag_id + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle POST'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def CreateTagView(request):
    if(request.method == 'POST'):
        # get info
        skill = request.POST.get('skill')
        tagType = request.POST.get('tagType')
        # send to containers model
        post_data = {'skill': skill, 'tagType': tagType}
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        #get info back from models container
        req = urllib.request.Request('http://models-api:8000/tag/create/', data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        #return
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle GET'
        }
    }

    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def DeleteTagView(request, tag_id):
    if (request.method == "POST"):
        req = urllib.request.Request('http://models-api:8000/tag/delete/' + tag_id + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle GET'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def AllTagsView(request):
    if(request.method == "GET"):
        req = urllib.request.Request('http://models-api:8000/tag/all/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle POST'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")
#-------------- TRANSACTION
@csrf_exempt
def TransactionView(request, transaction_id):
    if(request.method == "GET"):
        req = urllib.request.Request('http://models-api:8000/transaction/' + transaction_id + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle POST'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def CreateTransactionView(request):
    if(request.method == 'POST'):
        # get info
        buyer = request.POST.get('buyer')
        seller = request.POST.get('seller')
        skillSold = request.POST.get('skillSold')
        price = request.POST.get('price')
        # send to containers model
        post_data = {'buyer': buyer, 'seller': seller, 'skillSold':skillSold, 'price': price}
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        #get info back from models container
        req = urllib.request.Request('http://models-api:8000/transaction/create/', data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        #return
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle GET'
        }
    }

    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def DeleteTransactionView(request, transaction_id):
    if (request.method == "POST"):
        req = urllib.request.Request('http://models-api:8000/transaction/delete/' + transaction_id + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle GET'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def AllTransactionsView(request):
    if(request.method == "GET"):
        req = urllib.request.Request('http://models-api:8000/transaction/all/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle POST'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

#-------------- LISTING
@csrf_exempt
def ListingView(request, listing_id):
    if(request.method == "GET"):
        req = urllib.request.Request('http://models-api:8000/listing/' + listing_id + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle POST'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def CreateListingView(request):
    if(request.method == 'POST'):
        # get info
        header = request.POST.get('header')
        skill = request.POST.get('skill')
        price = request.POST.get('price')
        description = request.POST.get('description')
        skill_description = request.POST.get('skill_description')
        user = request.POST.get('user')
        # send to containers model
        post_data = {'header':header, 'skill': skill, 'price': price, 'description': description, 'skill_description':skill_description, 'user':user}
        #get info back from models container
        req = requests.post('http://models-api:8000/listing/create/', data=post_data)
        resp = req.json()

        produce=KafkaProducer(bootstrap_servers='kafka:9092')
        new_listing = {'id':resp['pk'], 'object':resp['result']['listing']}
        produce.send('new-listings-topic', json.dumps(new_listing).encode('utf-8'))

        #return
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle GET'
        }
    }

    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def DeleteListingView(request, listing_id):
    if (request.method == "POST"):
        req = urllib.request.Request('http://models-api:8000/listing/delete/' + listing_id + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle GET'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def AllListingsView(request):
    if(request.method == "GET"):
        req = urllib.request.Request('http://models-api:8000/listing/all/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle POST'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")


#----------------REVIEWS
@csrf_exempt
def CreateReviewView(request):
    if request.method == "POST":
        # get info
        header = request.POST.get('header')
        text = request.POST.get('text')
        user = request.POST.get('user')
        listing = request.POST.get('listing')
        rating = request.POST.get('rating')
        # send to containers model
        post_data = {'header':header, 'text': text, 'rating': rating, 'user': user, 'listing':listing}
        #get info back from models container
        req = requests.post('http://models-api:8000/review/create/', data=post_data)
        resp = req.json()
        #return
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle GET'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def DeleteReviewView(request, review_id):
    if request.method == "POST":
        req = requests.post('http://models-api:8000/review/delete/' + review_id + '/')
        resp = req.json()
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle GET'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def AllReviewsView(request, listing_id):
    # TODO: link with models layer
    if request.method == "GET":
        req = requests.get('http://models-api:8000/review/all/' + listing_id + '/')
        resp = req.json()
        return HttpResponse(json.dumps(resp), content_type="application/json")

    response = {
        'ok': 'False',
        'result':
        {
            'status': 'Cannot handle POST'
        }
    }
    return HttpResponse(json.dumps(response), content_type="application/json")


#----------------User Accounts
@csrf_exempt
def CreateAccount(request):
    if request.method == "POST":
        un = request.POST.get('username')
        pw = request.POST.get('password')
        em = request.POST.get('email')

        data = {"username":un, "password":pw, "email":em}

        response =requests.post('http://models-api:8000/createaccount/', data)
        resp = response.text
        return HttpResponse(resp, content_type="application/json")
    return HttpResponse(json.dumps({"status":"Does not support GET requests"}), content_type="application/json")

@csrf_exempt
def Login(request):
    if request.method == "POST":
        un = request.POST.get('username')
        pw = request.POST.get('password')

        post_data = {"username":un, "password":pw}
        #post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        #req = urllib.request.Request('http://models-api:8000/login/', data=post_encoded, method='POST')
        #get info back from models container
       # resp_json = urllib.request.urlopen(req).read().decode('utf-8')
       # resp = json.loads(resp_json)
        #return
       # return HttpResponse(json.dumps(resp), content_type="application/json")

        response =requests.post('http://models-api:8000/login/', post_data)
        resp = response.text
        return HttpResponse(resp, content_type="application/json")
    return HttpResponse(json.dumps({"status":"Does not support GET requests"}), content_type="application/json")



@csrf_exempt
def Logout(request):
    if request.method == "POST":
        token = request.POST.get('token')

        data = {"token": token}

        response = requests.post('http://models-api:8000/logout/', data)
        resp = response.text
        return HttpResponse(resp, content_type="application/json")
    return HttpResponse(json.dumps({"status":"Does not support GET requests"}), content_type="application/json")

@csrf_exempt
def Authenticate(request):
    if request.method == "POST":
        token = request.POST.get('token')

        data = {"token": token}

        response = requests.post('http://models-api:8000/authenticate/', data)
        resp = response.text
        return HttpResponse(resp, content_type="application/json")
    return HttpResponse(json.dumps({"status":"Does not support GET requests"}), content_type="application/json")


@csrf_exempt
def Search(request):
    if request.method == "POST":
        search_terms = request.POST.get('search_terms')
        search_query = {'query':{'query_string': {'query': search_terms}}, 'size':25}
        es = Elasticsearch(['es'])
        results = es.search(index='listing_index', body=search_query)
        results = results['hits']['hits']

        return HttpResponse(json.dumps(results), content_type="application/json")
    return HttpResponse(json.dumps({"status":"Does not support GET requests"}), content_type="application/json")

@csrf_exempt
def RecordClick(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        item_id = request.POST.get('item_id')

        produce=KafkaProducer(bootstrap_servers='kafka:9092')
        new_click = {'user_id':user_id, 'item_id':item_id}
        produce.send('record-click-topic', json.dumps(new_click).encode('utf-8'))

        return HttpResponse(json.dumps(new_click), content_type="application/json")
