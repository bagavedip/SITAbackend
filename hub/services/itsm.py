import logging
from django.db.models import Count, Q
from hub.models.itsm_data import ITSM
from hub.serializers.oei_serializers import OeiSerializer
from hub.serializers.oei_ticket_details import TicketDetailsSerializer

logger = logging.getLogger(__name__)


class ITSMService:
    
    @staticmethod
    def get_queryset():
        """Function to return all ITSM data"""
        return ITSM.objects.all()

    @staticmethod
    def itsm_filter(asset):

        filtered_data = ITSMService.get_queryset().filter(Asset_Name=asset)
        return filtered_data

    @staticmethod
    def get_oei(response_obj: OeiSerializer):
        query_data = ITSM.objects.filter(CreatedTime__lte=response_obj.start_date, Ending_time__lte=response_obj.end_date).values(*response_obj.model_group_map).order_by().annotate(events=Count('Itsm_id'))
        response_obj.set_request_queryset(query_data)
        return query_data

    @staticmethod
    def get_tickets(response_obj: TicketDetailsSerializer):
        filter_q = Q(**response_obj.filters)
        query_data = ITSM.objects.filter(filter_q).values(*response_obj.select_cols)
        return query_data

    @staticmethod
    def asset_details(ticket):
        data = ITSMService.get_queryset().filter(SIEM_id=ticket)
        asset = []
        assets = data.count()
        for query in data:
            request_status = {"text": query.Subject + " " + query.SIEM_id, "color": "#ffc107"}
            time_to_close = (query.Ending_time - query.CreatedTime)
            time = int(abs(time_to_close).total_seconds() / 3600)
            time_to_close = {"cardTitle": str(time) + " Hrs", "textColor": "#ffc107", "cardSubTitle": "Time to close",
                             "cardIcon": "OrangeWait"}
            expected_closure = (query.CreatedTime - query.SLA_Spare_Parts_Stock_Delivery_Time)
            time = int(abs(expected_closure).total_seconds() / 3600)
            print(time, "time")
            expected_closure = {"cardTitle": str(time) + " Hrs", "textColor": "#ffc107",
                                "cardSubTitle": "Time to close", "cardIcon": "OrangeWait"}
            if query.Priority == "High":
                priority = "RED"
                color = "#ff0000"
                card_icon = "RedCaution"
            elif query.Priority == "Low":
                priority = "Green"
                color = "#00FF00"
                card_icon = "LimeCaution"
            else:
                priority = "yellow"
                color = "#FFFF00"
                card_icon = "yellowCaution"
            tread_level = {"cardTitle": priority, "textColor": color, "cardSubTitle": "Threat Level",
                           "cardIcon": card_icon}
            card = [tread_level, time_to_close, expected_closure]
            incident_details = {"title": "INCIDENT DETAILS",
                                "description": query.Description}
            resolution_status = {
                "title": "RESOLUTION STATUS",
                "resolutionDetails": {
                    "title": "Resolution Details",
                    "description": query.Resolution,
                    "isEditable": "true"
                },
                "resolution_owner": {

                    "title": "Resolution Owner",
                    "description": query.submitted_by,
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
                    "value": query.Asset_Name,
                    "valueColor": "#333333"
                },
                {
                    "subTitle": "Geographies",
                    "value": query.location_name,
                    "valueColor": "#03AAC9"
                },
                {
                    "subTitle": "Org's",
                    "value":  query.Region,
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
                        "description": query.reply
                    }
                ]
            }
            data_dict = {
                "incidentStatus": request_status,
                "cards": card,
                "incidentDetails": incident_details,
                "resolutionStatus": resolution_status,
                "otherDetails": other_details,
                "update": updates
            }
            asset.append(data_dict)
        return asset
