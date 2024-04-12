#!/usr/bin/python3
# ##!
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest_framework.authtoken.views import obtain_auth_token

from matrices import views as matrices_views


router = DefaultRouter()

#   views/rest/matrix.py
router.register(r'benches', matrices_views.MatrixViewSet)

#   views/rest/cell.py
router.register(r'cells', matrices_views.CellViewSet)

#   views/rest/image.py
router.register(r'images', matrices_views.ImageViewSet)

#   views/rest/collection.py
router.register(r'collections', matrices_views.CollectionViewSet)

#   views/rest/user.py
router.register(r'users', matrices_views.UserViewSet)


urlpatterns = [

    path('inlineedit/', include('inlineedit.urls')),

    #   REST API
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),

    #   auth_views
    path('logout/', auth_views.LogoutView.as_view(template_name="user/login.html"), name='logout'),

    #   views/ajax
    path('ajax/overwrite_cell_leave/', matrices_views.ajax.overwrite_cell_leave, name='overwrite_cell_leave'),
    path('ajax/overwrite_cell/', matrices_views.ajax.overwrite_cell, name='overwrite_cell'),
    path('ajax/swap_cells/', matrices_views.ajax.swap_cells, name='swap_cells'),
    path('ajax/import_image/', matrices_views.ajax.import_image, name='import_image'),
    path('ajax/swap_columns/', matrices_views.ajax.swap_columns, name='swap_columns'),
    path('ajax/swap_rows/', matrices_views.ajax.swap_rows, name='swap_rows'),
    path('ajax/shuffle_columns/', matrices_views.ajax.shuffle_columns, name='shuffle_columns'),
    path('ajax/shuffle_rows/', matrices_views.ajax.shuffle_rows, name='shuffle_rows'),

    path('server_create/', matrices_views.ajax.server_create_update, name="server_create_update"),
    path('server_read/<int:server_id>/', matrices_views.ajax.server_read, name="server_read"),
    path('server_update/<int:server_id>/', matrices_views.ajax.server_create_update, name="server_create_update"),
    path('server_delete/<int:server_id>/', matrices_views.ajax.server_delete, name="server_delete"),

    path('bench_authorisation_create/', matrices_views.ajax.bench_authorisation_create,
         name="bench_authorisation_create"),
    path('bench_authorisation_create/<int:bench_id>/', matrices_views.ajax.bench_authorisation_create,
         name="bench_authorisation_create"),
    path('bench_authorisation_read/<int:authorisation_id>/', matrices_views.ajax.bench_authorisation_read,
         name="bench_authorisation_read"),
    path('bench_authorisation_update/<int:authorisation_id>/', matrices_views.ajax.bench_authorisation_update,
         name="bench_authorisation_update"),
    path('bench_authorisation_update/<int:authorisation_id>/<int:bench_id>/',
         matrices_views.ajax.bench_authorisation_update,
         name="bench_authorisation_update"),
    path('bench_authorisation_delete/<int:authorisation_id>/', matrices_views.ajax.bench_authorisation_delete,
         name="bench_authorisation_delete"),

    path('collection_authorisation_create/', matrices_views.ajax.collection_authorisation_create,
         name="collection_authorisation_create"),
    path('collection_authorisation_create/<int:collection_id>/', matrices_views.ajax.collection_authorisation_create,
         name="collection_authorisation_create"),
    path('collection_authorisation_read/<int:collection_authorisation_id>/',
         matrices_views.ajax.collection_authorisation_read,
         name="collection_authorisation_read"),
    path('collection_authorisation_update/<int:collection_authorisation_id>/',
         matrices_views.ajax.collection_authorisation_update,
         name="collection_authorisation_update"),
    path('collection_authorisation_update/<int:collection_authorisation_id>/<int:collection_id>/',
         matrices_views.ajax.collection_authorisation_update,
         name="collection_authorisation_update"),
    path('collection_authorisation_delete/<int:collection_authorisation_id>/',
         matrices_views.ajax.collection_authorisation_delete,
         name="collection_authorisation_delete"),

    path('collection_create/', matrices_views.ajax.collection_create, name="collection_create"),
    path('collection_read/<int:collection_id>/', matrices_views.ajax.collection_read, name="collection_read"),
    path('collection_update/<int:collection_id>/', matrices_views.ajax.collection_update, name="collection_update"),
    path('collection_delete/<int:collection_id>/', matrices_views.ajax.collection_delete, name="collection_delete"),
    path('collection_selection/<int:user_id>/', matrices_views.ajax.collection_selection, name='collection_selection'),
    path('active_collection_selection/<int:user_id>/', matrices_views.ajax.active_collection_selection,
         name='active_collection_selection'),
    path('collection_update_owner/<int:collection_id>/', matrices_views.ajax.collection_update_owner,
         name="collection_update_owner"),

    path('bench_read/<int:bench_id>/', matrices_views.ajax.bench_read, name='bench_read'),
    path('bench_create/', matrices_views.ajax.bench_create, name='bench_create'),
    path('bench_update/<int:bench_id>/', matrices_views.ajax.bench_update, name='bench_update'),
    path('bench_collection_update/<int:bench_id>/', matrices_views.ajax.bench_collection_update,
         name='bench_collection_update'),
    path('bench_update_owner/<int:bench_id>/', matrices_views.ajax.bench_update_owner,
         name="bench_update_owner"),
    path('bench_delete/<int:bench_id>/', matrices_views.ajax.bench_delete, name='bench_delete'),

    path('header_read/<int:bench_id>/<int:header_id>/', matrices_views.ajax.header_read, name='header_read'),
    path('header_update/<int:bench_id>/<int:header_id>/', matrices_views.ajax.header_update, name='header_update'),

    path('bench_blog_read/<int:bench_id>/', matrices_views.ajax.bench_blog_read, name='bench_blog_read'),
    path('bench_cell_blog_read/<int:cell_id>/', matrices_views.ajax.bench_cell_blog_read, name='bench_cell_blog_read'),
    path('aggregate_bench_cell_blog_read/<int:cell_id>/', matrices_views.ajax.aggregate_bench_cell_blog_read,
         name='aggregate_bench_cell_blog_read'),

    path('tag-autocomplete/<int:image_id>/', matrices_views.ajax.autocompleteTag, name='autocompleteTag'),

    path('add_columns/<int:matrix_id>/<int:column_id>/', matrices_views.ajax.add_columns,
         name='add_columns'),
    path('add_rows/<int:matrix_id>/<int:row_id>/', matrices_views.ajax.add_rows,
         name='add_rows'),
    path('add_cell/<int:matrix_id>/<int:cell_id>/', matrices_views.ajax.add_cell,
         name='add_cell'),
    path('delete_cell/<int:matrix_id>/<int:cell_id>/', matrices_views.ajax.delete_cell,
         name='delete_cell'),

    #   views/authorisation
    path('detail_user/<int:user_id>/', matrices_views.view_user, name='detail_user'),
    path('view_constrained_user/<int:user_id>/', matrices_views.view_constrained_user, name='view_constrained_user'),
    path('edit_user/<int:user_id>/', matrices_views.edit_user, name='edit_user'),
    path('edit_constrained_user/<int:user_id>/', matrices_views.edit_constrained_user, name='edit_constrained_user'),
    path('delete_user/<int:user_id>/', matrices_views.delete_user, name='delete_user'),
    path('detail_blog_credential/<int:credential_id>/', matrices_views.view_blog_credential,
         name='detail_blog_credential'),
    path('new_blog_credential/', matrices_views.new_blog_credential, name='new_blog_credential'),
    path('edit_blog_credential/<int:credential_id>/', matrices_views.edit_blog_credential,
         name='edit_blog_credential'),
    path('delete_blog_credential/<int:credential_id>/', matrices_views.delete_blog_credential,
         name='delete_blog_credential'),
    path('protected/<str:image_id>/', matrices_views.nginx_accel,
         name='nginx_accel'),

    #   views/ebi
    path('show_ebi_server/<int:server_id>/', matrices_views.ebi.show_ebi_server, name='ebi_show_ebi_server'),
    path('show_ebi_widget/<int:server_id>/<slug:experiment_id>/', matrices_views.ebi.show_ebi_widget,
         name='ebi_show_ebi_widget'),

    #   views/gallery
    path('show_server/<int:server_id>/', matrices_views.gallery.show_imaging_server,
         name='webgallery_show_imaging_server'),
    path('show_group/<int:server_id>/<int:group_id>/', matrices_views.gallery.show_group,
         name='webgallery_show_group'),
    path('show_project/<int:server_id>/<int:project_id>/<int:page_id>/', matrices_views.gallery.show_project,
         name='webgallery_show_project'),
    path('show_dataset/<int:server_id>/<int:dataset_id>/', matrices_views.gallery.show_dataset,
         name='webgallery_show_dataset'),
    path('show_dataset_filtered/<int:server_id>/<int:dataset_id>/', matrices_views.gallery.show_dataset_filtered,
         name='webgallery_show_dataset_filtered'),
    path('show_wordpress/<int:server_id>/<int:page_id>/', matrices_views.gallery.show_wordpress,
         name='webgallery_show_wordpress'),
    path('show_ebi_sca_upload_server/<int:server_id>/', matrices_views.gallery.show_ebi_sca_upload_server,
         name='webgallery_show_ebi_sca_upload_server'),
    path('show_cpw_upload_server/<int:server_id>/', matrices_views.gallery.show_cpw_upload_server,
         name='webgallery_show_cpw_upload_server'),
    path('add_dataset/<int:server_id>/<int:dataset_id>/', matrices_views.gallery.add_dataset,
         name='webgallery_add_dataset'),
    path('add_dataset_all/<int:server_id>/<int:dataset_id>/', matrices_views.gallery.add_dataset_all,
         name='webgallery_add_dataset_all'),
    path('add_dataset_all_filtered/<int:server_id>/<int:dataset_id>/', matrices_views.gallery.add_dataset_all_filtered,
         name='webgallery_add_dataset_all_filtered'),
    path('add_dataset_all_new_collection/<int:server_id>/<int:dataset_id>/',
         matrices_views.gallery.add_dataset_all_new_collection, name='webgallery_add_dataset_all_new_collection'),
    path('add_dataset_all_filtered_new_collection/<int:server_id>/<int:dataset_id>/',
         matrices_views.gallery.add_dataset_all_filtered_new_collection,
         name='webgallery_add_dataset_all_filtered_new_collection'),
    path('add_image/<int:server_id>/<int:image_id>/<int:roi_id>/<str:path_from>/<int:identifier>/', 
         matrices_views.gallery.add_image,
         name='webgallery_add_image'),
    path('add_ebi_sca_image/<int:server_id>/<str:image_id>/<str:path_from>/', matrices_views.gallery.add_ebi_sca_image,
         name='webgallery_add_ebi_sca_image'),
    path('add_cpw_image/<int:server_id>/<str:image_id>/<str:path_from>/', matrices_views.gallery.add_cpw_image,
         name='webgallery_add_cpw_image'),
    path('show_image/<int:server_id>/<int:image_id>/', matrices_views.gallery.show_image,
         name='webgallery_show_image'),
    path('show_wordpress_image/<int:server_id>/<int:image_id>/', matrices_views.gallery.show_wordpress_image,
         name='webgallery_show_wordpress_image'),
    path('show_ebi_sca_image/<int:server_id>/<str:image_id>/', matrices_views.gallery.show_ebi_sca_image,
         name='webgallery_show_ebi_sca_image'),
    path('show_cpw_image/<int:server_id>/<str:image_id>/', matrices_views.gallery.show_cpw_image,
         name='webgallery_show_cpw_image'),
    path('edit_image/<int:image_id>/', matrices_views.gallery.edit_image, name='webgallery_edit_image'),
    path('tag_image/<int:image_id>/<slug:slug>/', matrices_views.gallery.tag_image, name='webgallery_tag_image'),
    path('untag_image/<int:image_id>/<slug:slug>/', matrices_views.gallery.untag_image, name='webgallery_untag_image'),

    #   views/host
    path('', matrices_views.host.home, name='home'),
    path('home/', matrices_views.host.home, name='home'),
    path('authorisation/', matrices_views.host.authorisation, name='authorisation'),
    path('maintenance/', matrices_views.host.maintenance, name='maintenance'),
    path('list_imaging_hosts/', matrices_views.host.list_imaging_hosts, name='list_imaging_hosts'),
    path('list_bench_authorisation/', matrices_views.host.list_bench_authorisation, name='list_bench_authorisation'),
    path('list_bench_authorisation/<int:matrix_id>/', matrices_views.host.list_bench_authorisation,
         name='list_bench_authorisation'),
    path('list_my_bench_authorisation/', matrices_views.host.list_my_bench_authorisation,
         name='list_my_bench_authorisation'),
    path('list_user_bench_authorisation/<int:user_id>/', matrices_views.host.list_user_bench_authorisation,
         name='list_user_bench_authorisation'),
    path('list_collection_authorisation/', matrices_views.host.list_collection_authorisation,
         name='list_collection_authorisation'),
    path('list_collection_authorisation/<int:collection_id>/', matrices_views.host.list_collection_authorisation,
         name='list_collection_authorisation'),
    path('list_my_collection_authorisation/', matrices_views.host.list_my_collection_authorisation,
         name='list_my_collection_authorisation'),
    path('list_user_collection_authorisation/<int:user_id>/', matrices_views.host.list_user_collection_authorisation,
         name='list_user_collection_authorisation'),
    path('list_global/', matrices_views.host.list_global, name='list_global'),
    path('list_benches/', matrices_views.host.MatrixListView.as_view(), name='list_benches'),
    path('list_collections/', matrices_views.host.CollectionListView.as_view(), name='list_collections'),
    path('list_images_simple/', matrices_views.host.ImageSimpleListView.as_view(), name='list_images_simple'),
    path('list_images/', matrices_views.host.ImageListView.as_view(), name='list_images'),
    path('list_images/<int:collection_id>/', matrices_views.host.ImageListView.as_view(), name='list_images'),
    path('list_images/<int:collection_id>/<int:tag_id>/', matrices_views.host.ImageListView.as_view(),
         name='list_images'),

    #   views/maintenance
    path('detail_blog_command/<int:blog_id>/', matrices_views.maintenance.view_blog_command,
         name='detail_blog_command'),
    path('new_blog_command/', matrices_views.maintenance.new_blog_command, name='new_blog_command'),
    path('edit_blog_command/<int:blog_id>/', matrices_views.maintenance.edit_blog_command, name='edit_blog_command'),
    path('delete_blog_command/<int:blog_id>/', matrices_views.maintenance.delete_blog_command,
         name='delete_blog_command'),

    path('detail_command/<int:command_id>/', matrices_views.maintenance.view_command, name='detail_command'),
    path('new_command/', matrices_views.maintenance.new_command, name='new_command'),
    path('edit_command/<int:command_id>/', matrices_views.maintenance.edit_command, name='edit_command'),
    path('delete_command/<int:command_id>/', matrices_views.maintenance.delete_command, name='delete_command'),

    path('detail_protocol/<int:protocol_id>/', matrices_views.maintenance.view_protocol, name='detail_protocol'),
    path('new_protocol/', matrices_views.maintenance.new_protocol, name='new_protocol'),
    path('edit_protocol/<int:protocol_id>/', matrices_views.maintenance.edit_protocol, name='edit_protocol'),
    path('delete_protocol/<int:protocol_id>/', matrices_views.maintenance.delete_protocol, name='delete_protocol'),

    path('detail_type/<int:type_id>/', matrices_views.maintenance.view_type, name='detail_type'),
    path('new_type/', matrices_views.maintenance.new_type, name='new_type'),
    path('edit_type/<int:type_id>/', matrices_views.maintenance.edit_type, name='edit_type'),
    path('delete_type/<int:type_id>/', matrices_views.maintenance.delete_type, name='delete_type'),

    path('detail_location/<int:location_id>/', matrices_views.maintenance.view_location, name='detail_location'),
    path('new_location/', matrices_views.maintenance.new_location, name='new_location'),
    path('edit_location/<int:location_id>/', matrices_views.maintenance.edit_location, name='edit_location'),
    path('delete_location/<int:location_id>/', matrices_views.maintenance.delete_location, name='delete_location'),

    path('detail_gateway/<int:gateway_id>/', matrices_views.maintenance.view_gateway, name='detail_gateway'),
    path('new_gateway/', matrices_views.maintenance.new_gateway, name='new_gateway'),
    path('edit_gateway/<int:gateway_id>/', matrices_views.maintenance.edit_gateway, name='edit_gateway'),
    path('delete_gateway/<int:gateway_id>/', matrices_views.maintenance.delete_gateway, name='delete_gateway'),

    path('detail_environment/<int:environment_id>/', matrices_views.maintenance.view_environment,
         name='detail_environment'),
    path('new_environment/', matrices_views.maintenance.new_environment, name='new_environment'),
    path('edit_environment/<int:environment_id>/', matrices_views.maintenance.edit_environment,
         name='edit_environment'),
    path('delete_environment/<int:environment_id>/', matrices_views.maintenance.delete_environment,
         name='delete_environment'),

    path('detail_bench_authority/<int:bench_authority_id>/', matrices_views.maintenance.view_bench_authority,
         name='detail_bench_authority'),
    path('new_bench_authority/', matrices_views.maintenance.new_bench_authority, name='new_bench_authority'),
    path('edit_bench_authority/<int:bench_authority_id>/', matrices_views.maintenance.edit_bench_authority,
         name='edit_bench_authority'),
    path('delete_bench_authority/<int:bench_authority_id>/', matrices_views.maintenance.delete_bench_authority,
         name='delete_bench_authority'),

    path('detail_collection_authority/<int:collection_authority_id>/',
         matrices_views.maintenance.view_collection_authority, name='detail_collection_authority'),
    path('new_collection_authority/', matrices_views.maintenance.new_collection_authority,
         name='new_collection_authority'),
    path('edit_collection_authority/<int:collection_authority_id>/',
         matrices_views.maintenance.edit_collection_authority, name='edit_collection_authority'),
    path('delete_collection_authority/<int:collection_authority_id>/',
         matrices_views.maintenance.delete_collection_authority, name='delete_collection_authority'),

    #   views/matrices
    path('delete_image/<int:image_id>/', matrices_views.matrices.delete_image, name='webgallery_delete_image'),
    path('delete_collection_image/<int:collection_id>/<int:image_id>/',
         matrices_views.matrices.delete_collection_image, name='webgallery_delete_collection_image'),

    path('activate_collection/<int:collection_id>/', matrices_views.matrices.activate_collection,
         name='activate_collection'),
    path('activate_in_collection/<int:collection_id>/', matrices_views.matrices.activate_in_collection,
         name='activate_in_collection'),

    path('set_last_used_tag/<int:matrix_id>/<int:tag_id>/', matrices_views.matrices.set_last_used_tag_in_matrix,
         name='set_last_used_tag'),
    path('set_no_last_used_tag/<int:matrix_id>/', matrices_views.matrices.set_no_last_used_tag_in_matrix,
         name='set_no_last_used_tag'),

    path('aggregated_matrix_blog/<int:matrix_id>/', matrices_views.matrices.view_aggregated_blog,
         name='aggregated_matrix_blog'),
    path('detail_matrix_blog/<int:matrix_id>/', matrices_views.matrices.view_matrix_blog, name='detail_matrix_blog'),
    path('view_cell_blog/<int:matrix_id>/<int:cell_id>/', matrices_views.matrices.view_cell_blog,
         name='view_cell_blog'),
    path('matrix/<int:matrix_id>/', matrices_views.matrices.view_matrix, name='matrix'),
    path('clear_cell/<int:matrix_id>/<int:cell_id>/<str:path_from>/', matrices_views.matrices.clear_cell,
         name='clear_cell'),
    path('amend_cell/<int:matrix_id>/<int:cell_id>/', matrices_views.matrices.amend_cell, name='amend_cell'),
    path('delete_this_column/<int:matrix_id>/<int:column_id>/', matrices_views.matrices.delete_this_column,
         name='delete_this_column'),
    path('delete_this_row/<int:matrix_id>/<int:row_id>/', matrices_views.matrices.delete_this_row,
         name='delete_this_row'),

    path('search_image/<str:path_from>/<int:identifier>/', matrices_views.matrices.search_image, name='search_image'),

    path('link_images/<int:image_parent_id>/<int:image_child_id>/', matrices_views.matrices.link_images,
         name='link_images'),
    path('view_image_link/<int:image_link_id>/', matrices_views.matrices.view_image_link, name='view_image_link'),
    path('delete_image_link/<int:image_link_id>/', matrices_views.matrices.delete_image_link,
         name='delete_image_link'),

    path('view_all_image_links/', matrices_views.matrices.view_all_image_links, name='view_all_image_links'),
    path('view_a_image_link/<int:image_parent_id>/', matrices_views.matrices.view_parent_image_link,
         name='view_a_image_link'),
    path('view_b_image_link/<int:image_child_id>/', matrices_views.matrices.view_child_image_link,
         name='view_b_image_link'),
    path('view_a_and_b_image_links/<int:image_selected_id>/',
         matrices_views.matrices.view_parent_and_child_image_links, name='view_a_and_b_image_links'),

    #   views/user
    path('login/', matrices_views.user.login_user, name="login"),
    path('signup/', matrices_views.user.signup, name='signup'),
    path('account_activation_sent/', matrices_views.user.account_activation_sent, name='account_activation_sent'),
    path('activate/<str:uidb64>/<str:token>', matrices_views.user.activate, name='activate'),

    path('settings/password/', matrices_views.user.ChangePasswordView.as_view(), name='password_change'),
    path('settings/password/done/', matrices_views.user.ChangePasswordDoneView.as_view(), name='password_change_done'),

    path('reset/', matrices_views.user.ResetPasswordView.as_view(\
             email_template_name='user/password_reset_email.html',
             subject_template_name='user/password_reset_subject.txt'), name='password_reset'),
    path('reset/done/', matrices_views.user.ResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/', matrices_views.user.ResetPasswordConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/complete/', matrices_views.user.ResetPasswordCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
