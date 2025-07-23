import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화
cred = credentials.Certificate("cert.json")  # 🔑 서비스 키 경로
firebase_admin.initialize_app(cred)
db = firestore.client()


