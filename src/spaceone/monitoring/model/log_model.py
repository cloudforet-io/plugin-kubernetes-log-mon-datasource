from schematics import Model
from schematics.types import ModelType, StringType, DateTimeType, ListType, DictType, BaseType


class PodLogInfo(Model):
    timestamp = DateTimeType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)


class Log(Model):
    results = ListType(ModelType(PodLogInfo), default=[])
