from django.contrib.auth.models import User
from django import forms
from .models import Profile,Post,Comment


# Form for registering new user
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	email = forms.EmailField(max_length=254, help_text='Required field')
	class Meta:
		model = User
		fields = ['username','email','password']


# Form for updating user email
class UpdateUserForm(forms.ModelForm):
	email = forms.EmailField(max_length=254, help_text='Required field')

	class Meta:
		model = User
		fields = ['email']


# Form for updating profile
class UpdateProfileForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['status_info','profile_photo']


# Form for creating a post
class CreatePost(forms.ModelForm):
	
	class Meta:
		model = Post
		fields = ['post_text','post_picture']


# Form for creating a comment
class CreateComment(forms.ModelForm):
	
	class Meta:
		model = Comment
		fields = ['comment_text']
