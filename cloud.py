import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

class FBDB:
    def __init__(self, path_to_service_key='aira-47a70-firebase-adminsdk-04lj7-6c24d8d2f9.json', databaseURL='https://aira-47a70-default-rtdb.firebaseio.com/'):
        try:
            # Initialize Firebase only once
            if not firebase_admin._apps:
                cred = credentials.Certificate(path_to_service_key)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': databaseURL
                })
            self.ref = db.reference()  # Reference to the root of the database
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            raise e  # Reraise the error to stop execution if initialization fails

    def update(self, user_id, value):
        try:
            # Ensure that the value is serializable and valid
            if not isinstance(value, dict):
                value = {"data": value}  # Wrap value in a dictionary if not already a dictionary
            path = str(user_id)  # Ensure user_id is a string
            self.ref.child(path).update(value)
            print("Data updated to Firebase...")
            return True
        except Exception as e:
            print(f"Error updating value: {e}")
            return False

    def get(self, user_id):
        try:
            path = str(user_id)  # Ensure user_id is a string
            data = self.ref.child(path).get()  # Fetch the data from Firebase
            if data is None:
                print("No data found for this user.")
                return None
            if 'data' in data:  # Ensure the 'data' key exists
                data_string = data['data']
                data_json = json.loads(data_string)  # Parse the JSON string
                return data_json
            else:
                print("No 'data' field in the Firebase response.")
                return None
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return None
