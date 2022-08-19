from hub.constants import oei_constants


class TicketDetailsSerializer:

    def __init__(self, request) -> None:

        request_data = request.data

        print('Request Data is', request_data)
        self.start_date = request_data.get('fromDate')
        self.end_date = request_data.get('toDate')
        region = request_data.get('region')
        self.filters = {}
        self.filters['CreatedTime__gte'] = self.start_date
        self.filters['Ending_time__lte'] = self.end_date
        filter_arr = region.split("*")
        for filter_str in filter_arr:
            filter = filter_str.split("*")[0].split("~")[0]
            filter_key_val = filter.split("=")
            self.filters[filter_key_val[0]] = filter_key_val[1].split('-')[0]

        self.columns_headers = []
        self.select_cols = []
        for key in oei_constants.INSIGHT_TABLE_HEADER.keys():
            self.select_cols.append(oei_constants.INSIGHT_TABLE_HEADER.get(key))
            self.columns_headers.append(key)

    def get_response(self, data):
        col_headers = []
        for index in range(len(self.columns_headers)):
            col = {
                "key": "column" + str(index + 1),
                "headerText": self.columns_headers[index],
                "isSorting": True,
                "type": "TEXT"
            }
            col_headers.append(col)

        grid_data = []
        for row in data:
            row_data = {}
            for index in range(len(row)):
                row_data["column" + (str(index + 1))] = str(row.get(self.select_cols[index]))
            grid_data.append(row_data)

        response_json = {
            "gridSelectedFilter": {
                "startDate": self.start_date,
                "endDate": self.end_date,
                "selectedDropdownFiters": []
            },
            "gridAddOn": {
                "showFirstColumnAsCheckbox": True,
                "showLastColumnAsAction": True
            },
            "gridHeader": col_headers,
            "gridData": grid_data

        }
        return response_json
