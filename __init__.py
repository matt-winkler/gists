import logging
import enum
import azure.functions as func
import os
import time
import requests

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

def _trigger_job(account_id, job_id, msg) -> int:
    res = requests.post(
        url=f"https://cloud.getdbt.com/api/v2/accounts/{account_id}/jobs/{job_id}/run/",
        headers={'Authorization': f"Token {API_KEY}"},
        data={
            # Optionally pass a description that can be viewed within the dbt Cloud API.
            # See the API docs for additional parameters that can be passed in,
            # including `schema_override` 
            'cause': f"{msg}",
        }
    )

    try:
        res.raise_for_status()
    except:
        print(f"API token (last four): ...{API_KEY[-4:]}")
        raise

    response_payload = res.json()
    return response_payload['data']['id']

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
        msg = parameters.get('message', 'Triggered by Azure Data Factory Workflow')
    
    except KeyError:
        return func.HttpResponse(
             "Please pass the target account_id, job_id in the request body",
             status_code=400
        )
  
    job_run_id = _trigger_job(account_id=account_id, job_id=job_id, msg=msg)
    print(f"job_run_id = {job_run_id}")
    time.sleep(5)
    status = _get_job_run_status(account_id=account_id, job_run_id=job_run_id)

    if status == DbtJobRunStatus.QUEUED or status == DbtJobRunStatus.RUNNING:
        return func.HttpResponse(
                f"successfully triggered job {job_id} in account {account_id}",
                body={"job_run_id": job_run_id},
                status_code=200
            )

    else:
        return func.HttpResponse(
                f"Received status {status} triggering job {job_id} in account {account_id}",
                status_code=200
            )