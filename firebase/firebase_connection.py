import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from utils import Authenticator

cred = credentials.Certificate(Authenticator().read_config('firebase'))
firebase_admin.initialize_app(cred)
db = firestore.client()
users_ref = db.collection(u'profileLatest')
docs = users_ref.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')
