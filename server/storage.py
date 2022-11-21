import json


class Storage:

    file_name: str = "storage.json"
    _storage: dict = {}

    def update(self, content: dict):
        self._storage.update(content)

    def read(self):
        with open(self.file_name, 'r') as f:
            self._storage.update(json.load(f))

    def write(self):
        self.read()
        with open(self.file_name, 'w') as f:
            json.dump(self._storage, f, indent=2)
