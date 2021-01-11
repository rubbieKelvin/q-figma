import io
import json
import requests


class RemoteFigmaFile(object):
    """RemoteFigmaFile: use this class to fetch and save remote figma files"""

    def __init__(self, file_id: str, token: str):
        super(RemoteFigmaFile, self).__init__()
        self.file_id = file_id
        self.token = token
        self.data_ = None

    @property
    def data(self) -> dict:
        return self.data_

    @property
    def remote_url(self) -> str:
        """get the remote url for the file"""
        return f"https://api.figma.com/v1/files/{self.file_id}"

    @property
    def downloaded(self) -> bool:
        """has this content been downloaded"""
        return not (self.data is None)

    def download(self) -> bool:
        try:
            response = requests.get(self.remote_url, headers={'X-Figma-Token': self.token})
        except requests.exceptions.ConnectionError:
            return False

        if response.status_code == 200:
            self.data_ = response.json()
        return response.status_code == 200

    def save(self, file: io.BufferedWriter):
        """save the data to the file"""
        if self.downloaded:
            json.dump(self.data, file, indent=2)
