from googleapiclient.discovery import build
import pandas as pd

# # API Setup
# youtube = build('youtube', 'v3', developerKey=API_KEY)

# # Search YouTube
# def search_youtube(search_term, max_results=20):
#     response = youtube.search().list(
#         q=search_term,
#         part='snippet',
#         type='video',
#         maxResults=max_results
#     ).execute()

#     # Extract video details
#     videos = []
#     for item in response['items']:
#         print(item)
#         video_id = item['id']['videoId']
#         title = item['snippet']['title']
#         channel = item['snippet']['channelTitle']
#         videos.append({"Video Title": title, "Channel Name": channel, "Video ID": video_id})

#     return videos

# # Example Usage
# videos = search_youtube("Excel")
# # df = pd.DataFrame(videos)
# # df.to_csv("youtube_videos.csv", index=False)
# # print(df)


import os
from dotenv import load_dotenv
# from os import environ


load_dotenv()

# YouTube Data API setup
 


from googleapiclient.discovery import build
import pandas as pd

# YouTube Data API setup
API_KEY = os.getenv("API_KEY")  # Replace with your YouTube Data API key
youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_youtube_videos(search_term, max_results=20):
    """
    Search YouTube for videos based on a search term and retrieve their details.
    """
    response = youtube.search().list(
        q=search_term,
        part="snippet",
        type="video",
        maxResults=max_results
    ).execute()

    # Prepare a list for storing data
    videos = []

    for item in response['items']:
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"  # Construct video link
        title = item['snippet']['title']
        channel_title = item['snippet']['channelTitle']
        published_at = item['snippet']['publishedAt']
        description = item['snippet']['description']

        # Append video details to the list
        videos.append({
            "Video Title": title,
            "Channel Name": channel_title,
            "Published At": published_at,
            "Description": description,
            "Video URL": video_url
        })

    # Convert the list to a Pandas DataFrame
    df = pd.DataFrame(videos)
    return df

# Search YouTube and retrieve video details
search_term = "Excel"  # Replace with your search term
max_results = 20  # Adjust the number of results
df = search_youtube_videos(search_term, max_results)

# Save the results to a CSV file
csv_file = f"{search_term}_youtube_videos.csv"
df.to_csv(csv_file, index=False)

print(f"Data saved to {csv_file}")
print(df.head())


