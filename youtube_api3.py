from datetime import datetime
from googleapiclient.discovery import build
from google.api_core.datetime_helpers import to_rfc3339

date_entered = "06/19/2018"
datetime_str = f'{date_entered} 23:59:59'
datetime_object = datetime.strptime(datetime_str, '%m/%d/%Y %H:%M:%S')
rfc3339_str = to_rfc3339(datetime_object)

api_key = "AIzaSyCSdtXwwN3yrfIl0gwle_yG8ifI-mlx25A"
youtube = build('youtube','v3', developerKey=api_key)
search = "cricket"
search_date = "2022-08-18T23:59:59Z"

pl_request = youtube.search().list(
    part = 'snippet',
    q = search,
    maxResults = 50,
    pageToken = nextPageToken,
    publishedBefore = search_date
)

pl_response = pl_request.execute()

# for item in pl_response['items']:
#     print(item)

videos = []
vid_ids = []

for item in pl_response['items']:
    vid_ids.append(item['id']['videoId'])

vid_request = youtube.videos().list(
        part = ["statistics","snippet"],
        id= ','.join(vid_ids)
    )

vid_response = vid_request.execute()

for item in vid_response['items']:
    vid_views = item['statistics']['viewCount']
    vid_id = item['id']
    vid_title = item["snippet"]["title"]
    yt_link = f"https://youtu.be/{vid_id}"

    videos.append(
        {
            "views" : int(vid_views),
            "url" : yt_link,
            "title": vid_title
        }
    )

videos.sort(key=lambda vid: vid['views'],reverse=True)

for video in videos[:10]:
    print(video['url'],video['views'],video['title'])