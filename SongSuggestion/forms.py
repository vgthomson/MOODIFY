from django import forms

class UserEmotion(forms.Form):
    text_input = forms.CharField(
        label="Enter your text",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type a word or text here...',
            'class': 'form-control',
        })
    )
