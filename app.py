import os
import datetime as dt
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import streamlit as st

# Set up Google Calendar API
SCOPES_CALENDAR = ["https://www.googleapis.com/auth/calendar"]
def create_google_calendar_event(summary, description, start_datetime, end_datetime, calendar_id, timezone):
    credentials = service_account.Credentials.from_service_account_file(
        'service.json', scopes=SCOPES_CALENDAR)
    
    service = build("calendar", "v3", credentials=credentials)
    service_all = service

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

# Set up Google Drive API
SCOPES_DRIVE = ["https://www.googleapis.com/auth/drive.file"]
def upload_image_to_drive(image_file_path, folder_id):
    credentials = service_account.Credentials.from_service_account_file(
        'service.json', scopes=SCOPES_DRIVE)
    
    drive_service = build("drive", "v3", credentials=credentials)

    file_metadata = {
        'name': os.path.basename(image_file_path),
        'parents': [folder_id]  # Specify the folder ID where you want to upload the image
    }

    media = MediaFileUpload(image_file_path, resumable=True)

    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return file.get('id')

if __name__ == '__main__':
    summary = 'Sample Event 5'
    description = 'Huzefa Khambhati Meet and Greet.' 
    start_datetime = '2023-10-05T12:00:00'
    end_datetime = '2023-10-05T13:00:00'
    calendar_id = 'sentosafirestation@gmail.com'
    timezone = 'Asia/Singapore'

    # Create the Google Calendar event
    event = create_google_calendar_event(summary, description, start_datetime, end_datetime, calendar_id, timezone)

    # Upload the image to Google Drive (modify with your image file path and folder ID)
    image_file_path = 'hk.jpg'
    folder_id = '1-dxUDRz9jcWF7efcMUI4U3wbBCMF09Lj'  # Specify the folder ID where you want to upload the image
    image_id = upload_image_to_drive(image_file_path, folder_id)

    # Attach the image URL to the event (modify the event as needed)
    event_description = f'{description}\nImage URL: https://drive.google.com/uc?id={image_id}'
    event['description'] = event_description

    # Update the event with the new description
    credentials_image = service_account.Credentials.from_service_account_file(
        'service.json', scopes=SCOPES_CALENDAR)
    service_image = build("calendar", "v3", credentials=credentials_image)
    updated_event = service_image.events().update(calendarId=calendar_id, eventId=event['id'], body=event).execute()
    print('Event updated with image URL:', updated_event['htmlLink'])
