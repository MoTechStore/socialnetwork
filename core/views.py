from django.shortcuts import render,redirect
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import UserForm,UpdateUserForm,UpdateProfileForm,CreatePost,CreateComment
from django.http import HttpResponse 
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import User,Following,Follower,Post,Profile
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.hashers import make_password
import itertools



def index(request):
	return render(request, 'core/index.html')


def verifyInput(username,password):
	error = []
	if len(username) < 4:
		error.append('Username Should At Least Be 4 Character Long')
	elif len(password) < 8:
		error.append('Password Should At Least Be 8 Character Long')
	else:
		print('OK')

	return error
	


def registerUser(request):
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		hashed_password = make_password(password)

		error = verifyInput(username,password)

		if len(error) != 0:
			error = error[0]
			print(error)
			return render(request, 'core/registration_form.html', {'error': error})
		else:
			a = User(username=username, email=email, password=hashed_password)
			a.save()

			user = User.objects.get(username=username)
			user_id = User.objects.values_list('id', flat=True).filter( username = user)
			print('User id',user_id)
			Profile.objects.create(user_id=user_id)
			messages.success(request, 'Account Was Created Successfully')
			return redirect('register')
	else:
		return render(request, 'core/registration_form.html')



def index(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None and user.is_active:
			auth.login(request,user)
			return redirect('welcome')
		else:
			messages.info(request, 'Invalid Username or Password')
			return redirect('index')
	else:
		return render(request, 'core/index.html')



def dashboard(request):
	print(request.user)
	return render(request, 'core/dashboard.html')


def feed(request):
	try:
		post_all = Post.objects.all().order_by('created_at')
		print(post_all)
	except Exception as e:
		print(e)

	comment_form = CreateComment()
	username = request.user.username

	context = {
	'post_all': post_all,
	'comment_form': comment_form,
	'username': username,
	}

	return render(request, 'core/feed.html', context)



def followweb(request, username):
	if request.user.username != username:
		if request.method == 'POST':
			disciple = User.objects.get(username=request.user.username)
			leader = User.objects.get(username=username)
			
			leader.follower_set.create(follower_user = disciple)
			disciple.following_set.create(following_user = leader)
			url = reverse('profile', kwargs = {'username' : username})
			return redirect(url)




def unfollowweb(request, username):
	if request.method == 'POST':
		disciple = User.objects.get(username=request.user.username)
		leader = User.objects.get(username=username)
		
		leader.follower_set.get(follower_user = disciple).delete()
		disciple.following_set.get(following_user = leader).delete()
		url = reverse('profile', kwargs = {'username' : username})
		return redirect(url)


def postweb(request, username):
	if request.method == 'POST':
		post_form = CreatePost(request.POST, request.FILES)
		if post_form.is_valid():
			post_text = post_form.cleaned_data['post_text']
			post_picture = post_form.cleaned_data['post_picture']
			request.user.post_set.create(post_text=post_text, post_picture=post_picture)
			messages.success(request, f'Post Was Created Successfully')

	url = reverse('profile', kwargs={'username':username})
	return redirect(url)



def commentweb(request, username, post_id):
	if request.method == 'POST':
		comment_form = CreateComment(request.POST)

		if comment_form.is_valid():
			comment_text = comment_form.cleaned_data['comment_text']

			user =User.objects.get(username=username)
			post = user.post_set.get(pk=post_id)
			post.comment_set.create(user=request.user, comment_text=comment_text)
			messages.success(request, f'Comment Was Created Successfully')

	url = reverse('profile', kwargs={'username':username})
	return redirect(url)
	




def search(request):
    template='core/search.html'

    query = request.GET['q']
    print(query)
    data = query

    count = {}
    results = {}
    results['posts']= User.objects.none()
    queries = data.split()
    for query in queries:
        results['posts'] = results['posts'] | User.objects.filter(username__icontains=query)
        count['posts'] = results['posts'].count()


    count2 = {}
    queries2 = data.split()
    results2 = {}
    results2['posts'] = User.objects.none()
    queries2 = data.split()
    for query2 in queries:
        results2['posts'] = results2['posts'] | User.objects.filter(first_name__icontains=query2)
        count2['posts'] = results2['posts'].count()


    count3 = {}
    queries3 = data.split()
    results3 = {}
    results3['posts'] = User.objects.none()
    queries3 = data.split()
    for query3 in queries:
        results3['posts'] = results3['posts'] | User.objects.filter(last_name__icontains=query3)
        count3['posts'] = results3['posts'].count()
        

    files = itertools.chain(results['posts'],results2['posts'], results3['posts'])
    result = []
    for i in files:
        if i not in result:
            result.append(i)    

    paginate_by=2
    username = request.user.username
    print('current user',username)
    person = User.objects.get(username = username)
    print('person',person)
	
    context={ 'files':result }
    return render(request,template,context)




@login_required
def profile(request, username):
	
	if request.method == 'POST':
		u_form = UpdateUserForm(request.POST,instance=request.user)
		p_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
		

		if u_form.is_valid() and p_form.is_valid():

			u_form.save()
			p_form.save()
			

			messages.success(request,f'Your Profile has been updated!')
			url = reverse('profile', kwargs = {'username' : username})
			return redirect(url)

	else:
		if username == request.user.username:
			u_form = UpdateUserForm(instance=request.user)
			p_form = UpdateProfileForm(instance=request.user.profile)
			post_form = CreatePost()
			person = User.objects.get(username = username)

			context = {
					'u_form':u_form,
					'p_form':p_form,
					'post_form':post_form,
					'person':person,
					
			}	
		else:
			person = User.objects.get(username = username)
			already_a_follower=0
			for followers in person.follower_set.all():
				if (followers.follower_user ==  request.user.username):
					already_a_follower=1
					break;

			if already_a_follower==1:
				context = {
						'person':person,
						
							
					}
			else:
				context = {
						'person':person,
						'f':1,
						
					}
		comment_form = CreateComment()
		context.update({'comment_form':comment_form})

	return render(request, 'core/profile.html', context)




def welcome(request):
	url = reverse('profile', kwargs = {'username' : request.user.username})
	return redirect(url)
















































































