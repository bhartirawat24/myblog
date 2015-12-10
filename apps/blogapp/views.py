from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User,check_password
from blogapp.models import Profile, BlogTable, Category,Rating,Comment
from django.core.mail import send_mail
from django.contrib.auth import login as auth_login , logout as auth_logout, authenticate
from django.core.context_processors import csrf
import random
import string



def csrf_rejected(request, reason=''):
	ctx = {'reason':reason}
	return render_to_response('blog/csrf_rejected.html',ctx)

	
def register(request):
	n = 32
	key = "".join(random.choice(string.lowercase) for i in range(n))
	param_dict = {
		'message': ''
	}
	if request.method == 'GET':
		return render_to_response('blog/register.html',context_instance=RequestContext(request))
	if request.method == 'POST':
		
		first_name = request.POST.get('fname')
		last_name = request.POST.get('lname')
		email = request.POST.get('email')
		password = request.POST.get('pass')
		cpassword = request.POST.get('cpass')
		contact = request.POST.get('phn')
		gender = request.POST.get('gen')

		user=User.objects.filter(email=email)
		if user:
			return HttpResponse("user is already register with this email.Try another")
		profile = Profile.objects.filter(contact=contact).exists()
		if profile:
			return HttpResponse("user is with this contact no already registered.Try another")

		if not request.POST.get('fname'):
			param_dict['message'] = 'Please specify all mandatory fields'
			return render_to_response('blog/register.html', param_dict, context_instance=RequestContext(request))
		if not request.POST.get('lname'):
			param_dict['message'] = 'Please specify all mandatory fields'
			return render_to_response('blog/register.html', param_dict, context_instance=RequestContext(request))
		if not request.POST.get('email'):
			param_dict['message'] = 'Please specify all mandatory fields'
			return render_to_response('blog/register.html', param_dict, context_instance=RequestContext(request))
		if not request.POST.get('pass'):
			param_dict['message'] = 'Please specify all mandatory fields'
			return render_to_response('blog/register.html', param_dict, context_instance=RequestContext(request))
		if not request.POST.get('cpass'):
			param_dict['message'] = 'Please specify all mandatory fields'
			return render_to_response('blog/register.html', param_dict, context_instance=RequestContext(request))
		if not request.POST.get('phn'):
			param_dict['message'] = 'Please specify all mandatory fields'
			return render_to_response('blog/register.html', param_dict, context_instance=RequestContext(request))
		# if not request.POST.get('gender'):
		# 	param_dict['message'] = '1'
		# 	return render_to_response('blog/register.html', param_dict, context_instance=RequestContext(request))
		if password != cpassword:
			return render_to_response('blog/register.html', param_dict, context_instance=RequestContext(request)) 
		
		user = User.objects.create(first_name=first_name,last_name=last_name,email=email,username=email, is_active=0)
		user.set_password(password)
		user.save()
		profile = Profile.objects.create(user=user,contact=contact,activationkey=key,gender=gender)
		profile.save()
		url = 'http://localhost:8000/'+'verify-email-confirm'+'/'+email+'/'+key+'/'
		html_cont = 'Verify Your email by clicking at the link '+ url
		send_mail('Blog User Activation', html_cont, 'rawat92428@gmail.com', [email], fail_silently=False)

		return HttpResponse('congratulations to u...successfully registered')
	return render_to_response('blog/register.html', param_dict, context_instance=RequestContext(request)) 

def verifyemail(request):
	c = string.uppercase+string.lowercase+string.digits
	key = ''.join(random.choice(c) for i in range(32))
	if request.method == 'GET':
		return render_to_response('blog/verifyemail.html',context_instance=RequestContext(request))
	if request.method == 'POST':
		email = request.POST.get('email')
		url = 'http://localhost:8000/'+'verify-email'+'/'+email+'/'+key+'/'
		link_content = 'verify your email by clicking this link'+ url
		send_mail('verify your email', link_content ,'rawat92428@gmail.com', [email],fail_silently=False)
		return HttpResponse('congratulations to u...successfully email sent')
	return HttpResponse('error')


def email_verify_confirm(request,email,key):
	if request.method == 'GET':
		user_objects = User.objects.filter(email=email)
		profile = Profile.objects.get(user=user_objects[0])
		if profile.activationkey == key:
			user = user_objects[0]
			if user.is_active == True:
				return HttpResponse('user is already registered')
			else:
				user.is_active = True
				user.save()
				#login(request, user)
		return redirect('login')

def login(request):
	if request.method == 'GET':
		return render_to_response('blog/login.html',context_instance=RequestContext(request))
	if request.method == 'POST':
		
		email = request.POST.get('email')
		password = request.POST.get('pass')
		forgetpass = request.POST.get('fpass')
		user = authenticate(username=email, password=password)
		print user
		if user is not None:
			if user.is_active:
				auth_login(request, user)
				return redirect('profile')
		# if check_password(password,password):	
		# 	return HttpResponse("successfully logged in")
		elif forgetpass is not None:
			return redirect('forgetpass')
		return HttpResponse("error")

def forgetpassword(request):	
	c = string.uppercase+string.lowercase+string.digits
	key = ''.join(random.choice(c) for i in range(32))

	if request.method == "GET":
		# import pdb; pdb.set_trace()
		return render_to_response('blog/forgetpassword.html',context_instance=RequestContext(request))
	if request.method == "POST":
		email = request.POST.get('email')
		user = User.objects.get(email=email)
		profile = Profile.objects.get(user=user)
		profile.activationkey=key
		profile.save()

		url = 'http://localhost:8000/'+'verify-forgetpass/'+email+'/'+key+'/'
		html_cont = 'Reset Your password by clicking at the link '+ url
		send_mail('Blog User Activation', html_cont, 'rawat92428@gmail.com', [email], fail_silently=False)
		return HttpResponse("Succesfully reset password link in sent")


def verifyforgetpassword(request,email,key):
	
	if request.method == "GET":
		user = User.objects.get(email=email)
		profileu=Profile.objects.get(user=user)

		d={'user':user, 'profile':profileu}
		if profileu.activationkey == key:
			if user.is_active == True:
				return render_to_response('blog/resetpass.html',d,context_instance=RequestContext(request))
			else: 
				return HttpResponse("First Verify Your Email")
		

	if request.method == "POST":		
		newpass = request.POST.get('pass')
		confirm_password = request.POST.get('cpass')
		user = User.objects.get(email=email)
		password=user.password
		if password != newpass and password !=confirm_password:		
			if newpass == confirm_password:
				user.set_password(newpass)
				user.save()
		else:
			return HttpResponse("try again")

		user = authenticate(username=email, password=newpass)
		if user is not None:
			if user.is_active:
				auth_login(request, user)
				return redirect('profile')

def profile(request):
	if request.method == 'GET':
		d ={'user':''}		
		
		if request.user.is_authenticated():
			profile = Profile.objects.get(user=request.user)
			blog = BlogTable.objects.all()
			
			d={'user':request.user,'profile':profile,'blogs':blog}

		if not request.user.is_authenticated():
			return redirect(login)

		return render_to_response('blog/profile.html',d, context_instance=RequestContext(request))

def editprofile(request,pk):
	if request.method == 'GET':
		if request.user.is_authenticated(): 
			if request.user is not None and request.user.is_active:
				user = User.objects.get(email=request.user,id=pk)
				profile=Profile.objects.get(user=user)
				d = {'profile':profile}
				return render_to_response('blog/editprofile.html',d,context_instance=RequestContext(request))
	if request.method == 'POST':
		first_name = request.POST.get('fname')
		last_name = request.POST.get('lname')
		password = request.POST.get('pass')
		contact = request.POST.get('phn')
		user = User.objects.get(id=pk)
		user.first_name=first_name
		user.last_name=last_name
		user.set_password(password)
		user.save()
		
		profile1=Profile.objects.filter(user=user)
		profile1=profile1[0]
		if profile1.contact == contact:
			return HttpResponse("this no is already registered")
		profile1.contact=contact
		profile1.save()
		return redirect('profile')
	else:
		return render_to_response('blog/login.html',context_instance=RequestContext(request))


def image(request):	
	
	if request.method == "GET":
		if request.user.is_authenticated(): 
			if request.user is not None and request.user.is_active:
				return render_to_response('blog/image.html', context_instance=RequestContext(request))
	if request.method == "POST":
		# import pdb; pdb.set_trace()
		image = request.FILES.get('image')
		user = User.objects.get(email=request.user)
		profile = Profile.objects.get(user=user)
		profile.image = image
		profile.save()
		user = User.objects.get(email=request.user)
		profile=Profile.objects.get(user=user)
		d = {'profile':profile}
		return render_to_response('blog/editprofile.html',d,context_instance=RequestContext(request))
	return HttpResponse("first login")
		

def changepassword(request):
	if request.method == 'GET':
		if request.user.is_authenticated():
			return render_to_response('blog/changepassword.html',context_instance=RequestContext(request))

	if request.method == 'POST':
		old_password = request.POST.get('oldpass')
		new_password = request.POST.get('newpass')
		confirm_password = request.POST.get('confirmpass')
		user = User.objects.get(email=request.user)
		password=user.password
		p = user.check_password(old_password)
		if p:
			if new_password == confirm_password:
				user.set_password(new_password)
				user.save()		
				return redirect('profile')	
		else:
			return HttpResponse('error try again')
	return HttpResponse('error ')	


def addblog(request):
	if request.method == 'GET':
		if request.user.is_authenticated():
			d= {'category':''}
			category1 = Category.objects.all()
			d ={"categories":category1}
			return render_to_response("blog/addblog.html",d,context_instance=RequestContext(request))
	if  request.method == 'POST':
		title = request.POST.get('title')
		description = request.POST.get('desc')
		category = request.POST.get('blogcat')
		user = User.objects.get(email=request.user)
		blog = BlogTable.objects.create(user=user,title=title,description=description,status=0,category_id=category,is_publish=0)
		blog.save()
		blogid=blog.id
		blog1=BlogTable.objects.get(user=user,id=blogid)
		d={'title':title,'blogs':blog1}
		return redirect('profile')
	else:
		return HttpResponse("error")

def myblogs(request):
	if request.method == "GET":
		if request.user.is_authenticated():
			if request.user is not None and request.user.is_active:
				user=User.objects.get(email=request.user)
				blog = BlogTable.objects.filter(user=user)
				# rate_obj= Rating.objects.get(user=user,blog=blog)
				d={'blogs':blog}
		return render_to_response('blog/myblogs.html',d,context_instance=RequestContext(request))

def categoryblog(request):
	if request.method == "GET":
		if request.user.is_authenticated():
			if request.user is not None and request.user.is_active:
				category = Category.objects.all()
				d = {'categories':category}
			return render_to_response('blog/categoryblog.html',d,context_instance=RequestContext(request))
	if request.method == "POST":
		d={'blogs':''}
		category = request.POST.get('category')
		user = User.objects.get(email=request.user)
		blog = BlogTable.objects.filter(category=category)
		d={'blogs':blog}
		return render_to_response('blog/categorydetail.html',d,context_instance=RequestContext(request))

def blogs(request):
	if request.method == "GET":
		if request.user.is_authenticated():
			if request.user is not None and request.user.is_active:
				blogs = BlogTable.objects.all()
				d={'blogs':blogs}
		return render_to_response('blog/blogs.html',d,context_instance=RequestContext(request)) 

def viewblog(request,pk):
	if request.method == "GET":
		if request.user.is_authenticated():
			if request.user is not None and request.user.is_active:
				category1 = Category.objects.all()
				user = User.objects.get(email=request.user)
				blogs = BlogTable.objects.get(user=user,id=pk)
				d={'user':user,'blogs':blogs,'categories':category1}
				return render_to_response('blog/viewblog.html',d,context_instance=RequestContext(request))

def editblog(request,pk):
	if request.method == 'GET':
		if request.user.is_authenticated():
			category1 = Category.objects.all()
			user = User.objects.get(email=request.user)
			blogs = BlogTable.objects.get(user=user,id=pk)
			d={'user':user,'blogs':blogs,'categories':category1}
			return render_to_response('blog/editblog.html',d,context_instance=RequestContext(request))
		
	if request.method == 'POST':
		title=request.POST.get('title')
		desc = request.POST.get('desc')
		category = request.POST.get('blog')
		user = User.objects.get(email=request.user)
		blog = BlogTable.objects.get(user=user,id=pk)
		blog.title=title
		blog.description=desc
		blog.category_id=category
		blog.status=0
		blog.is_publish=0
		blog.save()
		return render_to_response('blog/addblog.html',context_instance=RequestContext(request))


def deleteblog(request,pk):
	if request.user.is_authenticated():
		if request.user is not None and request.user.is_active:
			user = User.objects.get(email=request.user)
			blog1 = BlogTable.objects.get(user=user,id=pk)
			blog1.delete()
		return redirect('profile')
	if not request.user.is_authenticated():
		return HttpResponse("Login")

def comment(request,pk):
	if request.method == 'GET':
		if request.user.is_authenticated():
			if request.user is not None and request.user.is_active:
				user = User.objects.get(email=request.user)
				blogs = BlogTable.objects.get(user=user,id=pk)
				d={'blog':blogs}
				return render_to_response('blog/comment.html',d,context_instance=RequestContext(request))
	if request.method == 'POST':
		description = request.POST.get('description')
		user = User.objects.get(email=request.user)
		blogs = BlogTable.objects.get(user=user,id=pk)
		comm_obj=Comment.objects.filter(blog=blogs,user=user).exists()
		if comm_obj:
			comm_obj.description = description
			comm_obj.save()
		else:
			comm_obj1 = Comment.objects.create(blog=blogs,user=user,description=description)
			comm_obj1.save()
		return HttpResponse("thanks to Comment us")

	return HttpResponse("error")

def rating(request,pk):
	if request.method == 'GET':
		if request.user.is_authenticated():
			if request.user is not None and request.user.is_active:
				user = User.objects.get(email=request.user)
				blogs = BlogTable.objects.get(user=user,id=pk)
				d={'blog':blogs}
				return render_to_response('blog/rate.html', d,context_instance=RequestContext(request))
	if request.method == 'POST':
		rating = request.POST.get('rate')
		user = User.objects.get(email=request.user)
		blogs = BlogTable.objects.get(user=user,id=pk)
		rate_obj=Rating.objects.filter(blog=blogs,user=user).exists()
		if rate_obj:
			rate_obj.rating = rating
			rate_obj.save()
		else:
			rate_obj1 = Rating.objects.create(blog=blogs,user=user,rating=rating)
			rate_obj1.save()
		return HttpResponse("thanks to rate us")
	return HttpResponse('im rating view')


def logout(request):
	if request.method == 'GET':
		if request.user.is_authenticated():
			auth_logout(request)
		return redirect('login')