from rest_framework import viewsets
from rest_framework.response import Response
from hub.services.itsm import ITSMService


class ITSMViewSet(viewsets.ModelViewSet):
    
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = ITSMService.get_queryset()

    def request_modes(self, request):
        try:
            Total_modes = []
            for mode in self.queryset.values():
                    Total_modes.append(mode.get('Request_mode'))
            # Created blank dict, added asset_type wise count in blank dict
            mode_types = dict()  
            for modes in Total_modes:
                mode_types[modes] = mode_types.get(modes, 0) + 1
            # added total asset types in dict by using other asset type counts
            mode_types['Total Requests'] = sum(mode_types.values())
            data = mode_types
            return Response(
                {
                    "Status": "Success",
                    "Data": data
                }
            )
        except:
            return Response(
                {
                    "Status": "Failed",
                    "Message": "You Don't have data"
                }
            )
        
    def false_positives(self, request):
        false_positive = 0
        ITSM_data = ITSMService.get_queryset()
        if ITSM_data:
            for data in ITSM_data:
                if data.Application_Status == "False Positive":
                    false_positive += 1
            data = {
                "False Positives": false_positive,
            }
            return Response(
                {
                    "Status": "Success",
                    "Data": data
                }
            )
        else:
            return Response(
                {
                    "Status": "Failed",
                    "Message": "You Don't have any ITSM data"
                }
            )

    