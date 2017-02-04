# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import qiniu as QiniuClass


class Qiniu(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self._access_key = app.config.get('QINIU_ACCESS_KEY', '')
        self._secret_key = app.config.get('QINIU_SECRET_KEY', '')
        self._bucket_name = app.config.get('QINIU_BUCKET_NAME', '')
        domain = app.config.get('QINIU_BUCKET_DOMAIN')
        if not domain:
            self._base_url = 'http://' + self._bucket_name + '.qiniudn.com'
        else:
            self._base_url = 'http://' + domain

    # localfile是本地的文件名 filename是远程的文件名
    def save(self, localfile, filename=None):
        auth = QiniuClass.Auth(self._access_key, self._secret_key)
        # filename是远程地址 也叫做key
        token = auth.upload_token(self._bucket_name,filename,3600)
        return QiniuClass.put_file(token, filename, localfile)

    def delete(self, filename):
        auth = QiniuClass.Auth(self._access_key, self._secret_key)
        bucket = QiniuClass.BucketManager(auth)
        return bucket.delete(self._bucket_name, filename)

    def url(self, filename):
        return urljoin(self._base_url, filename)