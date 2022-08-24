
filter_map = {
    "SLA": "sla_name",
    "Priority": "Priority",
    "Category": "category_id,service_category",
    "First_Response_Time": "first_response_time_id,Total_cost",
    "Response_Time": "response_time_id,Total_cost",
    "False_Positives": "false_positives_id,Number_of_Services",
    "Reopened": "reopened_id,Total_cost",
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
