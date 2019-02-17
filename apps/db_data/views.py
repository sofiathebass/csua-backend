import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_page

from .models import Event, Officer, Politburo, Sponsor
from .constants import DAYS_OF_WEEK, OH_TIMES


class EventsView(TemplateView):
    template_name = "events.html"

    def get_context_data(request):
        context = {}
        context["events"] = Event.objects.filter(
            enabled=True, date__gte=datetime.date.today()
        )
        return context


# @cache_page(3 * 60)
def officers(request):
    officer_queryset = Officer.objects.filter(enabled=True)
    calendar_contents = [
        [hour]
        + [
            officer_queryset.filter(office_hours=day + " " + hour)
            for day in DAYS_OF_WEEK
        ]
        for hour in OH_TIMES
    ]

    calendar = {"days": DAYS_OF_WEEK, "hours": OH_TIMES, "contents": calendar_contents}
    return render(
        request,
        "officers.html",
        {"officer_list": officer_queryset, "calendar": calendar},
    )


def politburo(request):
    return render(request, "politburo.html", {"pb": Politburo.objects.all()})


def sponsors(request):
    sponsors_current = Sponsor.objects.filter(current=True)
    sponsors_past = Sponsor.objects.filter(current=False)
    return render(
        request,
        "sponsors.html",
        {"sponsors_current": sponsors_current, "sponsors_past": sponsors_past},
    )


def json(request):
    officers_all = Officer.objects.filter(enabled=True).order_by("last_name")
    serialized_officers = [
        {
            "name": o.first_name + " " + o.last_name,
            "hours": o.office_hours,
            "img": o.photo1.url if o.photo1 else None,
            "img2": o.photo2.url if o.photo2 else None,
            "quote": o.blurb,
            "rootStaff": o.root_staff,
            "tutorSubjects": o.tutor_subjects,
        }
        for o in officers_all
    ]

    pb_arr = Politburo.objects.all()
    pb_dict = {}
    for pb_member in pb_arr:
        pb_dict[pb_member.position] = {
            "name": pb_member.officer.first_name + " " + pb_member.officer.last_name,
            "img": pb_member.officer.photo1.url if pb_member.officer.photo1 else None,
        }

    events_all = Event.objects.order_by("date")
    serialized_events = [
        {
            "name": e.name,
            "location": e.location,
            "date": e.date.strftime("%A - %m/%d"),
            "time": e.time,
            "description": e.description,
            "href": e.link,
        }
        for e in events_all
    ]

    sponsors_all = Sponsor.objects.order_by("name")
    serialized_sponsors = [
        {
            "name": s.name,
            "href": s.url,
            "type": s.description,
            "img": s.photo.url if s.photo else None,
            "current": s.current,
        }
        for s in sponsors_all
    ]

    result = {
        "officers": serialized_officers,
        "pb": pb_dict,
        "events": serialized_events,
        "sponsors": serialized_sponsors,
    }
    return JsonResponse(result)
