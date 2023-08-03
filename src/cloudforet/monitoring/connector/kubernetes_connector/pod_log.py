import logging
from cloudforet.monitoring.libs.connector import KubeConnector

__all__ = ['PodLog']
_LOGGER = logging.getLogger(__name__)

import dateutil.relativedelta
import dateutil.parser as date_parser
import datetime
import math
import re


class PodLog(KubeConnector):
    def __init__(self, client=None, **kwargs):
        super().__init__(**kwargs)

    def list_logs(self):
        try:
            namespace = self.query['namespace']
            pod_name = self.query['name']
            previous_time = self.previous_time

            difference = self.get_time_interval(previous_time)
            pod_logs = self.core_v1_client.read_namespaced_pod_log(name=pod_name, namespace=namespace,
                                                                   timestamps=True,
                                                                   since_seconds=math.ceil(difference))
            if not pod_logs:
                # if no logs exist, return empty list
                return []
            parsed_logs = pod_logs.rstrip('\n').split('\n')
            new_logs_index = self.find_new_logs(parsed_logs, previous_time)
            if new_logs_index:
                result = parsed_logs[new_logs_index+1:]
            else:
                result = parsed_logs

            # for lg in result:
            #     print(lg)
            # print(result[-1].split(' ')[0])  # last log timestamp

            return result
        except Exception as e:
            _LOGGER.error(f"[list_metrics]: {e}")
            return []


    @staticmethod
    def find_new_logs(parsed_logs, previous_time):
        for index,log in enumerate(parsed_logs):
            log_time = log.split(' ')[0]
            if re.match('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', log_time):
                if previous_time == log_time:
                    return index
        return False

    @staticmethod
    def get_time_interval(previous_time):
        if not previous_time:
            prev_month_time = datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
            previous_time = date_parser.parse(prev_month_time.isoformat())
        prev_time_seconds = previous_time.timestamp()
        parsed_curr_time = date_parser.parse(datetime.datetime.now().isoformat())
        curr_time_seconds = parsed_curr_time.timestamp()
        difference_result = curr_time_seconds - prev_time_seconds
        return difference_result

