import numpy as np

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Avg

from .viz.individuals import update_individuals_data
from .viz.team import update_team_data
from .viz.teams import update_teams_data


class Team(models.Model):
    name = models.CharField(max_length=20, unique=True)
    manager = models.OneToOneField(User)

    def __str__(self):
        return '%s (%s)' % (self.name, self.manager.first_name)

    def get_team_dates_happiness(self, start_date=None, end_date=None):
        employees = self.employee_set.all()
        h_set = Happiness.objects.filter(employee__in=employees).order_by('date')
        average_happinesses = h_set.values('date').annotate(average_happiness=Avg('happiness'))
        dates = average_happinesses.values_list('date', flat=True)
        happinesses = average_happinesses.values_list('average_happiness', flat=True)
        return (np.array(dates), np.array(happinesses))


class Employee(models.Model):
    user = models.OneToOneField(User)
    teams = models.ManyToManyField('happiness.Team')

    def __str__(self):
        return '%s (%s)' % (self.user.first_name, self.teams_list)

    @property
    def teams_list(self):
        return ', '.join([team.name for team in self.teams.all()])

    def get_dates_happiness(self):
        h_set = self.happiness_set.order_by('date')
        dates = h_set.values_list('date', flat=True)
        happinesses = h_set.values_list('happiness', flat=True)
        return (np.array(dates), np.array(happinesses))


class Happiness(models.Model):
    employee = models.ForeignKey(Employee)
    date = models.DateField()
    happiness = models.DecimalField(decimal_places=0, max_digits=1)

    unique_together = (('employee', 'date'),)

    def __str__(self):
        return '%s %s %s' % (self.employee.user.first_name, self.happiness, self.date)

    def get_absolute_url(self):
        return reverse('individual', kwargs={'pk': self.employee.user.pk})

    def save(self, *args, **kwargs):
        super(Happiness, self).save(*args, **kwargs)

        # When a new value of Happiness is saved, we update all the data for the bokeh sessions.
        # This is not optimized. Things that could be improved:
        #
        # - Send this off to an external process so that the user gets a quicker response
        # - Only update for users affected by this data (only get affected UserSessions)

        for us in UserSession.objects.all():
            # Process "individuals" plots
            if us.bokeh_session_individuals:
                update_individuals_data(user=us.user, bokeh_session_id=us.bokeh_session_individuals)
            # Process "team" plots
            if us.bokeh_session_team:
                update_team_data(user=us.user, bokeh_session_id=us.bokeh_session_team)
            # Process "teams" plots
            if us.bokeh_session_teams:
                update_teams_data(user=us.user, bokeh_session_id=us.bokeh_session_teams)


class UserSession(models.Model):
    user = models.ForeignKey(User)
    bokeh_session_individual = models.CharField(max_length=64)
    bokeh_session_individuals = models.CharField(max_length=64)
    bokeh_session_team = models.CharField(max_length=64)
    bokeh_session_teams = models.CharField(max_length=64)
