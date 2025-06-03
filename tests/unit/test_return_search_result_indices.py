from pathlib import Path

import polars as pl
import pytest
from sentence_transformers import SentenceTransformer
from sklearn.metrics import DistanceMetric
from src.functions import return_search_result_indices


# Define model info
model_name = 'all-MiniLM-L6-v2'
# Get Path to the /data folder - contains the sentenece tranformer model code
data_directory_path = Path(__file__).resolve().parent.parent.parent /"data"
model_path = f"{data_directory_path.joinpath(model_name)}"

# Load sentence transformer model
model = SentenceTransformer(model_path)

# Load video index data file via scan and not loading the data itself - saves complexity and resources!
df = pl.scan_parquet(f"{data_directory_path.joinpath("video_index_full.parquet")}")

# Ceate distance metric object
dist_name = 'manhattan'
dist_measure = DistanceMetric.get_metric(dist_name)

#query for testing
query = "text embeddings simply explained"

# Define the test data with pytext fixtures
test_data = [
    (query, df, model, dist_measure),
]

@pytest.mark.parametrize("query, df, model, dist_measure", test_data)
def test_return_search_result_indices(
    query: str, 
    df: pl.lazyframe.frame.LazyFrame,
    model: SentenceTransformer, 
    dist_measure: DistanceMetric
) -> None :
    """
    GIVEN return_search_result_indices, a method to obtain YouTuve video search results
    WHEN query, dataframe of video data, sententce transformer model, and similarity distance measures are provided
    THEN check that semantic search results for a video based on the query are returned.
    """
    assert return_search_result_indices(query, df, model, dist_measure) is not None