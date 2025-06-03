from pathlib import Path

from fastapi import FastAPI
import polars as pl
from sentence_transformers import SentenceTransformer
from sklearn.metrics import DistanceMetric
from src.functions import return_search_result_indices

# Define model info
model_name = 'all-MiniLM-L6-v2'
# Get Path to the /data folder - contains the sentenece tranformer model code
data_directory_path = Path(__file__).resolve().parent.parent /"data"
model_path = f"{data_directory_path.joinpath(model_name)}"

# Load sentence transformer model
model = SentenceTransformer(model_path)

# Load video index data file via scan and not loading the data itself - saves complexity and resources!
df = pl.scan_parquet(f"{data_directory_path.joinpath("video_index_full.parquet")}")

# Ceate distance metric object
dist_name = 'manhattan'
dist_measure = DistanceMetric.get_metric(dist_name)

# create FastAPI object API - for rendering the results of requests to the AI/ML model
app = FastAPI()

# API operations - GET requests for various endpoints
@app.get("/")
def health_check():
    return {"health_check": "OK"}

@app.get("/info")
def info():
    """ FASTAPI route for website """
    return {"name": "YouTube-Search", "description": "Search API for Shaw Talebi's YouTube videos."}

@app.get("/search")
def search(query: str):
    index_result = return_search_result_indices(query, df, model, dist_measure)
    return df.select(["title", "video_id"]).collect()[index_result].to_dict(as_series=False)