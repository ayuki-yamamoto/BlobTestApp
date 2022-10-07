import re
import uuid
import azure.storage.blob as blob

class ContainerClient:
    
    container_client = None     # コンテナークライアント
    
    # ContainerClientの作成
    def __init__(self,myblob):
        blob_service_client = blob.BlobServiceClient()
        self.container_client = blob_service_client.get_container_client('test-container')   # ContainerClientの作成

    # フォルダの名前一覧の取得
    def get_folder_list(self):
        set = set()
        blob_list = self.container_client.list_blobs()   # ファイルのリストを取得
        for blob in blob_list:
            set.add(re.sub(r'(.*)/.*', r'\1',blob.name)) # ファイル名からフォルダ名を取得しセットに追加
        return set
        
    # 指定ファイルと同じフォルダのファイル一覧の取得
    def get_file_list(self, myblob):
        file_list = self.container_client.list_blobs(myblob.folder_name)  # 指定フォルダ名から始まるファイルのリストを取得
        return file_list

    # 指定ファイルの読み込み(テキスト)
    def read_file(self,file):
        blob_client = self.container_client.get_blob_client(file.name)  # BlobClientを作成
        stream = blob_client.download_blob()    # StorageStreamDownloaderにストリームをダウンロード
        return stream.content_as_text("utf-8")  # 内容を読み取りデコード

    # 指定ファイルの読み込み(バイト)
    def read_file_chunks(self, file):
        blob_client = self.container_client.get_blob_client(file.name)
        stream = blob_client.download_blob()
        chunks = bytes()
        for chunk in stream.chunks():   # StorageStreamDownloaderの内容を分割して取得
            chunks += chunk             # 分割したchunkを結合
        return chunks

    # 指定ファイルの書き込み
    def write_file(self,file,data):
        blob_client = self.container_client.get_blob_client(file.name)
        stream = blob_client.download_blob()
        block_list = []     # BlobブロックのIDリスト

        for chunk in stream.chunks():
            block_id = str(uuid.uuid4())                            # BlobブロックIDの作成
            blob_client.stage_block(block_id=block_id, data=chunk)  # IDとデータを渡し、Blobブロックを作成
            block_list.append(blob.BlobBlock(block_id))             # IDリストに作成したBlobブロックのIDを追加

        block_id = str(uuid.uuid4())
        blob_client.stage_block(block_id=block_id, data=data)
        block_list.append(blob.BlobBlock(block_id))

        blob_client.commit_block_list(block_list)   # IDリストのIDと一致するBlobブロックを書き込み

    # 新規ファイルの作成
    def create_file(self,file,data):
        blob_client = self.container_client.get_blob_client(file.name)
        if blob_client.exists() == False:   # 指定ファイル名のファイルが存在するかを確認
            blob_client.upload_blob(data)   # ファイルをアップロード
