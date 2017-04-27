import os
import tempfile
import pytest
import unittest
from deltaNiner.dashboard import app
from pprint import pprint as pp

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def testIndex(self):
        rv = self.app.get('/')
        assert b'Bluemix Overview' in rv.data

    def testTags(self):
        rv = self.app.get('/tags')
        pp(rv)
        assert b'ibm_created' in rv.data

if __name__ == '__main__':
    unittest.main()