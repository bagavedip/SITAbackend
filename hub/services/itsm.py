import calendar
import logging
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo

from dateutil import relativedelta
from django.db.models import Count, Q
from hub.models.itsm_data import ITSM
from hub.serializers.oei_timeline import OeiTimeline
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

    @staticmethod
    def get_response_time(fromdate, todate):
        """Function to return response time data"""
        try:
            response_time = todate - fromdate
            return response_time
        except:
            return "-"

    @staticmethod
    def update(name, **kwargs):
        """
        Function update an asset from kwargs
        """
        for key, value in kwargs.items():
            setattr(name, key, value)
        name.save()

        return name

    @staticmethod
    def oei_sla_comment(selectedIncidents, comment):
        queryset = ITSM.objects.filter(SIEM_id=selectedIncidents)
        comments = {
            "comments": comment
        }
        for query in queryset:
            sla_comment = ITSMService.update(query, **comments)
        return sla_comment

    @staticmethod
    def oei_sla_timeline(response: OeiTimeline):
        for filter_data in response.request_filters:
            request_filter = filter_data
        for filter_data in response.header_filters:
            header_filter = filter_data
        filters = (request_filter + "-" + header_filter)
        start_time = datetime.strptime(response.start_date, '%Y-%m-%d').astimezone(ZoneInfo('America/New_York'))
        end_time = datetime.strptime(response.end_date, '%Y-%m-%d').astimezone(
            ZoneInfo('America/New_York'))
        total_days = int((end_time - start_time).days)
        delta = relativedelta.relativedelta(end_time, start_time)
        start_date = start_time
        time = []
        within_tickets=[]
        outside_tickets=[]
        data = {}
        dataset =[]
        returndata={}
        if total_days <= 31:
            title1 = "Day"+str(start_date.day)
            title2 = "Day"+str(end_time.day)
            for x in range(1, delta.days+1):
                within_query = ITSM.objects.filter(CreatedTime__gte=start_date,CreatedTime__lte=start_date + timedelta(days=1), service_category= "within sla").count()
                within_tickets.append(within_query)
                outside_query = ITSM.objects.filter(CreatedTime__gte=start_date,CreatedTime__lte=start_date + timedelta(days=1), service_category= "outside sla").count()
                outside_tickets.append(outside_query)

                time.append("day"+str(start_date.day))
                start_date = start_date + timedelta(days=1)
        if total_days <= 365 and total_days > 31:
            if (delta.days):
                delta.months +=1
            title1 = calendar.month_name[start_date.month]+str(start_date.year)
            title2 = calendar.month_name[end_time.month]+str(end_time.year)
            for x in range(0, delta.months):
                within_query = ITSM.objects.filter(CreatedTime__gte=start_date,CreatedTime__lte=(start_date+relativedelta.relativedelta(months=1)), service_category= "within sla").count()
                within_tickets.append(within_query)
                outside_query = ITSM.objects.filter(CreatedTime__gte=start_date,CreatedTime__lte=(start_date+relativedelta.relativedelta(months=1)), service_category= "outside sla").count()
                outside_tickets.append(outside_query)
                time.append(calendar.month_name[start_date.month])
                start_date = start_date + relativedelta.relativedelta(months=1)
        if total_days >365:
            if delta.months:
                delta.years += 1
            if delta.days:
                delta.years += 1
            title1 = start_date.year
            title2= end_time.year
            for x in range(1, delta.years+1):
                within_query = ITSM.objects.filter(CreatedTime__gte=start_date,CreatedTime__lte=(start_date + relativedelta.relativedelta(years=1)), service_category= "within sla").count()
                within_tickets.append(within_query)
                outside_query = ITSM.objects.filter(CreatedTime__gte=start_date,CreatedTime__lte=(start_date + relativedelta.relativedelta(years=1)), service_category= "outside sla").count()
                outside_tickets.append(outside_query)
                time.append(start_date.year)
                start_date = start_date + relativedelta.relativedelta(years=1)
        title = title1+"-"+title2
        newdata = {
            "label":"within sla",
            "data":within_tickets,
            "backgroundColor": "#16293A"
        },{
            "label":"outside sla",
            "data":outside_tickets,
            "backgroundColor": "#437DB1"

        }
        dataset.append(newdata)
        data = {
            "labels":time,
            "datasets":dataset
        }
        returndata = {
            "barChartHeading":{
                "title":filters,
                "subTitle":title
            },
            "chartOptions": {
                "stacked": "false",
                "stepSize": 250,
                "showLendend":"false",
                "legendPosition": "bottom",
                "categoryPercentage": 0.7,
                "scaleLabelofYaxis": {
                    "display": "true",
                    "labelString": "Incidents",
                    "fontStyle": "bold",
                    "fontSize": 14
                },
                "scaleLabelofXaxis": {
                    "display": "true",
                    "labelString": "Time",
                    "fontStyle": "bold",
                    "fontSize": 14
                }
            },
            "data" : data
        }
        return returndata


    @staticmethod
    def oei_ticket_timeline(response: OeiTimeline):
        for filter_data in response.request_filters:
            request_filter = filter_data
        for filter_data in response.header_filters:
            header_filter = filter_data
        filters = (request_filter + "-" + header_filter)
        start_time = datetime.strptime(response.start_date, '%Y-%m-%d').astimezone(ZoneInfo('America/New_York'))
        end_time = datetime.strptime(response.end_date, '%Y-%m-%d').astimezone(
            ZoneInfo('America/New_York'))
        total_days = int((end_time - start_time).days)
        delta = relativedelta.relativedelta(end_time, start_time)
        start_date = start_time
        tickets = []
        time = []
        data = {}
        dataset =[]
        returndata={}
        if total_days <= 31:
            title1 = "Day"+str(start_date.day)
            title2 = "Day"+str(end_time.day)
            for x in range(1, delta.days+1):
                query = ITSM.objects.filter(CreatedTime__gte=start_date,CreatedTime__lte=start_date + timedelta(days=1)).count()
                tickets.append(query)
                time.append("day"+str(start_date.day))
                start_date = start_date + timedelta(days=1)
        if total_days <= 365 and total_days > 31:
            if (delta.days):
                delta.months +=1
            title1 = calendar.month_name[start_date.month]+str(start_date.year)
            title2 = calendar.month_name[end_time.month]+str(end_time.year)
            for x in range(0, delta.months):
                query = ITSM.objects.filter(CreatedTime__gte=start_date,CreatedTime__lte=(start_date+relativedelta.relativedelta(months=1))).count()
                tickets.append(query)
                time.append(calendar.month_name[start_date.month])
                start_date = start_date + relativedelta.relativedelta(months=1)
        if total_days >365:
            if delta.months:
                delta.years += 1
            if delta.days:
                delta.years += 1
            title1 = start_date.year
            title2= end_time.year
            for x in range(1, delta.years+1):
                query = ITSM.objects.filter(CreatedTime__gte=start_date, CreatedTime__lte=start_date + relativedelta.relativedelta(years=1)).count()
                time.append(start_date.year)
                tickets.append(query)
                start_date = start_date + relativedelta.relativedelta(years=1)
        title = title1+"-"+title2
        newdata = {
            "data":tickets,
            "backgroundColor": "#16293A"
        }
        dataset.append(newdata)
        data = {
            "labels":time,
            "datasets":dataset
        }
        returndata = {
            "barChartHeading":{
                "title":filters,
                "subTitle":title
            },
            "chartOptions": {
                "stacked": "false",
                "stepSize": 250,
                "showLendend":"false",
                "legendPosition": "bottom",
                "categoryPercentage": 0.7,
                "scaleLabelofYaxis": {
                    "display": "true",
                    "labelString": "Incidents",
                    "fontStyle": "bold",
                    "fontSize": 14
                },
                "scaleLabelofXaxis": {
                    "display": "true",
                    "labelString": "Time",
                    "fontStyle": "bold",
                    "fontSize": 14
                }
            },
            "data" : data
        }
        return returndata

