from django.conf.urls import patterns, url
from blogapp import views

urlpatterns = patterns(
	'',
	url(r'^register/$',views.register, name='register'),
	url(r'^verify-email/$',views.verifyemail, name='verify-email'),
	url(r'^verify-email-confirm/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<key>[a-z]+)/$',views.email_verify_confirm, name='verify-email-confirm'),
	url(r'^login/$',views.login, name='login'),
	url(r'^forgetpass/$',views.forgetpassword, name='forgetpass'),
	url(r'^verify-forgetpass/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<key>[A-Za-z0-9]+)/$',views.verifyforgetpassword, name='verify-forgetpass'),
	url(r'^profile/$',views.profile ,name='profile'),
	url(r'^editprofile/(?P<pk>[0-9]+)/$',views.editprofile ,name='editprofile'),
	url(r'^image/$',views.image ,name='image'),
	url(r'^changepassword/$', views.changepassword, name='changepassword'),	
	url(r'^addblog/$',views.addblog ,name='addblog'),
	url(r'^myblogs/$',views.myblogs ,name='myblogs'),
	url(r'^categoryblog/$',views.categoryblog ,name='categoryblog'),
	url(r'^blogs/$',views.blogs ,name='blogs'),
	url(r'^viewblog/(?P<pk>[0-9]+)/$',views.viewblog ,name='viewblog'),
	url(r'^editblog/(?P<pk>[0-9]+)/$',views.editblog ,name='editblog'),	
	url(r'^deleteblog/(?P<pk>[0-9]+)/$',views.deleteblog ,name='deleteblog'),
	url(r'^comment/(?P<pk>[0-9]+)/$',views.comment ,name='comment'),	
	url(r'^rating/(?P<pk>[0-9]+)/$',views.rating ,name='rating'),
	url(r'^logout/$', views.logout, name='logout')

)
# urlpatterns = format_suffix_pattern(urlpatterns)+