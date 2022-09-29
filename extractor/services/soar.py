import json
import requests
from datetime import datetime,   timedelta
from extractor.models import SOAR


class SoarService:
    @staticmethod
    def get_all_cases():
        now = datetime.now()
        start_time = int((now - timedelta(days=1)).timestamp() * 1000)
        endtime = int(now.timestamp() * 1000)
        url = "https://192.168.200.98/api/external/v1/cases/GetCaseCardsByRequest"
        payload = {
            "pageSize": 20,
            "pageNumber": 1,
            "liveQueueSettings": {
                    "startTimeUnixTimeInMs": start_time,
                    "endTimeUnixTimeInMs": endtime
                }
            }
        headers = {
            'AppKey': 'a936681c-db8c-49b5-be95-e56e943f6426',
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post(url,  headers=headers, data=str(payload),  verify=False)
        output = json.loads(response.text)
        numbers = []
        a = []
        for data in output['caseCards']:
            keys = data.get('id')
            numbers.append(keys)
            for n in numbers:
                headers = {'AppKey': 'a936681c-db8c-49b5-be95-e56e943f6426'}
                url = "https://192.168.200.98/api/external/v1/cases/GetCaseFullDetails/" + str(n)
                payload = {}
                response = requests.request("GET", url, headers=headers, data=payload, verify=False)
                output = json.loads(response.text)
                priority = output.get('alerts')[0].get('additionalProperties').get('priority')
                environment = output.get('alerts')[0].get('additionalProperties').get('environment')
                last_updated_time = output.get('alerts')[0].get('additionalProperties').get('last_updated_time')
                products = output.get('alerts')[0].get('additionalProperties').get('deviceProduct')
                for source in output.get('alerts')[0].get('securityEventCards'):
                    sources = source.get('sources')
                    port = source.get('port')
                    outcome = source.get('outcome')
                    time = source.get('time')
                soar = {
                    "SOAR_ID": output.get('id', None),
                    "AssignedUser": output.get('assignedUserName', None),
                    "Title": output.get('title', None),
                    "Time": time,
                    "Tags": output.get('tags', None),
                    "Products": products,
                    "Incident": output.get('isIncident', None),
                    "Suspicious": output.get('hasSuspiciousEntity', None),
                    "Important": output.get('isImportant', None),
                    "Ports": port,
                    "Outcomes": outcome,
                    "Status": output.get('status', None),
                    "Environment": environment,
                    "Priority": priority,
                    "Stage": output.get('stage', None),
                    "TicketIDs": output.get("alerts", None)[0].get('ticketId'),
                    'ClosingTime': last_updated_time,
                    "Sources": sources,
                    "Reason": output.get("", None),
                    "RootCause": output.get("", None),
                    "Case_id": output.get('id', None),
                    "AlertsCount": output.get("", None),
                }
            values = SOAR.objects.create(**soar)
            a.append(soar)
        return a
