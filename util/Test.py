"""Test クライアント
"""

import re
from util.ContainerClient import ContainerClient
import azure.storage.blob as blob

class Test:
    """Test Client.
    """
    
    container_client: ContainerClient = None
    """コンテナークライアント格納用の変数
    """
    
    def __init__(self,client:ContainerClient):
        """コンストラクタ

        Args:
            client (ContainerClient): Containerクライアント
        """
        pass

    def get_folder_list(self,word: str, client: ContainerClient):
        """_summary_

        Args:
            word (str): キーワード
            client (ContainerClient): Containerクライアント

        Returns:
            set<ContainerClient>: ContainerクライアントのSet
        """
        set = set<ContainerClient>()
        blob_list = self.container_client.list_blobs()
        for blob in blob_list:
            set.add(re.sub(r'(.*)/.*', r'\1',blob.name))
        return set
