from googleapiclient.discovery import build

from os import path
import os
from dotenv import load_dotenv
from os import environ

load_dotenv()

# YouTube Data API setup
API_KEY = os.getenv("API_KEY")  # Replace with your YouTube Data API key
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_tags(video_id):
    """
    Fetches the tags (keywords) of a YouTube video using its video ID.
    """
    response = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()

    # Extract tags from the API response
    try:
        tags = response['items'][0]['snippet'].get('tags', [])
        return tags
    except (IndexError, KeyError):
        print(f"Could not retrieve tags for video ID: {video_id}")
        return []

# Example usage
video_id = "XHT4paRaY4g"  # Replace with the specific video ID
tags = get_video_tags(video_id)
print(f"Tags for video ID {video_id}: {tags}")
