from django import forms

from os import listdir
from os.path import isdir, join
from django.conf import settings

def getChoices():
	MEDIA_ROOT = settings.MEDIA_ROOT
	dirs = [(f, f) for f in listdir(MEDIA_ROOT) if isdir(join(MEDIA_ROOT, f))]
	
	dirs.append(("Other group", "Other group"))
	return dirs

class AnimeForm(forms.Form):
	title = forms.ChoiceField(choices=getChoices(), 
							widget=forms.Select(attrs={
								'class': 'form-control'
							}))
	otherTitle = forms.CharField(required=False,
								widget=forms.TextInput(attrs={
								'class': 'form-control',
								'id': 'otherTitle',
								'placeholder': 'Enter the title'
								}))
	episode = forms.IntegerField(label='',
								widget=forms.NumberInput(attrs={
									'placeholder':'Episode',
									'class': 'form-control'
								}))
	file = forms.FileField(label='',
							widget=forms.FileInput(attrs={
								'style': 'display: inline-block;',
								'multiple': 'multiple',
							}))
							