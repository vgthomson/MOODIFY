from django.shortcuts import render, redirect
from transformers import pipeline
from django.contrib import messages
import enchant
from django.http import HttpResponseRedirect
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserEmotion, LanguageSelectionForm
from .models import EmotionLog
from LoginRegistration.models import Playlist, Language
from django.urls import reverse

# Initialize the emotion detection model
emotion_model = pipeline("text-classification", model="joeddav/distilbert-base-uncased-go-emotions-student")

# Initialize the enchant dictionary for English language
d = enchant.Dict("en_US")

# Function to check if a word exists in the dictionary using pyenchant
def is_valid_word(word):
    return d.check(word)

# @login_required
def detect_emotion(request):
    emotion = None
    is_real_word = None
    invalid_words = []
    form = UserEmotion()
    language_form = None
    playlist_url = None
    languages = None
    
    if request.method == 'POST':
        # Check if the form submission is for emotion detection
        if 'text_input' in request.POST:
            form = UserEmotion(request.POST)
            if form.is_valid():
                user_input = form.cleaned_data['text_input']
                words = user_input.split()
                invalid_words = [word for word in words if not is_valid_word(word)]

                if not invalid_words:
                    result = emotion_model(user_input)
                    emotion = result[0]['label']
                    is_real_word = True

                    if request.user.is_authenticated:
                        EmotionLog.objects.create(user=request.user, emotion=emotion, timestamp=now())
                    
                    # Get available languages that have playlists for this emotion
                    available_languages = Language.objects.filter(
                        playlist__emotion=emotion
                    ).distinct()
                    
                    if available_languages.exists():
                        language_form = LanguageSelectionForm()
                        language_form.fields['language'].queryset = available_languages
                    else:
                        messages.warning(request, f"No playlists found for '{emotion}' emotion in any language")
                else:
                    is_real_word = False
                    
        # Check if the form submission is for language selection
        elif 'language' in request.POST and 'emotion' in request.POST:
            selected_language_id = request.POST.get('language')
            emotion = request.POST.get('emotion')
            
            try:
                selected_language = Language.objects.get(id=selected_language_id)
                playlist = Playlist.objects.get(emotion=emotion, language=selected_language)
                playlist_url = playlist.playlist_url
                
                # Keep the emotion detection result visible
                is_real_word = True
                language_form = LanguageSelectionForm(request.POST)
                
                # For re-displaying the form with correct data
                form = UserEmotion({'text_input': request.POST.get('original_text', '')})
                
            except (Language.DoesNotExist, Playlist.DoesNotExist):
                messages.error(request, "Selected playlist not found")

    return render(request, 'SongSuggestion/emotion_input.html', {
        'form': form,
        'emotion': emotion,
        'is_real_word': is_real_word,
        'invalid_words': invalid_words,
        'language_form': language_form,
        'playlist_url': playlist_url,
        'original_text': request.POST.get('text_input', '') if request.method == 'POST' else '',
    })


@login_required
def emotion_history_view(request):
    logs = EmotionLog.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'SongSuggestion/emotion_history.html', {'logs': logs})

def LogoutView(request):
    logout(request)

    # Prevent the browser from caching the page and going back to it after logout
    response = redirect('login')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response