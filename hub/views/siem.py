import logging

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from hub.serializers.siem import SIEMSerializer
from shared_stage.services.rules import RulesService
from shared_stage.services.usecase import UseCaseService
from hub.services.siem import SIEMService

logger = logging.getLogger(__name__)


class SIEMViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    
    serializer_class = SIEMSerializer

    def event_count_data(self, request):
        """
         function to count events
        """
        logger.info(f"request data is {request.data}")
        if request.query_params:
            start_date = request.query_params["start_datetime"]
            if start_date: 
                siem_data = SIEMService.get_queryset().filter(start_datetime=start_date)
                if siem_data:
                    total_events = 0
                    for events in siem_data:
                        total_events += events.event_count
                    data = {
                        "Total Events": total_events
                    }
                    return Response(
                        {
                            "Status": status.HTTP_200_OK,
                            "Data": data,
                        }
                    )
                else:
                    return Response(
                        {
                            "Status": status.HTTP_404_NOT_FOUND,
                            "Message": "No Dates matching"
                        }
                    )
            else:
                return Response(
                    {
                        "Status": status.HTTP_400_BAD_REQUEST,
                        "Message": "Send a valid Date-Time"
                    }
                )
        else:
            return Response(
                {
                    "Status": status.HTTP_400_BAD_REQUEST,
                    "Message": "Pass a parameter 'Start Datetime'"
                }
            )

    def event_count_by_usecases(self, request):
        """
         function to count events of every use_case
        """
        logger.info(f"request data is {request.data}")
        if request.query_params:
            usecase = request.query_params["usecase"]
            usecases = UseCaseService.get_queryset().filter(usecase=usecase)
            total_events = 0
            if usecases:
                for usecase in usecases:
                    id = usecase.id
                    rules = RulesService.get_queryset().filter(usecase=id)
                    if rules:
                        for rule in rules:
                            rule_name = rule.rule_name
                            siem_data = SIEMService.get_queryset().filter(rule_name=rule_name)
                            if siem_data:
                                for events in siem_data:
                                    total_events += events.event_count
                        data = {
                            "Total Events": total_events
                        }
                        return Response(
                            {
                                "status": status.HTTP_200_OK,
                                "Data": data
                            }
                        )
                    else:
                        return Response(
                            {
                                "status": status.HTTP_404_NOT_FOUND,
                                "Message": "Rules Not Found for this use_case",
                            }
                        )
            else:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "Message": "UseCase Not Matching",
                    }
                )
        else:
            return Response(
                {
                    "Status": status.HTTP_400_BAD_REQUEST,
                    "Message": "Pass a parameter 'UseCase'"
                }
            )

    def severity_by_offenses(self, request):
        """
         function to get severity by offences
        """
        logger.info(f"request data is {request.data}")
        if request.query_params:
            offense = request.query_params["offense_source"]
            siem_data = SIEMService.get_queryset().filter(offense_source=offense)
            if siem_data:
                for data in siem_data:
                    severity = data.severity
                    magnitude = data.magnitude
                    severity_mean = (severity + magnitude)/2
                    if severity_mean > 6:
                        label = "Critical"
                    elif severity_mean > 4:
                        label = "High"
                    else:
                        label = "Low"
                    data = {
                        "Severity Mean": severity_mean,
                        "Priority": label
                    }
                    return Response(
                        {
                            "Status": status.HTTP_200_OK,
                            "Data": data
                        }
                    )
            else:
                return Response(
                    {
                        "Status": status.HTTP_404_NOT_FOUND,
                        "Message": "Offense Not Matched"
                    }
                )
        else:
            return Response(
                {
                    "Status": status.HTTP_400_BAD_REQUEST,
                    "Message": "Pass a parameter 'Offense Source'"
                }
            )

    def severity_by_usecase(self, request):
        """
         function to get severity for each use_case
        """
        logger.info(f"request data is {request.data}")
        if request.query_params:
            usecase = request.query_params["usecase"]
            usecases = UseCaseService.get_queryset().filter(usecase=usecase)
            total_events_data = dict()
            total_events = 0
            total_high_events = 0
            total_medium_events = 0
            total_low_events = 0
            if usecases:
                for usecase in usecases:
                    id = usecase.id
                    rules = RulesService.get_queryset().filter(usecase=id)
                    if rules:
                        high = 0
                        medium = 0
                        low = 0
                        for rule in rules:
                            rule_name = rule.rule_name
                            siem_data = SIEMService.get_queryset().filter(rule_name=rule_name)
                            if siem_data:
                                for data in siem_data:
                                    total_events += data.event_count
                                    severity = data.severity
                                    magnitude = data.magnitude
                                    severity_mean = (severity + magnitude)/2
                                    if severity_mean > 6:
                                        total_events_data['High'] = total_events_data.get('High', 0) + 1
                                        high += 1
                                        total_events_data['total_high_events'] = (
                                                total_events_data.get('total_high_events', 0) + data.event_count)
                                        total_high_events += data.event_count
                                    elif severity_mean > 4:
                                        total_events_data['Medium'] = total_events_data.get('Medium', 0) + 1
                                        medium += 1
                                        total_events_data['total_medium_events'] = (
                                            total_events_data.get('total_medium_events', 0) + data.event_count)
                                        total_medium_events += data.event_count
                                    else:
                                        total_events_data['Low'] = total_events_data.get('Low', 0) + 1
                                        low += 1
                                        total_events_data['total_low_events'] = (
                                                total_events_data.get('total_low_events', 0) + data.event_count)
                                        total_low_events += data.event_count
                data = {
                    "Total Events": total_events,
                    "Low Offenses": low,
                    "Total Low Events": total_low_events,
                    "Medium": medium,
                    "Total Medium Events": total_medium_events,
                    "High": high,
                    "Total High Events": total_high_events,
                    "datas": total_events_data,
                }
                return Response(
                    {
                        "status": status.HTTP_200_OK,
                        "Data": data,
                        
                    }
                )
            else:
                return Response({
                    "Status": status.HTTP_404_NOT_FOUND,
                    "Message": "You don't have this Use_case"
                })
        else:
            return Response(
                {
                    "Status": status.HTTP_400_BAD_REQUEST,
                    "Message": "Pass a parameter 'Use-Case'"
                }
            )

    def usecase_details(self, request):
        """
         function to  get details of use_case
        """
        logger.info(f"request data is {request.data}")
        all_data = []
        usecases = UseCaseService.get_queryset()
        usecase_count = UseCaseService.get_queryset().count()
        total_events = 0
        if usecases:
            for usecase in usecases:
                total_offences = 0
                rules = RulesService.get_queryset().filter(usecase=usecase.id)
                if rules:
                    high = 0
                    medium = 0
                    low = 0
                    for rule in rules:
                        siem_data = SIEMService.get_queryset().filter(rule_name=rule.rule_name)
                        if siem_data:
                            for data in siem_data:
                                total_offences += 1
                                total_events += data.event_count
                                severity = data.severity
                                magnitude = data.magnitude
                                severity_mean = (severity + magnitude)/2
                                if severity_mean > 6:
                                    high += 1
                                elif severity_mean > 4:
                                    medium += 1
                                else:
                                    low += 1
                data = {

                    "Total Offence": total_offences,
                    "Total Events": total_events,
                    "Low Offenses": low,
                    "Medium": medium,
                    "High": high,
                }
                all_data.append(data)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "Data": all_data,
                    
                }
            )
        else:
            return Response(
                {
                    "Status": status.HTTP_400_BAD_REQUEST,
                    "Message": "Pass a parameter 'Offense Source'"
                }
            )

    def severity(self, request):
        """
         function to get severity details
        """
        logger.info(f"request data is {request.data}")
        siem_data = SIEMService.get_queryset()
        count = 0
        low = 0
        high = 0
        critical = 0
        if siem_data:
            for data in siem_data:
                count += 1
                severity = data.severity
                magnitude = data.magnitude
                severity_mean = (severity + magnitude)/2
                if severity_mean > 6:
                    critical += 1
                elif severity_mean > 4:
                    high += 1
                else:
                    low += 1
            data = {
                "Total Offences": count,
                "Low": low,
                "High": high,
                "Critical": critical,
            }
            return Response(
                {
                    "Status": status.HTTP_200_OK,
                    "Data": data
                }
            )
        else:
            return Response(
                {
                    "Status": status.HTTP_404_NOT_FOUND,
                    "Message": "You Don't have any data",
                }
            )

    def avg_res_time(self, request):
        """
         function to get average response time
        """
        logger.info(f"request data is {request.data}")
        siem_data = SIEMService.get_queryset()
        count = 0
        all_works_done = 0
        if siem_data:
            for siem in siem_data:
                count += 1
                work_done = (siem.close_time - siem.start_datetime).days
                all_works_done += work_done
            avg_res = all_works_done / count
            data = {
                "Average Response Time": avg_res
            }
            return Response(
                {
                    "Status": status.HTTP_200_OK,
                    "Data": data
                }
            )
        else:
            return Response(
                {
                    "Status": status.HTTP_404_NOT_FOUND,
                    "Message": "No SIEM data found"
                }
            )

    def seim_all_data(self, request):
        """
         function to get all siem records
        """
        logger.info(f"request data is {request.data}")
        siem_data = SIEMService.get_queryset()
        if siem_data:
            serializer = SIEMSerializer(siem_data, many=True)
            return Response(
                {
                    "Status": status.HTTP_200_OK,
                    "Data": serializer.data
                }
            )
        else:
            return Response(
                {
                    "Status": status.HTTP_404_NOT_FOUND,
                    "Message": "You don't have Data",
                }
            )

    def offence_by_usecases(self, request):
        """
         function to get details of offence by use_case
        """
        logger.info(f"request data is {request.data}")
        usecases = UseCaseService.get_queryset()
        all_usecase = []
        for usecase in usecases.values():
            all_usecase.append(usecase.get("id"))
        offences = 0
        for data in all_usecase:
            rules = RulesService.get_queryset().filter(usecase=data)
            if rules:
                for rule in rules:
                    rule_name = rule.rule_name
                    siem_data = SIEMService.get_queryset().filter(rule_name=rule_name).count()
                    if siem_data:
                        offences += siem_data
        data = {
            "Total Offences": siem_data
        }
        return Response(
            {
                "status": status.HTTP_200_OK,
                "Data": data
            }
        )
