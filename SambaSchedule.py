import cgi
import logging
import webapp2
import jinja2
import os
from google.appengine.ext import db
import ScheduleProcessor

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'teams': teams
        }
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

class TeamSchedule(webapp2.RequestHandler):
    def get(self, team_name):
        for m in matches:
            if m.white == team_name or m.dark == team_name:
                self.response.out.write(str(m) + '\n')

html = open('sample.html').read()
matches = ScheduleProcessor.processPage(html)
logging.info(str(len(matches)) + ' matches found')

teams = set([m.white for m in matches] + [m.dark for m in matches])
logging.info(str(len(teams)) + ' teams found')

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPage, name='home'),
    webapp2.Route(r'/<team_name>', handler=TeamSchedule, name='team')
    ], debug=True)
