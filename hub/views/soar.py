from rest_framework import viewsets
from rest_framework.response import Response
from hub.serializers.soar import SOARSerializer
from hub.services.siem import SIEMService
from hub.services.soar import SOARService
from shared_stage.services.rules import RulesService
from shared_stage.services.usecase import UseCaseService


class SOARViewSet(viewsets.ModelViewSet):

    serializer_class = SOARSerializer

    def incident(self, request, *args, **kwargs):
        count = 0
        unresolved = 0
        resolved = 0
        client_to_respond = 0
        soar_data = SOARService.get_queryset()
        if soar_data:
            for data in soar_data:
                count += 1
                if data.Incident ==True :
                    resolved += 1
                elif data.Incident == False:
                    unresolved += 1
                else:
                    client_to_respond += 1
            data = {
                "Total Incident": count,
                "Resolved": resolved,
                "Unresolved": unresolved,
                "Client To Respond": client_to_respond,
            }
            return Response(
                {
                    "Status":"Success",
                    "Data": data
                }
            )
        else:
            return Response(
                {
                    "Status":"Failed",
                    "Message":"SOAR Data Not Available"
                }
            )

    def usecase_incident(self, request, *args, **kwargs):
        if request.query_params:
            usecase = request.query_params["usecase"]
            usecases = UseCaseService.get_queryset().filter(usecase = usecase)
            if usecases:
                for usecase in usecases:
                    id = usecase.id
                    rules = RulesService.get_queryset().filter(usecase = id)
                    count  = 0
                    unresolved = 0
                    resolved = 0
                    client_to_respond = 0
                    if rules:
                        for rule in rules:
                            rule_name = rule.rule_name
                            siem_data = SIEMService.get_queryset().filter(rule_name = rule_name)
                            if siem_data:
                                for events in siem_data:
                                    seim_id = events.seim_id
                                    soar_data = SOARService.get_queryset().filter(TicketIDs = seim_id)
                                    if soar_data:
                                        for data in soar_data:
                                            count += 1
                                            if data.Incident == True :
                                                resolved += 1
                                            elif data.Incident == False:
                                                unresolved += 1
                                            else:
                                                client_to_respond += 1
                                        data = {
                                            "Total Incident" : count,
                                            "Resolved" : resolved,
                                            "Unresolved" : unresolved,
                                            "Client To Respond" : client_to_respond,
                                        }
                                        return Response(
                                            {
                                                "Status": "Success",
                                                "Data": data
                                            }
                                            
                                        )
                                    return Response(
                                        {
                                            "Status":"Success",
                                            "Message": "SOAR data is not matched with SIEM"
                                        }
                                    )
                            return Response(
                                {
                                    "status":"Success",
                                    "Message":"SIEM data is not matched with this Rule"
                                }
                            )
                    else:
                        return Response(
                            {
                                "status":"Success",
                                "Message":"Rules Not Found for this usecase",
                            }
                        )
            else:
                return Response(
                    {
                        "status":"Success",
                        "Message":"This UseCase is not available",
                    }
                )
        else:
            return Response (
                {
                    "Status": "Failed",
                    "Message":"Pass a parameter 'UseCase'"
                }
            )
