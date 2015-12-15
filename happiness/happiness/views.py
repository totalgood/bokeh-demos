import numpy as np

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
        plot_source = bokeh_session.document.get_model_by_name('source')
        plot_source.data = self.get_user_data()
        script = autoload_server(None, app_path='/individual', session_id=bokeh_session.id)
        return script

    def get_context_data(self, *args, **kwargs):
        context = super(IndividualDashboardView, self).get_context_data(*args, **kwargs)
        context.update(dashboard='individual', script=self.get_bokeh_script())
        return context

    def get_user_data(self):
        user = self.object
        if user.employee:
            h_set = user.employee.happiness_set.all()
            dates = h_set.values_list('date', flat=True)
            x = np.array(dates)
            happinesses = h_set.values_list('happiness', flat=True)
            y = np.array(happinesses)
        else:
            x = []
            y = []
        return dict(x=x, y=y)


class TeamDashboardView(ContextMixin, DetailView):
    template_name = 'happiness/dashboard_team.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, *args, **kwargs):
        context = super(TeamDashboardView, self).get_context_data(*args, **kwargs)
        context.update(dashboard='team')
        return context
