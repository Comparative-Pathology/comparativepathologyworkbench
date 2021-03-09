from django import forms

from inlineedit.adaptors import BasicAdaptor


class BlockedAdaptor(BasicAdaptor):
    # "Demonstrate adaptor level permission setting"
    def has_edit_perm(self, user):

        owner = self._model.owner

        allow_flag = False

        if owner == user:

            allow_flag = True

        else:

            if user.is_superuser:

                allow_flag = True


        return allow_flag
