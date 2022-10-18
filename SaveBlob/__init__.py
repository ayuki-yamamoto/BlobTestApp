# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt
"""Blobにデータを保存
"""

import logging


def main(name: str) -> str:
    """テキスト編集

    Args:
        name (str): 編集対象テキスト

    Returns:
        str: 編集後テキスト
    """
    return f"{name}Save Blob!"
