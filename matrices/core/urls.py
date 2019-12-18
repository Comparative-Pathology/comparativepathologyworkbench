from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

	url(r'^home/$', views.home, name='home'),
	url(r'^about/$', views.about, name='about'),
	url(r'^people/$', views.people, name='people'),
	url(r'^howto/$', views.howto, name='howto'),

	url(r'^$', views.index_matrix, name='index'),

	url(r'^list_matrix/$', views.list_matrix, name='list_matrix'),

	url(r'^list_imaging_hosts/$', views.list_imaging_hosts, name='list_imaging_hosts'),
	url(r'^maintenance/$', views.maintenance, name='maintenance'),
	url(r'^authorisation/$', views.authorisation, name='authorisation'),
	url(r'^list_image_cart/$', views.list_image_cart, name='list_image_cart'),

	url(r'^show_ebi_server/(?P<server_id>[0-9]+)/$', views.show_ebi_server, name='ebi_show_ebi_server'),

	url(r'^show_server/(?P<server_id>[0-9]+)/$', views.show_imaging_server, name='webgallery_show_imaging_server'),
	url(r'^show_group/(?P<server_id>[0-9]+)/(?P<group_id>[0-9]+)/$', views.show_group, name='webgallery_show_group'),
	url(r'^show_project/(?P<server_id>[0-9]+)/(?P<project_id>[0-9]+)/$', views.show_project, name='webgallery_show_project'),
	url(r'^show_dataset/(?P<server_id>[0-9]+)/(?P<dataset_id>[0-9]+)/$', views.show_dataset, name='webgallery_show_dataset'),
	url(r'^show_image/(?P<server_id>[0-9]+)/(?P<image_id>[0-9]+)/$', views.show_image, name='webgallery_show_image'),

	url(r'^show_wordpress/(?P<server_id>[0-9]+)/(?P<page_id>[0-9]+)/$', views.show_wordpress, name='webgallery_show_wordpress'),
	url(r'^show_wordpress_image/(?P<server_id>[0-9]+)/(?P<image_id>[0-9]+)/$', views.show_wordpress_image, name='webgallery_show_wordpress_image'),

	url(r'^add_image/(?P<server_id>[0-9]+)/(?P<image_id>[0-9]+)/(?P<roi_id>[0-9]+)/$', views.add_image, name='webgallery_add_image'),
	url(r'^delete_image/(?P<image_id>[0-9]+)/$', views.delete_image, name='webgallery_delete_image'),

	url(r'^detail_user_general/(?P<user_id>[0-9]+)/$', views.view_user_general, name='detail_user_general'), 
	url(r'^edit_user_general/(?P<user_id>[0-9]+)/$', views.edit_user_general, name='edit_user_general'),

	url(r'^detail_user/(?P<user_id>[0-9]+)/$', views.view_user, name='detail_user'), 
	url(r'^edit_user/(?P<user_id>[0-9]+)/$', views.edit_user, name='edit_user'),
	url(r'^delete_user/(?P<user_id>[0-9]+)/$', views.delete_user, name='delete_user'),

	url(r'^detail_server/(?P<server_id>[0-9]+)/$', views.view_server, name='detail_server'), 
	url(r'^new_server/$', views.new_server, name='new_server'),
	url(r'^edit_server/(?P<server_id>[0-9]+)/$', views.edit_server, name='edit_server'),
	url(r'^delete_server/(?P<server_id>[0-9]+)/$', views.delete_server, name='delete_server'),

	url(r'^detail_blog_command/(?P<blog_id>[0-9]+)/$', views.view_blog_command, name='detail_blog_command'), 
	url(r'^new_blog_command/$', views.new_blog_command, name='new_blog_command'),
	url(r'^edit_blog_command/(?P<blog_id>[0-9]+)/$', views.edit_blog_command, name='edit_blog_command'),
	url(r'^delete_blog_command/(?P<blog_id>[0-9]+)/$', views.delete_blog_command, name='delete_blog_command'),

	url(r'^detail_blog_credential/(?P<credential_id>[0-9]+)/$', views.view_blog_credential, name='detail_blog_credential'), 
	url(r'^new_blog_credential/$', views.new_blog_credential, name='new_blog_credential'),
	url(r'^edit_blog_credential/(?P<credential_id>[0-9]+)/$', views.edit_blog_credential, name='edit_blog_credential'),
	url(r'^delete_blog_credential/(?P<credential_id>[0-9]+)/$', views.delete_blog_credential, name='delete_blog_credential'),

	url(r'^detail_command/(?P<command_id>[0-9]+)/$', views.view_command, name='detail_command'), 
	url(r'^new_command/$', views.new_command, name='new_command'),
	url(r'^edit_command/(?P<command_id>[0-9]+)/$', views.edit_command, name='edit_command'),
	url(r'^delete_command/(?P<command_id>[0-9]+)/$', views.delete_command, name='delete_command'),

	url(r'^detail_protocol/(?P<protocol_id>[0-9]+)/$', views.view_protocol, name='detail_protocol'), 
	url(r'^new_protocol/$', views.new_protocol, name='new_protocol'),
	url(r'^edit_protocol/(?P<protocol_id>[0-9]+)/$', views.edit_protocol, name='edit_protocol'),
	url(r'^delete_protocol/(?P<protocol_id>[0-9]+)/$', views.delete_protocol, name='delete_protocol'),

	url(r'^detail_type/(?P<type_id>[0-9]+)/$', views.view_type, name='detail_type'),	 # ex: /maintenance/new_type
	url(r'^new_type/$', views.new_type, name='new_type'),
	url(r'^edit_type/(?P<type_id>[0-9]+)/$', views.edit_type, name='edit_type'),
	url(r'^delete_type/(?P<type_id>[0-9]+)/$', views.delete_type, name='delete_type'),

	url(r'^(?P<matrix_id>[0-9]+)/detail_matrix_blog/$', views.view_matrix_blog, name='detail_matrix_blog'), 
	url(r'^(?P<matrix_id>[0-9]+)/view_cell_blog/(?P<cell_id>[0-9]+)/$', views.view_cell_blog, name='view_cell_blog'),

	url(r'^(?P<matrix_id>[0-9]+)/detail_matrix/$', views.view_matrix, name='detail_matrix'), 
	url(r'^new_matrix/$', views.new_matrix, name='new_matrix'),
	url(r'^(?P<matrix_id>[0-9]+)/edit_matrix/$', views.edit_matrix, name='edit_matrix'),
	url(r'^(?P<matrix_id>[0-9]+)/delete_matrix/$', views.delete_matrix, name='delete_matrix'),
	url(r'^(?P<matrix_id>[0-9]+)/matrix/$', views.matrix, name='matrix'),
	url(r'^(?P<matrix_id>[0-9]+)/add_cell/$', views.add_cell, name='add_cell'),
	url(r'^(?P<matrix_id>[0-9]+)/edit_cell/(?P<cell_id>[0-9]+)/$', views.edit_cell, name='edit_cell'),
	url(r'^(?P<matrix_id>[0-9]+)/view_cell/(?P<cell_id>[0-9]+)/$', views.view_cell, name='view_cell'),
	url(r'^(?P<matrix_id>[0-9]+)/add_column/$', views.add_column, name='add_column'),
	url(r'^(?P<matrix_id>[0-9]+)/add_column_left/(?P<column_id>[0-9]+)/$', views.add_column_left, name='add_column_left'),
	url(r'^(?P<matrix_id>[0-9]+)/add_column_right/(?P<column_id>[0-9]+)/$', views.add_column_right, name='add_column_right'),
	url(r'^(?P<matrix_id>[0-9]+)/delete_this_column/(?P<column_id>[0-9]+)/$', views.delete_this_column, name='delete_this_column'),
	url(r'^(?P<matrix_id>[0-9]+)/delete_column/$', views.delete_column, name='delete_column'),
	url(r'^(?P<matrix_id>[0-9]+)/add_row/$', views.add_row, name='add_row'),
	url(r'^(?P<matrix_id>[0-9]+)/add_row_above/(?P<row_id>[0-9]+)/$', views.add_row_above, name='add_row_above'),
	url(r'^(?P<matrix_id>[0-9]+)/add_row_below/(?P<row_id>[0-9]+)/$', views.add_row_below, name='add_row_below'),
	url(r'^(?P<matrix_id>[0-9]+)/delete_this_row/(?P<row_id>[0-9]+)/$', views.delete_this_row, name='delete_this_row'),
	url(r'^(?P<matrix_id>[0-9]+)/delete_row/$', views.delete_row, name='delete_row'),
] 

