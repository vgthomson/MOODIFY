from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from SongSuggestion.models import EmotionLog
import json
from .forms import *
from django.http import HttpResponse
from django.dispatch import receiver
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt

@login_required
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated
    return render(request,'LoginRegistration/index.html')

def RegisterView(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_has_error = False

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, "Username already exists")

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "Email already exists")

        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, "Password must be at least 5 characters")

        if user_data_has_error:
            return redirect('register')
        else:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )
            messages.success(request, "Account created. Login now")
            return redirect('login')

    return render(request, 'LoginRegistration/register.html')

def LoginView(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('home')
        
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'LoginRegistration/login.html')

def LogoutView(request):
    logout(request)

    # Prevent the browser from caching the page and going back to it after logout
    response = redirect('login')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response

def ForgotPasswordView(request):

    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

    return render(request, 'LoginRegistration/forgot_password.html')

def ResetPasswordSentView(request, reset_id):

    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'LoginRegistration/password_reset_sent.html', {'reset_id': reset_id})

    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

def ResetPasswordSentView(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'LoginRegistration/password_reset_sent.html', {'reset_id': reset_id})
    else:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')


def ResetPasswordView(request, reset_id):
    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # Error flag
            passwords_have_error = False

            # Validation checks
            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)
            if timezone.now() > expiration_time:
                messages.error(request, 'Reset link has expired')
                password_reset_id.delete()
                return redirect('forgot-password')

            # If no errors, reset the password
            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                # Delete the reset record
                password_reset_id.delete()

                messages.success(request, 'Password reset successfully. Please log in.')
                return redirect('login')

        # Render the form again with error messages
        return render(request, 'LoginRegistration/reset_password.html', {'reset_id': reset_id})

    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')



def playsongs(request):
    spotify_playlist_url = 'https://open.spotify.com/playlist/2WOSfi8hrqVUFTETPHV5JZ?si=8c222de5161c44ac'
    return redirect(spotify_playlist_url)

def redirecttosongmodule(request):
    return redirect(reverse('emotion'))

#-----Admin views-----#
def is_superadmin(user):
    return user.is_authenticated and user.is_superuser  # Allow only superusers

@user_passes_test(is_superadmin)
def manage_playlists(request):
    playlists = Playlist.objects.all()
    return render(request, 'Admin/manage_playlists.html', {'playlists': playlists})

@user_passes_test(is_superadmin)
def dashboard(request):
    # Get total users count (excluding deleted users).filter(is_deleted=False)
    total_users = User.objects.count()
    
    # Count active playlists
    active_playlists = Playlist.objects.count()
    
    # Count total emotion logs (representing song interactions)
    total_songs = EmotionLog.objects.count()
    
    # Count languages available
    available_languages = Language.objects.count()
    
    # Get most common emotions (top 5) with percentage calculation
    emotion_count = EmotionLog.objects.count()
    top_emotions = EmotionLog.objects.values('emotion').annotate(
        count=Count('emotion')
    ).order_by('-count')[:5]
    
    # Calculate percentage for each emotion
    if emotion_count > 0:
        for emotion in top_emotions:
            emotion['percentage'] = (emotion['count'] / emotion_count) * 100
    
    # Get language distribution for the chart based on playlists
    # Since EmotionLog doesn't have a direct language field, we need to get this data from the Playlist model
    language_distribution = Playlist.objects.values('language__name').annotate(
        count=Count('language')
    ).order_by('-count')
    
    # Alternatively, if you want language distribution based on emotions that have linked playlists
    # This gets languages from playlists that match emotions users have logged
    # language_distribution = Playlist.objects.filter(
    #     emotion__in=EmotionLog.objects.values_list('emotion', flat=True)
    # ).values('language__name').annotate(
    #     count=Count('language')
    # ).order_by('-count')
    
    # Recent emotion logs
    recent_logs = EmotionLog.objects.select_related('user').order_by('-timestamp')[:10]
    
    context = {
        'total_users': total_users,
        'active_playlists': active_playlists,
        'total_songs': total_songs,
        'available_languages': available_languages,
        'top_emotions': top_emotions,
        'recent_logs': recent_logs,
        'language_distribution': language_distribution,
    }
    
    return render(request, 'Admin/admin_dashboard.html', context)

@user_passes_test(is_superadmin)
def manage_users(request):
    users = User.objects.filter(is_active=True)  # Retrieve only active users
    return render(request, 'Admin/manage_users.html', {'users': users})

@csrf_exempt
@user_passes_test(is_superadmin)
def add_playlist(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Ensure JSON decoding
            emotion = data.get("emotion")
            playlist_url = data.get("playlist_url")
            language_name = data.get("language")
            print(data)

            if not emotion or not playlist_url or not language_name:
                return JsonResponse({"message": "Missing fields"}, status=400)

            # Get or create the language
            language, created = Language.objects.get_or_create(name=language_name)

            # Check if a playlist with same emotion and language already exists
            existing_playlist = Playlist.objects.filter(
                emotion=emotion, 
                language=language
            ).first()

            if existing_playlist:
                return JsonResponse(
                    {"message": "A playlist for this emotion and language already exists"}, 
                    status=400
                )

            # Create new playlist
            Playlist.objects.create(
                emotion=emotion, 
                playlist_url=playlist_url,
                language=language
            )
            return JsonResponse({"message": "Playlist added successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request"}, status=405)

@csrf_exempt
@user_passes_test(is_superadmin)
def update_playlist(request, id):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))  # Ensure JSON decoding
            playlist = get_object_or_404(Playlist, id=id)
            
            emotion = data.get("emotion")
            playlist_url = data.get("playlist_url")
            language_name = data.get("language")

            if not emotion or not playlist_url or not language_name:
                return JsonResponse({"message": "Missing fields"}, status=400)

            # Get or create the language
            language, created = Language.objects.get_or_create(name=language_name)

            # Check if another playlist with same emotion and language exists
            existing_playlist = Playlist.objects.filter(
                emotion=emotion, 
                language=language
            ).exclude(id=id).first()

            if existing_playlist:
                return JsonResponse(
                    {"message": "A playlist for this emotion and language already exists"}, 
                    status=400
                )

            # Update playlist
            playlist.emotion = emotion
            playlist.playlist_url = playlist_url
            playlist.language = language
            playlist.save()
            
            return JsonResponse({"message": "Playlist Updated"}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    
    return JsonResponse({"message": "Invalid request"}, status=405)

@csrf_exempt
@user_passes_test(is_superadmin)
def delete_playlist(request, id):
    if request.method == "POST":
        Playlist.objects.filter(id=id).delete()
        return JsonResponse({"message": "Playlist Deleted"}, status=200)

    return JsonResponse({"message": "Invalid request"}, status=400)

# View to get languages for populating dropdown
def get_languages(request):
    languages = Language.objects.all().values_list('name', flat=True)
    return JsonResponse(list(languages), safe=False)

@csrf_exempt
@user_passes_test(is_superadmin)
def update_user(request, id):
    if request.method == "POST":
        user = get_object_or_404(User, id=id)
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.save()

        return JsonResponse({"message": "User updated successfully"})

    return JsonResponse({"message": "Invalid request"}, status=400)

@csrf_exempt
@user_passes_test(is_superadmin)
def delete_user(request, id):
    if request.method == "POST":
        user = get_object_or_404(User, id=id)
        user.is_active = False
        user.save()
        return JsonResponse({"message": "User deleted successfully"})

    return JsonResponse({"message": "Invalid request"}, status=400)


def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return JsonResponse({'success': True, 'message': 'Feedback submitted successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)  # Return errors if form is invalid
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
import json
from .models import Feedback
from datetime import datetime

def is_admin(user):
    """Check if user is an admin"""
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def manage_feedback(request):
    """
    View for administrators to manage user feedback
    Displays all feedback entries in a table with filtering options
    """
    # Get all feedback entries ordered by created date (newest first)
    feedbacks = Feedback.objects.all().order_by('-created_at')
    
    context = {
        'feedbacks': feedbacks,
        'active_page': 'manage_feedback'  # For highlighting the active sidebar menu item
    }
    
    return render(request, 'Admin/manage_feedback.html', context)

@login_required
@user_passes_test(is_admin)
@require_POST
def update_feedback(request, feedback_id):
    """
    View to handle AJAX requests to update feedback status
    """
    feedback = get_object_or_404(Feedback, id=feedback_id)
    
    try:
        # Parse the request body as JSON
        data = json.loads(request.body)
        status = data.get('status')
        admin_note = data.get('admin_note', '')
        
        # Validate status
        valid_statuses = ['Pending', 'In Progress', 'Resolved']
        if status not in valid_statuses:
            return JsonResponse({
                'message': 'Invalid status value'
            }, status=400)
        
        # Update the feedback
        feedback.status = status
        feedback.admin_note = admin_note
        feedback.updated_at = datetime.now()
        feedback.save()
        
        return JsonResponse({
            'message': 'Feedback status updated successfully',
            'status': status
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'message': f'Error updating feedback: {str(e)}'
        }, status=500)

@login_required
@user_passes_test(is_admin)
@require_POST
def delete_feedback(request, feedback_id):
    """
    View to handle AJAX requests to delete feedback
    """
    try:
        feedback = get_object_or_404(Feedback, id=feedback_id)
        feedback.delete()
        
        return JsonResponse({
            'message': 'Feedback deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'message': f'Error deleting feedback: {str(e)}'
        }, status=500)