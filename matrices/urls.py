from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from matrices.core import views as core_views


urlpatterns = [
	url(r'^matrices/', include('matrices.core.urls', namespace="matrices")),
	
	url(r'^$', core_views.home, name='home'),
	url(r'^signup/$', core_views.signup, name='signup'),
	url(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', core_views.activate, name='activate'),

    url(r'^login/$', 
    				auth_views.login, {'template_name': 'user/login.html'}, 
    					name='login'),
	url(r'^logout/$', 
					auth_views.logout, {'next_page': 'login'}, 
						name='logout'),

    url(r'^reset/$', 
    				auth_views.PasswordResetView.as_view(
            			template_name='user/password_reset.html',
				        email_template_name='user/password_reset_email.html',
				        subject_template_name='user/password_reset_subject.txt'), 
			            	name='password_reset'),
    url(r'^reset/done/$', 
    				auth_views.PasswordResetDoneView.as_view(
    					template_name='user/password_reset_done.html'), 
    					name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
			        auth_views.PasswordResetConfirmView.as_view(
			        	template_name='user/password_reset_confirm.html'),
			        		name='password_reset_confirm'),
    url(r'^reset/complete/$',
			        auth_views.PasswordResetCompleteView.as_view(
			        	template_name='user/password_reset_complete.html'),
				        	name='password_reset_complete'),
    url(r'^settings/password/$', 
    				auth_views.PasswordChangeView.as_view(
    					template_name='user/password_change.html'),
					        name='password_change'),
    url(r'^settings/password/done/$', 
    				auth_views.PasswordChangeDoneView.as_view(
    					template_name='user/password_change_done.html'),
					        name='password_change_done'),
					        
] 
