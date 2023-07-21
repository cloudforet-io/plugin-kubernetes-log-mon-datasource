import logging
from spaceone.core.manager import BaseManager
from spaceone.monitoring.connector.kubernetes_connector.pod_log import PodLog
from spaceone.monitoring.model.data_source_response_model import DataSourceMetadata
from spaceone.monitoring.manager.metadata_manager import MetadataManager

_LOGGER = logging.getLogger(__name__)


class DataSourceManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def init(params):
        options = params['options']
        meta_manager = MetadataManager()
        response_model = DataSourceMetadata({'_metadata': meta_manager.get_data_source_metadata()}, strict=False)
        return response_model.to_primitive()

    def verify(self, params):
        activity_log_connector: PodLog = self.locator.get_connector('PodLog', **params)
        activity_log_connector.set_connect(params.get('query'), params.get('options'), params.get('secret_data'))
