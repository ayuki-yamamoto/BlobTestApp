"""Timer Trigger

Call an Orchestrator function periodically

Attributes:
    orchestrator_name(str): Orchestrator function name
    job_status_file(str): Job status file path
"""
import json
import logging

import azure.functions as func
import azure.durable_functions as df

import util.ContainerClient as cc

orchestrator_name = 'DurableFunctionsOrchestrator'
job_status_file = 'temp/jobStatus.json'

async def main(mytimer: func.TimerRequest, starter: str) -> None:
    """main

    Call an Orchestrator function periodically

    Args:
        mytimer (azure.functions.TimerRequest): TimerTrigger
        starter (str): Orchestrator starter
    """
    logging.info('BlobStorageTrigger() -start')
    
    myblob = None
    myblob.name = ""

    container_client = cc.ContainerClient(myblob)

    input_object = json.loads()

    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new(orchestrator_name, input_object, None)

    logging.info(f'DurableFunction[{instance_id} -start]')
