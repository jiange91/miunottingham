from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from activities.models import Groups, Activities, GroupConfirmString
from accounts.models import User
from django.urls import reverse
from activities.forms import ActivitiesForm, GroupsForm, EditForm, EditGroup
from django.core.exceptions import ObjectDoesNotExist
import hashlib
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from accounts.forms import LoginForm
from django.core.paginator import Paginator


def success(likecount):
    data = {}
    data['status'] = 'SUCCESS'
    data['like_num'] = likecount
    return JsonResponse(data)


def error(message):
 data = {}
 data['status'] = 'ERROR'
 data['message'] = message
 return JsonResponse(data)


def hash_code(s, salt='confirm'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(group):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(group.group_name, now)
    GroupConfirmString.objects.create(code=code, group=group)
    return code


def send_group_email(email, code, username, user_id, group_name):
    subject = 'From Miunottingham'
    text_content = 'If you see this message, it tells that your email server does not support HTML content'
    html_content = '''
                    <p>Hello {}, you are trying to register a group: {}</p>
                    <p><a href="http://localhost:8000/miunottingham/groupconfirm/{}/{}" target=blank>
                     you must to click this link to confirm your group</a></p>
                    <p>Have fun, and don't hesitate to contact us with your feedback</p>
                    <p>This link lasts for {} days</p>'''.format(username, group_name, code, user_id, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def main_page(request):

    page_num = request.GET.get('page', 1)
    acts_list = Activities.objects.all()
    paginator = Paginator(acts_list, 9)
    page_range = paginator.page_range
    actspage = paginator.get_page(page_num)
    activities = actspage.object_list
    current = int(page_num)
    displayrange = list(range(max(current-2,1),min(current+2, paginator.num_pages)+1))
    # 加省略号
    if displayrange[0] - 1 >= 2:
        displayrange.insert(0, "...")
    if paginator.num_pages - displayrange[-1] >= 2:
        displayrange.append("...")
        # 加最前最后页链接
    if displayrange[0] != 1:
        displayrange.insert(0, 1)
    if displayrange[-1] != paginator.num_pages:
        displayrange.append(paginator.num_pages)

    authenticated = request.session.get('is_login')
    form = LoginForm()
    if authenticated:
        id = request.session.get('user_id')
        user = User.objects.get(id=id)
    return render(request, 'miunottingham/main_page.html', locals())


def groups(request):
    group_list = Groups.objects.all()
    context = {'group_list': group_list}
    return render(request, 'miunottingham/groups.html', context)


def group_acts(request, group_id):
    group = get_object_or_404(Groups, id=group_id)
    page_num = request.GET.get('page', 1)
    acts_list = group.activities_set.all()
    paginator = Paginator(acts_list, 9)
    page_range = paginator.page_range
    actspage = paginator.get_page(page_num)
    activities = actspage.object_list
    group_name = group.group_name
    current = actspage.number
    displayrange = [x for x in range(current - 2, current + 2)
                    if 0 < x <= paginator.num_pages]
    # 加省略号
    if displayrange[0] - 1 >= 2:
        displayrange.insert(0, "...")
    if paginator.num_pages - displayrange[-1] >= 2:
        displayrange.append("...")
        # 加最前最后页链接
    if displayrange[0] != 1:
        displayrange.insert(0, 1)
    if displayrange[-1] != paginator.num_pages:
        displayrange.append(paginator.num_pages)

    authenticated = request.session.get('is_login')
    form = LoginForm()
    if authenticated:
        id = request.session.get('user_id')
        user = User.objects.get(id=id)
    # if request.session.get('is_login'):
    #     id = request.session.get('user_id')
    #     user = User.objects.get(id=id)
    #     if user.groups_set.filter(user_id=id):
    #         if user.groups_set.get(user_id=id).id == group_id and user.groups_set.get(user_id=id).has_confirmed:
    #             notice = "your_group"
    return render(request, 'miunottingham/group_acts.html', locals())


def details(request, act_id):
    activity = Activities.objects.get(id=act_id)
    group = activity.group_name
    authenticated = request.session.get('is_login')
    form = LoginForm()
    if authenticated:
        id = request.session.get('user_id')
        user = User.objects.get(id=id)
        if user.groups_set.filter(user_id=id):
            if user.groups_set.get(user_id=id).id == group.id and user.groups_set.get(user_id=id).has_confirmed:
                notice = "your_group"
    return render(request, 'miunottingham/test_maotou_details.html', locals())


def new_activity(request, group_id):
    group_name = Groups.objects.get(id=group_id).group_name
    if request.method != 'POST':
        form = ActivitiesForm()
    else:
        form = ActivitiesForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.group_name = Groups.objects.get(id=group_id)
            activity.save()
            return HttpResponseRedirect(reverse('miunottingham:group_acts',args=[group_id]))
    return render(request, 'miunottingham/new_activity.html', locals())


def edit_activity(request, act_id):
    if not request.session.get('is_login'):
        return render(request, 'miunottingham/main_page.html')
    else:
        activity = Activities.objects.get(id=act_id)
        group = activity.group_name
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        if user.groups_set.filter(user_id=user_id):
            if user.groups_set.get(user_id=user_id).id == group.id:
                if request.method != 'POST':
                    form = EditForm(instance=activity)
                else:
                    form = EditForm(instance=activity, data=request.POST)
                    if form.is_valid():
                        form.save()
                        if request.FILES.get('img'):
                            activity.img = request.FILES.get('img')
                            activity.save()
                        return HttpResponseRedirect(reverse('miunottingham:your_acts'))
                return render(request, 'miunottingham/edit_activity.html', locals())


def new_group(request, userid):
    if request.method == "POST":
            group_name = request.POST.get('group_name', None)
            img = request.FILES.get('avatar', None)
            if Groups.objects.filter(group_name=group_name):
                message = 'Group already exists'
                return render(request, 'miunottingham/test_register.html', locals())
            group = Groups()
            group.group_name = group_name
            group.img = img
            user = User.objects.get(id=userid)
            username = user.username
            group.user = user
            group.has_confirmed = True
            group.save()

            message = 'you have successfully registered a group' + ': ' + group_name
            return render(request,'miunottingham/confirm.html',locals())
    form = GroupsForm()
    return render(request, 'miunottingham/test_register.html', locals())


def groupconfirm(request, code, user_id):
    user = User.objects.get(id=user_id)
    message = None
    try:
        confirmation = GroupConfirmString.objects.get(code=code)
    except ObjectDoesNotExist:
        message = 'Invalid confirmation'
        return render(request, 'miunottingham/confirm.html', locals())

    c_time = confirmation.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirmation.delete()
        confirmation.group.delete()
        message = 'Your email link has expired, please try to register again'
        return render(request, 'miunottingham/confirm.html', locals())
    else:
        confirmation.group.has_confirmed = True
        confirmation.group.save()
        confirmation.delete()
        message = 'You have successfully register a group.'
        return render(request, 'miunottingham/confirm.html', locals())


def delete_act(request, act_id):
    if not request.session.get('is_login'):
        return render(request, 'miunottingham/main_page.html')
    else:
        activity = Activities.objects.get(id=act_id)
        group = activity.group_name
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        if user.groups_set.filter(user_id=user_id):
            if user.groups_set.get(user_id=user_id).id == group.id:
                activity.delete()
                return HttpResponseRedirect(reverse('miunottingham:your_acts'))


def your_acts(request):
    if not request.session.get('is_login'):
        return HttpResponseRedirect(reverse('miunottingham:main_page'))
    else:
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        group = user.groups_set.get(user_id=user_id)
        activities = group.activities_set.all()
        return render(request, 'miunottingham/your_acts.html', locals())


def editgroup(request, group_id):
    if not request.session.get('is_login'):
        return render(request, 'miunottingham/main_page.html')
    else:
        group = Groups.objects.get(id=group_id)
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        if user.groups_set.filter(user_id=user_id):
            if user.groups_set.get(user_id=user_id).id == group_id:
                if request.method != 'POST':
                    form = EditGroup(instance=group)
                else:
                    form = EditGroup(instance=group, data=request.POST)
                    if form.is_valid():
                        form.save()
                        if request.FILES.get('img'):
                            group.img = request.FILES.get('img')
                        if request.FILES.get('logo'):
                            group.logo = request.FILES.get('logo')
                        group.save()
                        message = "成功修改组织信息"
                return render(request, 'miunottingham/editgroup.html', locals())