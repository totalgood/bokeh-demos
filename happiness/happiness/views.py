from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from .models import Team


class ContextMixin(object):

    def get_context_data(self, *args, **kwargs):
        context = super(ContextMixin, self).get_context_data(*args, **kwargs)
        users = User.objects.filter(is_superuser=False).order_by('username')
        teams = Team.objects.all().order_by('name')
        context.update(all_users=users, all_teams=teams)
        return context


class HomeView(ContextMixin, TemplateView):
    template_name = 'happiness/home.html'


class IndividualDashboardView(ContextMixin, DetailView):
    template_name = 'happiness/dashboard_individual.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, *args, **kwargs):
        context = super(IndividualDashboardView, self).get_context_data(*args, **kwargs)
        context.update(dashboard='individual')
        return context


class TeamDashboardView(ContextMixin, DetailView):
    template_name = 'happiness/dashboard_team.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, *args, **kwargs):
        context = super(TeamDashboardView, self).get_context_data(*args, **kwargs)
        context.update(dashboard='team')
        return context
