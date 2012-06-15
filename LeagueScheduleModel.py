import datetime

from google.appengine.ext import db

refresh_time = datetime.timedelta(hours = 1)

class LeagueSchedule(db.Model):
	name = db.StringProperty()
	source_url = db.StringProperty(required = True)
	html = db.StringProperty(required = True)
	model = db.UserProperty(required = True)
	retrieved = db.DateProperty(required = True)

def get_LeagueSchedule(url):
	ls_k = db.Key.from_path('LeagueSchedule', url)
	schedule = db.get(ls_k)
	if schedule is None or (datetime.datetime.now() - schedule.retrieved > refresh_time):
		#update schedule
		pass
	return schedule