import dropbox as dropbox
import csv
import os


class DropBoxAuth:
    def __init__(self):
        self._path_dropbox = 'db.csv'
        self._token = 'm-UYk-cYBOQAAAAAAAAAAXgFomQ2Z5UsC43-sm_5e551dFedV26NWoMKKU_DygTv'
        self._dbx = dropbox.Dropbox(self._token)
        self._db = []
        self._field_names = ['log', 'pass']
        self._get_db()

    def _download_db(self):
        with open(self._path_dropbox, 'wb') as f:
            metadata, res = self._dbx.files_download(path='/' + self._path_dropbox)
            f.write(res.content)

    def _upload_db(self):
        with open(self._path_dropbox, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self._field_names)

            writer.writeheader()
            for row in self._db:
                writer.writerow(row)

        with open(self._path_dropbox, 'rb') as f:
            response = self._dbx.files_upload(f.read(), '/' + self._path_dropbox,
                                              mode=dropbox.files.WriteMode.overwrite)

        self._rm_db()

    def _get_db(self):
        self._download_db()

        with open(self._path_dropbox) as f:
            next(f)
            for line in csv.DictReader(f, fieldnames=self._field_names):
                self._db.append(line)

        self._rm_db()

    def _rm_db(self):
        if os.path.isfile(self._path_dropbox):
            os.remove(self._path_dropbox)

    def signin(self, login, password):
        user_data = [i for i in self._db if i['log'] == login]
        if user_data != [] and user_data[0]['pass'] == password:
            return True
        return False

    def register(self, login, password):
        if not [i for i in self._db if i['log'] == login]:
            self._db.append({'log': login, 'pass': password})
            self._upload_db()
            return True
        return False
