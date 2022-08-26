from hub.constants.filter_map import Map


class HubTimeline:
    def __init__(self, request) -> None:
        self.request_filters = []
        self.model_group_map = []
        self.queryset = None
        self.datasets = []
        self.hier_data = {}
        self.legend_filter = ""
        filter_data = request.data
        self.start_date = filter_data.get('fromDate')
        self.end_date = filter_data.get('toDate')
        self.request_filters.append((filter_data.get('filterOptions').get('headerOption')))
        print(request.data)
        index = 1
        print(self.request_filters, "self")
        for filter in self.request_filters:
            self.model_group_map = self.model_group_map + Map.get_filter(filter).split(',')
            # ds = Dataset().init_response_dataset()
            # ds['id'] = index
            # ds['label'] = filter
            # self.datasets.append(ds)
            # index += 1