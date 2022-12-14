import re
import json
from secrets import choice
from tokenize import group
from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from keywords.models import Keyword
from .models import Post, PostImg
from meetings.models import Meetings
from groups.models import Group
from logins.models import User
from .forms import PostForm, PostImgForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def main(request):
    # 검색
    if request.GET.get('titleSearch'):
        search = request.GET.get('titleSearch')
        openRange = request.GET.get('openRange')

        if openRange == '전체공개':
            posts = Post.objects.filter(logTitle__icontains=search, openRange=openRange)|Post.objects.filter(logKeywords__keyword__contains=search, openRange=openRange)
        elif openRange == '그룹공개':

            user = request.user
            myGroups = []
            posts = []
            groups = Group.objects.all()
            for group in groups:
                for member in group.members.all():
                    if member == user:
                        myGroups.append(group.id)


            allPosts = Post.objects.filter(logTitle__icontains=search, openRange=openRange)|Post.objects.filter(logKeywords__keyword__contains=search, openRange=openRange)

            for post in allPosts:
                for myGroup in myGroups:
                    if post.groupId.id == myGroup:
                        posts.append(post)

        else:
            posts = Post.objects.filter(logTitle__icontains=search, openRange=openRange,userId = request.user)|Post.objects.filter(logKeywords__keyword__contains=search, openRange=openRange,userId = request.user)

    # if request.GET.get('openRange'):
    #     # todo 공개범위 에따른 로그인 판별 필요
    #     # ?????????????????????????
    #     openRange = request.GET.get('openRange')
    #     if openRange == '0':
    #         posts = Post.objects.filter(openRange=0, userId = request.user.id)
    #     elif openRange == '1':
    #         #???????
            
    #         posts = Post.objects.filter(openRange=1)
    #     else:
    #         posts = Post.objects.filter(openRange=2)
    # else:
    #     posts = Post.objects.filter(openRange=2)
    elif request.GET.get('openRange'):
        openRange = request.GET.get('openRange')
        if openRange == '비공개':
            posts = Post.objects.filter(openRange='비공개', userId = request.user)
        elif openRange == '그룹공개':
            user = request.user
            myGroups = []
            posts = []
            groups = Group.objects.all()
            for group in groups:
                for member in group.members.all():
                    if member == user:
                        myGroups.append(group.id)
            # myGroups = Group.objects.filter(members=user)
            
            allPosts = Post.objects.filter(openRange='그룹공개')
            for post in allPosts:
                for myGroup in myGroups:
                    if post.groupId.id == myGroup:
                        posts.append(post)
            # myMeetings = []
            # for myGroup in myGroups:
            #     meeting = Meetings.objects.filter(meetGroupId=myGroup)
            #     myMeetings.append(meeting)
            # print(myMeetings)
            # 게시물 = 약속아이디 -> 그룹아이디 -> 그룹의 멤버에서 -> 내가속한지 확인
            
            # posts = Post.objects.filter(openRange='그룹공개', groupId__in=myGroups)
        else:
            #전체공개
            posts = Post.objects.filter(openRange='전체공개')
    else:
        openRange = request.GET.get('openRange')
        posts = Post.objects.filter(openRange='openRange')

    nowPost = []
    for post in posts:
        tmp = {}
        tmp['post'] = post
        tmp['postImgs'] = PostImg.objects.filter(logId=post.id)
        nowPost.append(tmp)
        

    context = {
        'posts': nowPost,
        'openRange': openRange,
    }

    return render(request, 'posts/main.html', context)


def detail(request, postId):
    #todo 상세페이지 로그인 판별 필요 
    #(비공개인 경우는 로그인한 유저만 접근 가능)
    # 그룹공개 설정 필요 (로그인한 유저가 그룹에 속한 경우)
    post = Post.objects.get(id=postId)
    postImgs = PostImg.objects.filter(logId=postId)
    meetMembers = post.meetMembers.all()
    myMeetMembers = []
    for meetMember in meetMembers:
        myMeetMembers.append(meetMember.nickname)
    logKeywords = post.logKeywords.all()
    myKeywords = []
    for keyword in logKeywords:
        myKeywords.append(keyword.keyword)

    context = {
        'post': post,
        'postImgs': postImgs,
        'myMeetMembers': myMeetMembers,
        'myKeywords': myKeywords,
    }
    return render(request, 'posts/detail.html', context)

@login_required
def create(request):
    # imgFormSet = modelformset_factory(PostImg, form=PostImgForm, max_num=3, extra=1)
    if request.method == 'POST':
        postForm = PostForm(request.POST)
        # formset = imgFormSet(request.POST, request.FILES, queryset=PostImg.objects.none())
        postKeywords = request.POST.get('basic')

        if postForm.is_valid():
            post = postForm.save(commit=False)
            post.userId = request.user
            meetId = request.POST.get('meetId')
            post.meetId = Meetings.objects.get(id=meetId)
            places = request.POST.getlist('place[]')
            placesJson = { 'places': places }
            post.places = placesJson
            post.groupId = post.meetId.meetGroupId
            post.logStartDate = request.POST.get('startTime')
            post.logEndDate =  request.POST.get('endTime')
            print(post.logStartDate)
            post.save()
            
            if postKeywords != '':
                for keyword in eval(postKeywords):
                    key,flag = Keyword.objects.get_or_create(keyword=keyword['value'])
                    post.logKeywords.add(key)

            meetMembers = post.meetId.meetMembers.all()
            for member in meetMembers:
                post.meetMembers.add(member)
          
            for img in request.FILES.getlist('logImgs[]'):
                postImg = PostImg(logId=post, image=img)
                postImg.save()
            # for form in formset.cleaned_data:
            #     if form:
            #         image = form['image']
            #         photo = PostImg(logId=post, image=image)
            #         photo.save()
            
            return redirect('posts:detail', postId=post.id)
        else:
            print(postForm.errors)
            return redirect('posts:create')
    else:
        if request.GET.get('meetId'):
            meetId = request.GET.get('meetId')
            meeting = Meetings.objects.get(id=meetId)
            postForm = PostForm(initial={'logTitle': meeting.meetName, 'userId': request.user})
            # formset = imgFormSet(queryset=PostImg.objects.none())
            openRanges = Post.openRangeChoices
            meetUsers = meeting.meetMembers.all()
            myMeetMembers = []
            for user in meetUsers:
                myMeetMembers.append(user.name)

            print(meeting.meetStartTime)
            startTime = meeting.meetStartTime.strftime("%Y-%m-%d %H:%M")
            endTime = meeting.meetEndTime.strftime("%Y-%m-%d %H:%M")
            context = {
                #'keywords': Post.keyWords,
                'openRanges': openRanges,
                'postForm': postForm,
                # 'formset': formset,
                'meeting': meeting,
                'myMeetMembers': myMeetMembers,
                'startTime' : startTime,
                'endTime' : endTime,
            }
            return render(request, 'posts/create.html', context)
        else:
            postForm = PostForm(initial={'logTitle': '', 'userId': request.user})
            # formset = imgFormSet(queryset=PostImg.objects.none())

            meetings = Meetings.objects.filter(meetMembers__in=[request.user], meetStatus='3')
            meetingsId = []
            for meeting in meetings:
                tmp = {}
                tmp['id'] = meeting.id
                tmp['meetName'] = meeting.meetName
                meetingsId.append(tmp)
            #내가 속한 meeting 목록을 넘겨주기
            openRanges = Post.openRangeChoices
            context = {
                #'keywords': Post.keyWords,
                'openRanges': openRanges,
                'postForm': postForm,
                # 'formset': formset,
                'meetingsId': meetingsId,
            }
            return render(request, 'posts/create.html', context)

    

    

@login_required
def update(request, postId):

    # 로그인 되어있는 유저가 이 게시물의 저자 라면 업데이트 페이지로 이동가능
    # 아니라면 디테일페이지로 강제 이동 (알림 메세지)
    nowpost = Post.objects.get(id=postId)
    if (nowpost.userId == request.user):
        if request.method == 'POST':
            postForm = PostForm(request.POST, instance=nowpost)
            postKeywords = request.POST.get('basic')
            if postForm.is_valid():
                #nowpost.logDate = request.POST.get('logDate')
                #nowpost.logKeywords = request.POST.get('logKeywords')
                places = request.POST.getlist('place[]')
                placesJson = { 'places': places }
                nowpost.places = placesJson
                if postKeywords!='':
                    for keyword in eval(postKeywords):
                        key,flag = Keyword.objects.get_or_create(keyword=keyword['value'])
                        nowpost.logKeywords.add(key)

                for img in request.FILES.getlist('logImgs[]'):
                    postImg = PostImg(logId=nowpost, image=img)
                    postImg.save()
                nowpost.save()
                return redirect('posts:detail', postId=postId)
            else:
                print(postForm.errors)
        
        nowpostImgs = PostImg.objects.filter(logId=nowpost)
        meetMembers = nowpost.meetMembers.all()
        myMeetMembers = []
        for user in meetMembers:
            myMeetMembers.append(user.name)
        openRanges = Post.openRangeChoices
        logKeywords = nowpost.logKeywords.all()
        myKeywords = []
        for keyword in logKeywords:
            myKeywords.append(keyword.keyword)
        startTime = nowpost.logStartDate.strftime("%Y-%m-%d %H:%M")
        endTime = nowpost.logEndDate.strftime("%Y-%m-%d %H:%M")
        meeting = {
            'post': nowpost,
            'nowpostImgs': nowpostImgs,
            'startTime' : startTime,
            'endTime' : endTime,
        }
        context = {
                'post': meeting,
                'openRanges': openRanges,
                'myMeetMembers': myMeetMembers,
                'myKeywords': myKeywords,
        }
        return render(request, 'posts/update.html', context)
    else:
        return redirect('posts:detail', postId=postId)


@login_required
def delete(request, postId):
    # 로그인 되어있으면 삭제 가능
    # 아니라면 디테일페이지로 강제 이동 (알림 메세지)
    if request.method == 'POST':
        nowpost = Post.objects.get(id=postId)
        if nowpost.userId == request.user:
            nowpost.delete()
            return redirect('posts:main')
        else:
            return redirect('posts:detail', postId=postId)

@login_required
def loadMeetingMembers(request):
    req = json.loads(request.body)
    if request.method == 'POST':
        meetingId = req['meetingId']
        thisMeet = Meetings.objects.get(id=meetingId)
        meetingPlace = thisMeet.meetPlace
        meeting = Meetings.objects.get(id = meetingId)
        startTime = meeting.meetStartTime.strftime("%Y-%m-%d %H:%M")
        endTime = meeting.meetEndTime.strftime("%Y-%m-%d %H:%M")
        allMembers = meeting.meetMembers.all()
        meetingMembers = []
        for member in allMembers:
            meetingMembers.append(member.name)
        return JsonResponse({'members': meetingMembers, 'place': meetingPlace, 'startTime': startTime, 'endTime' : endTime})
        