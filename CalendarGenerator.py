from datetime import timedelta
import logging

from icalendar import Calendar, Event, Alarm

import ScheduleProcessor

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

    if reminder:
        evt.add_component(createReminder(reminder))

    return evt

def calendarFromMatches(matches, team, reminder=None):
    cal = Calendar()
    cal.add('version', '2.0')
    cal.add('prodid', '-//com/appspot/SambaSchedule//NONSGML v1.0//EN')
    for match in matches:
        evt = eventFromMatch(match, team, reminder)
        if evt:
            cal.add_component(evt)
    return cal

def createReminder(minutes):
    a = Alarm()
    a.add('ACTION', 'DISPLAY')
    a.add('DESCRIPTION', 'starting soon...')
    a.add('TRIGGER', timedelta(minutes = -minutes))
    return a

if __name__ == '__main__':
    html = open('sample.html').read()
    matches = ScheduleProcessor.processPage(html)
    cal = calendarFromMatches(matches, 'The Captain')
    a = createReminder(35)
