
filter_map = {
    "SLA": "sla_name",
    "Priority": "Priority",
    "Category": "service_category",
    "First_Response_Time": "Response_due_time",
    "Response_Time": "Response_due_time",
    "False_Positives": "Itsm_id",
    "Tickets": "Subject",
    "Reopened": "Reopened",
    "status": "RequestStatus",
    "value0": "is_overdue"
}


class Map:
    @staticmethod
    def get_filter(name):
        return filter_map.get(name)
