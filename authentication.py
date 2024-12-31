from nicegui import ui, app
import os
import cards
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError

# Google OAuth2 credentials
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
port = int(os.getenv('PORT', 8082))

# Update the redirect URI for production
REDIRECT_URI = 'https://cogscikid.com/habit-tracker/oauth_callback'
if os.getenv('ENVIRONMENT', 'development') == 'development':
    REDIRECT_URI = f'http://localhost:{port}/oauth_callback'
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


AUTH_BASE_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'
SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid',
]


@ui.page('/oauth_callback')
def oauth_callback(code):
    if not code:
        ui.notify('Authentication failed', color='negative')
        return ui.navigate.to('/')

    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    token = google.fetch_token(
        TOKEN_URL,
        client_secret=CLIENT_SECRET,
        authorization_response=f"{REDIRECT_URI}?code={code}"
    )
    
    # Get user info
    user_info = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    
    # Store everything in app.storage.user
    app.storage.user.update({
        'logged_in': True,
        'email': user_info['email'],
        'token': token
    })
    
    ui.navigate.to('/')

def start_oauth():
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, _ = google.authorization_url(AUTH_BASE_URL)
    return authorization_url

def logout():
    app.storage.user.clear()
    ui.navigate('/')

#async def check_session():
#    if not app.storage.user.get('logged_in', False):
#        return
        
#    # Check if stored token is still valid
#    token = app.storage.user.get('token')
#    if token:
#        try:
#            google = OAuth2Session(CLIENT_ID, token=token)
#            user_info = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
#        except TokenExpiredError:
#            app.storage.user.clear() 