from django.shortcuts import render, redirect
from transformers import pipeline
from django.contrib import messages
import enchant
from django.http import HttpResponseRedirect
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserEmotion
from .models import EmotionLog
from LoginRegistration.models import Playlist
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

    if request.method == 'POST':
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

                # Check if a playlist exists in the database
                playlist = Playlist.objects.filter(emotion=emotion).first()
                if playlist:
                    return render(request, 'SongSuggestion/emotion_input.html', {
                        'form': form,
                        'emotion': emotion,
                        'playlist_url': playlist.playlist_url  # Pass the URL to the template
                    })
                else:
                    messages.warning(request, f"No playlist found for {emotion}")

            else:
                is_real_word = False  

    return render(request, 'SongSuggestion/emotion_input.html', {
        'form': form,
        'emotion': emotion,
        'is_real_word': is_real_word,
        'invalid_words': invalid_words
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