import os
from django.shortcuts import redirect, render
from django.contrib import messages
from groups.forms import GroupForm
from groups.utils import groupCodeGenerate
from .models import Group
from meetings.models import Meetings
from config import settings

# Create your views here.

def main(request):
    currentUser= request.user.id
    groups = Group.objects.filter(members=currentUser)
    context = {
        'groups' : groups
    }
    return render(request, 'groups/main.html', context=context)

def create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.head = request.user.username
            group.save()
            group.code =  groupCodeGenerate(request.user.username, group.id)
            group.save()
            group.members.add(request.user.id)
            return redirect(f'/groups/group/{group.id}')
        else:
            form = GroupForm()
            context = {
            'form' : form
            }
            return render(request, template_name='groups/create.html', context=context)
    else:
        form = GroupForm()
        context = {
            'form' : form
        }
        return render(request, template_name='groups/create.html', context=context)

def join(request):
    if request.method == 'POST':
        code = request.POST['code']
        user = request.user.id

        # 케이스별로 예외처리 논의 필요
        try:    
            group = Group.objects.get(code=code)
        except Group.DoesNotExist:
            messages.error(request, '유효하지 않은 그룹 코드입니다.')
            return redirect('/groups/join/')
        
        try:
            group.blackList.get(id=user)
            messages.error(request, '그룹의 블랙리스트에 등록되어있습니다.')
            return redirect('/groups/join/')
        except:
            try: 
                group.members.get(id=user)
                messages.error(request, '이미 해당 그룹의 멤버입니다.')
                return redirect('/groups/join/')
            except:
                group.members.add(user)
                return redirect(f'/groups/group/{group.id}')  
    else:
        return render(request, template_name='groups/join.html')

def detail(request, id):
    group = Group.objects.get(id = id)
    user = request.user
    members = group.members.all()

    #그룹내 약속정보들 가져오기
    meetings = Meetings.objects.filter(meetGroupId=group)
    context = {
        'group' : group,
        'members' : members,
        'user' : user,
        'meetings': meetings,
    }
    return render(request, template_name='groups/detail.html', context=context)

def leave(request, id):
    if request.method == 'POST':
        user = request.user.id
        group = Group.objects.get(id=id)
        group.members.remove(user)
    
    return redirect('/groups/')

def modify(request, id):
    group = Group.objects.get(id=id)
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)

        #취소 박스 선택 값 가져오기
        imageCancel = request.POST.get('image-clear', False)

        #취소가 선택됬다면 이미지 경로에서 이미지 삭제 후 그룹 이미지 필드값을 빈 문자열로 재설정
        if imageCancel:
            os.remove(os.path.join(settings.MEDIA_ROOT, group.image.path))
            group.image = ''

        if form.is_valid():
            group.name = form.cleaned_data['name']
            group.introduction = form.cleaned_data['introduction']
            group.purpose = form.cleaned_data['purpose']
            # group.image = form.cleaned_data['image']           
            if form.cleaned_data['image']:
                group.image = form.cleaned_data['image']
            else:
                group.image = group.image
            group.save()
            return redirect(f'/groups/group/{group.id}')
    else:
        form = GroupForm(instance=group)
    
        context = {
            'form' : form,
            'group' : group
        }

        return render(request, template_name='groups/modify.html', context=context)

def members(request, id):
    group = Group.objects.get(id=id)
    members = group.members.all()
    user = request.user.username

    context = {
        'group' : group,
        'members' : members, 
        'user' : user,
    }
    return render(request, template_name='groups/members.html', context=context)