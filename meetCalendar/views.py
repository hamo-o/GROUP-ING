import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from groups.models import Group

from meetings.views import changeStatus

from .utils import dateContinue
from .forms import meetDayForm, meetTravelForm
from django.contrib import messages
from django.db.models import Max,Min

from meetCalendar.models import meetDay, meetDayVote, meetTravel, meetTravelInfo,meetDayInfo, meetTravelVote
from logins.models import User

from meetings.models import Meetings

# Create your views here.


def main(request, meetId):

    #test = meetTravelInfo.objects.filter(meetId=meetId)
    #print(test[0].meetUsers.count())
    #test2 = test.filter(year=2022,month=8,day=18)
    #print(test2[0].meetUsers.all())
    #users = test[0].meetUsers.all()
    #print(users[0].username)

    groupId = Meetings.objects.get(id=meetId).meetGroupId.id

    context = {
        'groupId': groupId,
        'meetId': meetId,
    }

    return render(request, 'meetCalendar/main.html',context)

@csrf_exempt
def getDayInfo(request):
    req = json.loads(request.body)
    meetId = req['meetId1']
    year = req['viewYear']
    month = req['viewMonth']
    month +=1
    meet = Meetings.objects.get(id=meetId)
    meetDayInfos = meetDayInfo.objects.filter(meetId=meet,year=year,month=month)

    dayInfo = []
    for meetDay in meetDayInfos:
        dayInfo.append({
            'year' : meetDay.year,
            'month' : meetDay.month,
            'day' : meetDay.day,
            'hour' : meetDay.hour,
            'userCount' : meetDay.meetUsers.count(),
        })
        
    return JsonResponse({'dayInfo':dayInfo})

@csrf_exempt
def getTravelInfo(request):
    req = json.loads(request.body)
    meetId = req['meetId1']
    year = req['viewYear']
    month = req['viewMonth']
    month +=1
    meet = Meetings.objects.get(id=meetId)
    meetTravelInfos = meetTravelInfo.objects.filter(meetId=meet,year=year,month=month)

    travelInfo = []
    for meetTravel in meetTravelInfos:
        travelInfo.append({
            'year' : meetTravel.year,
            'month' : meetTravel.month,
            'day' : meetTravel.day,
            'userCount' : meetTravel.meetUsers.count(),
        })
        
    return JsonResponse({'travelInfo':travelInfo})


@csrf_exempt
def getDates(request):
    req = json.loads(request.body)
    meetId = req['meetId']
    meet = Meetings.objects.get(id=meetId)
    startDate = meet.meetStart
    endDate = meet.meetEnd
    meetType = meet.meetType

    meetCount = meet.meetMembers.count()

    return JsonResponse({'startDate': startDate, 'endDate': endDate, 'meetType': meetType, 'meetCount': meetCount});

#login ?????? ???????????
def create(request, meetId):
    meeting = Meetings.objects.get(id=meetId)
    if meeting.meetType == 'today':
        form = meetDayForm()
    elif meeting.meetType == 'travel':
        form = meetTravelForm()


    if request.method == 'POST':
        if meeting.meetType == 'today':

            form = meetDayForm(request.POST)

            if form.is_valid():
              meetDay = form.save(commit=False)
              meetDay.meetId = meeting
              meetDay.userId = request.user
              meeting.meetMembers.add(request.user)
              meetDay.save()
              savemeetDayInfo(meetDay)
              return redirect('meetCalendar:main', meeting.id)
            else:
                messages.error(request, '????????? ?????????????????????. ?????? ??????????????????.')

        elif meeting.meetType == 'travel':
            form = meetTravelForm(request.POST)

            if form.is_valid():
                meetTravel = form.save(commit=False)
                meetTravel.meetId = meeting
                meetTravel.userId = request.user
                meeting.meetMembers.add(request.user)
                meetTravel.save()
                saveTravelInfo(meetTravel)
                return redirect('meetCalendar:main', meeting.id)
            else:
                messages.error(request, '????????? ?????????????????????. ?????? ??????????????????.')
            
                
    context={
            'form' : form,
            'meetId' : meetId,
            'meeting' : meeting,
            'meetTimes' : meetTravelForm.TIME_CHOICE,
        }


    return render(request, template_name='meetCalendar/create.html',context=context)

def saveTravelInfo (meetTravel):
    meetId = meetTravel.meetId
    userId = meetTravel.userId
    startDate = meetTravel.startDate
    endDate = meetTravel.endDate
    #?????? ???????????? ?????? ???????????? ??????
    #?????? ????????? ?????????????????? ?????????????????? ??????
    delta = datetime.timedelta(days=1)
    while startDate <= endDate:

        year = startDate.year
        month = startDate.month
        day = startDate.day

        if meetTravelInfo.objects.filter(meetId=meetId,year=year,month=month,day=day).exists():
            meetTravelInfo.objects.get(meetId=meetId,year=year,month=month,day=day).meetUsers.add(userId)
            
        else:
            meetTravelInfo.objects.create(meetId=meetId,year=year,month=month,day=day)
            meetTravelInfo.objects.get(meetId=meetId,year=year,month=month,day=day).meetUsers.add(userId)
        
        startDate += delta
            

def savemeetDayInfo(meetDay):
    meetId = meetDay.meetId
    userId = meetDay.userId
    validDate = meetDay.validDate
    year = validDate.year
    month = validDate.month
    day = validDate.day
    startTime = int(meetDay.startTime)
    endTime = int(meetDay.endTime)
    print (startTime, type(startTime))

    
    while startTime <= endTime:
        if meetDayInfo.objects.filter(meetId=meetId,year=year,month=month,day=day,hour=startTime).exists():
            meetDayInfo.objects.get(meetId=meetId,year=year,month=month,day=day,hour=startTime).meetUsers.add(userId)
        else:
            meetDayInfo.objects.create(meetId=meetId,year=year,month=month,day=day,hour=startTime)
            meetDayInfo.objects.get(meetId=meetId,year=year,month=month,day=day,hour=startTime).meetUsers.add(userId)
        startTime += 1

def voteDayCandidate(request, meetId):
    meeting = Meetings.objects.get(id=meetId)
    voteList = meetDayVote.objects.filter(meetId=meetId)
    if request.method == 'POST':
        results = request.POST.getlist('selection[]')
        for result in results:
            mdv = meetDayVote.objects.get(id=int(result)) 
            mdv.voteUser += 1
            mdv.save()
        meeting.meetVote.add(request.user.id)
        if meeting.meetVote.all().count() == meeting.meetMembers.all().count():
            changeStatus(request, meeting.meetGroupId.id, meetId)
        return redirect('meetings:detail', meeting.meetGroupId.id, meeting.id)
    else:
        context = {
            'meeting' : meeting,
            'voteList' : voteList,
        }

        return render(request, template_name='meetCalendar/voteDayCandidate.html', context=context)

def voteTravelCandidate(request, meetId):
    meeting = Meetings.objects.get(id=meetId)
    voteList = meetTravelVote.objects.filter(meetId=meetId)
    if request.method == 'POST':
        results = request.POST.getlist('selection[]')
        print(results)
        for result in results:
            mdv = meetTravelVote.objects.get(id=int(result)) 
            mdv.voteUser += 1
            mdv.save()
        meeting.meetVote.add(request.user.id)
        if meeting.meetVote.all().count() == meeting.meetMembers.all().count():
            changeStatus(request, meeting.meetGroupId.id, meetId)
        return redirect('meetings:detail', meeting.meetGroupId.id, meeting.id)
    else:
        context = {
            'meeting' : meeting,
            'voteList' : voteList,
        }

        return render(request, template_name='meetCalendar/voteTravelCandidate.html', context=context)

def fixDayCandidate(request, meetId):
    meeting = Meetings.objects.get(id=meetId)

    if request.method == 'POST':
        fixedTime = meetDayVote.objects.get(id=request.POST['fix'])
        meeting.meetStartTime = datetime.datetime(fixedTime.year, fixedTime.month, fixedTime.day, fixedTime.startTime)
        meeting.meetEndTime = datetime.datetime(fixedTime.year, fixedTime.month, fixedTime.day, fixedTime.endTime)
        meeting.meetStatus = 3
        meeting.save()

    return redirect('meetings:detail', meeting.meetGroupId.id, meeting.id)


def fixTravelCandidate(request, meetId):
    meeting = Meetings.objects.get(id=meetId)
    if request.method == 'POST':
        fixedTime = meetTravelVote.objects.get(id=request.POST['fix'])
        st = meetTravel.objects.filter(startDate=datetime.datetime(fixedTime.startYear, fixedTime.startMonth, fixedTime.startDay)).aggregate(Max('startTime'))
        et = meetTravel.objects.filter(endDate=datetime.datetime(fixedTime.endYear, fixedTime.endMonth, fixedTime.endDay)).aggregate(Min('endTime'))
        print(et)
        meeting.meetStartTime = datetime.datetime(fixedTime.startYear, fixedTime.startMonth, fixedTime.startDay, int(st['startTime__max']))
        meeting.meetEndTime = datetime.datetime(fixedTime.endYear, fixedTime.endMonth, fixedTime.endDay, int(et['endTime__min']))
        meeting.meetStatus = 3
        meeting.save()

    return redirect('meetings:detail', meeting.meetGroupId.id, meeting.id)
