from googleapiclient.discovery import build
import pandas as pd


# from os import path
import os
from dotenv import load_dotenv
# from os import environ


load_dotenv()

# YouTube Data API setup
API_KEY = os.getenv("API_KEY")  # Replace with your YouTube Data API key
youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_youtube_videos(search_term, max_results=30):
    """
    Search YouTube for videos based on a search term and retrieve basic details.
    """
    response = youtube.search().list(
        q=search_term,
        part="snippet",
        type="video",
        maxResults=max_results
    ).execute()

    # Prepare a list for storing basic video data
    videos = []

    for item in response['items']:
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"  # Construct video link
        title = item['snippet']['title']
        channel_title = item['snippet']['channelTitle']
        published_at = item['snippet']['publishedAt']
        description = item['snippet']['description']

        # Append basic video details to the list
        videos.append({
            "Video Title": title,
            "Channel Name": channel_title,
            "Published At": published_at,
            "Description": description,
            "Video URL": video_url,
            "Video ID": video_id  # Store video ID for further details
        })

    # Convert the list to a Pandas DataFrame
    df = pd.DataFrame(videos)
    return df

def fetch_video_details(video_ids):
    """
    Fetch additional details for a list of video IDs.
    """
    # Split video IDs into chunks of up to 50 (API limit per request)
    chunks = [video_ids[i:i+50] for i in range(0, len(video_ids), 50)]

    details = []
    for chunk in chunks:
        response = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=",".join(chunk)
        ).execute()

        for item in response['items']:
            video_id = item['id']
            tags = item['snippet'].get('tags', [])
            view_count = item['statistics'].get('viewCount', 0)
            like_count = item['statistics'].get('likeCount', 0)
            comment_count = item['statistics'].get('commentCount', 0)
            duration = item['contentDetails']['duration']

            details.append({
                "Video ID": video_id,
                "Tags": tags,
                "View Count": int(view_count),
                "Like Count": int(like_count),
                "Comment Count": int(comment_count),
                "Duration": duration
            })

    # Convert to a DataFrame
    details_df = pd.DataFrame(details)
    return details_df

# Search YouTube and retrieve basic video details
search_term = "Excel AI"  # Replace with your search term
max_results = 20  # Adjust the number of results
basic_df = search_youtube_videos(search_term, max_results)

# Fetch additional details using video IDs
video_ids = basic_df["Video ID"].tolist()
details_df = fetch_video_details(video_ids)

# Merge the two DataFrames on Video ID
final_df = pd.merge(basic_df, details_df, on="Video ID")

# Save the final results to a CSV file
# csv_file = f"{search_term}_tableau_videos_detailed.csv"
# final_df.to_csv(csv_file, index=False)

# print(f"Detailed data saved to {csv_file}")
print(final_df.head())
