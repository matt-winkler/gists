import logging
import enum
import azure.functions as func
import os
import time
import requests

#ACCOUNT_ID = os.getenv('DBT_CLOUD_ACCOUNT_ID')
#JOB_ID = os.getenv('DBT_CLOUD_JOB_ID')

# Store your dbt Cloud API token securely in your workflow tool
API_KEY = os.getenv('DBT_CLOUD_API_KEY')

# These are documented on the dbt Cloud API docs
class DbtJobRunStatus(enum.IntEnum):
    QUEUED = 1
    STARTING = 2
    RUNNING = 3
    SUCCESS = 10
    ERROR = 20
    CANCELLED = 30

def _get_job_run_status(account_id, job_run_id):
    res = requests.get(
        url=f"https://cloud.getdbt.com/api/v2/accounts/{account_id}/runs/{job_run_id}/",
        headers={'Authorization': f"Token {API_KEY}"},
    )

    res.raise_for_status()
    response_payload = res.json()
    return response_payload['data']['status']

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        parameters = req.get_json()
        job_id = parameters['job_id']
        account_id = parameters['account_id']
    
    except KeyError:
        return func.HttpResponse(
             "Please pass the target account_id, job_id in the request body",
             status_code=400
        )    
