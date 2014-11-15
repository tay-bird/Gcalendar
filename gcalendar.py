class Gcalendar():
    
    def __init__(self, service):
        self.service = service

    # Returns a list of calendars formatted as calendar objects.
    def list_calendars(self):
        page_token = None
        results = []
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                results.append(calendar_list_entry)
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return results

    # Returns a calendar ID by calendar name.
    def get_calendar_id(self, name):
        calendars = self.list_calendars()
        for cal in calendars:
            if cal['summary'] == name:
                return cal['id']
        return None
    
    # Creates a new calendar with the given name.    
    def add_calendar(self, name):
        calendar = { 'summary': name }
        self.service.calendars().insert(body=calendar).execute()

    # Returns a list of events formatted as strings.
    def list_events(self, calendarId):
        page_token = None
        results = []
        while True:
            events = self.service.events().list(calendarId=calendarId, pageToken=page_token).execute()
            for event in events['items']:
                results.append(event['summary'])
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return results
    
    # Returns a dictionary of events formatted as Event objects.
    def get_events(self, calendarId):
        page_token = None
        results = []
        while True:
            events = self.service.events().list(calendarId=calendarId, pageToken=page_token).execute()
            for event in events['items']:
	    	if event['status'] != u'cancelled':
                    results.append(Event(event))
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return results

    # Returns a dictionary of events.
    def get_events_raw(self, calendarId):
        page_token = None
        results = []
        while True:
            events = self.service.events().list(calendarId=calendarId, pageToken=page_token).execute()
            for event in events['items']:
                results.append(event)
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return results

    # Returns an Event object representing the given event ID.
    def get_event(self, calendarId, eventId):
        event = self.service.events().get(calendarId=calendarId, eventId=eventId).execute()
        return Event(event)
    
    # Returns the raw event provided by Google representing the given ID.
    def get_event_raw(self, calendarId, eventId):
        event = self.service.events().get(calendarId=calendarId, eventId=eventId).execute()
	return event

    # Adds an event to the calendar.
    def add_event(self, calendarId, summary, desc, date, allday, startT=None, endT=None):
    	event = Event()
        event.summary = summary
        event.description = desc
        event.startDate = date.split(" ")[0]
        event.endDate = date.split(" ")[0]
        if not allday:
            event.startTime = date.split(" ")[1]
            event.endTime = date.split(" ")[1]

	created_event = self.service.events().insert(calendarId=calendarId, body=event.json()).execute()
        return created_event['id']

    # Removes an event from the calendar.
    def remove_event(self, calendarId, eventId):
        try:
            self.service.events().delete(calendarId=calendarId, eventId=eventId).execute()
            return 1
        except:
            return 0


# Provides utilities for Event objects through the CalAp.get_events function.
class Event:

    def __init__(self, event=None):
        if event:
	    self.id = event['id']
	    self.summary = event['summary']
	    try:
                self.description = event['description']
            except KeyError:
                self.description = None
            try:
                _start = event['start']['dateTime']
                _end = event['end']['dateTime']
                self.startDate = _start.split("T")[0]
                self.startTime = _start.split("T")[1].split("-")[0]
                self.endDate = _end.split("T")[0]
                self.endTime = _end.split("T")[1].split("-")[0]
                self.allday = False
                self.eventType = None
            except KeyError:
                _start = event['start']['date']
                _end = event['end']['date']
                self.startDate = _start
                self.startTime = None
                self.endDate = _end
                self.endTime = None
                self.allday = True
                self.eventType = None
        else:
            self.summary = None
            self.description = None
            self.startDate = None
            self.endDate = self.startDate
            selfstartTime = None
            self.endTime = None
            self.allday = None
            self.eventType = None


    def __repr__(self):
        return '%s(%s)' % (self.__class__, self.summary)

    def json(self):
        event = {
            'summary': self.summary,
            'start': {
                'dateTime': self.startDate + 'T' + self.startTime + ':00.000-07:00'
                },
            'end': {
                'dateTime': self.endDate + 'T' + self.startTime + ':00.000-07:00'
                },
            'description': self.description
            }
        return event
