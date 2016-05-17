from django import forms

class BoardForm(forms.Form):
    player = forms.IntegerField(required=True, widget=forms.HiddenInput())
    move = forms.CharField(required=True, widget=forms.HiddenInput())
    game = forms.IntegerField(required=True, widget=forms.HiddenInput())