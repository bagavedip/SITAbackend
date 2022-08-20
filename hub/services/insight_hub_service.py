from datetime import datetime

from numpy.ma import count

from hub.constants.filter_map import Map
from hub.models.hub import Hub
from django.db.models import Count, Sum

from hub.serializers.hub import InsightsSerializer


class HubService:

    @staticmethod
    def get_queryset():
        queryset = Hub.objects.all()
        return queryset

    @staticmethod
    def get_insights(reesponse_obj: InsightsSerializer):
        query_data = Hub.objects.filter(starttime__gte=reesponse_obj.start_date, endtime__lte=reesponse_obj.end_date).values(*reesponse_obj.model_group_map).order_by().annotate(events=Sum('events'))
        reesponse_obj.set_requst_queryset(query_data)
        incidents = Hub.objects.filter(starttime__gte=reesponse_obj.start_date, endtime__lte=reesponse_obj.end_date).values('criticality').order_by().annotate(events=Sum('events'))
        for row in incidents:
            reesponse_obj.donut_center[row.get('criticality')] = row.get('events')
        return query_data
    
    @staticmethod
    def get_legends(reesponse_obj: InsightsSerializer):
        query_data = Hub.objects.filter(starttime__gte=reesponse_obj.start_date, endtime__lte=reesponse_obj.end_date).values(reesponse_obj.legend_filter).distinct(reesponse_obj.legend_filter)
        legends = []
        for row in query_data:
            legends.append(row.get(reesponse_obj.legend_filter))
        return legends

    @staticmethod
    def asset_details(incident):
        data = HubService.get_queryset().filter(soar_id=incident)
        asset = []
        desktop = 0
        laptop = 0
        mobile = 0
        entityes = 0
        assets = data.count()
        for type in data:
            asset_type = type.asset_type
            entity = type.entity_name
            if entity:
                entityes = entityes + 1
            if asset_type == "Desktop":
                desktop = desktop + 1
            if asset_type == "Laptop":
                laptop = laptop + 1
            if asset_type == "Mobile":
                mobile = mobile + 1
        asset_types = "MOBILE" + "~" + str(mobile) + "*" + "DESKTOP" + "~" + str(desktop) + "*" + "LAPTOP" + "~" + str(laptop)
        entity_count = entityes
        for query in data:
            incident_status = {"text": query.status, "color": "#ffc107"}
            time_to_close = (query.assigned_time - query.starttime)
            time = int(abs(time_to_close).total_seconds()/3600)
            time_to_close = {"cardTitle": str(time) + " Hrs", "textColor": "#ffc107", "cardSubTitle": "Time to close",
                             "cardIcon": "OrangeWait"}
            suspicious = {"cardTitle": query.Suspicious, "textColor": "#ffc107", "cardSubTitle": "Risk profile impact",
                          "cardIcon": "OrangeChartLineUp"}
            if query.priority == "High":
                priority = "RED"
                color = "#ff0000"
                card_icon = "RedCaution"
            elif query.priority == "Low":
                priority = "Green"
                color = "#00FF00"
                card_icon = "LimeCaution"
            else:
                priority = "yellow"
                color = "#FFFF00"
                card_icon = "yellowCaution"
            tread_level = {"cardTitle": priority, "textColor": color, "cardSubTitle": "Threat Level",
                           "cardIcon": card_icon}
            card = [tread_level, time_to_close, suspicious]
            incident_details = {"title": "INCIDENT DETAILS",
                                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
                                               " Id odiosed tempor netus purus nec pharetra amet iaculis. Sit eros, "
                                               "semper adipiscing risus lacus, in non. Id odio sed tempor netus "
                                               "purusSiteros, semper adipiscing risus lacus, in non. Id odio sed View "
                                               "More"}
            resolution_status = {
                "title": "RESOLUTION STATUS",
                "resolutionDetails": {
                    "title": "Resolution Details",
                    "description": query.resolution,
                    "isEditable": "true"
                },
                "resolution_owner": {

                    "title": "Resolution Owner",
                    "description": query.group,
                    "isEditable": "true"
                }
            }
            details = [{
                "subTitle": "Assets Affected",
                "value": assets,
                "valueColor": "#333333"
            },
                {
                    "subTitle": "Assets Type",
                    "value": asset_types,
                    "valueColor": "#333333"
                },
                {
                    "subTitle": "Geographies",
                    "value": query.location_name,
                    "valueColor": "#03AAC9"
                },
                {
                    "subTitle": "Org's",
                    "value": entity_count,
                    "valueColor": "03AAC9"
                },
                {
                    "subTitle": "Breach's cost",
                    "value": "480",
                    "valueColor": "#333333"
                }
            ]
            other_details = {"title": "OTHER DETAILS",
                             "details": details}
            updates = {
                "title": "UPDATES",
                "data": [
                    {
                        "updateDateTime": "YYYY-MM-DDTHH:mm:ss",
                        "description": query.replys
                    }
                        ]
                     }
            data_dict = {
                "incidentStatus": incident_status,
                "cards": card,
                "incidentDetails": incident_details,
                "resolutionStatus": resolution_status,
                "otherDetails": other_details,
                "update": updates
            }
            asset.append(data_dict)
        return asset
