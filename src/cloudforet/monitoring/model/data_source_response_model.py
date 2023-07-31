from schematics import Model
from schematics.types.compound import PolyModelType
from cloudforet.monitoring.model import LogMetadata


class DataSourceMetadata(Model):
    _metadata = PolyModelType(LogMetadata, serialized_name='metadata', serialize_when_none=False)
