from bokeh.client import pull_session
from bokeh.embed import autoload_server

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

    def get_bokeh_script(self):
        bokeh_session = pull_session(session_id=None, url='ws://localhost:5006/individual/ws')
        source = bokeh_session.document.get_model_by_name('employee_pk_source')
        source.data = dict(employee_pk=[self.object.employee.pk])
        script = autoload_server(None, app_path='/individual', session_id=bokeh_session.id)
        return script

    def get_context_data(self, *args, **kwargs):
        context = super(IndividualDashboardView, self).get_context_data(*args, **kwargs)
        context.update(dashboard='individual', script=self.get_bokeh_script())
        return context


class TeamDashboardView(ContextMixin, DetailView):
    template_name = 'happiness/dashboard_team.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, *args, **kwargs):
        context = super(TeamDashboardView, self).get_context_data(*args, **kwargs)
        context.update(dashboard='team')
        return context
