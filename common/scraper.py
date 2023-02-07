import requests as req
from bs4 import BeautifulSoup

def room_plan(**kwargs):
    url = 'http://moria.umcs.lublin.pl/room/'

    weekdays = {'poniedziałek': "monday", 'wtorek':"tuesday", 'środa':"wednesday", 'czwartek':"thursday", 'piątek':"friday"}
    result = {"monday": [], "tuesday": [], "wednesday": [], "thursday": [], "friday":[]}

    room_id = kwargs.get("room_id")
    if not isinstance(room_id, int):
        return False

    response = req.get(url+str(room_id))
    soup = BeautifulSoup(response.content, "html.parser")
    plan = soup.find("div", {"class": "planrange"}).find("div", {"class": 'plancontainer'})
    blocks = plan.find_all("div", {"class": "activity_block"})

    for block in blocks:
        attrs = block.attrs

        weekday = weekdays.get(attrs.get("data-weekdaytext"))
        start = attrs.get("data-starttime")
        end = attrs.get("data-endtime")

        obj = block.find("div", {"class": "activity_block_top"})
        subject = obj.find("a", {"class": "subject"}).getText()
        infos = obj.find("div", {"class": "itemlist"}).find_all("a")
        details = []
        for info in infos:
            attrs = info.attrs
            title = attrs.get("title")
            if title is not None:
                details.append(attrs.get("title"))
        if len(details) > 1:
            course = details.pop(-1)
        else:
            course = None
        result[weekday].append({"subject": subject,
                                "teachers": details,
                                "course": course,
                                "start": start,
                                "end": end})
    return result
