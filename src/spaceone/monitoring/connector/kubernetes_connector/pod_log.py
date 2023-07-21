import logging
from spaceone.core import utils
from spaceone.monitoring.libs.connector import KubeConnector

__all__ = ['PodLog']
_LOGGER = logging.getLogger(__name__)

import dateutil.parser as date_parser
import datetime
import math


def find_new_logs(logs_list, prevTime):
    for i in range(len(logs_list)):
        if prevTime == logs_list[i].split(' ')[0]:
            return i
    return -1


class PodLog(KubeConnector):
    def __init__(self, client=None, **kwargs):
        super().__init__(**kwargs)

        # if client:
        #     self.client = client

    def list_logs(self):
        try:
            result = []
            pod_logs = ""
            if self.prevTime:
                print("PREV TIME EXISTS")
                parsed_prev_time = date_parser.parse(self.prevTime)
                prev_time_seconds = parsed_prev_time.timestamp()
                parsed_curr_time = date_parser.parse(datetime.datetime.now().isoformat())
                curr_time_seconds = parsed_curr_time.timestamp()
                pod_logs = self.core_v1_client.read_namespaced_pod_log(name=self.podName, namespace=self.namespace, timestamps=True, since_seconds=math.ceil(curr_time_seconds-prev_time_seconds))
                logs_list = pod_logs.rstrip('\n').split('\n')
                new_logs_index = find_new_logs(logs_list, self.prevTime)
                if new_logs_index != -1:
                    result = logs_list[new_logs_index+1:]
                else:
                    result = logs_list
            else:
                pod_logs = self.core_v1_client.read_namespaced_pod_log(name=self.podName, namespace=self.namespace, timestamps=True)
                result = pod_logs.rstrip('\n').split('\n')
            for lg in result:
                print(lg)
            print(result[-1].split(' ')[0])  # last log timestamp
            return result
        except Exception as e:
            _LOGGER.error(f"[list_metrics]: {e}")
            return []

    @staticmethod
    def _convert_timestamp(metric_datetime):
        return utils.datetime_to_iso8601(metric_datetime)

    @staticmethod
    def _get_metric_data(metric_value):
        if metric_value:
            return metric_value
        else:
            return 0
