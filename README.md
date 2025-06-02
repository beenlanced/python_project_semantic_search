How to get your Youtube API key
https://www.youtube.com/watch?v=LLAZUTbc97I&t=48s

1. run perform_data_ingestion module by itself to first to accomplish data engineering aspects
   ETL extract transform and load data.

Produces the data files

2.

##

`Note` because of changes to YouTube API, I had to use alternate data files to truly show the ML solution.

These files are

- video_transcripts_full.parquet

  - A more robust file of video ids, datetimes, titles, and transcripts

- video_index_full.parquet

  - A

- eval_raw.csv

  - A file of user queries, and video ids. This file is used to evaluate the Machine Learning Solutions.

  ## Deep Learning Transformer models used

  Rnaking for each evaluation query happens

  SentenceTransformers is a set of models and frameworks that enable training and generating sentence embeddings from given data. The generated sentence embeddings can be utilized for Clustering, Semantic Search and other tasks.

  Hugging face (sentence transformer models)

  - all-MiniLM-L6-v2
  - multi-qa-distilbert-cos-v1
  - multi-qa-mpnet-base-dot-v1

Distance Measures:

- Euclidean
- Manhattan
- Chebyshev

Similarity measures:

- Cosine Similarity
- Dot Score

Evaluation using 3 different possible embeddings:

- Title (most sparse)
- Transcript
- Title + Transcript (most dense)

## Summary - model choice

The best embedding method overall was `all-MiniLM-L6-v2_title_transcript_manhattan` for this project because:

- all-MiniLM-L6-v2 is the most compact transformer and gives computational efficiency.

- It ranked hig as far as Mean. It was in the top 3 of the methods, and although not number 1 in the top-1
  it appears fairly efficient for its low cost complexity and size.

- It utilizes both title and transcript.

┌─────────────────────────────────┬─────────────────┬──────────────┬──────────────┐
│ method_name ┆ rank_query-mean ┆ num_in_top-1 ┆ num_in_top-3 │
│ --- ┆ --- ┆ --- ┆ --- │
│ str ┆ f64 ┆ u32 ┆ u32 │
╞═════════════════════════════════╪═════════════════╪══════════════╪══════════════╡
│ all-MiniLM-L6-v2_title_transcr… ┆ 0.875 ┆ 41 ┆ 60 │
│ all-MiniLM-L6-v2_title_manhatt… ┆ 0.921875 ┆ 44 ┆ 58 │
│ all-MiniLM-L6-v2_title_transcr… ┆ 0.96875 ┆ 41 ┆ 61 │
│ all-MiniLM-L6-v2_title_euclide… ┆ 1.09375 ┆ 45 ┆ 57 │
│ all-MiniLM-L6-v2_title_cos-sim ┆ 1.09375 ┆ 45 ┆ 57 │
└─────────────────────────────────┴─────────────────┴──────────────┴──────────────┘

## Created final data store using the winning method

`video_index_full.parquet`
This file will be the final data store will use in our production system. Essentially the data that
get's stored in the cloud and/or used for production purposes

## Generating User interface

reference: https://realpython.com/polars-lazyframe/
use with Polars dataframes

Test in the browser. with Gradio
videos won't render as well in the
