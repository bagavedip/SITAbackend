from hub.constants.filter_map import Map


class HubTimeline:
    def __init__(self, request) -> None:
        self.request_filters = []
        self.header_filters = []
        self.model_group_map = []
        self.queryset = None
        self.datasets = []
        self.hier_data = {}
        self.legend_filter = ""
        filter_data = request.data
        self.start_date = filter_data.get('fromDate')
        self.end_date = filter_data.get('toDate')
        self.request_filters.append((filter_data.get('filterOptions').get('headerOption')))
        index = 1
        filters = filter_data.get('filterOptions').get('headerFilters')
        for filter in filters:
            self.header_filters.append(filter)
        for filter in self.request_filters:
            self.model_group_map = self.model_group_map + Map.get_filter(filter).split(',')
           
