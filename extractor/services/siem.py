from datetime import datetime
import os
import requests
import time
import sys

from urllib.parse import urljoin

from extractor.models import SIEM

# Remove warnings messages
requests.packages.urllib3.disable_warnings()

# Constants
GET_DOMAIN_INFO = '/api/config/domain_management/domains'
GET_OFFENSES = '/api/siem/offenses'
GET_RULE = '/api/analytics/rules/{rule_id}'
DATE_FORMAT = '%d/%m/%Y'
FILE_PATH = '{root}\offenses.json'


class SiemService:
    def __init__(self, base_url, api_key):
        self.url = base_url
        self.api_key = api_key
        self.session = requests.session()
        self.session.verify = False
        self.session.headers = {'SEC': api_key}
        self.file_path = FILE_PATH.format(root=os.path.dirname(os.path.abspath(__file__)))
        start_time = datetime.now()

    def get_offenses(self, start_time, filter=None):
        start_time_timestamp = int(time.mktime(start_time.timetuple()) * 1000)
        params = {'filter': 'start_time >= {start_time} {filter}'.format(start_time=start_time_timestamp, filter='' if filter is None else filter)}
        response = self.session.get(urljoin(self.url, GET_OFFENSES), params=params)
        return response.json()

    def get_domain_info(self, name):
        params = {'filter': 'name ilike \'%{}%\''.format(name)}
        response = self.session.get(urljoin(self.url, GET_DOMAIN_INFO), params=params)
        if len(response.json()) > 1:
            return False
        else:
            return response.json()[0].get('id')

    def get_rule_by_id(self, rule_id):
        url = urljoin(self.url, GET_RULE.format(rule_id=rule_id))
        self.session.headers['Range'] = None
        response = self.session.get(url)
        return {'rule_name': response.json().get('name')}

    def qradar(self):
        if len(sys.argv) < 4:
            raise Exception('Uso del script: qradar.py <URL> <API Key> <Fecha> [Cliente]')
        # print('argumentos = {}'.format(sys.argv))
        qradar = SiemService(base_url=sys.argv[1], api_key=sys.argv[2])
        start_time = datetime.strptime(sys.argv[3], DATE_FORMAT)
        name = None if len(sys.argv) < 5 else sys.argv[4]
        domain_id = qradar.get_domain_info(name) if name is not None else None
        offenses = qradar.get_offenses(start_time=start_time,
                                       filter=None if domain_id is None else ' and domain_id = {}'.format(domain_id))
        final_offenses = []
        final_siem = []
        for offense in offenses:
            rules = []
            for rule in offense.get('rules'):
                rules.append(qradar.get_rule_by_id(rule.get('id')))
            offense['rule_details'] = rules
            final_offenses.append(offense)
            siem = {
                "last_persisted_time": offense.get("last_persisted_time", None),
                "username_count": offense.get("username_count", None),
                "description": offense.get('description', None),
                "rules": rules,
                "event_count": offense.get('event_count', None),
                "flow_count": offense.get('flow_count', None),
                "assigned_to": offense.get('assigned_to', None),
                "security_category_count": offense.get('security_category_count', None),
                "follow_up": offense.get('follow_up', None),
                "source_address_ids": offense.get('[local_destination_address_ids]', None),
                "source_count": offense.get('source_count', None),
                "inactive": offense.get('inactive', None),
                "protected": offense.get('protected', None),
                "closing_user": offense.get('closing_user', None),
                "destination_networks": offense.get('[destination_networks]', None),
                "source_network": offense.get('source_network', None),
                "category_count": offense.get('category_count', None),
                "close_time": offense.get('close_time', None),
                "remote_destination_count": offense.get('remote_destination_count', None),
                "start_time": offense.get('start_time', None),
                "magnitude": offense.get('magnitude', None),
                "last_updated_time": offense.get('last_updated_time', None),
                "credibility": offense.get('credibility', None),
                "id": offense.get('id', None),
                "categories": offense.get('', None),
                "severity": offense.get('severity', None),
                "policy_category_count": offense.get('policy_category_count', None),
                "log_sources": offense.get('', None),
                "closing_reason_id": offense.get('closing_reason_id', None),
                "device_count": offense.get('device_count', None),
                "first_persisted_time": offense.get('first_persisted_time', None),
                "offense_type": offense.get('offense_type', None),
                "relevance": offense.get('relevance', None),
                "domain_id": offense.get('domain_id', None),
                "offense_source": offense.get('offense_source', None),
                "local_destination_address_ids": offense.get('[local_destination_address_ids]', None),
                "local_destination_count": offense.get('local_destination_count', None),
                "status": offense.get('status', None),
                "rule_details": offense.get('rule_details', None)
            }
            final_siem.append(siem)
        a = SIEM.objects.all(**siem)
        return a


# if __name__ == '__main__':
#     Qradar1 = QradarService(base_url='https://192.168.200.206', api_key='f52645f4-0dcf-400f-bb6c-56c9e20f87c6')
#     Qradar1.qradar()
