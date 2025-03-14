from django import forms
from LoginRegistration.models import Language

class UserEmotion(forms.Form):
    text_input = forms.CharField(
        label="Enter your text",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type a word or text here...',
            'class': 'form-control',
        })
    )

class LanguageSelectionForm(forms.Form):
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        empty_label="Select a language",
        widget=forms.Select(attrs={
            'class': 'form-control language-select',
            'style': 'border-radius: 8px; border: 2px solid #6c5ce7; padding: 10px; font-size: 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: all 0.3s ease; color: #333333; background-color: #ffffff;',
            'onchange': 'this.classList.add("selected-language")',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].label_attrs = {'class': 'language-label fw-bold mb-2'}
        # Add a custom CSS class to the label
        self.fields['language'].label = 'Choose Your Language Preference'