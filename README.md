# Gcalendar.
This package can be used to fetch calendar and event information from **Google Calendar**.

## Usage.
Make sure the oauth2client and apiclient packages are in your project's working directory. You will need to use the oauth2client package to get a valid *credentials* object. This tutorial assumes you have successfully done this.

Make a connection and authorize the credentials.

    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build("calendar", "v3", http=http)

Pass the authorization to Gcalender.

    gcalendar = Gcalendar(service)

You may now access your Google Calendar. All calendars will have a default calendar with an id of *primary*. Let's get a list of events.

    events = gcalendar.get_events("primary")
    
    for event in events:
        print event.summary
        # "A Party"
        # "Dentist Appt"
        # "Build Better Calendar."
        # "Fistfight w/ Putin."

## Event Objects.

Gcalendar represents calendar events with its own Events object.

    events = gcalendar.get_events("primary")
    some_event = events[0]

    print some_event  # gcalendar.gcalendar.Event(A Party)
    print some_event.summary  # "A Party"
    print some_event.description  # "There's going to be a party!"
    print some_event.startDate  # "20XX-MM-DD"
    print some_event.startTime  # "24:MM:SS"
    print some_event.allday  # False

If you would like to get the raw [Google Calendar API event](https://developers.google.com/google-apps/calendar/v3/reference/events), you may do so.

    events = gcalendar.get_events_raw("primary")
    some_raw_event = events[0]
