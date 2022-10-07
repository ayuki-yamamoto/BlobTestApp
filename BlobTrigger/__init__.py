import logging

import azure.functions as func
from BlobTrigger2.ContainerClient import ContainerClient

def main(myblob: func.InputStream):

    logging.info(f"Import File is \"{myblob.name}\"")
