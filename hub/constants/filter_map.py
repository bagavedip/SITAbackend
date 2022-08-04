
filter_map = {
    "Assets": "asset_id,asset_name",
    "Assets_Tyoe": "asset_type",
    "Entity": "entity_id,entity_name",
    "Location": "location_id,location_name",
    "Function": "function_id,function_name",
    "UseCase": "usecase_id,use_case",
    "Severity": "severity",
    "Criticality": "criticality"
}


class Map:
    @staticmethod
    def get_filter(name):
        return filter_map.get(name)
