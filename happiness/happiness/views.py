import datetime
from bokeh.client import push_session
from bokeh.embed import autoload_server

from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from .models import Team, Happiness
from .forms import HappinessForm
from .viz import IndividualPlot, IndividualsPlot, TeamPlot, TeamsPlot


class ContextMixin(object):

    def get_context_data(self, *args, **kwargs):
        context = super(ContextMixin, self).get_context_data(*args, **kwargs)
        users = User.objects.filter(is_superuser=False).order_by('username')
        teams = Team.objects.all().order_by('name')
        context.update(all_users=users, all_teams=teams)
        return context

    def get_bokeh_script(self, document):
        bokeh_session = push_session(document)
        script = autoload_server(None, session_id=bokeh_session.id)
        bokeh_session.close()
        return script


class HomeView(ContextMixin, TemplateView):
    template_name = 'happiness/home.html'


class IndividualDashboardView(ContextMixin, DetailView):
    template_name = 'happiness/dashboard_individual.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, *args, **kwargs):
        context = super(IndividualDashboardView, self).get_context_data(*args, **kwargs)
        happiness = Happiness(date=datetime.date.today())
        context.update(
            dashboard='individual',
            form=HappinessForm(instance=happiness)
        )
        if hasattr(self.object, 'employee'):
            individual = IndividualPlot(user=self.object)
            context.update(individual_script=self.get_bokeh_script(individual.document))
        if hasattr(self.object, 'team'):
            individuals = IndividualsPlot(user=self.object)
            context.update(individuals_script=self.get_bokeh_script(individuals.document))
        return context


class TeamDashboardView(ContextMixin, DetailView):
    template_name = 'happiness/dashboard_team.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, *args, **kwargs):
        context = super(TeamDashboardView, self).get_context_data(*args, **kwargs)
        context.update(
            dashboard='team',
        )
        if hasattr(self.object, 'employee'):
            team = TeamPlot(user=self.object)
            context.update(team_script=self.get_bokeh_script(team.document))
        if hasattr(self.object, 'team'):
            teams = TeamsPlot(user=self.object)
            context.update(teams_script=self.get_bokeh_script(teams.document))
        return context


#################### Happiness Views

class AddHappinessView(CreateView):
    model = Happiness
    fields = ('date', 'happiness')
    template_name = 'happiness/add_happiness.html'

    def dispatch(self, *args, **kwargs):
        self.user_pk = kwargs.get('pk')
        return super(AddHappinessView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        user = User.objects.get(pk=self.user_pk)
        form.instance.employee = user.employee
        return super(AddHappinessView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(AddHappinessView, self).get_context_data(*args, **kwargs)
        context.update(user=User.objects.get(pk=self.user_pk))
        return context
