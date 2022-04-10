from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^user/(?P<user_id>[0-9]+)/', views.UserView, name="UserView"),
    url(r'^user/create/', views.CreateUserView, name="CreateUserView"),
    url(r'^user/delete/(?P<user_id>[0-9]+)', views.DeleteUserView, name="DeleteUserView"),
    url(r'^user/all/', views.AllUsersView, name="AllUsersView"),
    url(r'^skill/(?P<skill_id>[0-9]+)/', views.SkillView, name="SkillView"),
    url(r'^skill/delete/(?P<skill_id>[0-9]+)/', views.DeleteSkillView, name="DeleteSkillView"),
    url(r'^skill/create/$', views.CreateSkillView, name="CreateSkillView"),
    url(r'^skill/all/', views.AllSkillsView, name="AllSkillsView"),
    url(r'^tag/(?P<tag_id>[0-9]+)/$', views.TagView, name="TagView"),
    url(r'^tag/delete/(?P<tag_id>[0-9]+)/$', views.DeleteTagView, name="DeleteTagView"),
    url(r'^tag/create/$', views.CreateTagView, name="CreateTagView"),
    url(r'^tag/all/', views.AllTagsView, name="AllTagsView"),
    url(r'^transaction/(?P<transaction_id>[0-9]+)/$', views.TransactionView, name="TransactionView"),
    url(r'^transaction/delete/(?P<transaction_id>[0-9]+)/$', views.DeleteTransactionView, name="DeleteTransactionView"),
    url(r'^transaction/create/$', views.CreateTransactionView, name="CreateTransactionView"),
    url(r'^transaction/all/', views.AllTransactionsView, name="AllTransactionsView"),
    url(r'^listing/(?P<listing_id>[0-9]+)/$', views.ListingView, name="ListingView"),
    url(r'^listing/delete/(?P<listing_id>[0-9]+)/$', views.DeleteListingView, name="DeleteListingView"),
    url(r'^listing/create/$', views.CreateListingView, name="CreateListingView"),
    url(r'^listing/all/', views.AllListingsView, name="AllListingsView"),
    url(r'^review/(?P<review_id>[0-9]+)/$', views.ReviewView, name="ReviewView"),
    url(r'^review/delete/(?P<review_id>[0-9]+)/$', views.DeleteReviewView, name="DeleteReviewView"),
    url(r'^review/create/$', views.CreateReviewView, name="CreateReviewView"),
    url(r'^review/all/(?P<listing_id>[0-9]+)', views.AllReviewView, name="AllReviewView"),
    url(r'^login/', views.Login, name="Login"),
    url(r'^logout/', views.Logout, name="Logout"),
    url(r'^createaccount', views.CreateAccount, name="CreateAccount"),
    url(r'^authenticate/', views.Authenticate, name="Authenticate")
]
