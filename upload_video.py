from youtube_upload.client import YoutubeUploader
import os
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.discovery import build

# Read the title from the file
title_file_path = 'uploaded_video_name.txt'
with open(title_file_path, 'r', encoding='utf-8') as title_file:
    title = title_file.read().strip()

# Read the description from the file
description_file_path = 'uploaded_video_description.txt'
with open(description_file_path, 'r', encoding='utf-8') as description_file:
    description = description_file.read().strip()

# Define the token storage path
token_file_path = 'token.json'

# Initialize YoutubeUploader and authenticate if needed
if os.path.exists(token_file_path):
    # Load credentials from the storage
    storage = Storage(token_file_path)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        # Re-authenticate if the credentials are invalid
        flow = flow_from_clientsecrets('client.json', scope='https://www.googleapis.com/auth/youtube.upload')
        credentials = run_flow(flow, storage)
else:
    # Authenticate and save credentials if not present
    flow = flow_from_clientsecrets('client.json', scope='https://www.googleapis.com/auth/youtube.upload')
    storage = Storage(token_file_path)
    credentials = run_flow(flow, storage)

# Initialize YoutubeUploader with credentials
youtube = build('youtube', 'v3', credentials=credentials)
uploader = YoutubeUploader(secrets_file_path='client.json')
uploader.youtube = youtube

video_options = {
    "title": title,
    "description": description,
    "tags": ["Shorts", "Пример"],
    "categoryId": "22",  # Категория "Люди и блоги"
    "privacyStatus": "public",
    "kids": False
}

video_path = 'Final.mp4'
# Upload the video and get the response
response = uploader.upload(video_path, video_options)

# Extract video ID and generate YouTube URL
if response and 'id' in response:
    video_id = response['id']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"Video successfully uploaded: {video_url}")
else:
    print("Failed to retrieve video ID after upload.")

uploader.close()
