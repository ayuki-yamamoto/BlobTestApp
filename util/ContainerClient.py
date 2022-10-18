"""Azure Blob Storage Container Client

"""

import re
import uuid
import azure.storage.blob as blob

class ContainerClient:
    """Azure Blob Storage Container Client.
    """
    
    container_client = None
    """コンテナークライアント格納用の変数
    """
    
    def __init__(self,myblob):
        """Constructor.

        Args:
            myblob (azure.function.InputStream): Blob Data.
        """

        blob_service_client = blob.BlobServiceClient()
        self.container_client = blob_service_client.get_container_client(re.sub(r'(.*)/.*/.*', r'\1',myblob.name)) 

    def get_folder_list(self):
        """Get foldername list.

        Returns:
            set<str>: folder name list.
        """
        set = set()
        blob_list = self.container_client.list_blobs()
        for blob in blob_list:
            set.add(re.sub(r'(.*)/.*', r'\1',blob.name))
        return set
        
    def get_file_list(self, myblob):
        """Get blobProperties list.

        Args:
            myblob (azure.function.InputStream): Blob Data.

        Returns:
            BlobProperties[]: BlobProperties list.
        """
        file_list = self.container_client.list_blobs(myblob.folder_name)
        return file_list

    def read_file(self,file_name):
        """Read file as str.

        Args:
            file_name (str): file name.

        Returns:
            str: file content.
        """
        blob_client = self.container_client.get_blob_client(file_name)
        stream = blob_client.download_blob()
        return stream.content_as_text("utf-8")

    def read_file_chunks(self, file_name):
        """Read file as bytes.

        Read the file with the specified file name from inside the container owned by ContainerClient.
        The return value is returned in bytes type.

        Args:
            file_name (str): file name.

        Returns:
            bytes[]: file content.
        """
        blob_client = self.container_client.get_blob_client(file_name)
        stream = blob_client.download_blob()
        chunks = bytes()
        for chunk in stream.chunks():
            chunks += chunk
        return chunks

    def write_file(self,file,data):
        """Write content to file.

        Args:
            file (BlobProperties): file instance.
            data (any): content to write.
        """
        blob_client = self.container_client.get_blob_client(file.name)
        stream = blob_client.download_blob()
        block_list = []

        for chunk in stream.chunks():
            block_id = str(uuid.uuid4())
            blob_client.stage_block(block_id=block_id, data=chunk)
            block_list.append(blob.BlobBlock(block_id))

        block_id = str(uuid.uuid4())
        blob_client.stage_block(block_id=block_id, data=data)
        block_list.append(blob.BlobBlock(block_id))

        blob_client.commit_block_list(block_list)

    def create_file(self,file,data):
        """create new file and write content.

        Args:
            file (BlobProperties): file instance to create.
            data (any): content to write.
        """
        blob_client = self.container_client.get_blob_client(file.name)
        file = blob.BlobProperties()
        file.last_modified

        if blob_client.exists() == False:
            blob_client.upload_blob(data)
