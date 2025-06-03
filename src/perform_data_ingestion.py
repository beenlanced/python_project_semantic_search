from pathlib import Path

from get_video_data import extract_video_data, get_yt_transcripts, validate_and_transform_data


def main() -> None:
    """
    Ingest data (video id's and transcripts) from youtube
    """
    # Get video id data
    # Initialize Page token
    page_token = None
    extract_video_data(page_token)
    
    # Get transcript data
    video_id_file_path = Path(__file__).resolve().parent.parent /"data/video_ids.parquet"
    video_transcript_file_path = Path(__file__).resolve().parent.parent /"data/video_transcripts.parquet"

    get_yt_transcripts(str(video_id_file_path))
    validate_and_transform_data(str(video_transcript_file_path))

if __name__ == "__main__":
    main()
