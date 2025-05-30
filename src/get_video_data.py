import json
from pathlib import Path
import os

from dotenv import load_dotenv
from exceptions.custom_exceptions import NoVideoDataError
import polars as pl
import requests
from youtube_transcript_api import YouTubeTranscriptApi


# Load environment variables from the .env file (if present)
# Use override=True to fetch the correct value whenever it is updated 
if load_dotenv(override=True):
    #add future logging message here saying .env is present

    #Access environment variables
    API_URL = os.getenv("API_URL")
    CHANNEL_ID = os.getenv("CHANNEL_ID")
    MY_YOUTUBE_API_KEY = os.getenv("MY_YOUTUBE_API_KEY")
else:
    #add future logging message
    print(".env not present")
    print("unable to obtain CHANNEL_ID or MY_YOUTUBE_API_KEY")

# Get Path to the /data folder
data_directory_path = Path(__file__).resolve().parent.parent /"data"

def make_video_records(response: requests.models.Response) -> list[dict[str,str]]:
    """
    Method to extract YouTube video data from GET request responses generating
    a list of dictionaries.

    Args:
        response (requests.models.Response): _description_

    Returns:
        list[dict[str, str]]: A list of dictionaries with keys: `video_id`, `datetime`, `title`
        derived from YouTube (YT) video data.
    """
    video_record_list = []

    for raw_item in json.loads(response.text)['items']:

        # Execute for YouTube videos only
        if raw_item["id"]["kind"] != "youtube#video":
            continue

        # Creata a video_record
        video_record = {} 
        video_record["video_id"] = raw_item["id"]["videoId"]
        video_record["datetime"] = raw_item["snippet"]["publishedAt"]
        video_record["title"] = raw_item["snippet"]["title"]

        video_record_list.append(video_record)

        return video_record_list

def extract_video_data(
        page_token: int,
        channel_id: str = CHANNEL_ID,
        api_url: str = API_URL,
        yt_api_key: str = MY_YOUTUBE_API_KEY
) -> None:
    """
    Method to generate two video_id data files in the following formats {.csv and .parquet}
    
    Args:
        page_token (int): Unique token for a YouTube video
        channel_id (str): The YouTube channel ID. Defaults to CHANNEL_ID.
        api_url (str): The YouTube API url. Defaults to API_URL.
        yt_api_key (str): A unique YouTube API key. Defaults to MY_YOUTUBE_API_KEY.

    Returns:
        None: Two files should be created and placed into the /data folder
            - video_ids.csv
            - video_ids.parquet
    """
    video_record_list = []

    # Extract video data across multiple search result pages
    while page_token != 0:
        # Define parameters for API call
        params = {
            "channel_id": channel_id,
            "key": yt_api_key,
            "maxResults": 50,
            "order": "date",
            "page_token": page_token,
            "part": ["snippet", "id"]
        }

        # Execute GET request
        response = requests.get(api_url, params=params)

        # Append generated video records to list
        video_record_list += make_video_records(response)

        try:
            page_token = json.loads(response.text)["nextPageToken"]
        except Exception:
            #logger.info("No next page token stopping the while loop")
            page_token = 0

    # Write data to files
    if video_record_list:
        pl.DataFrame(video_record_list).write_parquet(f"{data_directory_path.joinpath("video_ids.parquet")}")
        pl.DataFrame(video_record_list).write_csv(f"{data_directory_path.joinpath("video_ids.csv")}")
    else:
        raise NoVideoDataError("A data ingestion related error occurred: No videos were obtained ", channel_id)

    return None

def extract_transcript_text(transcript: list[dict[str, str]]) -> str:
    """
    Method to create a transcript text blog as a single string 
    derived from a list of transcript dictionaries

    Args:
        transcript (list[str]): list of YouTube transcript text

    Returns:
        str: a single string derived from a list of transcript string data
    """
    transcript_list = [transcript[i]["text"] for i in range(len(transcript))]
    return " ".join(transcript_list)

def get_yt_transcripts(video_id_file: str) -> None:
    """
    Method to get YouTube transcript string data from files specified by
    specific video ids in order to produce two data files: video_transcripts.csv 
    and video_transcripts.parquet

    Args:
        video_id_file (str): The path to the file containg the YouTube video ids

    Returns:
        None: Should produce two data files in the /data folder
        - video_transcripts.csv
        - video_transcripts.parquet
    """
    df = pl.read_parquet(video_id_file)

    transcript_text_list = []

    # Number of rows of polars df use df.height
    for row in range(df.height):
        # try to extract transcript data
        try:
            transcript = YouTubeTranscriptApi.get_transcript(df["video_id"][row])
            transcript_text = extract_transcript_text(transcript)
        except Exception:
            # No transcript available so setting value to n/a
            transcript_text = "n/a"

        transcript_text_list.append(transcript_text)

    # Put transcripts_text into the original dataframe
    df = df.with_columns(pl.Series(name="transcript", values=transcript_text_list))

    # Write data to files
    df.write_parquet(f"{data_directory_path.joinpath("video_transcripts.parquet")}")
    df.write_csv(f"{data_directory_path.joinpath("video_transcripts.csv")}")


# See notebook - eda.ipynb
# Peformed exploratory data analysis (EDA) on the transcript data to
# validate and transform the data appropriately. The function
# below performs the necessary as discovered from the EDA
# Including it here to simply all areas of the code to keep with
# The theme of Extract, Transform, and Load (ETL) of the data.
def validate_and_transform_data(video_id_file: str) -> None:
    """_
    Method to validate and transform current data files to fix
    issues uncovered during EDA. Updates two data files: 
    video_transcripts.csv and video_transcripts.parquet

    Args:
        video_id_file (str): The path to the file containg the YouTube video ids

    Returns:
        None: Should update two data files in the /data folder
        - video_transcripts.csv
        - video_transcripts.parquet
    """
    df = pl.read_parquet(video_id_file)

    #update the datetype format
    # change datetime to Datetime dtype
    df = df.with_columns(pl.col('datetime').cast(pl.Datetime))

    # Fixing the special strings
    # Uncovered during EDA special strings 
    special_strings = ['&#39;', '&amp;', 'sha ']
    special_string_replacements = ["'", "&", "Shaw "]

    for i in range(len(special_strings)):
        df = df.with_columns(df['title'].str.replace(special_strings[i], special_string_replacements[i]).alias('title'))
        df = df.with_columns(df['transcript'].str.replace(special_strings[i], special_string_replacements[i]).alias('transcript'))

    # Update data files
    df.write_parquet(f"{data_directory_path.joinpath("video_transcripts.parquet")}")
    df.write_csv(f"{data_directory_path.joinpath("video_transcripts.csv")}")