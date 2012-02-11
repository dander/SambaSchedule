import cgi
import logging
import os

import webapp2
import jinja2
from google.appengine.ext import db

import ScheduleProcessor
import CalendarGenerator

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {'teams': teams}
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))


class TeamSchedule(webapp2.RequestHandler):
    def get(self, team_name):
        template = jinja_environment.get_template('schedule.html')
        template_values = {
            'team_name': team_name,
            'games': [{'time':m.formatted_time(),
                       'color':m.color(team_name),
                       'opponent':m.opponent(team_name)}
                      for m in matches
                      if m.contains_team(team_name)]
            }
        self.response.out.write(template.render(template_values))


class TeamCalendar(webapp2.RequestHandler):
    def get(self, team_name):
        try:
            reminder = int(self.request.get('reminder'))
        except:
            reminder = None
        self.response.out.write(
            str(CalendarGenerator.calendarFromMatches(
                matches, team_name, reminder)))

html = open('sample.html').read()

matches = ScheduleProcessor.processPage(html)
logging.info(str(len(matches)) + ' matches found')

teams = set([m.white for m in matches] + [m.dark for m in matches])
logging.info(str(len(teams)) + ' teams found')

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPage, name='home'),
    webapp2.Route(r'/<team_name>', handler=TeamSchedule, name='team'),
    webapp2.Route(r'/<team_name>/calendar.ics', handler=TeamCalendar,
                  name='calendar')
    ], debug=True)
