from django.contrib.auth.models import User
from django.views.generic.base import TemplateView

from .models import Team


class BaseView(TemplateView):

    def get_context_data(self, *args, **kwargs):
        context = super(BaseView, self).get_context_data(*args, **kwargs)
        users = User.objects.filter(is_superuser=False).order_by('username')
        teams = Team.objects.all().order_by('name')
        context.update(users=users, teams=teams)
        return context


class HomeView(BaseView):
    template_name = 'happiness/home.html'


class IndividualDashboardView(BaseView):
    template_name = 'happiness/home.html'


class TeamDashboardView(BaseView):
    template_name = 'happiness/home.html'
