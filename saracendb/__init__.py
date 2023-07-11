import os
import bson
import shutil

class SaracenDB:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = {}
        self.deleted = False
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.data = bson.decode(f.read())

    def get(self, key: str):
        """Returns the value associated with the given key, or None if no entry is found."""
        try:
            return self.data[key]
        except KeyError:
            print(f'No entry found for key: {key}')
            return None

    def search(self, prefix: str):
        """Returns a list of keys that start with the given prefix."""
        return [key for key in list(self.data.keys()) if key.startswith(prefix)]

    def put(self, key: str, value):
        """Create or update an entry with the given key and value."""
        self.data[key] = value
    
    def rm(self, key: str):
        """Delete an entry with the given key."""
        try:
            del self.data[key]
            self.deleted = True
        except KeyError:
            print(f'No entry found for key: {key}')
        
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