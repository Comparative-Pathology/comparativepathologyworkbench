from django.conf.urls import url, include

from django.contrib.auth import views as auth_views

from django.urls import path

from matrices import views as matrices_views

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'benches', matrices_views.MatrixViewSet)
router.register(r'cells', matrices_views.CellViewSet)
router.register(r'images', matrices_views.ImageViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

	url(r'^$', matrices_views.home, name='home'),

	url(r'^signup/$', matrices_views.signup, name='signup'),
	url(r'^account_activation_sent/$', matrices_views.account_activation_sent, name='account_activation_sent'),
	path('activate/<str:uidb64>/<str:token>', matrices_views.activate, name='activate'),
	
    url(r'^login/$', auth_views.LoginView.as_view(template_name="user/login.html"), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="user/login.html"), name='logout'),	       
    
    url(r'^reset/$', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html', email_template_name='user/password_reset_email.html', subject_template_name='user/password_reset_subject.txt'), name='password_reset'),
    url(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,65})/$', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/complete/$', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='user/password_change.html'), name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'), name='password_change_done'),
					        
	url(r'^index/$', matrices_views.index_matrix, name='index'),
	url(r'^home/$', matrices_views.home, name='home'),
	url(r'^about/$', matrices_views.about, name='about'),
	url(r'^people/$', matrices_views.people, name='people'),
	url(r'^howto/$', matrices_views.howto, name='howto'),
	#url(r'^mailer/$', matrices_views.mailer, name='mailer'),

	url(r'^list_matrix/$', matrices_views.index_matrix, name='list_matrix'),

	url(r'^maintenance/$', matrices_views.maintenance, name='maintenance'),
	url(r'^authorisation/$', matrices_views.authorisation, name='authorisation'),

	url(r'^list_imaging_hosts/$', matrices_views.list_imaging_hosts, name='list_imaging_hosts'),
	url(r'^list_image_cart/$', matrices_views.list_image_cart, name='list_image_cart'),

    url(r'^ajax/overwrite_cell_leave/$', matrices_views.overwrite_cell_leave, name='overwrite_cell_leave'),
    url(r'^ajax/overwrite_cell/$', matrices_views.overwrite_cell, name='overwrite_cell'),
    url(r'^ajax/swap_cells/$', matrices_views.swap_cells, name='swap_cells'),
    url(r'^ajax/import_image/$', matrices_views.import_image, name='import_image'),
    url(r'^ajax/swap_columns/$', matrices_views.swap_columns, name='swap_columns'),
    url(r'^ajax/swap_rows/$', matrices_views.swap_rows, name='swap_rows'),
    url(r'^ajax/shuffle_columns/$', matrices_views.shuffle_columns, name='shuffle_columns'),
    url(r'^ajax/shuffle_rows/$', matrices_views.shuffle_rows, name='shuffle_rows'),

	url(r'^show_ebi_server/(?P<server_id>[0-9]+)/$', matrices_views.show_ebi_server, name='ebi_show_ebi_server'),
	path('show_ebi_widget/<int:server_id>/<slug:experiment_id>/', matrices_views.show_ebi_widget, name='ebi_show_ebi_widget'),

	url(r'^show_server/(?P<server_id>[0-9]+)/$', matrices_views.show_imaging_server, name='webgallery_show_imaging_server'),
	url(r'^show_group/(?P<server_id>[0-9]+)/(?P<group_id>[0-9]+)/$', matrices_views.show_group, name='webgallery_show_group'),
	url(r'^show_project/(?P<server_id>[0-9]+)/(?P<project_id>[0-9]+)/$', matrices_views.show_project, name='webgallery_show_project'),
	url(r'^show_dataset/(?P<server_id>[0-9]+)/(?P<dataset_id>[0-9]+)/$', matrices_views.show_dataset, name='webgallery_show_dataset'),
	url(r'^show_image/(?P<server_id>[0-9]+)/(?P<image_id>[0-9]+)/$', matrices_views.show_image, name='webgallery_show_image'),

	url(r'^show_wordpress/(?P<server_id>[0-9]+)/(?P<page_id>[0-9]+)/$', matrices_views.show_wordpress, name='webgallery_show_wordpress'),
	url(r'^show_wordpress_image/(?P<server_id>[0-9]+)/(?P<image_id>[0-9]+)/$', matrices_views.show_wordpress_image, name='webgallery_show_wordpress_image'),

	url(r'^add_image/(?P<server_id>[0-9]+)/(?P<image_id>[0-9]+)/(?P<roi_id>[0-9]+)/$', matrices_views.add_image, name='webgallery_add_image'),
	url(r'^delete_image/(?P<image_id>[0-9]+)/$', matrices_views.delete_image, name='webgallery_delete_image'),

	url(r'^detail_user/(?P<user_id>[0-9]+)/$', matrices_views.view_user, name='detail_user'), 
	url(r'^edit_user/(?P<user_id>[0-9]+)/$', matrices_views.edit_user, name='edit_user'),
	url(r'^delete_user/(?P<user_id>[0-9]+)/$', matrices_views.delete_user, name='delete_user'),

	url(r'^detail_server/(?P<server_id>[0-9]+)/$', matrices_views.view_server, name='detail_server'), 
	url(r'^new_server/$', matrices_views.new_server, name='new_server'),
	url(r'^edit_server/(?P<server_id>[0-9]+)/$', matrices_views.edit_server, name='edit_server'),
	url(r'^delete_server/(?P<server_id>[0-9]+)/$', matrices_views.delete_server, name='delete_server'),

	url(r'^detail_blog_command/(?P<blog_id>[0-9]+)/$', matrices_views.view_blog_command, name='detail_blog_command'), 
	url(r'^new_blog_command/$', matrices_views.new_blog_command, name='new_blog_command'),
	url(r'^edit_blog_command/(?P<blog_id>[0-9]+)/$', matrices_views.edit_blog_command, name='edit_blog_command'),
	url(r'^delete_blog_command/(?P<blog_id>[0-9]+)/$', matrices_views.delete_blog_command, name='delete_blog_command'),

	url(r'^detail_blog_credential/(?P<credential_id>[0-9]+)/$', matrices_views.view_blog_credential, name='detail_blog_credential'), 
	url(r'^new_blog_credential/$', matrices_views.new_blog_credential, name='new_blog_credential'),
	url(r'^edit_blog_credential/(?P<credential_id>[0-9]+)/$', matrices_views.edit_blog_credential, name='edit_blog_credential'),
	url(r'^delete_blog_credential/(?P<credential_id>[0-9]+)/$', matrices_views.delete_blog_credential, name='delete_blog_credential'),

	url(r'^detail_command/(?P<command_id>[0-9]+)/$', matrices_views.view_command, name='detail_command'), 
	url(r'^new_command/$', matrices_views.new_command, name='new_command'),
	url(r'^edit_command/(?P<command_id>[0-9]+)/$', matrices_views.edit_command, name='edit_command'),
	url(r'^delete_command/(?P<command_id>[0-9]+)/$', matrices_views.delete_command, name='delete_command'),

	url(r'^detail_protocol/(?P<protocol_id>[0-9]+)/$', matrices_views.view_protocol, name='detail_protocol'), 
	url(r'^new_protocol/$', matrices_views.new_protocol, name='new_protocol'),
	url(r'^edit_protocol/(?P<protocol_id>[0-9]+)/$', matrices_views.edit_protocol, name='edit_protocol'),
	url(r'^delete_protocol/(?P<protocol_id>[0-9]+)/$', matrices_views.delete_protocol, name='delete_protocol'),

	url(r'^detail_type/(?P<type_id>[0-9]+)/$', matrices_views.view_type, name='detail_type'),	 # ex: /maintenance/new_type
	url(r'^new_type/$', matrices_views.new_type, name='new_type'),
	url(r'^edit_type/(?P<type_id>[0-9]+)/$', matrices_views.edit_type, name='edit_type'),
	url(r'^delete_type/(?P<type_id>[0-9]+)/$', matrices_views.delete_type, name='delete_type'),

	url(r'^detail_authority/(?P<authority_id>[0-9]+)/$', matrices_views.view_authority, name='detail_authority'),
	url(r'^new_authority/$', matrices_views.new_authority, name='new_authority'),
	url(r'^edit_authority/(?P<authority_id>[0-9]+)/$', matrices_views.edit_authority, name='edit_authority'),
	url(r'^delete_authority/(?P<authority_id>[0-9]+)/$', matrices_views.delete_authority, name='delete_authority'),

	url(r'^(?P<matrix_id>[0-9]+)/detail_matrix_blog/$', matrices_views.view_matrix_blog, name='detail_matrix_blog'), 
	url(r'^(?P<matrix_id>[0-9]+)/view_cell_blog/(?P<cell_id>[0-9]+)/$', matrices_views.view_cell_blog, name='view_cell_blog'),

	url(r'^(?P<matrix_id>[0-9]+)/matrix/$', matrices_views.matrix, name='matrix'),

	url(r'^(?P<matrix_id>[0-9]+)/detail_matrix/$', matrices_views.view_matrix, name='detail_matrix'), 
	url(r'^new_matrix/$', matrices_views.new_matrix, name='new_matrix'),
	url(r'^(?P<matrix_id>[0-9]+)/edit_matrix/$', matrices_views.edit_matrix, name='edit_matrix'),
	url(r'^(?P<matrix_id>[0-9]+)/delete_matrix/$', matrices_views.delete_matrix, name='delete_matrix'),
	url(r'^(?P<matrix_id>[0-9]+)/add_cell/$', matrices_views.add_cell, name='add_cell'),
	url(r'^(?P<matrix_id>[0-9]+)/edit_cell/(?P<cell_id>[0-9]+)/$', matrices_views.edit_cell, name='edit_cell'),
	url(r'^(?P<matrix_id>[0-9]+)/view_cell/(?P<cell_id>[0-9]+)/$', matrices_views.view_cell, name='view_cell'),
	url(r'^(?P<matrix_id>[0-9]+)/add_column/$', matrices_views.add_column, name='add_column'),
	url(r'^(?P<matrix_id>[0-9]+)/add_column_left/(?P<column_id>[0-9]+)/$', matrices_views.add_column_left, name='add_column_left'),
	url(r'^(?P<matrix_id>[0-9]+)/add_column_right/(?P<column_id>[0-9]+)/$', matrices_views.add_column_right, name='add_column_right'),
	url(r'^(?P<matrix_id>[0-9]+)/delete_this_column/(?P<column_id>[0-9]+)/$', matrices_views.delete_this_column, name='delete_this_column'),
	url(r'^(?P<matrix_id>[0-9]+)/delete_column/$', matrices_views.delete_column, name='delete_column'),
	url(r'^(?P<matrix_id>[0-9]+)/add_row/$', matrices_views.add_row, name='add_row'),
	url(r'^(?P<matrix_id>[0-9]+)/add_row_above/(?P<row_id>[0-9]+)/$', matrices_views.add_row_above, name='add_row_above'),
	url(r'^(?P<matrix_id>[0-9]+)/add_row_below/(?P<row_id>[0-9]+)/$', matrices_views.add_row_below, name='add_row_below'),
	url(r'^(?P<matrix_id>[0-9]+)/delete_this_row/(?P<row_id>[0-9]+)/$', matrices_views.delete_this_row, name='delete_this_row'),
	url(r'^(?P<matrix_id>[0-9]+)/delete_row/$', matrices_views.delete_row, name='delete_row'),
	
	url(r'^list_authorisation/$', matrices_views.list_authorisation, name='list_authorisation'),
	url(r'^list_my_authorisation/$', matrices_views.list_my_authorisation, name='list_my_authorisation'),
	url(r'^list_bench_authorisation/(?P<matrix_id>[0-9]+)/$', matrices_views.list_bench_authorisation, name='list_bench_authorisation'),
	url(r'^list_my_bench_authorisation/(?P<matrix_id>[0-9]+)/(?P<user_id>[0-9]+)/$', matrices_views.list_my_bench_authorisation, name='list_my_bench_authorisation'),
	url(r'^list_user_bench_authorisation/(?P<user_id>[0-9]+)/$', matrices_views.list_user_bench_authorisation, name='list_user_bench_authorisation'),

	url(r'^detail_authorisation/(?P<authorisation_id>[0-9]+)/$', matrices_views.view_authorisation, name='detail_authorisation'),
	url(r'^new_authorisation/(?P<matrix_id>[0-9]+)/$', matrices_views.new_matrix_authorisation, name='new_matrix_authorisation'),
	url(r'^new_authorisation/$', matrices_views.new_authorisation, name='new_authorisation'),
	url(r'^edit_authorisation/(?P<authorisation_id>[0-9]+)/$', matrices_views.edit_authorisation, name='edit_authorisation'),
	url(r'^edit_authorisation/(?P<matrix_id>[0-9]+)/(?P<authorisation_id>[0-9]+)/$', matrices_views.edit_matrix_authorisation, name='edit_matrix_authorisation'),
	url(r'^delete_authorisation/(?P<authorisation_id>[0-9]+)/$', matrices_views.delete_authorisation, name='delete_authorisation'),
]