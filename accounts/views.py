from django.urls import reverse_lazy
from allauth.account.views import PasswordChangeView


class MyPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        success_url = reverse_lazy("account_login")
        
        return success_url