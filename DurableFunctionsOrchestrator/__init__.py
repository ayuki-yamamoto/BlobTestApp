# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt


import logging
import azure.durable_functions as df

job_manager_file = None

def orchestrator_function(context: df.DurableOrchestrationContext):

    logging.info('DurableFunctionsOrchestrator() -start')
    logging.info(f'input object is [{context.get_input()}]')

    result1 = yield context.call_activity('CheckJob', context.get_input())
    result2 = yield context.call_activity('GetBlob', result1)
    result3 = yield context.call_activity('SaveBlob', result2)

    logging.info(f"result[{result3}]")
    return result3

main = df.Orchestrator.create(orchestrator_function)
