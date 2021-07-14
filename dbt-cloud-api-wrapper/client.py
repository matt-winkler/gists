# sourced from: https://github.com/dwallace0723/py-dbt-cloud/blob/master/pydbtcloud/client.py

# -*- coding: utf-8 -*-
import json
import requests
import time
from enums import DbtJobRunStatus


class DbtCloud(object):
    """
    Class for interacting with the dbt Cloud API
    * :py:meth:`list_jobs` - list all Jobs for the specified Account ID
    * :py:meth:`get_run` - Get information about a specified Run ID
    * :py:meth:`trigger_job_run` - Trigger a Run for a specified Job ID
    * :py:meth: `try_get_run` - Attempts to get information about a specific Run ID for up to max_tries
    * :py:meth: `run_job` - Triggers a run for a job using the job name
    """

    def __init__(self, account_id, api_token):
        self.account_id = account_id
        self.api_token = api_token
        self.api_base = 'https://cloud.getdbt.com/api'

    def _get(self, url_suffix):
        url = self.api_base + url_suffix
        headers = {'Authorization': 'Token %s' % self.api_token}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise RuntimeError(response.content)

    def _post(self, url_suffix, data=None):
        url = self.api_base + url_suffix
        headers = {'Authorization': 'token %s' % self.api_token}
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise RuntimeError(response.content)
    
    def create_job(self, request):
        response = self._post('/v3/accounts/%s/jobs/', data=request)
        response.raise_for_status()
        return response

    def get_environment_by_name(self, env_name):
        pass

    def list_environments(self):
        return self._get('/v3/accounts/%s/environments/' % self.account_id).get('data')

    def list_jobs(self):
        return self._get('/v2/accounts/%s/jobs/' % self.account_id).get('data')

    def get_run(self, run_id):
        return self._get('/v2/accounts/%s/runs/%s/' % (self.account_id, run_id)).get('data')
    
    def get_run_artifact(self, run_id, artifact_name, save_to_file=True):
        if save_to_file:
            data = self._get('/v2/accounts/%s/runs/%s/%s' % (self.account_id, run_id, artifact_name)).get('data')
            self.save_artifact_to_file(data, artifact_name)
            return data
        else:
            return self._get('/v2/accounts/%s/runs/%s/%s' % (self.account_id, run_id, artifact_name)).get('data')
    
    def save_artifact_to_file(data, artifact_name):
        """Saves run artifacts locally"""
        with open(f'./artifacts/{artifact_name}', 'wt') as output_file:
            json.dump(data, output_file)

    def trigger_job_run(self, job_id, data=None):
        return self._post(url_suffix='/v2/accounts/%s/jobs/%s/run/' % (self.account_id, job_id), data=data).get('data')

    def try_get_run(self, run_id, max_tries=3):
        for i in range(max_tries):
            try:
                run = self.get_run(run_id)
                return run
            except RuntimeError as e:
                print("Encountered a runtime error while fetching status for {}".format(run_id))
                time.sleep(10)

        raise RuntimeError("Too many failures ({}) while querying for run status".format(run_id))
    
    def get_run_status(self, run_id, max_polling_time=600, polling_interval=10):
        """Identifies the status on a given run"""
        status = None
        for i in range(max_polling_time):
            status_data = self.get_run(run_id=run_id)
            status = status_data['status']
            
            if status == DbtJobRunStatus.SUCCESS:
                break
            elif status == DbtJobRunStatus.ERROR or status == DbtJobRunStatus.CANCELLED:
                raise Exception("Job run failed!")

            time.sleep(polling_interval)
        
        return status
    
    def run_job(self, job_name, data=None, ):
        jobs = self.list_jobs()

        job_matches = [j for j in jobs if j['name'] == job_name]
        if len(job_matches) != 1:
            raise Exception("{} jobs found for {}".format(len(job_matches), job_name))

        job_def = job_matches[0]
        trigger_resp = self.trigger_job_run(job_id=job_def['id'], data=data)
        run_id = trigger_resp['id']
        status = self.get_run_status(run_id=run_id)
        return status


