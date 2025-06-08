'''
import firebase_admin
from firebase_admin import credentials, storage
from google.cloud.exceptions import NotFound
import os
# Initialize Firebase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if not firebase_admin._apps:
    cred = credentials.Certificate(os.path.join(BASE_DIR, 'config', 'credentials', 'firebase_service_key.json'))
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'capstoneproject-b0d62.firebasestorage.app'
    })
    

try:
    bucket = storage.bucket('capstoneproject-b0d62.firebasestorage.app')
    if not bucket.exists():
        print("❌ 버킷이 존재하지 않습니다. 이름이 잘못되었을 수 있습니다.")
    else:
        print("✅ 버킷이 정상적으로 존재합니다:", bucket.name)
    bucket.exists()
except NotFound:
    print("❌ 버킷이 존재하지 않습니다. (NotFound 예외)")
    
    
def upload_file_to_firebase(file, filename):
    blob = bucket.blob(f"photos/{filename}")
    blob.upload_from_file(file)
    blob.make_public()
    return blob.public_url
    '''