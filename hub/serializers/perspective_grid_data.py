from hub.constants import perspective


class PerspectiveSerializer:
    """
     Serializer for Perspective Grid data for Insights(Hub)
    """

    def __init__(self, request) -> None:

        self.request_filter = []
        filter_data = request.data
        self.header_filters = []
        self.start_date = filter_data.get('fromDate')
        self.end_date = filter_data.get('toDate')
        self.filters = dict()
        self.filters['starttime__gte'] = self.start_date
        self.filters['endtime__lte'] = self.end_date
        # self.request_filter.get("dropdownFilters").get("id")
        filters = filter_data.get("dropdownFilters").get("value")
        for filters in filters:
            self.header_filters.append(filters)

        self.columns_headers = []
        self.select_cols = []
        for key in perspective.PERSPECTIVE_TABLE_HEADER.keys():
            self.select_cols.append(perspective.PERSPECTIVE_TABLE_HEADER.get(key))
            self.columns_headers.append(key)

    def get_response(self, data):
        col_headers = []
        for index in range(len(self.columns_headers)):
            col = {
                "key": "column" + str(index + 1),
                "headerText": self.columns_headers[index],
                "isSorting": True,
                "type": "TEXT",
                "hideOnUI": False,
                "dataDisplayLength": 0
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
                "dropdownFiters": []
            },
            "gridAddOn": {
                "showFirstColumnAsCheckbox": False,
                "showLastColumnAsAction": True
            },
            "gridHeader": col_headers,
            "gridData": grid_data

        }
        return response_json
