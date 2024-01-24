import PySimpleGUI as sg
from icalendar import Calendar, Event
from datetime import datetime
import pytz
import os.path


def add_event_to_ics_file(start_date, end_date, event_name, additional_notes, location):
    # Überprüfe, ob die Datei bereits existiert
    ics_filename = "termine_jdk.ics"
    if os.path.isfile(ics_filename):
        # Öffne die Datei und lese die vorhandenen Ereignisse
        with open(ics_filename, 'rb') as f:
            cal = Calendar.from_ical(f.read())
            events = cal.walk('VEVENT')

        # Erstelle ein neues Ereignis
        event = Event()
        event.add('summary', event_name)
        event.add('dtstart', start_date)
        event.add('dtend', end_date)
        event.add('description', additional_notes)
        event.add('location', location)
        event.add('dtstamp', datetime.now(tz=pytz.timezone('Europe/Berlin')))

        # Bilde die UID aus dem Summary und dem DTSTART
        uid_str = f"{event_name}{start_date.strftime('%Y%m%dT%H%M%S')}"
        event.add('uid', uid_str)

        # Füge das Ereignis zur Kalender-Instanz hinzu
        cal.add_component(event)

        # Speichere die aktualisierte Datei
        with open(ics_filename, 'wb') as f:
            f.write(cal.to_ical())

        sg.popup("Das Ereignis wurde erfolgreich hinzugefügt!")
    else:
        # Erstelle eine neue Datei mit dem Ereignis
        cal = Calendar()
        cal.add('prodid', '-//My calendar product//mxm.dk//')
        cal.add('version', '2.0')

        event = Event()
        event.add('summary', event_name)
        event.add('dtstart', start_date)
        event.add('dtend', end_date)
        event.add('description', additional_notes)
        event.add('location', location)
        event.add('dtstamp', datetime.now(tz=pytz.timezone('Europe/Berlin')))

        # Bilde die UID aus dem Summary und dem DTSTART
        uid_str = f"{event_name}{start_date.strftime('%Y%m%dT%H%M%S')}"
        event.add('uid', uid_str)

        cal.add_component(event)

        with open(ics_filename, 'wb') as f:
            f.write(cal.to_ical())

        sg.popup("Die Datei wurde erfolgreich erstellt!")


# Erstelle das Userinterface
layout = [
    [sg.Text('Startdatum (DD.MM.YYYY):'), sg.InputText()],
    [sg.Text('Startzeit (HH:MM):'), sg.InputText()],
    [sg.Text('Enddatum (DD.MM.YYYY):'), sg.InputText()],
    [sg.Text('Endzeit (HH:MM):'), sg.InputText()],
    [sg.Text('Name des Termins:'), sg.InputText()],
    [sg.Text('Zusätzliche Notizen:'), sg.InputText()],
    [sg.Text('Ort:'), sg.InputText()],
    [sg.Button('Erstellen')]
]

window = sg.Window('ICS-Datei erstellen', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Erstellen':
        # Konvertiere die Eingabe in das richtige Format
        start_date = datetime.strptime(values[0], '%d.%m.%Y')
        start_time = datetime.strptime(values[1], '%H:%M')
        end_date = datetime.strptime(values[2], '%d.%m.%Y')
        end_time = datetime.strptime(values[3], '%H:%M')
        start_date = datetime.combine(start_date, start_time.time(), tzinfo=pytz.timezone('Europe/Berlin'))
        end_date = datetime.combine(end_date, end_time.time(), tzinfo=pytz.timezone('Europe/Berlin'))
        event_name = values[4]
        additional_notes = values[5]
        location = values[6]

        # Füge das Ereignis zur ICS-Datei hinzu
        add_event_to_ics_file(start_date, end_date, event_name, additional_notes, location)

window.close()
