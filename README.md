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

## Generating a solution.

We include the `all-MiniLM-L6-v2` sentence transformer model code for the containerized solution
as it is the ML/AI model being used and would get passed into code.
downloaded from
https://github.com/henrytanner52/all-MiniLM-L6-v2

To run during development
in the same directory as the app.py folder
`$ uv run fastapi dev app.py`

Then: in tests folder you can run a notebook that will run some tests
Open a browser and use: http://127.0.0.1:8000

## Special Notes

#you can put these three in an .env folder locally and to add in github secrets for your own actions (see placement in .github/workflow/{}.yml)

API_URL="https://www.googleapis.com/youtube/v3/search" #Publically available API from YOUTUBE
CHANNEL_ID="UCa9gErQ9AE5jT2DZLjXBIdA" # Channel ID of the Shaw Talebi's youtub chanel
MY_YOUTUBE_API_KEY="GET YOUR OWN YOUTUBE API KEY" #link to video of how to get your own API

I ignore warning message like below during testing and running the code.

```
 PerformanceWarning: Determining the column names of a LazyFrame requires resolving its schema, which is a potentially expensive operation. Use `LazyFrame.collect_schema().names()` to get the column names without this warning.
    dist_arr = dist.pairwise(df.select(df.columns[4:388]).collect(), query_embedding) + dist.pairwise(df.select(df.columns[388:]).collect(), query_embedding)
```

As the code works fine and making the suggested change breaks the code. There is a reported [bug: use LazyFrame.collect_schema().names() over LazyFrame.columns #1744](https://github.com/unionai-oss/pandera/issues/1744) for this issue and the recommendation is to not use the suggested change in the warning message.

## Docker file

using uv dual build

created image using
$ docker build -t semantic_search_app .

creating container
-d will run the container in the background
$ docker run -d -p 80:80 --name yt_semantic_search_demo semantic_search_app

Use the notebook in the /data test folder to test docker container is running
(See Section)

- make sure container is running (optional check in )
  - $ docker ps -a # check if your container is running
  - view in dockerhub ui (optional)

## AWS

in your account
Elastic Container Service (ECS)
Need

1. Navigate to the ECS console and select the 'yt_search_cluster_demo' cluster

2. In the cluster view, locate the service 'yt_search_demo-service-66z0w9ow' and select it

3. Review the 'Events' tab for the service to identify specific deployment failure reasons

4. Check the 'Deployments' tab to see if there are any failed tasks or if the desired count doesn't match the running count

5. If tasks are failing, select a failed task and review its logs for error messages

6. Verify the task definition:

   - Ensure the container image exists and is accessible
   - Check if the container port mappings are correct
   - Verify the task CPU and memory allocations are sufficient

7. Review the service's network configuration:

   - Ensure the VPC, subnets, and security groups are properly configured
   - Verify that the necessary inbound and outbound rules are set in the security groups

8. Check the service auto scaling settings (if enabled) to ensure they are not causing issues

9. If the issue persists, consider rolling back to the previous task definition version:

   - Go to the 'Task Definitions' section
   - Select the previous working version of the task definition
   - Choose 'Create new revision'
   - Update the service to use this new revision

10. If you don't have permissions to perform any of these actions, contact your AWS Administrator

11. If all else fails, consider force deploying a new service:

    - Create a new service with a different name but using the same task definition and configuration
    - Once the new service is stable, delete the old service

12. Monitor the deployment progress in the ECS console to ensure the changes resolve the issue

https://gallery.ecr.aws/docker/library/python

###

Get hub actions

crontabresource
https://crontab.guru/

Setup github actions to generate new image and push to docker.
Complete readme

# Issues running Githu actions running out of space

https://github.com/orgs/community/discussions/25678
