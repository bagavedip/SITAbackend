from django.urls import path
from .views.siem import SIEMViewSet
from .views.source import SourceViewSet
from .views.soar import SOARViewSet
from .views.itsm import ITSMViewSet
from .views.assets import AssetViewSet
from .views.add_assets import AddAssetViewSet
from .views.functions import FunctionViewSet
from .views.entity import EntityViewSet
from .views.geolocation import GeoLocationViewSet
from .views.category import AddCategoryViewSet
from .views.process import AddProcessViewSet


source = SourceViewSet.as_view({"post": "create"})
source_data = SourceViewSet.as_view({"get": "source_data"})

SIEM_event_count = SIEMViewSet.as_view({"get": "event_count_data"})
SIEM_all_data = SIEMViewSet.as_view({"get": "seim_all_data"})
SIEM_event_count_by_usecase = SIEMViewSet.as_view({"get": "event_count_by_usecases"})
Severity_Importance = SIEMViewSet.as_view({"get": "severity_by_offenses"})
avg_res_time = SIEMViewSet.as_view({"get": "avg_res_time"})
severity = SIEMViewSet.as_view({"get": "severity"})
severity_by_usecase = SIEMViewSet.as_view({"get":"severity_by_usecase"})
usecase_details = SIEMViewSet.as_view({"get":"usecase_details"})
usecase_offences = SIEMViewSet.as_view({"get": "offence_by_usecases"})


incident_priority = SOARViewSet.as_view({"get": "incident"})
usecase_incident = SOARViewSet.as_view({"get": "usecase_incident"})

request_mode = ITSMViewSet.as_view({"get": "request_modes"})
false_positives = ITSMViewSet.as_view({"get": "false_positives"})

asset_types = AssetViewSet.as_view({"get": "asset_types"})
asset = AssetViewSet.as_view({"get": "asset"})
add_asset = AddAssetViewSet.as_view({"post": "addasset"})
offence_asset_types = AssetViewSet.as_view({"get": "offence_asset_types"})

functions = FunctionViewSet.as_view({"get": "function"})
functiondetails = FunctionViewSet.as_view({"get": "functionlocationentity"})
asset_function = FunctionViewSet.as_view({"get": "function_asset"})
functions_offence = FunctionViewSet.as_view({"get": "offence_function"})

geo_location = GeoLocationViewSet.as_view({"get": "geo_locations"})
offence_location = GeoLocationViewSet.as_view({"get": "offence_location"})

entities = EntityViewSet.as_view({"get": "entities"})
offence_entity = EntityViewSet.as_view({"get": "offence_entity"})
offence_entity_assets = EntityViewSet.as_view({"get": "offence_entity_asset_types"})
offence_entity_location = EntityViewSet.as_view({"get": "offence_entity_location"})
offence_entity_function = EntityViewSet.as_view({"get": "offence_entity_function"})
offence_entity_geo_assettypes = EntityViewSet.as_view({"get": "offence_entity_geo_asset_types"})
offence_entity_geo_function = EntityViewSet.as_view({"get": "offence_entity_geo_function"})

add_category = AddCategoryViewSet.as_view({"post": "addcategory"})
add_process = AddProcessViewSet.as_view({"post": "addprocess"})


urlpatterns = [
    path(r"source/", source, name="Source",),
    path(r"source/data/", source_data, name="Source_data",),
    path(r"siem/", SIEM_all_data, name="SIEM_all_data",),
    path(r"siem-event/", SIEM_event_count, name="SIEM_event_count",),
    path(r"siem-event-by-usecase/", SIEM_event_count_by_usecase, name="Event_Count_by_Usecase",),
    path(r"severity-importance/", Severity_Importance, name="Severity_For_Offense",),
    path(r"average-response/", avg_res_time, name="Average_Response_Time",),
    path(r"severities/", severity, name="Severity_Mean_Details",),
    path(r"usecase_severity/", severity_by_usecase, name="UseCase_Severity",),
    path(r"usecase_details/", usecase_details, name="Usecase_Details",),
    path(r"incident_priority/", incident_priority, name="Incident_Priority",),
    path(r"usecase_incident/", usecase_incident, name="Usecase_Incident",),
    path(r"request_mode/", request_mode, name="Request_modes"),
    path(r"false_positives/", false_positives, name="False Positives"),
    path(r"asset_types/", asset_types, name="Asset_Types"),
    path(r"asset/", asset, name="Asset_Details"),
    path(r"add_asset/", add_asset, name="Add Asset Details"),
    path(r"add_category/", add_category, name="Add Category Details"),
    path(r"add_process/", add_process, name="Add Process Details"),
    path(r"offence/asset_types/", offence_asset_types, name="Offence for Asset_Types"),
    path(r"function/", functions, name="All Function"),
    path(r"function_details/", functiondetails, name="All Function Details"),
    path(r"function/assets/", asset_function, name="Asset for Functions"),
    path(r"function/offence/", functions_offence, name="Offence for Functions"),
    path(r"geo_locations/", geo_location, name="Geo Location"),
    path(r"geo_locations/offence/", offence_location, name="Offence for Geo Location"),
    path(r"entities/", entities, name= "Entities_Data"),
    path(r"entity/offence/", offence_entity, name="Offence for Entity"),
    path(r"usecase/offence/", usecase_offences, name="Offence for Usecase"),
    path(r"usecase/asset/entity/offence/", offence_entity_assets, name="Offences for Asset & Entity"),
    path(r"usecase/location/entity/offence/", offence_entity_location, name="Offences for Entity & location"),
    path(r"usecase/function/entity/offence/", offence_entity_function, name="Offences for Entity & function"),
    path(r"usecase/asset/geo/entity/offence/", offence_entity_geo_assettypes,
         name="Offences for Entity, Geo and Asset types"),
    path(r"usecase/function/geo/entity/offence/", offence_entity_geo_function,
         name="Offences for Entity, Geo and Function"),
]
