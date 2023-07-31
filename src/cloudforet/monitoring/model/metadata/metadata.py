from schematics import Model
from schematics.types import ListType, ModelType, PolyModelType, StringType
from cloudforet.monitoring.model.metadata.metadata_dynamic_layout import BaseLayoutField, TableDynamicLayout
from cloudforet.monitoring.model.metadata.metadata_dynamic_search import BaseDynamicSearch
from cloudforet.monitoring.model.metadata.metadata_dynamic_widget import BaseDynamicWidget


class MetaDataViewTable(Model):
    layout = PolyModelType(BaseLayoutField)


class MetaDataViewSubData(Model):
    layouts = ListType(PolyModelType(BaseLayoutField))


class MetaDataView(Model):
    table = PolyModelType(MetaDataViewTable, serialize_when_none=False)
    sub_data = PolyModelType(MetaDataViewSubData, serialize_when_none=False)
    search = ListType(PolyModelType(BaseDynamicSearch), serialize_when_none=False)
    widget = ListType(PolyModelType(BaseDynamicWidget), serialize_when_none=False)


class LogMetadata(Model):
    view = ModelType(MetaDataView)
    required_keys = ListType(StringType, default=['data.pod_logs'])
    supported_providers = ListType(StringType, default=['kubernetes'])

    @classmethod
    def set_fields(cls, name='', fields=[]):
        _table = MetaDataViewTable({'layout': TableDynamicLayout.set_fields(name, fields=fields)})
        return cls({'view': MetaDataView({'table': _table})})

    @classmethod
    def set_meta(cls, name='', fields=[], search=[], widget=[]):
        table_meta = MetaDataViewTable({'layout': TableDynamicLayout.set_fields(name, fields)})
        return cls({'view': MetaDataView({'table': table_meta, 'search': search, 'widget': widget})})


