import os
import requests
import json
import csv
import pandas as pd


account_id = <dbt-account-id>
job_run_id = <dbt-job-run-id>

API_KEY = os.getenv('DBT_CLOUD_API_USER_TOKEN')
HEADERS = {'Authorization': 'Token '+ API_KEY + ''}

def run():
    url = f"https://cloud.getdbt.com/api/v2/accounts/{account_id}/runs/{job_run_id}/artifacts/run_results.json"
    response = requests.get(url, headers= HEADERS)

    response.raise_for_status()
    run_results = response.json()

    metadata = run_results.get('metadata')
    job_details = metadata.get('env')

    result = []
    for model in run_results['results']:
        result.append([model['unique_id'], model['status'], model['execution_time']])

    df_results = pd.DataFrame(result, columns = ['model_name', 'status', 'execution_time'])

    df_results = df_results.assign(
        invocation_id = metadata.get('invocation_id'),
        generated_at = metadata.get('generated_at'), #this is not really accurate since this is the global value
        project_id = job_details.get('DBT_CLOUD_PROJECT_ID'),
        run_id = job_details.get('DBT_CLOUD_RUN_ID'),
        job_id = job_details.get('DBT_CLOUD_JOB_ID'),
        run_reason = job_details.get('DBT_CLOUD_RUN_REASON')
        )

    pd.io.gbq.to_gbq(dataframe = df_results,destination_table = 'scratch.test', project_id = '<gcp-project-id>',if_exists = 'append') #private_key = 'metadata-discourse-project-73411f6c62a1.json'
    print('Saved to BQ')

if __name__ == '__main__':
    run()
