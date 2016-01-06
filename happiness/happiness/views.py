import datetime
from bokeh.client import pull_session
from bokeh.embed import autoload_server

from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from .models import Team, Happiness, Employee
from .forms import HappinessForm


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
        bokeh_session = pull_session(session_id=None, url='http://localhost:5006/individual/')
        # We want to make this less cumbersome see https://github.com/bokeh/bokeh/issues/3349
        employee_source = bokeh_session.document.get_model_by_name('employee_pk_source')
        if hasattr(self.object, 'employee'):
            employee_source.data = dict(employee_pk=[self.object.employee.pk])
        else:
            employee_source.data = dict(employee_pk=[-1])
        script = autoload_server(None, app_path='/individual', session_id=bokeh_session.id)
        return script

    def get_context_data(self, *args, **kwargs):
        context = super(IndividualDashboardView, self).get_context_data(*args, **kwargs)
        happiness = Happiness(date=datetime.date.today())
        context.update(
            dashboard='individual',
            script=self.get_bokeh_script(),
            form=HappinessForm(instance=happiness)
        )
        return context


class TeamDashboardView(ContextMixin, DetailView):
    template_name = 'happiness/dashboard_team.html'
    model = User
    context_object_name = 'user'

    def get_bokeh_script(self):
        bokeh_session = pull_session(session_id=None, url='http://localhost:5006/team/')
        employee_source = bokeh_session.document.get_model_by_name('employee_pk_source')
        if hasattr(self.object, 'employee'):
            employee_source.data = dict(employee_pk=[self.object.employee.pk])
        else:
            employee_source.data = dict(employee_pk=[-1])
        script = autoload_server(None, app_path='/team', session_id=bokeh_session.id)
        return script

    def get_context_data(self, *args, **kwargs):
        context = super(TeamDashboardView, self).get_context_data(*args, **kwargs)
        context.update(
            dashboard='team',
            script=self.get_bokeh_script(),
        )
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
