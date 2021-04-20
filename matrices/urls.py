#!/usr/bin/python3
###!
# \file         urls.py
# \author       Mike Wicks
# \date         March 2021
# \version      $Id$
# \par
# (C) University of Edinburgh, Edinburgh, UK
# (C) Heriot-Watt University, Edinburgh, UK
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be
# useful but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.
# \brief
# All the URL Paths used by the CPW.
###

from django.conf.urls import url, include

from django.contrib.auth import views as auth_views

from django.urls import path

from matrices import views as matrices_views

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

from django_filters.views import FilterView


router = DefaultRouter()

#   views_rest_matrix.py
router.register(r'benches', matrices_views.MatrixViewSet)

#   views_rest_cell.py
router.register(r'cells', matrices_views.CellViewSet)

#   views_rest_image.py
router.register(r'images', matrices_views.ImageViewSet)


urlpatterns = [

    path('inlineedit/', include('inlineedit.urls')),

#   REST API
    path('api/', include(router.urls)),

#   auth_views
    path('login/', auth_views.LoginView.as_view(template_name="user/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="user/login.html"), name='logout'),

#   auth_views
    path('reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html', email_template_name='user/password_reset_email.html', subject_template_name='user/password_reset_subject.txt'), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='user/password_change.html'), name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'), name='password_change_done'),

#   views_about.py
	path('about/', matrices_views.about, name='about'),
	path('people/', matrices_views.people, name='people'),
	path('howto/', matrices_views.howto, name='howto'),

#   views_ajax.py
    path('ajax/overwrite_cell_leave/', matrices_views.overwrite_cell_leave, name='overwrite_cell_leave'),
    path('ajax/overwrite_cell/', matrices_views.overwrite_cell, name='overwrite_cell'),
    path('ajax/swap_cells/', matrices_views.swap_cells, name='swap_cells'),
    path('ajax/import_image/', matrices_views.import_image, name='import_image'),
    path('ajax/swap_columns/', matrices_views.swap_columns, name='swap_columns'),
    path('ajax/swap_rows/', matrices_views.swap_rows, name='swap_rows'),
    path('ajax/shuffle_columns/', matrices_views.shuffle_columns, name='shuffle_columns'),
    path('ajax/shuffle_rows/', matrices_views.shuffle_rows, name='shuffle_rows'),

#   views_authorisation.py
	path('mailer/', matrices_views.mailer, name='mailer'),
	path('collectivization/', matrices_views.collectivization, name='collectivization'),
	path('detail_user/<int:user_id>/', matrices_views.view_user, name='detail_user'),
	path('edit_user/<int:user_id>/', matrices_views.edit_user, name='edit_user'),
	path('delete_user/<int:user_id>/', matrices_views.delete_user, name='delete_user'),
	path('detail_blog_credential/<int:credential_id>/', matrices_views.view_blog_credential, name='detail_blog_credential'),
	path('new_blog_credential/', matrices_views.new_blog_credential, name='new_blog_credential'),
	path('edit_blog_credential/<int:credential_id>/', matrices_views.edit_blog_credential, name='edit_blog_credential'),
	path('delete_blog_credential/<int:credential_id>/', matrices_views.delete_blog_credential, name='delete_blog_credential'),

#   views_ebi.py
	path('show_ebi_server/<int:server_id>/', matrices_views.show_ebi_server, name='ebi_show_ebi_server'),
	path('show_ebi_widget/<int:server_id>/<slug:experiment_id>/', matrices_views.show_ebi_widget, name='ebi_show_ebi_widget'),

#   views_gallery.py
	path('show_server/<int:server_id>/', matrices_views.show_imaging_server, name='webgallery_show_imaging_server'),
	path('show_group/<int:server_id>/<int:group_id>/', matrices_views.show_group, name='webgallery_show_group'),
	path('show_project/<int:server_id>/<int:project_id>/', matrices_views.show_project, name='webgallery_show_project'),
	path('show_dataset/<int:server_id>/<int:dataset_id>/', matrices_views.show_dataset, name='webgallery_show_dataset'),
	path('show_image/<int:server_id>/<int:image_id>/', matrices_views.show_image, name='webgallery_show_image'),
	path('show_wordpress/<int:server_id>/<int:page_id>/', matrices_views.show_wordpress, name='webgallery_show_wordpress'),
	path('show_wordpress_image/<int:server_id>/<int:image_id>/', matrices_views.show_wordpress_image, name='webgallery_show_wordpress_image'),
	path('add_image/<int:server_id>/<int:image_id>/<int:roi_id>/', matrices_views.add_image, name='webgallery_add_image'),

#   views_host.py
	path('', matrices_views.home, name='home'),
	path('home/', matrices_views.home, name='home'),
	path('detail_server/<int:server_id>/', matrices_views.view_server, name='detail_server'),
	path('new_server/', matrices_views.new_server, name='new_server'),
	path('edit_server/<int:server_id>/', matrices_views.edit_server, name='edit_server'),
	path('delete_server/<int:server_id>/', matrices_views.delete_server, name='delete_server'),
	path('authorisation/', matrices_views.authorisation, name='authorisation'),
	path('maintenance/', matrices_views.maintenance, name='maintenance'),
    path('list_benches/', matrices_views.MatrixListView.as_view(), name='list_benches'),
    path('list_imaging_hosts/', matrices_views.list_imaging_hosts, name='list_imaging_hosts'),
	path('list_image_cart/', matrices_views.list_image_cart, name='list_image_cart'),
    path('list_collections/', matrices_views.CollectionListView.as_view(), name='list_collections'),
	path('list_bench_authorisation/', matrices_views.list_bench_authorisation, name='list_bench_authorisation'),
	path('list_my_bench_authorisation/', matrices_views.list_my_bench_authorisation, name='list_my_bench_authorisation'),
	path('list_my_bench_bench_authorisation/<int:matrix_id>/<int:user_id>/', matrices_views.list_my_bench_bench_authorisation, name='list_my_bench_bench_authorisation'),
	path('list_bench_bench_authorisation/<int:matrix_id>/', matrices_views.list_bench_bench_authorisation, name='list_bench_bench_authorisation'),
	path('list_user_bench_bench_authorisation/<int:user_id>/', matrices_views.list_user_bench_bench_authorisation, name='list_user_bench_bench_authorisation'),
	path('list_collection_authorisation/', matrices_views.list_collection_authorisation, name='list_collection_authorisation'),
	path('list_my_collection_authorisation/', matrices_views.list_my_collection_authorisation, name='list_my_collection_authorisation'),
	path('list_my_collection_collection_authorisation/<int:collection_id>/<int:user_id>/', matrices_views.list_my_collection_collection_authorisation, name='list_my_collection_collection_authorisation'),
	path('list_collection_collection_authorisation/<int:collection_id>/', matrices_views.list_collection_collection_authorisation, name='list_collection_collection_authorisation'),
	path('list_user_collection_collection_authorisation/<int:user_id>/', matrices_views.list_user_collection_collection_authorisation, name='list_user_collection_collection_authorisation'),

#   views_maintenance.py
	path('detail_blog_command/<int:blog_id>/', matrices_views.view_blog_command, name='detail_blog_command'),
	path('new_blog_command/', matrices_views.new_blog_command, name='new_blog_command'),
	path('edit_blog_command/<int:blog_id>/', matrices_views.edit_blog_command, name='edit_blog_command'),
	path('delete_blog_command/<int:blog_id>/', matrices_views.delete_blog_command, name='delete_blog_command'),
	path('detail_command/<int:command_id>/', matrices_views.view_command, name='detail_command'),
	path('new_command/', matrices_views.new_command, name='new_command'),
	path('edit_command/<int:command_id>/', matrices_views.edit_command, name='edit_command'),
	path('delete_command/<int:command_id>/', matrices_views.delete_command, name='delete_command'),
	path('detail_protocol/<int:protocol_id>/', matrices_views.view_protocol, name='detail_protocol'),
	path('new_protocol/', matrices_views.new_protocol, name='new_protocol'),
	path('edit_protocol/<int:protocol_id>/', matrices_views.edit_protocol, name='edit_protocol'),
	path('delete_protocol/<int:protocol_id>/', matrices_views.delete_protocol, name='delete_protocol'),
	path('detail_type/<int:type_id>/', matrices_views.view_type, name='detail_type'),
	path('new_type/', matrices_views.new_type, name='new_type'),
	path('edit_type/<int:type_id>/', matrices_views.edit_type, name='edit_type'),
	path('delete_type/<int:type_id>/', matrices_views.delete_type, name='delete_type'),
	path('detail_bench_authority/<int:bench_authority_id>/', matrices_views.view_bench_authority, name='detail_bench_authority'),
	path('new_bench_authority/', matrices_views.new_bench_authority, name='new_bench_authority'),
	path('edit_bench_authority/<int:bench_authority_id>/', matrices_views.edit_bench_authority, name='edit_bench_authority'),
	path('delete_bench_authority/<int:bench_authority_id>/', matrices_views.delete_bench_authority, name='delete_bench_authority'),
	path('detail_collection_authority/<int:collection_authority_id>/', matrices_views.view_collection_authority, name='detail_collection_authority'),
	path('new_collection_authority/', matrices_views.new_collection_authority, name='new_collection_authority'),
	path('edit_collection_authority/<int:collection_authority_id>/', matrices_views.edit_collection_authority, name='edit_collection_authority'),
	path('delete_collection_authority/<int:collection_authority_id>/', matrices_views.delete_collection_authority, name='delete_collection_authority'),

#   views_matrix.py
	path('delete_image/<int:image_id>/', matrices_views.delete_image, name='webgallery_delete_image'),
	path('detail_collection/<int:collection_id>/', matrices_views.detail_collection, name='detail_collection'),
	path('view_collection/<int:collection_id>/', matrices_views.view_collection, name='view_collection'),
	path('view_active_collection/', matrices_views.view_active_collection, name='view_active_collection'),
	path('view_all_collections/', matrices_views.view_all_collections, name='view_all_collections'),
	path('new_collection/', matrices_views.new_collection, name='new_collection'),
	path('edit_collection/<int:collection_id>/', matrices_views.edit_collection, name='edit_collection'),
	path('delete_collection/<int:collection_id>/', matrices_views.delete_collection, name='delete_collection'),
	path('choose_collection/<int:matrix_id>/<int:collection_id>/', matrices_views.choose_collection, name='choose_collection'),
	path('activate_collection/<int:collection_id>/', matrices_views.activate_collection, name='activate_collection'),
	path('<int:matrix_id>/detail_matrix_blog/', matrices_views.view_matrix_blog, name='detail_matrix_blog'),
	path('<int:matrix_id>/view_cell_blog/<int:cell_id>/', matrices_views.view_cell_blog, name='view_cell_blog'),
	path('<int:matrix_id>/matrix/', matrices_views.view_matrix, name='matrix'),
	path('<int:matrix_id>/detail_matrix/', matrices_views.detail_matrix, name='detail_matrix'),
	path('new_matrix/', matrices_views.new_matrix, name='new_matrix'),
	path('<int:matrix_id>/edit_matrix/', matrices_views.edit_matrix, name='edit_matrix'),
	path('<int:matrix_id>/delete_matrix/', matrices_views.delete_matrix, name='delete_matrix'),
	path('<int:matrix_id>/add_cell/', matrices_views.add_cell, name='add_cell'),
	path('<int:matrix_id>/edit_cell/<int:cell_id>/', matrices_views.edit_cell, name='edit_cell'),
	path('<int:matrix_id>/view_cell/<int:cell_id>/', matrices_views.view_cell, name='view_cell'),
	path('<int:matrix_id>/append_column/', matrices_views.append_column, name='append_column'),
	path('<int:matrix_id>/add_column_left/<int:column_id>/', matrices_views.add_column_left, name='add_column_left'),
	path('<int:matrix_id>/add_column_right/<int:column_id>/', matrices_views.add_column_right, name='add_column_right'),
	path('<int:matrix_id>/delete_this_column/<int:column_id>/', matrices_views.delete_this_column, name='delete_this_column'),
	path('<int:matrix_id>/delete_last_column/', matrices_views.delete_last_column, name='delete_last_column'),
	path('<int:matrix_id>/append_row/', matrices_views.append_row, name='append_row'),
	path('<int:matrix_id>/add_row_above/<int:row_id>/', matrices_views.add_row_above, name='add_row_above'),
	path('<int:matrix_id>/add_row_below/<int:row_id>/', matrices_views.add_row_below, name='add_row_below'),
	path('<int:matrix_id>/delete_this_row/<int:row_id>/', matrices_views.delete_this_row, name='delete_this_row'),
	path('<int:matrix_id>/delete_last_row/', matrices_views.delete_last_row, name='delete_last_row'),

#   views_permissions.py
	path('detail_bench_authorisation/<int:bench_authorisation_id>/', matrices_views.view_bench_authorisation, name='detail_bench_authorisation'),
	path('new_bench_authorisation/', matrices_views.new_bench_authorisation, name='new_bench_authorisation'),
	path('new_bench_bench_authorisation/<int:matrix_id>/', matrices_views.new_bench_bench_authorisation, name='new_bench_bench_authorisation'),
	path('edit_bench_authorisation/<int:bench_authorisation_id>/', matrices_views.edit_bench_authorisation, name='edit_bench_authorisation'),
	path('edit_bench_bench_authorisation/<int:matrix_id>/<int:bench_authorisation_id>/', matrices_views.edit_bench_bench_authorisation, name='edit_bench_bench_authorisation'),
	path('delete_bench_authorisation/<int:bench_authorisation_id>/', matrices_views.delete_bench_authorisation, name='delete_bench_authorisation'),
	path('detail_collection_authorisation/<int:collection_authorisation_id>/', matrices_views.view_collection_authorisation, name='detail_collection_authorisation'),
	path('new_collection_authorisation/', matrices_views.new_collection_authorisation, name='new_collection_authorisation'),
	path('new_collection_collection_authorisation/<int:collection_id>/', matrices_views.new_collection_collection_authorisation, name='new_collection_collection_authorisation'),
	path('edit_collection_authorisation/<int:collection_authorisation_id>/', matrices_views.edit_collection_authorisation, name='edit_collection_authorisation'),
	path('edit_collection_collection_authorisation/<int:collection_id>/<int:collection_authorisation_id>/', matrices_views.edit_collection_collection_authorisation, name='edit_collection_collection_authorisation'),
	path('delete_collection_authorisation/<int:collection_authorisation_id>/', matrices_views.delete_collection_authorisation, name='delete_collection_authorisation'),

#   views_user.py
	path('signup/', matrices_views.signup, name='signup'),
	path('account_activation_sent/', matrices_views.account_activation_sent, name='account_activation_sent'),
	path('activate/<str:uidb64>/<str:token>', matrices_views.activate, name='activate'),

]
