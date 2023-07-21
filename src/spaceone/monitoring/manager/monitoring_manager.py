import logging
from spaceone.core.manager import BaseManager
from spaceone.core import utils
from spaceone.core.utils import get_dict_value
from spaceone.monitoring.conf.monitoring_conf import *
from spaceone.monitoring.connector.kubernetes_connector.pod_log import PodLog
from spaceone.monitoring.model.log_model import Log, PodLogInfo
import dateutil.parser as date_parser

_LOGGER = logging.getLogger(__name__)



class MonitoringManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list_logs(self, params):
        results = []
        kubernetes_log_connector: PodLog = self.locator.get_connector('PodLog', **params)
        kubernetes_log_connector.set_connect(params.get('options'), params.get('secret_data'))

        logs = kubernetes_log_connector.list_logs()

        for log in logs:
            log_dict = self.create_log_dict(log)
            results.append(PodLogInfo(log_dict, strict=False))
        yield Log({'results': results})

    # @staticmethod
    # def keyword_filter(log, params):
    #     if keyword := params.get('keyword'):
    #         # value = get_dict_value(log, DEFAULT_EVENT_NAME_PATH)
    #         if keyword.lower() in log or keyword.capitalize() in log:
    #             return log
    #         else:
    #             return None
    #     else:
    #         return log

    def create_log_dict(self, log):
        timestamp, message = log.split(' ', 1)
        utc_time = date_parser.parse(timestamp)
        result = dict()
        result['timestamp'] = utc_time
        result['message'] = message
        return result
