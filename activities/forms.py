from django import forms
from activities.models import Activities, Groups


class ActivitiesForm(forms.ModelForm):
    class Meta:
        model = Activities
        fields = ['short_name', 'links', 'desc', 'location', 'begin', 'end', 'img']
        labels = {'short_name': "活动名称", 'links': '详情链接','desc': '简短描述',
                  'location': '活动地点', 'begin': "开始时间", 'end': '结束时间', 'img': '添加照片'}
        widgets = {'short_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'links': forms.TextInput(attrs={'class': 'form-control'}),
                   'desc': forms.TextInput(attrs={'class': 'form-control'}),
                   'location': forms.TextInput(attrs={'class': 'form-control'}),
                   'begin': forms.DateTimeInput(attrs={'class': 'form-control'}),
                   'end': forms.DateTimeInput(attrs={'class': 'form-control'}),
                   'img': forms.FileInput(attrs={'class':'custom-file-input'})}


class GroupsForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = ['group_name', 'img']
        labels = {'group_name': "group's name", 'img': 'avatar'}
