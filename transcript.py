import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api import (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable)

class TranscriptError(Exception):
    """
    Custom exception for transcript related errors"""
    pass

def extract_video_id(url: str) -> str:
    """
    Extract the YouTube video ID from a URL
    """

    pattern = r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern,url)

    if not match:
        raise TranscriptError("Invalid YouTube URL format")
    
    return match.group(1)

def fetch_transcript(video_id: str) -> str:
    """
    Fetch transcript text for a given video ID
    """
    try:
        transcript = YouTubeTranscriptApi()
        output = transcript.fetch(video_id)
        return " ".join([t.text for t in output])
        
    
    except TranscriptsDisabled:
        raise TranscriptError("Transcripts are disabled for this video")
    
    except NoTranscriptFound:
        raise TranscriptError("No transcript found for this video")
    
    except VideoUnavailable:
        raise TranscriptError("Video is unavailable")
    
    except Exception as e:
        raise TranscriptError(f"Unexpected error: {str(e)}")
    

def get_transcript_from_url(url:str) -> str:
    """
    Validates URL and return transcript
    """

    video_id = extract_video_id(url)
    return fetch_transcript(video_id)

    