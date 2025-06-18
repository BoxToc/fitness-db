import yt_dlp
from yt_dlp.utils import DownloadError

# Initialize YouTube Downloader object with default options
ydl = yt_dlp.YoutubeDL()

# Fetch video metadata
def get_info(url):
    with ydl:
        try:
            # Extract video information without downloading the video
            result = ydl.extract_info(url, download=False)
        except DownloadError:
            # Return None if the video fails to load (invalid URL)
            return None

    # If it's a playlist or search result, grab the first video
    if "entries" in result:
        video = result["entries"][0]
    else:
        video = result

    # Define the fields we want to extract from the video metadata
    infos = ['id', 'title', 'channel', 'view_count', 'like_count',
             'channel_id', 'duration', 'categories', 'tags']

    # Remap id field to video_id for consistency with the database
    def key_name(key):
        return "video_id" if key == "id" else key

    # Return a dictionary with the selected and renamed fields
    return {key_name(key): video[key] for key in infos}
