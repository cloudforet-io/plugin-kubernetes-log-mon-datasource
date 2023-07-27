import logging
from spaceone.monitoring.libs.connector import KubeConnector

__all__ = ['PodLog']
_LOGGER = logging.getLogger(__name__)

import dateutil.relativedelta
import dateutil.parser as date_parser
import datetime
import math



class PodLog(KubeConnector):
    def __init__(self, client=None, **kwargs):
        super().__init__(**kwargs)

    def list_logs(self, params):
        try:
            previous_time = params.get('start', '')
            query = params.get('query', {})
            namespace = query.get('namespace', '')
            pod_name = query.get('name', '')
            result = []
            pod_logs = ""

            if previous_time == '':
                prev_month_time = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
                previous_time = date_parser.parse(prev_month_time.isoformat())
            prev_time_seconds = previous_time.timestamp()
            parsed_curr_time = date_parser.parse(datetime.datetime.now().isoformat())
            curr_time_seconds = parsed_curr_time.timestamp()
            difference = curr_time_seconds - prev_time_seconds
            pod_logs = self.core_v1_client.read_namespaced_pod_log(name=pod_name, namespace=namespace,
                                                                   timestamps=True,
                                                                   since_seconds=math.ceil(difference))
            logs_list = pod_logs.rstrip('\n').split('\n')
            new_logs_index = self.find_new_logs(logs_list, previous_time)
            if new_logs_index:
                result = logs_list[new_logs_index+1:]
            else:
                result = logs_list
            # for lg in result:
            #     print(lg)
            # print(result[-1].split(' ')[0])  # last log timestamp

            return result
        except Exception as e:
            _LOGGER.error(f"[list_metrics]: {e}")
            return []

    @staticmethod
    def find_new_logs(logs_list, previous_time):
        for i in range(len(logs_list)):
            # 여기서, logs_list[i].split(' ')[0]의 값이 일단 timestamp 형식인지 확인하고, 아닐 경우 그냥 continue
            if previous_time == logs_list[i].split(' ')[0]:
                return i
        return False
