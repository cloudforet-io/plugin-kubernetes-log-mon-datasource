import os
import unittest
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import utils
from spaceone.tester import TestCase, print_json


class TestCollector(TestCase):

    @classmethod
    def setUpClass(cls):
        CLUSTER_NAME = os.environ.get('CLUSTER_NAME', None)
        TOKEN = os.environ.get('TOKEN', None)
        SERVER = os.environ.get('SERVER', None)
        CERTIFICATE_AUTHORITY_DATA = os.environ.get('CERTIFICATE_AUTHORITY_DATA', None)

        cls.secret_data = {
            "cluster_name": CLUSTER_NAME,
            "certificate_authority_data": CERTIFICATE_AUTHORITY_DATA,
            "server": SERVER,
            "token": TOKEN
        }
        super().setUpClass()

    def test_init(self):
        v_info = self.monitoring.DataSource.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        options = {
        }
        v_info = self.monitoring.DataSource.verify({'options': options, 'secret_data': self.secret_data})
        print_json(v_info)

    def test_collect(self):
        query = {'namespace': 'sooyoung', 'podName': 'nginx'}
        start = '2023-07-21T05:36:57.634876054Z'
        end = '2022-08-01T06:00:53.873Z'

        resource_stream = self.monitoring.Log.list({'options': {},
                                                    'secret_data': self.secret_data,
                                                    'query': query,
                                                    'start': start,
                                                    'end': end})

        for res in resource_stream:
            print_json(res)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
