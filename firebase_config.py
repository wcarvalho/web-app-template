import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

def initialize_firebase():
    # Expects firebase-key.json in the same directory as this file
    cred = credentials.Certificate(
        Path(__file__).parent / 'firebase-key.json'
    )
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = initialize_firebase() 