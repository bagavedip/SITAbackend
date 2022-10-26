from hub.constants import dashboard_constants

from hub.models import SecurityPulse


class DashboardGridGridSerializer:
    """
     Serializer for Ticket Details for Insights(Hub)
    """

    def __init__(self, request) -> None:

        request_data = request.data

        self.columns_headers = []
        self.select_cols = []
        for key in dashboard_constants.SECURITY_PULSE_TABLE_HEADER.keys():
            self.select_cols.append(dashboard_constants.SECURITY_PULSE_TABLE_HEADER.get(key))
            self.columns_headers.append(key)

    def get_response(self, data):
        col_headers = []
        for index in range(len(self.columns_headers)):
            col = {
                "key": "column" + str(index + 1),
                "title": self.columns_headers[index],
                "isExternal": True,
                "type": "TEXT"
            }
            col_headers.append(col)

        grid_data = []
        for row in data:
            row_data = {}
            external = []
            internal = []
            for index in range(len(row)):
                link = row.get("links")
                links = link[0].get("linkUrl")
                row_data["column" + (str(index + 1))] = str(row.get(self.select_cols[index]))
                external.append(links)
            grid_data.append(row_data)

        response_json = {
            "gridAddOn": {
                "showFirstColumnAsCheckbox": True,
                "showLastColumnAsAction": True
            },
            "gridHeader": col_headers,
            "gridData": grid_data

        }
        return response_json