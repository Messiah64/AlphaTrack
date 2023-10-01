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
    
    

    json_file = {
  "type": "service_account",
  "project_id": "alpha-track-400504",
  "private_key_id": "ef10fabdc75ef10e9c6ba99440536798dd608d1b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCxYICUviknIAQm\n/FlvOFEObeBEH23AFHq0qnO710JmXg5SaLAKf5OdDz6prgkGe1TKWTdDyvGeYHuY\nPPkkS1GA3+jSR+sWUtTgxBwvvMPboK3l7WsWAW49/CXE2ANOKC4/s7Y2nfi1w6wk\nfqq+YGua3f3pJFIjNHDFEx9C8/KbUfQ49IlbK3AnDYSYGs/Lxy7EcT86b1ZWNx5z\ngPZTNIJ4Ouu23sea5YXQVfPXJbrl61mrWq9x4Qz0f1raJaBdwj+KVfUgQSm98KS0\nBzVDl/2P9CiNCkEqWqegRAT2TJtzq32HpdFccPEsmQoNR6bMlzxzSHi0uI1cDWCW\noUoYaBh3AgMBAAECggEAUU3ComtnwZ9TR+tzsx9FSC/lFFSzoc/BTv6yfe91aCbE\nudFyn91KdDuApZY4XNg7TWUHh/OGPOpMvMN2D8TWXxRDS9/bSig9m6lIojkMLafB\nDht9cmDFf3QMe+Xn3fNc/6YIZ5CRZ/+A8Fl/OjRIHnyS3kLfw3NOHYdeVPoswjRS\n51FbRLqkJlOz+pwFMUNg+ll0FXFX7tiMQbyG3jbMDt8h2s3+rFzuN8T0u9Hwjce6\nToM5FEizfI/OPpoPaM52z2OU6uzGaYAw6/AuQc13UYLIEz2CgugWFx6pgps8pvBa\nceXwTcciEg884Abm0UwvgKGj9IjVZemv32+quyGLQQKBgQDh0WEDesHsKFj3Pwz+\nIN4x7rPXM8S3E9627hpcduCRFx+7+LEtEtxoirgUq3IBqff2x1KCeTbim079BXJH\nmZi28Q06BFMVg6EopNrp/braWM4ki0sgNvovjOIeEQC82gXIccp4alkcPoppbyvS\ntFqzmaToyB30cc+zwFhlrHcS3QKBgQDJFakuSX0kimYP6zkLTJ4/dkXoV5zw7p8T\nglOBs/zc8ksbnVGWfSo5zCspaFJU0Ex9xFnsAQj/92WWf51XyZD1oU73Y6LwG/vy\n2ryJBfOOzjVGBI/4Ye+PvU3aVy14LoAhdzVjjKcAjV9svfuXWS6wJYJA2xwu2B0s\nlr+0RAWxYwKBgQC34l9EjRcS7nwbwg0bd7pYIM/zoyVCC/0lK1juCKOvoovl7oqg\ncKZovuVNd5rbvgO8wezvcDOAbgXxRhkcMvhHqJ0jrFfXwhte1HeraUFaAkzDN2aS\nshIi3G9ZGnFmV4e0BO1iBv/PXyIo3y1pZBIkBC5knGjAIFmJP0z8ZmeERQKBgQCF\n1/siKhw4BD7m/aSclsUGbM0fV6HI5KvRqn+253y5/DRuDwrNZkaC7hkUmLGkbnlb\nhSRtaEr7RUrDH/I1Cp+IP3R2SkWcGKRdA6dWdTWmqi7fig3iQB3aySBW4owLYLg8\njkJlHqvSPEd19AbQuLXQ3UaTsMRTkdnpYfX8IQLBDQKBgFvOG8BSjSgoX2tayQR8\nxMblZ1q4/TKiVj29OguV4nRDz88iacmaoMAnfzFT64uFxnGKd0ytjY4HQfxSNj3a\nWbWUzOPdFiNEGV/QtEup2Xo7hsHm0N5mVomh9oXTPYxxPCGPDQbV8XCoiDIeNNJv\nphI6sbzsN8YkxOVayc8ZNft5\n-----END PRIVATE KEY-----\n",
  "client_email": "sentosafirestation@alpha-track-400504.iam.gserviceaccount.com",
  "client_id": "110361392616457721801",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sentosafirestation%40alpha-track-400504.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
    
    credentials = service_account.Credentials.from_service_account_info( json_file , scopes=SCOPES_CALENDAR)
        
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
    
    json_file = {
  "type": "service_account",
  "project_id": "alpha-track-400504",
  "private_key_id": "ef10fabdc75ef10e9c6ba99440536798dd608d1b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCxYICUviknIAQm\n/FlvOFEObeBEH23AFHq0qnO710JmXg5SaLAKf5OdDz6prgkGe1TKWTdDyvGeYHuY\nPPkkS1GA3+jSR+sWUtTgxBwvvMPboK3l7WsWAW49/CXE2ANOKC4/s7Y2nfi1w6wk\nfqq+YGua3f3pJFIjNHDFEx9C8/KbUfQ49IlbK3AnDYSYGs/Lxy7EcT86b1ZWNx5z\ngPZTNIJ4Ouu23sea5YXQVfPXJbrl61mrWq9x4Qz0f1raJaBdwj+KVfUgQSm98KS0\nBzVDl/2P9CiNCkEqWqegRAT2TJtzq32HpdFccPEsmQoNR6bMlzxzSHi0uI1cDWCW\noUoYaBh3AgMBAAECggEAUU3ComtnwZ9TR+tzsx9FSC/lFFSzoc/BTv6yfe91aCbE\nudFyn91KdDuApZY4XNg7TWUHh/OGPOpMvMN2D8TWXxRDS9/bSig9m6lIojkMLafB\nDht9cmDFf3QMe+Xn3fNc/6YIZ5CRZ/+A8Fl/OjRIHnyS3kLfw3NOHYdeVPoswjRS\n51FbRLqkJlOz+pwFMUNg+ll0FXFX7tiMQbyG3jbMDt8h2s3+rFzuN8T0u9Hwjce6\nToM5FEizfI/OPpoPaM52z2OU6uzGaYAw6/AuQc13UYLIEz2CgugWFx6pgps8pvBa\nceXwTcciEg884Abm0UwvgKGj9IjVZemv32+quyGLQQKBgQDh0WEDesHsKFj3Pwz+\nIN4x7rPXM8S3E9627hpcduCRFx+7+LEtEtxoirgUq3IBqff2x1KCeTbim079BXJH\nmZi28Q06BFMVg6EopNrp/braWM4ki0sgNvovjOIeEQC82gXIccp4alkcPoppbyvS\ntFqzmaToyB30cc+zwFhlrHcS3QKBgQDJFakuSX0kimYP6zkLTJ4/dkXoV5zw7p8T\nglOBs/zc8ksbnVGWfSo5zCspaFJU0Ex9xFnsAQj/92WWf51XyZD1oU73Y6LwG/vy\n2ryJBfOOzjVGBI/4Ye+PvU3aVy14LoAhdzVjjKcAjV9svfuXWS6wJYJA2xwu2B0s\nlr+0RAWxYwKBgQC34l9EjRcS7nwbwg0bd7pYIM/zoyVCC/0lK1juCKOvoovl7oqg\ncKZovuVNd5rbvgO8wezvcDOAbgXxRhkcMvhHqJ0jrFfXwhte1HeraUFaAkzDN2aS\nshIi3G9ZGnFmV4e0BO1iBv/PXyIo3y1pZBIkBC5knGjAIFmJP0z8ZmeERQKBgQCF\n1/siKhw4BD7m/aSclsUGbM0fV6HI5KvRqn+253y5/DRuDwrNZkaC7hkUmLGkbnlb\nhSRtaEr7RUrDH/I1Cp+IP3R2SkWcGKRdA6dWdTWmqi7fig3iQB3aySBW4owLYLg8\njkJlHqvSPEd19AbQuLXQ3UaTsMRTkdnpYfX8IQLBDQKBgFvOG8BSjSgoX2tayQR8\nxMblZ1q4/TKiVj29OguV4nRDz88iacmaoMAnfzFT64uFxnGKd0ytjY4HQfxSNj3a\nWbWUzOPdFiNEGV/QtEup2Xo7hsHm0N5mVomh9oXTPYxxPCGPDQbV8XCoiDIeNNJv\nphI6sbzsN8YkxOVayc8ZNft5\n-----END PRIVATE KEY-----\n",
  "client_email": "sentosafirestation@alpha-track-400504.iam.gserviceaccount.com",
  "client_id": "110361392616457721801",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sentosafirestation%40alpha-track-400504.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
    
    credentials = service_account.Credentials.from_service_account_info( json_file , scopes=SCOPES_CALENDAR)
    
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

                json_file = {
  "type": "service_account",
  "project_id": "alpha-track-400504",
  "private_key_id": "ef10fabdc75ef10e9c6ba99440536798dd608d1b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCxYICUviknIAQm\n/FlvOFEObeBEH23AFHq0qnO710JmXg5SaLAKf5OdDz6prgkGe1TKWTdDyvGeYHuY\nPPkkS1GA3+jSR+sWUtTgxBwvvMPboK3l7WsWAW49/CXE2ANOKC4/s7Y2nfi1w6wk\nfqq+YGua3f3pJFIjNHDFEx9C8/KbUfQ49IlbK3AnDYSYGs/Lxy7EcT86b1ZWNx5z\ngPZTNIJ4Ouu23sea5YXQVfPXJbrl61mrWq9x4Qz0f1raJaBdwj+KVfUgQSm98KS0\nBzVDl/2P9CiNCkEqWqegRAT2TJtzq32HpdFccPEsmQoNR6bMlzxzSHi0uI1cDWCW\noUoYaBh3AgMBAAECggEAUU3ComtnwZ9TR+tzsx9FSC/lFFSzoc/BTv6yfe91aCbE\nudFyn91KdDuApZY4XNg7TWUHh/OGPOpMvMN2D8TWXxRDS9/bSig9m6lIojkMLafB\nDht9cmDFf3QMe+Xn3fNc/6YIZ5CRZ/+A8Fl/OjRIHnyS3kLfw3NOHYdeVPoswjRS\n51FbRLqkJlOz+pwFMUNg+ll0FXFX7tiMQbyG3jbMDt8h2s3+rFzuN8T0u9Hwjce6\nToM5FEizfI/OPpoPaM52z2OU6uzGaYAw6/AuQc13UYLIEz2CgugWFx6pgps8pvBa\nceXwTcciEg884Abm0UwvgKGj9IjVZemv32+quyGLQQKBgQDh0WEDesHsKFj3Pwz+\nIN4x7rPXM8S3E9627hpcduCRFx+7+LEtEtxoirgUq3IBqff2x1KCeTbim079BXJH\nmZi28Q06BFMVg6EopNrp/braWM4ki0sgNvovjOIeEQC82gXIccp4alkcPoppbyvS\ntFqzmaToyB30cc+zwFhlrHcS3QKBgQDJFakuSX0kimYP6zkLTJ4/dkXoV5zw7p8T\nglOBs/zc8ksbnVGWfSo5zCspaFJU0Ex9xFnsAQj/92WWf51XyZD1oU73Y6LwG/vy\n2ryJBfOOzjVGBI/4Ye+PvU3aVy14LoAhdzVjjKcAjV9svfuXWS6wJYJA2xwu2B0s\nlr+0RAWxYwKBgQC34l9EjRcS7nwbwg0bd7pYIM/zoyVCC/0lK1juCKOvoovl7oqg\ncKZovuVNd5rbvgO8wezvcDOAbgXxRhkcMvhHqJ0jrFfXwhte1HeraUFaAkzDN2aS\nshIi3G9ZGnFmV4e0BO1iBv/PXyIo3y1pZBIkBC5knGjAIFmJP0z8ZmeERQKBgQCF\n1/siKhw4BD7m/aSclsUGbM0fV6HI5KvRqn+253y5/DRuDwrNZkaC7hkUmLGkbnlb\nhSRtaEr7RUrDH/I1Cp+IP3R2SkWcGKRdA6dWdTWmqi7fig3iQB3aySBW4owLYLg8\njkJlHqvSPEd19AbQuLXQ3UaTsMRTkdnpYfX8IQLBDQKBgFvOG8BSjSgoX2tayQR8\nxMblZ1q4/TKiVj29OguV4nRDz88iacmaoMAnfzFT64uFxnGKd0ytjY4HQfxSNj3a\nWbWUzOPdFiNEGV/QtEup2Xo7hsHm0N5mVomh9oXTPYxxPCGPDQbV8XCoiDIeNNJv\nphI6sbzsN8YkxOVayc8ZNft5\n-----END PRIVATE KEY-----\n",
  "client_email": "sentosafirestation@alpha-track-400504.iam.gserviceaccount.com",
  "client_id": "110361392616457721801",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sentosafirestation%40alpha-track-400504.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
    
                credentials_image = service_account.Credentials.from_service_account_info( json_file , scopes=SCOPES_CALENDAR)
                service_image = build("calendar", "v3", credentials=credentials_image)
                updated_event = service_image.events().update(calendarId=calendar_id, eventId=event['id'], body=event).execute()

                st.success(f'Event created with image: {updated_event["htmlLink"]}')

if __name__ == '__main__':
    main()
