from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
    

class ChoiceForm(forms.Form):
    choice_text = forms.CharField(help_text="Enter text for choice!")
    def clean_choice_text(self):
        data = self.cleaned_data['choice_text']
        return data

class QuestionForm(forms.Form):
    edited_question_text = forms.CharField(help_text="Enter new text for question!")
    edited_pub_date = forms.DateField(help_text="Enter new publication date!")
    choices = []
    def clean_edited_question_text(self):
        data = self.cleaned_data['edited_question_text']
        
        # Remember to always return the cleaned data.
        return data
    def clean_edited_pub_date(self):
        data = self.cleaned_data['edited_pub_date']
        
        # Remember to always return the cleaned data.
        return data

class NewPollForm(forms.Form):
    new_question_text = forms.CharField(help_text="Enter text for question!")
    new_pub_date = forms.DateField(help_text="Enter new publication date (DD/MM/AAAA)!")
    def clean_edited_question_text(self):
        data = self.cleaned_data['edited_question_text']
        
        # Remember to always return the cleaned data.
        return data
    def clean_edited_pub_date(self):
        data = self.cleaned_data['edited_pub_date']
        
        # Remember to always return the cleaned data.
        return data


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username', 'first_name', 'last_name', 'email']