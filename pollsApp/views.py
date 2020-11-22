from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from .models import Choice, Question
from .form import QuestionForm
from .form import SignUpForm
from .form import UserUpdateForm
from .form import NewPollForm
from .form import NewChoiceForm

class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '../accounts/login/'
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')

class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '../../accounts/login/'
    model = Question
    template_name = 'polls/details.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(LoginRequiredMixin, generic.DetailView):
    login_url = '../../../accounts/login/'
    model = Question
    template_name = 'polls/results.html'

class PollsByUserListView(LoginRequiredMixin, generic.ListView):
    login_url = '../../../accounts/login/'
    model = Question
    template_name ='polls/polls_list_creator_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Question.objects.filter(creator=self.request.user).order_by('-pub_date')

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def edit_question_view(request, question_id):
    question_instance = get_object_or_404(Question, pk=question_id)

    if (question_instance.creator != request.user):
        raise ValueError('HEY, BRO!! You do not have permission to edit this question!')
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = QuestionForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            question_instance.question_text = form.cleaned_data['edited_question_text']
            question_instance.pub_date = form.cleaned_data['edited_pub_date']
            question_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('polls:myPolls') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_question_text_edited = question_instance.question_text
        proposed_pub_date_edited = question_instance.pub_date
        form = QuestionForm(initial={'edited_question_text': proposed_question_text_edited, 'edited_pub_date': proposed_pub_date_edited})

    context = {
        'form': form,
        'question_instance': question_instance,
    }

    return render(request, 'polls/edit_question.html', context)

def new_poll(request):
    question_instance = Question()

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = NewPollForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            question_instance.question_text = form.cleaned_data['new_question_text']
            question_instance.pub_date = form.cleaned_data['new_pub_date']
            question_instance.creator = request.user
            question_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/polls/' + str(question_instance.pk) + '/newchoice')
    else:
        proposed_question_text_edited = question_instance.question_text
        proposed_pub_date_edited = question_instance.pub_date
        form = NewPollForm(initial={'new_question_text': proposed_question_text_edited, 'new_pub_date': proposed_pub_date_edited})

    context = {
        'form': form,
        'question_instance': question_instance,
    }


    return render(request, 'polls/create_poll.html', context)

def new_choice(request, question_id):
    choice_instance = Choice()
    question = get_object_or_404(Question, pk=question_id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = NewChoiceForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            choice_instance.choice_text = form.cleaned_data['new_choice_text']
            choice_instance.question = question
            choice_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/polls/'+str(question_id)+'/newchoice')
    else:
        proposed_choice_text = choice_instance.choice_text
        form = NewChoiceForm(initial={'new_choice_text': proposed_choice_text})

    context = {
        'form': form,
        'choice_instance': choice_instance,
        'question_text': question.question_text
    }
    return render(request, 'polls/create_choice.html', context)

def edit_choice(request, choice_id):
    choice_instance = get_object_or_404(Choice, pk=choice_id)
    question = get_object_or_404(Question, pk=choice_instance.question.pk)
    if (question.creator != request.user):
        raise ValueError('HEY, BRO!! You do not have permission to edit this choice!')

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = NewChoiceForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            choice_instance.choice_text = form.cleaned_data['new_choice_text']
            choice_instance.question = question
            choice_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/polls/'+str(question_id)+'/edit')
    else:
        proposed_choice_text = choice_instance.choice_text
        form = NewChoiceForm(initial={'new_choice_text': proposed_choice_text})

    context = {
        'form': form,
        'choice_instance': choice_instance,
        'question_text': question.question_text
    }
    return render(request, 'polls/edit_choice.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('polls:index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('polls:index')
    else:
        form = UserUpdateForm(instance=request.user)

    context={'form': form}
    return render(request, 'registration/edit_profile.html', context)
    