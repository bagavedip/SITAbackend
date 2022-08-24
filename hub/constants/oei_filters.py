
filter_map = {
    "SLA": "sla_name",
    "Priority": "Priority",
    "Category": "category_id,service_category",
    "First_Response_Time": "first_response_time_id,total_cost",
    "Response_Time": "response_time_id,total_cost",
    "False_Positives": "false_positives_id,number_of_services",
    "Reopened": "reopened_id,total_cost",
    "Status": "RequestStatus",
    "value0": "is_overdue",
    "value1": "is_overdue",
    "value2": "is_overdue",
    "value3": "is_overdue",
    "Tickets": "Itsm_id"
}


class Map:
    @staticmethod
    def get_filter(name):
        return filter_map.get(name)
