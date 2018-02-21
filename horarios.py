from icalendar import Calendar
from urllib.request import urlopen
from datetime import date, datetime
import os.path
from time import ctime
class Horario:
    ruta = 'static/offices/A.ics'
    salas = {
        'A': 'https://calendar.google.com/calendar/ical/uceva.edu.co_l5k4pi6mpj74lf8pm4khsjvsso%40group.calendar.google.com/public/basic.ics',
        'B': 'https://calendar.google.com/calendar/ical/uceva.edu.co_uk9iq9n9k65dhtspjnutpa6peo%40group.calendar.google.com/public/basic.ics',
        'C': 'https://calendar.google.com/calendar/ical/uceva.edu.co_mulrou6itu1adg7h5ldlbi09mc%40group.calendar.google.com/public/basic.ics',
        'D': 'https://calendar.google.com/calendar/ical/uceva.edu.co_qb6i8h30m8c5bveqv8udd0ilgs%40group.calendar.google.com/public/basic.ics',
        'E': 'https://calendar.google.com/calendar/ical/uceva.edu.co_sqr8ph2931r7lcaccq9tii31e4%40group.calendar.google.com/public/basic.ics',
        'F': 'https://calendar.google.com/calendar/ical/uceva.edu.co_5p6pspppml9m1mpbddht8d7qu0%40group.calendar.google.com/public/basic.ics',
        'G': 'https://calendar.google.com/calendar/ical/uceva.edu.co_gdrqrq8prv9fp26tks5ijeoa3c%40group.calendar.google.com/public/basic.ics'
    }
    def getCalendar(self):
        for k, v in self.salas.items():
            with urlopen(v) as r:
                with open("static/offices/"+k + ".ics", "wb") as f:
                    f.write(r.read())
                    print("%s descargado correctamente." % k)

    def getHorario(self):
        lista = list()
        if not os.path.isfile(self.ruta):
            self.getCalendar()
        filetime = os.path.getmtime(self.ruta)
        creacion = datetime.strptime(ctime(filetime), "%a %b %d %H:%M:%S %Y")
        if creacion.month + 1 == date.today().month:
            self.getCalendar()
        for name in self.salas.keys():
            with open('static/offices/'+name+'.ics', 'rb') as ics_file:
                ics_cal = Calendar.from_ical(ics_file.read())
                for anio in range(2010, date.today().year + 1):
                    total = 0

                    for component in ics_cal.walk():
                        if component.name == "VEVENT":
                            fin = component.decoded('dtend')
                            diferencia=(fin-component.decoded('dtstart')).total_seconds()*0.000277778
                            if fin.year == anio:
                                total += diferencia if diferencia < 10 else (diferencia/24.0)*8
                    lista.append({'uso':total, 'anio':anio, 'name':name})
        return lista

