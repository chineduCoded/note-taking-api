from fastapi import UploadFile


class FileUploadService:

    @staticmethod
    def upload_file(file: UploadFile) -> dict:
        pass

    @staticmethod
    def delete_file(file_name: str) -> dict:
        pass

    @staticmethod
    def get_file(file_name: str) -> dict:
        pass

    @staticmethod
    def get_files() -> dict:
        pass

    @staticmethod
    def download_file(file_name: str) -> dict:
        pass

    @staticmethod
    def download_files() -> dict:
        pass

    @staticmethod
    def get_file_info(file_name: str) -> dict:
        pass

    @staticmethod
    def get_files_info() -> dict:
        pass

    @staticmethod
    def process_file(file: UploadFile) -> str:
        pass