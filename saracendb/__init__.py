import os
import bson
import shutil

class SaracenDB:
    def __init__(self, filename: str, collection: str='default'):
        self.filename = filename
        self.collection = collection
        self.data = {}
        self.deleted = False
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.data = bson.decode(f.read())
        if self.collection not in self.data:
            self.data[self.collection] = []

    def query(self, key: str, value: str):
        matching_entries = []
        for entry in self.data[self.collection]:
            if key in entry and entry[key] == value:
                matching_entries.append(entry)
        return matching_entries

    def get(self, index: int):
        """Returns the entry at the given index in the current collection, or None if no entry is found."""
        try:
            return self.data[self.collection][index]
        except IndexError:
            print(f'No entry found at index: {index} in collection: {self.collection}')
            return None

    def put(self, key: str, value, index: int=None):
        """Add a new entry to the current collection."""
        data = {key: value}
        if index is None:
            self.data[self.collection].append(data)
        else:
            self.data[self.collection][index] = data

    def rm(self, index: int):
        """Delete an entry at the given index from the current collection."""
        try:
            del self.data[self.collection][index]
            self.deleted = True
        except IndexError:
            print(f'No entry found at index: {index} in collection: {self.collection}')

    def rm_collection(self):
        """Delete the current collection."""
        try:
            del self.data[self.collection]
            self.deleted = True
        except KeyError:
            print(f'No collection found for name: {self.collection}')

    def push(self):
        """Write changes to the database."""
        with open(self.filename, 'wb') as f:
            f.write(bson.encode(self.data))
        if self.deleted:
            self.compact()
            self.deleted = False

    def compact(self):
        """Remove deleted entries from the database / reduce file size."""
        temp_filename = self.filename + '.tmp'
        with open(temp_filename, 'wb') as f:
            f.write(bson.encode(self.data))
        shutil.move(temp_filename, self.filename)
        