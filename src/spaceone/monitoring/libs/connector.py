import os
import logging
from spaceone.core.connector import BaseConnector
# from spaceone.monitoring.error.azure import *
from kubernetes import client
from kubernetes.config.kube_config import KubeConfigLoader

__all__ = ['KubeConnector']
_LOGGER = logging.getLogger(__name__)


class KubeConnector(BaseConnector):
    def __init__(self, *args, **kwargs):
        """
        kwargs
            - schema
            - options
            - secret_data
        """

        super().__init__(*args, **kwargs)
        self.core_v1_client = None

    @staticmethod
    def _get_kube_config(secret_data):
        return {
            "apiVersion": "v1",
            "kind": "Config",
            "clusters": [
                {
                    "cluster": {
                        "server": secret_data.get('server', ''),
                        "certificate-authority-data": secret_data.get('certificate_authority_data', '')
                    },
                    "name": secret_data.get('cluster_name', '')
                }
            ],
            "contexts": [
                {
                    "context": {
                        "cluster": secret_data.get('cluster_name', ''),
                        "user": secret_data.get('cluster_name', '')
                    },
                    "name": secret_data.get('cluster_name', '')
                }
            ],
            "current-context": secret_data.get('cluster_name', ''),
            "users": [
                {
                    "name": secret_data.get('cluster_name', ''),
                    "user": {
                        "token": secret_data.get('token', '')
                    }
                }
            ]
        }

    def set_connect(self, options: dict, secret_data: dict):
        """
        comment 바꾸기
        """
        try:
            kube_config = self._get_kube_config(secret_data)
            loader = KubeConfigLoader(config_dict=kube_config)
            configuration = client.Configuration()
            configuration.retries = 3
            configuration.client_side_validation = False
            loader.load_and_set(configuration)
            self.config = client.ApiClient(configuration)
            self.core_v1_client = client.CoreV1Api(self.config)

        except Exception as e:
            raise Exception("WHAT IS HAPPENING?", str(e))
