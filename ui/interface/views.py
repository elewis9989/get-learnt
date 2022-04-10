from django.shortcuts import render, redirect, reverse
import urllib.request
import urllib.parse
import json
import urllib
import requests
from django.http import HttpResponseRedirect, HttpResponse

from .forms import LoginForm, SignupForm, CreateListingForm, ReviewForm, SearchForm

# Create your views here.

searchForm = SearchForm()
#-------------- Index
def index(request):
    """The index functions renders the home page of the website.  Currently,
    it renders the same page for every user type.
    TODO: Add user levels to home page
    """
    loggedin = request.COOKIES.get('auth')
    if loggedin:
        return render(request, 'index.html', {'loggedIn':True, 'searchForm':searchForm})
    return render(request, 'index.html', {'loggedIn':False, 'searchForm':searchForm})


#-------------- Search
def search(request):

    loggedin = request.COOKIES.get('auth')

    if not loggedin:
        form = LoginForm()
        return render(request, 'login.html', {'form':form, 'loggedIn':loggedin, 'searchForm':searchForm})

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            search_terms = data['search_terms']
            post_data = {'search_terms':search_terms}
            req = requests.post('http://exp-api:8000/search/', data=post_data)
            response = req.json()
            if not response:
                return render(request, 'noListings.html', {'error':"something went wrong"})

            listingList = []
            for listing in response:
                listing = listing["_source"]["object"]
                listingList.append(listing)

            if listingList:
                return render(request, 'searchList.html', {"listingList":listingList, 'searchForm':searchForm})
            else:
                return render(request, 'noListings.html', {'searchForm':searchForm})


#-------------- Sign Up
def signup(request):
    """The create-profile function renders the sign up page of the website"""



    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            email = data['email']
            # TODO: link with experience layer to create a new user
            post_data = {'username':username, 'password':password, 'email':email}
            req = requests.post('http://exp-api:8000/createaccount', data=post_data)
            response = req.json()
            if not response or not response['status'] == 'success':
                return render(request, 'signup.html', {'error':response['status'], 'form':form, 'searchForm':searchForm})
            return render(request, 'index.html')

    else:
        form = SignupForm()
        loggedin = False
        return render(request, 'signup.html', {'form':form, 'loggedIn':loggedin, 'searchForm':searchForm})


#-------------- Log in
def login(request):
    """The login function renders the login page of the website. """
    loggedin = request.COOKIES.get('auth')

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            # TODO: Link with experience layer to check user and login

            """Get next destination to send user upon login"""
            next = reverse('index')

            """Attempt to log user in"""
            resp = login_exp_api(username, password)

            """Check to see if user is allowed to log in"""
            if not resp or not 'successful' in resp['status']:
                return render(request, 'login.html', {'error':resp['status'], 'form':form, 'searchForm':searchForm})

            """"Log User in"""
            authenticator = resp['token']
            user_id = resp['user_id']

            """Set cookie and direct to next page"""
            response = HttpResponseRedirect(next)
            response.set_cookie("auth", authenticator)
            response.set_cookie("user", username)
            response.set_cookie("id", user_id)


            return response

            #return render(request, 'thanks.html', {'username':username, 'password':password})

        else:
            return render(request, 'index.html', {'error':'Your Username or Password is not recognized', 'form':form, 'searchForm':searchForm})

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form, 'loggedIn':loggedin, 'searchForm':searchForm})

def login_exp_api(username, password):
    post_data = {'username':username, 'password':password}
    req = requests.post('http://exp-api:8000/login/', data=post_data)
    return req.json()

#-------------- Log Out
def logout(request):
    token = request.COOKIES.get('auth')
    post_data={'token':token}
    req = requests.post('http://exp-api:8000/logout/', data=post_data)
    response = HttpResponseRedirect(reverse('login'))
    response.delete_cookie('auth')
    response.delete_cookie('user')

    return response



def listings(request):


    #Get the list of skills from the experience layer
    listingList = getListings()

    #render the skills view page, if skills exist.  Otherwise, render the
    #no skills page

    if listingList:
        return render(request, 'listingList.html', {"listingList":listingList, 'searchForm':searchForm})
    else:
        return render(request, 'noListings.html', {'searchForm':searchForm})


def getListings():
    """Calls the experience layer to get skills to populate the skills list"""
    #TODO Add experience layer calling
    req = urllib.request.Request("http://exp-api:8000/listing/all/")
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)['result']['listings']

    return resp

#    retDict = [{"title":"Django", "description": "A web development framework used \
#    to build many applications.  I'm ok at teaching it. If i make the description arbitrarily longer, it looks cool on the page", "user":"Wyatt", "tags":["Tech", "web"]},
#    {"title":"Mario Kart", "description":"A fun racing game that keith likes to think he's good at",
#    "User":"keith", "tags":["Game", "tech"]},
#    {"title":"Another Skill", "description": "another skill to learn", "user":"anon", "tags":["yuh"]},
#    {"title":"Another Skill2", "description": "another skill to learn", "user":"anon", "tags":["yuh"]},
#    {"title":"Another Skill3", "description": "another skill to learn", "user":"anon", "tags":["yuh"]}
#    ]
    return retDict

def detail(request, skill_id):
    """Displays details on a skill linked to by the listings page"""
    user_id = request.COOKIES.get('id')
    listing = getListing(skill_id)
    reviews = getReviews(skill_id)
    recommendations = listing['recommendations']
    recs = []
    if recommendations == "none":
        recs=""
    else:
        rec_ids = recommendations.split(",")
        for rec in rec_ids:
            recs.append(getListing(rec))



    form = ReviewForm()
    RecordClick(user_id, skill_id)
    return render(request, 'item-detail.html',{"listing":listing, "user":user_id, "reviews":reviews, "form":form, 'searchForm':searchForm, 'recs':recs})


def getListing(id):
    """Gets individual listing from experience layer"""
    req = urllib.request.Request("http://exp-api:8000/listing/" + id + "/")
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)['result']
    return resp

def getReviews(id):
    req = requests.get("http://exp-api:8000/review/all/" + id + "/")
    resp = req.json()
    return resp

def CreateReview(request, user_id, listing_id):
    if request.method == 'POST':

        form = ReviewForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            header = data['header']
            text = data['text']
            rating = data['rating']
            user = user_id
            listing = listing_id
            post_data = {'header':header, 'text':text, 'rating':rating, 'user':user, 'listing':listing}
            req = requests.post('http://exp-api:8000/request/create/', data=post_data)
            return redirect('/detail/' + listing + '/')

    return redirect('/listings/')

def createListings(request):

    auth = request.COOKIES.get('auth')

    # If the authenticator cookie wasn't set...
    if not auth:
      # Handle user not logged in while trying to create a listing
      return HttpResponseRedirect(reverse("login"))


    if request.method == 'POST':

        form = CreateListingForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            header = data['header']
            user = request.COOKIES.get('id')
            skill = data['skill']
            price = data['price']
            description = data['description']
            skill_description = data['skill_description']
            post_data = {'header':header, 'skill':skill, 'price':price, 'description':description, 'skill_description':skill_description, 'user':user}
            req = requests.post('http://exp-api:8000/listing/create/', data=post_data)
            return render(request, 'created-listing.html', {'searchForm':searchForm, 'header':header, 'skill':skill, 'price':price, 'description':description, 'skill_description':skill_description})

    form = CreateListingForm()
    return render(request, 'create-listing.html', {'form':form, 'loggedIn':True, 'searchForm':searchForm})

def RecordClick(user_id, item_id):
    post_data = {'user_id':user_id, 'item_id':item_id}
    req = requests.post('http://exp-api:8000/recordclick/', post_data)
