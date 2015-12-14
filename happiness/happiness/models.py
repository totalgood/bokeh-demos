from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=20)
    manager = models.OneToOneField(User)

    def __str__(self):
        return '%s (%s)' % (self.name, self.manager.first_name)


class Employee(models.Model):
    user = models.OneToOneField(User)
    teams = models.ManyToManyField('happiness.Team')

    def __str__(self):
        return '%s (%s)' % (self.user.first_name, self.teams_list)

    @property
    def teams_list(self):
        return ', '.join([team.name for team in self.teams.all()])


class Happiness(models.Model):
    employee = models.ForeignKey(Employee)
    date = models.DateField()
    happiness = models.DecimalField(decimal_places=0, max_digits=1)

    unique_together = (('employee', 'date'),)

    def __str__(self):
        return '%s %s %s' % (self.employee.user.first_name, self.happiness, self.date)
