import numpy as np
import polars
import sentence_transformers
import sklearn

def return_search_result_indices(query: str, 
                        df: polars.lazyframe.frame.LazyFrame, 
                        model: sentence_transformers, 
                        dist: sklearn.metrics.DistanceMetric) -> np.ndarray:
    """
    Method to return the indices of the top search results

    Args:
        query (str): The user query string to search for videos
        df (polars.lazyframe.frame.LazyFrame): the data 
        model (sentence_transformers): The sentence transformer model
        dist (sklearn.metrics.DistanceMetric): The distance measure used here it is Manhattan

    Returns:
        np.ndarray: the top indices of the search results from a given query
    """
    # Embed the query. Use reshape(-1,1) for a single feature; i.e., single column
    query_embedding = model.encode(query).reshape(1, -1)
    
    # Compute distances between query and titles/transcripts
    dist_arr = dist.pairwise(df.select(df.columns[4:388]).collect(), query_embedding) + dist.pairwise(df.select(df.columns[388:]).collect(), query_embedding)


    # Search paramaters
    threshold = 40 # eye balled threshold for manhattan distance 40 or less
    top_k = 5

    # Evaluate videos close to query based on threshold
    index_below_threshold = np.argwhere(dist_arr.flatten()<threshold).flatten()

    # Keep top k closest videos
    index_sorted = np.argsort(dist_arr[index_below_threshold], axis=0).flatten()

    # Return indices of search results
    return index_below_threshold[index_sorted][:top_k]