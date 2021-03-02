from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q

from sortable_listview import SortableListView


from matrices.models import CollectionSummary

from matrices.routines import get_header_data
from matrices.routines import collection_list_by_user_and_direction


class CollectionListView(LoginRequiredMixin, SortableListView):

    allowed_sort_fields = {'collection_id': {'default_direction': '', 'verbose_name': 'Bench Id'},
                           'collection_title': {'default_direction': '', 'verbose_name': 'Title'},
                           'collection_active': {'default_direction': '', 'verbose_name': 'Activity'},
                           'collection_image_count': {'default_direction': '', 'verbose_name': 'Images'},
                           'collection_owner': {'default_direction': '', 'verbose_name': 'Owner'},
                           'collection_authorisation_authority': {'default_direction': '', 'verbose_name': 'Authority'}
                           }

    default_sort_field = 'collection_id'

    paginate_by = 10

    template_name = 'host/list_collections.html'

    model = CollectionSummary

    context_object_name = 'collection_summary_list'


    def get_queryset(self):

        sort_parameter = ''

        if self.request.GET.get('sort', None) == None:

            sort_parameter = 'collection_id'

        else:

            sort_parameter = self.request.GET.get('sort', None)

        return collection_list_by_user_and_direction(self.request.user, sort_parameter)


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        data = get_header_data(self.request.user)

        context.update(data)

        return context
