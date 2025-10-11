# Moodify

Moodify is an intelligent music recommendation system that suggests songs and playlists based on user emotions detected from text input. It enhances the user experience by allowing them to play random songs, analyze emotions, and view their past emotion history.

## Features

### User Features
- **Play Random Songs**: Users can play songs without inputting emotions.
- **Emotion Detection**: Users enter text input, and Moodify detects the emotion using an AI model.
- **Playlist Suggestion**: Based on detected emotions, the system suggests relevant playlists.
- **Emotion History**: Users can view their past detected emotions and associated playlists.
- **User Authentication**: Login is required to track emotion history securely. Logout ensures cache-control for session security.

### Admin Features
- **Manage Playlists**: Admins can add playlists for each detected emotion.
- **User Management**: Admins can manage user accounts and their activities.

## Technology Stack

### Frontend
- HTML
- CSS
- JavaScript
- Bootstrap

### Backend
- Django (Python)
- SQLite (Database)

## Core Functionalities

### Emotion Detection
- Uses **Hugging Face transformers** with a pre-trained **DistilBERT-based emotion detection model** (`joeddav/distilbert-base-uncased-go-emotions-student`)
- Classifies emotions from user text input

### Spell Check
- Uses **pyenchant** to validate user input, ensuring proper English words

### Emotion Log
- Stores detected emotions along with timestamps and user information in the `EmotionLog` model

### Playlist Suggestion
- Matches detected emotions with predefined playlists stored in the `Playlist` model
- Displays the playlist URL if available

### Emotion History
- Allows users to track and review their previous emotion detection logs

## Installation & Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/vgthomson/moodify.git
   cd moodify
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On iOS use: source venv/bin/activate 
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser (for admin access):**
   ```sh
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```sh
   python manage.py runserver
   ```

7. **Access the application:**
   - Open `http://127.0.0.1:8000/` in your web browser.
   - Admin panel: `http://127.0.0.1:8000/dashboard`

## Future Enhancements
- Implement a more advanced recommendation system with personalized suggestions
- Integrate additional streaming platforms for direct playback
- Improve UI/UX for a more engaging experience

## License
This project is licensed under the MIT License.

---

Enjoy discovering music that matches your emotions with **Moodify**! 🎵

## Author
Developed by 
## V G Thomson

GitHub: https://github.com/vgthomson
Linkedin: https://www.linkedin.com/in/vgthomson/

