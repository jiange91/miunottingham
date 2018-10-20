from django import forms
from activities.models import Activities, Groups

class ActivitiesForm(forms.ModelForm):
    class Meta:
        model = Activities
        fields = ['short_name', 'links', 'begin', 'end', 'img']
        labels = {'short_name': "activity's name", 'links': 'link',
                  'begin': "when will your activity start", 'end': 'when will your activity end', 'img': 'attach a picture'}
        widgets = {'short_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'links': forms.TextInput(attrs={'class': 'form-control'}),
                   'begin': forms.DateTimeInput(attrs={'class': 'form-control'}),
                   'end': forms.DateTimeInput(attrs={'class': 'form-control'}),
                   'img': forms.FileInput(attrs={'class':'custom-file-input'})}


class GroupsForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = ['group_name', 'img']
        labels = {'group_name': "group's name", 'img': 'avatar'}
