from datetime import datetime, timedelta
import logging

from BeautifulSoup import BeautifulSoup
from icalendar import Calendar, Event
from pacific_tzinfo import Pacific

def processPage(html):
    soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
    date = None
    matches = []
    lines = [f.text for f in soup.findAll('font')]
    logging.info(str(len(lines)) + ' lines in the html found')
    for line in lines:
        newDate = parseDate(line)
        if newDate:
            date = newDate
            logging.debug('updated date to {0}'.format(date))
        else:
            match = parseMatch(line, date)
            logging.debug('parseMatch returned {0}'.format(match))
            if match:
                matches.append(match)
                logging.debug('added match: {0}'.format(match))
    return matches

def parseDate(line):
    try:
        return datetime.strptime(''.join(line.split()[:2]), '%A,%m/%d/%y')
    except:
        return None

def parseMatch(line, date):
    logging.debug('parsing "{0}"'.format(line))
    try:
        teams = line.split("vs")
        time = datetime.strptime(teams[0].split()[0], '%I:%M%p').time()
        logging.debug('extracted {0} as time'.format(time))
        dark = ' '.join(teams[0].split()[1:])
        logging.debug('dark = {0}'.format(dark))
        white = teams[1].strip()
        logging.debug('white = {0}'.format(white))
        return Match(dark = dark,
                     white = white,
                     time = datetime.combine(date, time)
                                    .replace(tzinfo=Pacific))
    except:
        return None

class Match(object):
    def __init__(self, time, dark, white):
        self.dark = dark
        self.white = white
        self.time = time

    def __str__(self):
        return "{0}(dark) vs {1}(white) @ {2}".format(
            self.dark, self.white, self.formatted_time())

    def __repr__(self):
        return str(self)

    def color(self, my_name):
        if self.white == my_name:
            return 'White'
        elif self.dark == my_name:
            return 'Dark'
        else:
            return None

    def opponent(self, my_name):
        if self.white == my_name:
            return self.dark
        elif self.dark == my_name:
            return self.white
        else:
            return None

    def formatted_time(self):
        return self.time.strftime("%a, %x %I:%M%p")

    def contains_team(self, team_name):
        return self.white == team_name or self.dark == team_name

def eventFromMatch(match, team, reminder=None):
    if team == None:
        color = match.white + ' (white)'
        opponent = match.dark + ' (dark)'
    elif match.white == team:
        color = 'White'
        opponent = match.dark
    elif match.dark == team:
        color = 'Dark'
        opponent = match.white
    else:
        return None

    evt = Event()
    evt.add('summary', 'Soccer - {0} vs. {1}'.format(color, opponent))
    evt.add('dtstart', match.time)
    evt.add('dtend', match.time + timedelta(hours = 1))
    return evt

def calendarFromMatches(matches, team):
    cal = Calendar()
    cal.add('version', '2.0')
    cal.add('prodid', '-//com/appspot/SambaSchedule//NONSGML v1.0//EN')
    for match in matches:
        evt = eventFromMatch(match, team)
        if evt:
            cal.add_component(evt)
    return cal

if __name__ == '__main__':
    html = open('sample.html').read()
    soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
    matchstr = '   8:45pm  Mad Samba                      vs Tuxedos'
    datestr = 'Tuesday, 12/20/11 (week 1/10)'
    d = parseDate(datestr)
    t = datetime.strptime('8:45pm', '%I:%M%p')
    matches = processPage(html)
    cal = calendarFromMatches(matches, 'The Captain')
