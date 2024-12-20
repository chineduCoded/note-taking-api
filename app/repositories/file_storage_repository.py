from app.interfaces.file_storage import FileStorage

class FileStorageRepository:
    def __init__(self, file_storage: FileStorage):
        self.file_storage = file_storage

    def upload(self, file: bytes) -> str:
        return self.file_storage.upload(file)