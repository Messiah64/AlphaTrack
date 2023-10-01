import os
import datetime as dt
import streamlit as st
import requests
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Set up Google Calendar API
SCOPES_CALENDAR = ["https://www.googleapis.com/auth/calendar"]
# Set up Google Drive API
SCOPES_DRIVE = ["https://www.googleapis.com/auth/drive.file"]


def create_google_calendar_event(summary, description, start_datetime, end_datetime, calendar_id, timezone):
    
    json_key = "https://drive.google.com/file/d/1GFJ4sUGDMIlhO2eOuD3gst7E-MB3yjVZ/view?usp=sharing"
    response = requests.get(json_key)

    # Check if succesful response
    if response.status_code == 200:
        json_key = json.loads(response.text)
        credentials = service_account.Credentials.from_service_account_file(
            json_key , scopes=SCOPES_CALENDAR)
        
        service = build("calendar", "v3", credentials=credentials)

        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_datetime,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_datetime,
                'timeZone': timezone,
            },
        }

        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        return event



def upload_image_to_drive(image_file_path, folder_id):
    
    json_key = "https://drive.google.com/file/d/1GFJ4sUGDMIlhO2eOuD3gst7E-MB3yjVZ/view?usp=sharing"
    response = requests.get(json_key)

    # Check if succesful response
    if response.status_code == 200:
        json_key = json.loads(response.text)
        credentials = service_account.Credentials.from_service_account_file(
            json_key , scopes=SCOPES_CALENDAR)
    
        drive_service = build("drive", "v3", credentials=credentials)

        file_metadata = {
            'name': os.path.basename(image_file_path),
            'parents': [folder_id]  # Specify the folder ID where you want to upload the image
        }

        media = MediaFileUpload(image_file_path, resumable=True)

        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        return file.get('id')

def main():
    st.title('AlphaTrack - Sentosa Fire Station')

    # Input fields
    summary = st.text_input('Event Name')
    description = st.text_area('Event Description')
    start_date = st.date_input('Start Date')
    end_date = st.date_input('End Date')
    location = st.text_input('Location')
    
    # Google Calendar settings
    calendar_id = 'sentosafirestation@gmail.com'
    timezone = 'Asia/Singapore'

    # Upload the image to Google Drive
    image_file = st.file_uploader('Upload Image', type=['jpg', 'png', 'jpeg'])

    # Submit button (conditionally based on image upload)
    if image_file is not None:
        if st.button('Create Event with Image'):
            if summary and start_date and end_date:
                start_datetime = start_date.strftime('%Y-%m-%dT%H:%M:%S')
                end_datetime = end_date.strftime('%Y-%m-%dT%H:%M:%S')

                # Create the Google Calendar event
                event = create_google_calendar_event(summary, description, start_datetime, end_datetime, calendar_id, timezone)

                # Upload the image to Google Drive
                image_file_path = 'temp.jpg'
                with open(image_file_path, 'wb') as f:
                    f.write(image_file.read())
                folder_id = '1-dxUDRz9jcWF7efcMUI4U3wbBCMF09Lj'  # Specify the folder ID where you want to upload the image
                image_id = upload_image_to_drive(image_file_path, folder_id)

                # Attach the image URL to the event (modify the event as needed)
                event_description = f'{description}\nLocation: {location}\nImage URL: https://drive.google.com/uc?id={image_id}'
                event['description'] = event_description

                # Update the event with the new description
                json_key = "https://drive.google.com/file/d/1GFJ4sUGDMIlhO2eOuD3gst7E-MB3yjVZ/view?usp=sharing"
                response = requests.get(json_key)

                # Check if succesful response
                if response.status_code == 200:
                    json_key = json.loads(response.text)
                    credentials = service_account.Credentials.from_service_account_file(
                        json_key , scopes=SCOPES_CALENDAR)
                    service_image = build("calendar", "v3", credentials=credentials_image)
                    updated_event = service_image.events().update(calendarId=calendar_id, eventId=event['id'], body=event).execute()

                    st.success(f'Event created with image: {updated_event["htmlLink"]}')

if __name__ == '__main__':
    main()
