from django.urls import path

from .views.hub import InsightHub
from .views.process import ProcessViewSet
from .views.siem import SIEMViewSet
from .views.source import SourceViewSet
from .views.soar import SOARViewSet
from .views.itsm import ITSMViewSet
from .views.assets import AssetViewSet
from .views.functions import FunctionViewSet
from .views.entity import EntityViewSet
from .views.geolocation import GeoLocationViewSet
from .views.category import CategoryViewSet

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

# asset urls
asset_types = AssetViewSet.as_view({"get": "asset_types"})
asset = AssetViewSet.as_view({"get": "asset"})
add_asset = AssetViewSet.as_view({"post": "addasset"})
delete_asset = AssetViewSet.as_view({"delete": "asset_delete"})
update_asset = AssetViewSet.as_view({"put": "update_asset"})
offence_asset_types = AssetViewSet.as_view({"get": "offence_asset_types"})

# Function urls
add_function = FunctionViewSet.as_view({"post":"addfunction"})
delete_function = FunctionViewSet.as_view({"delete":"function_delete"})
update_function = FunctionViewSet.as_view({"put":"update_function"})
functions = FunctionViewSet.as_view({"get": "function"})
functiondetails = FunctionViewSet.as_view({"get": "functionlocationentity"})
asset_function = FunctionViewSet.as_view({"get": "function_asset"})
functions_offence = FunctionViewSet.as_view({"get": "offence_function"})

# Geolocation urls
add_location = GeoLocationViewSet.as_view({"post":"addlocation"})
delete_location = GeoLocationViewSet.as_view({"delete":"location_delete"})
update_location = GeoLocationViewSet.as_view({"put":"update_location"})
geo_location = GeoLocationViewSet.as_view({"get": "geo_locations"})
offence_location = GeoLocationViewSet.as_view({"get": "offence_location"})

# entity
entities = EntityViewSet.as_view({"get": "entities"})
add_entity = EntityViewSet.as_view({"post":"addentity"})
delete_entity = EntityViewSet.as_view({"delete":"entity_delete"})
update_entity = EntityViewSet.as_view({"put":"update_entity"})
offence_entity = EntityViewSet.as_view({"get": "offence_entity"})
offence_entity_assets = EntityViewSet.as_view({"get": "offence_entity_asset_types"})
offence_entity_location = EntityViewSet.as_view({"get": "offence_entity_location"})
offence_entity_function = EntityViewSet.as_view({"get": "offence_entity_function"})
offence_entity_geo_assettypes = EntityViewSet.as_view({"get": "offence_entity_geo_asset_types"})
offence_entity_geo_function = EntityViewSet.as_view({"get": "offence_entity_geo_function"})
get_ticket_id = ITSMViewSet.as_view({"get": "get_ticket_id"})

# category
add_category = CategoryViewSet.as_view({"post":"addcategory"})
category_details = CategoryViewSet.as_view({"get":"category_details"})
delete_category = CategoryViewSet.as_view({"delete":"category_delete"})
update_category = CategoryViewSet.as_view({"put":"update_category"})

# process
add_process = ProcessViewSet.as_view({"post": "addprocess"})
process_details = ProcessViewSet.as_view({"get": "process_details"})
delete_process = ProcessViewSet.as_view({"delete": "process_delete"})
update_process = ProcessViewSet.as_view({"put": "update_process"})

# Hub
insight_tickets = InsightHub.as_view({"post": "insight_tickets"})
hub = InsightHub.as_view({"post": "insights_hub"})
grid_master = InsightHub.as_view({"post": "master_data"})




urlpatterns = [
    path(r"update_asset/<int:asset>", update_asset, name="update_asset"),
    path(r"delete_asset/<int:asset_id>", delete_asset, name="Asset_Delete"),
    path(r"add_asset/", add_asset, name="Add Asset Details"),
    path(r"asset_types/", asset_types, name="Asset_Types"),
    path(r"asset/", asset, name="Asset_Details"),

    path(r"add_category/", add_category, name="Add Category Details"),
    path(r"delete_category/<int:category_id>", delete_category, name="Delete Category"),
    path(r"update_category/<int:category_id>", update_category, name="Update Category"),
    path(r"categories/", category_details, name="Category Details"),

    path(r"add_process/", add_process, name="Add Process Details"),
    path(r"process_details/", process_details, name="Process Details"),
    path(r"delete_process/<int:process_id>", delete_process, name="Delete Process Details"),
    path(r"update_process/<int:process_id>", update_process, name="Update Process"),

    path(r"add_function/", add_function, name="Add Function"),
    path(r"function/", functions, name="All Function"),
    path(r"delete_function/<int:function_id>", delete_function, name="Delete Function"),
    path(r"update_function/<int:function_id>", update_function, name="Update Function"),
    path(r"function_details/", functiondetails, name="All Function Details"),

    path(r"function/assets/", asset_function, name="Asset for Functions"),
    path(r"function/offence/", functions_offence, name="Offence for Functions"),

    path(r"add_location/", add_location, name="Add Geo Location"),
    path(r"geo_locations/", geo_location, name="Geo Location"),
    path(r"delete_location/<int:location_id>", delete_location, name="Delete Geo Location"),
    path(r"update_location/<int:location_id>", update_location, name="Update Location"),

    path(r"geo_locations/offence/", offence_location, name="Offence for Geo Location"),

    path(r"add_entity/", add_entity, name="Add Entity Details"),
    path(r"entities/", entities, name="Entities_Data"),
    path(r"delete_entity/<int:entity_id>", delete_entity, name="Delete Entities Data"),
    path(r"update_entity/<int:entity_id>", update_entity, name="Update Entity"),

    path(r"entity/offence/", offence_entity, name="Offence for Entity"),

    path(r"ticket_id/", get_ticket_id, name="get_ticket_id"),
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
    path(r"offence/asset_types/", offence_asset_types, name="Offence for Asset_Types"),

    path(r"usecase/offence/", usecase_offences, name="Offence for Usecase"),
    path(r"usecase/asset/entity/offence/", offence_entity_assets, name="Offences for Asset & Entity"),
    path(r"usecase/location/entity/offence/", offence_entity_location, name="Offences for Entity & location"),
    path(r"usecase/function/entity/offence/", offence_entity_function, name="Offences for Entity & function"),
    path(r"usecase/asset/geo/entity/offence/", offence_entity_geo_assettypes,
         name="Offences for Entity, Geo and Asset types"),
    path(r"usecase/function/geo/entity/offence/", offence_entity_geo_function,
         name="Offences for Entity, Geo and Function"),

    path(r"insight_tickets/", insight_tickets, name="insight_tickets"),
    path(r"insights/", hub, name="insight_hub"),
    path(r"chart-data", hub, name="insight_hub"),
    path(r"insight-grid", insight_tickets, name="insight_tickets"),
    path(r"insight-grid-master-dropdowns", grid_master, name="grid_master"),
]
