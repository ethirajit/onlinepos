from __future__ import with_statement, unicode_literals
import errno
import os

from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class
from django.test import TestCase
from django.utils.functional import LazyObject

from compressor import storage
from compressor.conf import settings
from compressor.tests.test_base import css_tag
from compressor.tests.test_templatetags import render


class GzipStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class('compressor.storage.GzipCompressorFileStorage')()


class StorageTestCase(TestCase):
    def setUp(self):
        self.old_enabled = settings.COMPRESS_ENABLED
        settings.COMPRESS_ENABLED = True
        self.default_storage = storage.default_storage
        storage.default_storage = GzipStorage()

    def tearDown(self):
        storage.default_storage = self.default_storage
        settings.COMPRESS_ENABLED = self.old_enabled

    def test_gzip_storage(self):
        storage.default_storage.save('test.txt', ContentFile('yeah yeah'))
        self.assertTrue(os.path.exists(os.path.join(settings.COMPRESS_ROOT, 'test.txt')))
        self.assertTrue(os.path.exists(os.path.join(settings.COMPRESS_ROOT, 'test.txt.gz')))

    def test_css_tag_with_storage(self):
        template = """{% load compress %}{% compress css %}
        <link rel="stylesheet" href="{{ STATIC_URL }}css/one.css" type="text/css">
        <style type="text/css">p { border:5px solid white;}</style>
        <link rel="stylesheet" href="{{ STATIC_URL }}css/two.css" type="text/css">
        {% endcompress %}
        """
        context = {'STATIC_URL': settings.COMPRESS_URL}
        out = css_tag("/static/CACHE/css/1d4424458f88.css")
        self.assertEqual(out, render(template, context))

    def test_race_condition_handling(self):
        # Hold on to original os.remove
        original_remove = os.remove

        def race_remove(path):
            "Patched os.remove to raise ENOENT (No such file or directory)"
            original_remove(path)
            raise OSError(errno.ENOENT, 'Fake ENOENT')

        try:
            os.remove = race_remove
            self.default_storage.save('race.file', ContentFile('Fake ENOENT'))
            self.default_storage.delete('race.file')
            self.assertFalse(self.default_storage.exists('race.file'))
        finally:
            # Restore os.remove
            os.remove = original_remove
