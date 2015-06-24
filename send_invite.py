from icalendar import (Calendar, Event,
                       Timezone, TimezoneDaylight, TimezoneStandard)
from flanker import mime


def create_ical_object():
    cal = Calendar()
    cal['prodid'] = '-//Mozilla.org/NONSGML Mozilla Calendar V1.1//EN'
    cal['version'] = '2.0'
    cal['method'] = 'REQUEST'

    tz = Timezone()
    tz['tzid'] = 'America/Los_Angeles'
    tz['x-lic-location'] = 'America/Los_Angeles'

    daylight = TimezoneDaylight()
    daylight['tzoffsetfrom'] = '-0800'
    daylight['tzoffsetto'] = '-0700'
    daylight['tzname'] = 'PDT'
    daylight['dtstart'] = '19700308T020000'
    daylight.add('rrule', '', parameters={'freq': '3DYEARLY',
                                          'byday': '3D2SU',
                                          'bymonth': '3D3'})
    tz.add_component(daylight)

    std = TimezoneStandard()
    std['tzoffsetfrom'] = '-0700'
    std['tzoffsetto'] = '-0800'
    std['tzname'] = 'PST'
    std['dtstart'] = '19701101T020000'
    std.add('rrule', '', parameters={'freq': '3DYEARLY',
                                     'byday': '3D1SU',
                                     'bymonth': '3D11'})
    tz.add_component(std)

    cal.add_component(tz)

    event = Event()
    event['created'] = '20150623T162711Z'
    event['last-modified'] = '20150623T162740Z'
    event['dtstamp'] = '20150623T162740Z'
    event['uid'] = '51ae3508-fe9e-4519-9756-6b4cc4fcae05'
    event['summary'] = 'Nylas Developer Night'
    event.add('organizer', 'mailto:spang@nylas.com',
              parameters={'rsvp': '3DTRUE', 'partstat': '3DNEEDS-ACTION',
                          'role': 'RDREQ-PARTICIPANT'})
    event.add('attendee', 'mailto:christine@spang.cc',
              parameters={'rsvp': '3DTRUE', 'partstat': '3DNEEDS-ACTION',
                          'role': '3DREQ-PARTICIPANT'})
    event['transp'] = 'OPAQUE'
    event['dtstart'] = '20150624T190000'
    event['dtend'] = '20150624T210000'

    cal.add_component(event)

    return cal


def create_cal_mime_msg(to_addr, from_addr, ical_obj):
    ical_string = ical_obj.to_string()

    event = [sc for sc in ical_obj.subcomponents if sc.name == 'VEVENT']
    assert len(event) == 1

    msg = mime.create.multipart('mixed')
    body = mime.create.multipart('alternative')
    # TODO: fix body
    body.append(
        mime.create.text('html', '<p>A new event!</p>'),
        mime.create.text('calendar;method=REPLY', ical_string))

    attachment = mime.create.attachment(
        'text/calendar',
        ical_string,
        'invite.ics',
        disposition='attachment')

    msg.append(body)
    msg.append(attachment)

    msg.headers['To'] = to_addr
    msg.headers['Reply-To'] = to_addr
    msg.headers['From'] = from_addr
    msg.headers['Subject'] = 'RSVP to "{}"'.format(event[0].summary)

if __name__ == '__main__':
    print create_ical_object().to_string()
