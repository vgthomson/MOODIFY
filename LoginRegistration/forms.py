from django import forms
from .models import Playlist

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['emotion', 'playlist_url']
        widgets = {
            'emotion': forms.TextInput(attrs={'class': 'form-control'}),
            'playlist_url': forms.URLInput(attrs={'class': 'form-control'}),
        }