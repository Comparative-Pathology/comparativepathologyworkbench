from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q

from sortable_listview import SortableListView


from matrices.models import MatrixSummary

from matrices.routines import get_header_data
from matrices.routines import bench_list_by_user_and_direction


class MatrixListView(LoginRequiredMixin, SortableListView):

    allowed_sort_fields = {'matrix_id': {'default_direction': '', 'verbose_name': 'Bench Id'},
                           'matrix_title': {'default_direction': '', 'verbose_name': 'Title'},
                           'matrix_created': {'default_direction': '', 'verbose_name': 'Created On'},
                           'matrix_modified': {'default_direction': '', 'verbose_name': 'Updated On'},
                           'matrix_owner': {'default_direction': '', 'verbose_name': 'Owner'},
                           'matrix_authorisation_authority': {'default_direction': '', 'verbose_name': 'Authority'}
                           }


    default_sort_field = 'matrix_id'

    paginate_by = 10

    template_name = 'host/list_benches.html'

    model = MatrixSummary

    context_object_name = 'matrix_summary_list'


    def get_queryset(self):

        sort_parameter = ''

        if self.request.GET.get('sort', None) == None:

            sort_parameter = 'matrix_id'

        else:

            sort_parameter = self.request.GET.get('sort', None)

        return bench_list_by_user_and_direction(self.request.user, sort_parameter)


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        data = get_header_data(self.request.user)

        context.update(data)

        return context
