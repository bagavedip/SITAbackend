import logging
from datetime import timedelta

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
        query_data = ITSM.objects.filter(CreatedTime__gte=response_obj.start_date, Ending_time__lte=response_obj.end_date).values(*response_obj.model_group_map).order_by().annotate(events=Count('Itsm_id'))
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
        assets = str(data.count())
        for query in data:
            request_status = {"text": query.Subject + " " + query.SIEM_id, "color": "#ffc107"}
            time_to_close = (query.assigned_time - query.CreatedTime)
            time = int(abs(time_to_close).total_seconds() / 3600)
            time_to_close = {"cardTitle": str(time) + " Hrs", "textColor": "#ffc107", "cardSubTitle": "Time to close",
                             "cardIcon": "OrangeWait"}
            a = query.CreatedTime
            b = query.sla_completion_time
            c = a + timedelta(days=int(b))
            expected_closure = (c - query.CreatedTime)
            time = int(abs(expected_closure).total_seconds() / 3600)
            expected_closure = {"cardTitle": str(time) + " Hrs", "textColor": "#ffc107",
                                "cardSubTitle": "Time to close", "cardIcon": "BlueChartLineUp"}
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
                "resolutionOwner": {

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
                "updates": updates
            }
        return data_dict
