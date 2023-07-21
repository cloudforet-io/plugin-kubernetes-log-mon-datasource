import logging
from spaceone.core.manager import BaseManager
from spaceone.monitoring.model.metadata.metadata import LogMetadata
from spaceone.monitoring.model.metadata.metadata_dynamic_field import TextDyField, DateTimeDyField, ListDyField, \
    MoreField
from spaceone.monitoring.conf.monitoring_conf import *

_LOGGER = logging.getLogger(__name__)


class MetadataManager(BaseManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get_data_source_metadata():
        metadata = LogMetadata.set_fields(
            name='kubernetes-pod-table',
            fields=[
                DateTimeDyField.data_source('Timestamp', 'timestamp'),
                TextDyField.data_source('Message', 'message'),
            ]
        )
        return metadata
