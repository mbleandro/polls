from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # /polls/
    path('', views.IndexView.as_view(), name='index'),
    # /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # /polls/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # /polls/myquestions/
    path('myquestions/', views.PollsByUserListView.as_view(), name='myPolls'),
    # /polls/5/edit
    path('<int:question_id>/edit/', views.edit_question_view, name='edit-question'),
    # /polls/newpoll
    path('newpoll/', views.new_poll, name = 'newPoll'),
    # /polls/singup
    path('signup/', views.signup, name='signup'),
    # /polls/myprofile
    path('myprofile/', views.profile, name='profile'),
]