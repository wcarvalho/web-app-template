from nicegui import ui, app
from pathlib import Path
from dotenv import load_dotenv
import os
import authentication
import cards
from datetime import datetime, timedelta
from firebase_config import db

# Load environment variables
load_dotenv()

@ui.page('/')
def home():
    card = cards.default()
    with card:
        if not app.storage.user.get('logged_in', False):
            ui.button('Login with Google',
                    on_click=lambda: ui.navigate.to(authentication.start_oauth()))
        else:
            ui.label(f'Welcome back, {app.storage.user.get("email")}!')
            
            # Create tabs
            with ui.tabs().classes('w-full') as tabs:
                ui.tab('Habits')
                ui.tab('Tab 2')
                ui.tab('Tab 3')

            ui.button('Logout', on_click=authentication.logout)

@ui.page('/test-firebase')
def test_firebase():
    try:
        # Try to write a test document
        doc_ref = db.collection('test').document('test')
        doc_ref.set({'test': 'successful'})
        ui.label('Firebase connection successful!')
    except Exception as e:
        ui.label(f'Firebase error: {str(e)}')

# Run the app
port = int(os.getenv('PORT', 8082))
ui.run(
    port=port,
    storage_secret=os.getenv('STORAGE_SECRET', 'generate_a_secure_random_key_and_store_in_env'),
    host='0.0.0.0')
