from django.urls import path
from rest_framework import routers
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

simple_router = routers.SimpleRouter()
source = SourceViewSet.as_view({"post": "create"})
source_data = SourceViewSet.as_view({"get": "source_data"})

SIEM_event_count = SIEMViewSet.as_view({"get": "event_count_data"})
SIEM_all_data = SIEMViewSet.as_view({"get": "seim_all_data"})
SIEM_event_count_by_usecase = SIEMViewSet.as_view({"get": "event_count_by_usecases"})
Severity_Importance = SIEMViewSet.as_view({"get": "severity_by_offenses"})
avg_res_time = SIEMViewSet.as_view({"get": "avg_res_time"})
severity = SIEMViewSet.as_view({"get": "severity"})
severity_by_usecase = SIEMViewSet.as_view({"get": "severity_by_usecase"})
usecase_details = SIEMViewSet.as_view({"get": "usecase_details"})
usecase_offences = SIEMViewSet.as_view({"get": "offence_by_usecases"})


incident_priority = SOARViewSet.as_view({"get": "incident"})
usecase_incident = SOARViewSet.as_view({"get": "usecase_incident"})

request_mode = ITSMViewSet.as_view({"get": "request_modes"})
false_positives = ITSMViewSet.as_view({"get": "false_positives"})

# asset urls
asset_types = AssetViewSet.as_view({"get": "asset_types"})
asset = AssetViewSet.as_view({"get": "asset"})
add_asset = AssetViewSet.as_view({"post": "addasset"})
validate_asset = AssetViewSet.as_view({"post": "validate_asset_csv"})
upload_asset = AssetViewSet.as_view({"post": "upload_asset"})
delete_asset = AssetViewSet.as_view({"delete": "asset_delete"})
update_asset = AssetViewSet.as_view({"put": "update_asset"})
offence_asset_types = AssetViewSet.as_view({"get": "offence_asset_types"})

# Function urls
add_function = FunctionViewSet.as_view({"post": "addfunction"})
validate_function = FunctionViewSet.as_view({"post": "validate_function_csv"})
upload_function = FunctionViewSet.as_view({"post": "upload_function"})
delete_function = FunctionViewSet.as_view({"delete": "function_delete"})
update_function = FunctionViewSet.as_view({"put": "update_function"})
functions = FunctionViewSet.as_view({"get": "function"})
functiondetails = FunctionViewSet.as_view({"get": "functionlocationentity"})
asset_function = FunctionViewSet.as_view({"get": "function_asset"})
functions_offence = FunctionViewSet.as_view({"get": "offence_function"})

# Geolocation urls
add_location = GeoLocationViewSet.as_view({"post": "addlocation"})
validate_location = GeoLocationViewSet.as_view({"post": "validate_location"})
upload_location = GeoLocationViewSet.as_view({"post": "upload_location"})
delete_location = GeoLocationViewSet.as_view({"delete": "location_delete"})
update_location = GeoLocationViewSet.as_view({"put": "update_location"})
geo_location = GeoLocationViewSet.as_view({"get": "geo_locations"})
offence_location = GeoLocationViewSet.as_view({"get": "offence_location"})

# entity
entities = EntityViewSet.as_view({"get": "entities"})
add_entity = EntityViewSet.as_view({"post": "addentity"})
validate_entity = EntityViewSet.as_view({"post": "validate_entity"})
upload_entity = EntityViewSet.as_view({"post": "upload_entity"})
delete_entity = EntityViewSet.as_view({"delete": "entity_delete"})
update_entity = EntityViewSet.as_view({"put": "update_entity"})
offence_entity = EntityViewSet.as_view({"get": "offence_entity"})
offence_entity_assets = EntityViewSet.as_view({"get": "offence_entity_asset_types"})
offence_entity_location = EntityViewSet.as_view({"get": "offence_entity_location"})
offence_entity_function = EntityViewSet.as_view({"get": "offence_entity_function"})
offence_entity_geo_assettypes = EntityViewSet.as_view({"get": "offence_entity_geo_asset_types"})
offence_entity_geo_function = EntityViewSet.as_view({"get": "offence_entity_geo_function"})
get_ticket_id = ITSMViewSet.as_view({"get": "get_ticket_id"})

# category
add_category = CategoryViewSet.as_view({"post": "addcategory"})
validate_category = CategoryViewSet.as_view({"post": "validate_category"})
upload_category = CategoryViewSet.as_view({"post": "upload_category"})
category_details = CategoryViewSet.as_view({"get": "category_details"})
delete_category = CategoryViewSet.as_view({"delete": "category_delete"})
update_category = CategoryViewSet.as_view({"put": "update_category"})

# process
add_process = ProcessViewSet.as_view({"post": "addprocess"})
validate_process = ProcessViewSet.as_view({"post": "validate_process"})
upload_process = ProcessViewSet.as_view({"post": "upload_process"})
process_details = ProcessViewSet.as_view({"get": "process_details"})
delete_process = ProcessViewSet.as_view({"delete": "process_delete"})
update_process = ProcessViewSet.as_view({"put": "update_process"})

# Hub
hub = InsightHub.as_view({"post": "insights_hub"})
insight_tickets = InsightHub.as_view({"post": "insight_tickets"})
grid_master = InsightHub.as_view({"post": "master_data"})
asset_details = InsightHub.as_view({"post": "asset_details"})
oei_chart_data = ITSMViewSet.as_view({"post": "oei_chart_data"})
ticket_dropdown_data = ITSMViewSet.as_view({"post": "ticket_dropdown_data"})
oei_tickets = ITSMViewSet.as_view({"post": "oei_tickets"})
ticket_details = ITSMViewSet.as_view({"post": "ticket_details"})
sla_dropdown_data = ITSMViewSet.as_view({"post": "sla_dropdown_data"})
incident_close = ITSMViewSet.as_view({"post": "incident_close"})

urlpatterns = simple_router.urls
urlpatterns = urlpatterns + [
    path(r"api/v1/update_asset/<int:asset>", update_asset, name="update_asset"),
    path(r"api/v1/delete_asset/<int:asset_id>", delete_asset, name="Asset_Delete"),
    path(r"api/v1/add_asset/", add_asset, name="Add Asset Details"),
    path(r"api/v1/asset_types/", asset_types, name="Asset_Types"),
    path(r"api/v1/asset/", asset, name="Asset_Details"),
    path(r"api/v1/validate_asset/", validate_asset, name="validate Asset Details"),
    path(r"api/v1/upload_asset/", upload_asset, name="Upload Asset File"),

    path(r"api/v1/add_category/", add_category, name="Add Category Details"),
    path(r"api/v1/validate_category/", validate_category, name="validate Category Details"),
    path(r"api/v1/upload_category/", upload_category, name="Upload Category Details"),
    path(r"api/v1/delete_category/<int:category_id>", delete_category, name="Delete Category"),
    path(r"api/v1/update_category/<int:category_id>", update_category, name="Update Category"),
    path(r"api/v1/categories/", category_details, name="Category Details"),

    path(r"api/v1/add_process/", add_process, name="Add Process Details"),
    path(r"api/v1/validate_process/", validate_process, name="validate Process Details"),
    path(r"api/v1/upload_process/", upload_process, name="Upload Process Details"),
    path(r"api/v1/process_details/", process_details, name="Process Details"),
    path(r"api/v1/delete_process/<int:process_id>", delete_process, name="Delete Process Details"),
    path(r"api/v1/update_process/<int:process_id>", update_process, name="Update Process"),

    path(r"api/v1/add_function/", add_function, name="Add Function"),
    path(r"api/v1/validate_function/", validate_function, name="validate Function Details"),
    path(r"api/v1/upload_function/", upload_function, name="Upload Function Details"),
    path(r"api/v1/function/", functions, name="All Function"),
    path(r"api/v1/delete_function/<int:function_id>", delete_function, name="Delete Function"),
    path(r"api/v1/update_function/<int:function_id>", update_function, name="Update Function"),
    path(r"api/v1/function_details/", functiondetails, name="All Function Details"),

    path(r"api/v1/function/assets/", asset_function, name="Asset for Functions"),
    path(r"api/v1/function/offence/", functions_offence, name="Offence for Functions"),

    path(r"api/v1/add_location/", add_location, name="Add Geo Location"),
    path(r"api/v1/validate_location/", validate_location, name="validate location Details"),
    path(r"api/v1/upload_location/", upload_location, name="Upload location Details"),
    path(r"api/v1/geo_locations/", geo_location, name="Geo Location"),
    path(r"api/v1/delete_location/<int:location_id>", delete_location, name="Delete Geo Location"),
    path(r"api/v1/update_location/<int:location_id>", update_location, name="Update Location"),

    path(r"api/v1/geo_locations/offence/", offence_location, name="Offence for Geo Location"),

    path(r"api/v1/add_entity/", add_entity, name="Add Entity Details"),
    path(r"api/v1/validate_entity/", validate_entity, name="validate Entity Details"),
    path(r"api/v1/upload_entity/", upload_entity, name="Upload Entity Details"),
    path(r"api/v1/entities/", entities, name="Entities_Data"),
    path(r"api/v1/delete_entity/<int:entity_id>", delete_entity, name="Delete Entities Data"),
    path(r"api/v1/update_entity/<int:entity_id>", update_entity, name="Update Entity"),

    path(r"api/v1/entity/offence/", offence_entity, name="Offence for Entity"),

    path(r"api/v1/ticket_id/", get_ticket_id, name="get_ticket_id"),
    path(r"api/v1/source/", source, name="Source",),
    path(r"api/v1/source/data/", source_data, name="Source_data",),
    path(r"api/v1/siem/", SIEM_all_data, name="SIEM_all_data",),
    path(r"api/v1/siem-event/", SIEM_event_count, name="SIEM_event_count",),
    path(r"api/v1/siem-event-by-usecase/", SIEM_event_count_by_usecase, name="Event_Count_by_Usecase",),
    path(r"api/v1/severity-importance/", Severity_Importance, name="Severity_For_Offense",),
    path(r"api/v1/average-response/", avg_res_time, name="Average_Response_Time",),
    path(r"api/v1/severities/", severity, name="Severity_Mean_Details",),
    path(r"api/v1/usecase_severity/", severity_by_usecase, name="UseCase_Severity",),
    path(r"api/v1/usecase_details/", usecase_details, name="Usecase_Details",),
    path(r"api/v1/incident_priority/", incident_priority, name="Incident_Priority",),
    path(r"api/v1/usecase_incident/", usecase_incident, name="Usecase_Incident",),
    path(r"api/v1/request_mode/", request_mode, name="Request_modes"),
    path(r"api/v1/false_positives/", false_positives, name="False Positives"),
    path(r"api/v1/offence/asset_types/", offence_asset_types, name="Offence for Asset_Types"),

    path(r"api/v1/usecase/offence/", usecase_offences, name="Offence for Usecase"),
    path(r"api/v1/usecase/asset/entity/offence/", offence_entity_assets, name="Offences for Asset & Entity"),
    path(r"api/v1/usecase/location/entity/offence/", offence_entity_location, name="Offences for Entity & location"),
    path(r"api/v1/usecase/function/entity/offence/", offence_entity_function, name="Offences for Entity & function"),
    path(r"api/v1/usecase/asset/geo/entity/offence/", offence_entity_geo_assettypes,
         name="Offences for Entity, Geo and Asset types"),
    path(r"api/v1/usecase/function/geo/entity/offence/", offence_entity_geo_function,
         name="Offences for Entity, Geo and Function"),

    path(r"api/v1/insight_tickets/", insight_tickets, name="insight_tickets"),
    path(r"api/v1/insights/", hub, name="insight_hub"),
    path(r"api/v1/chart-data", hub, name="insight_hub"),
    path(r"api/v1/insight-grid", insight_tickets, name="insight_tickets"),
    path(r"api/v1/insight-grid-master-dropdowns", grid_master, name="grid_master"),
    path(r"api/v1/asset_details/", asset_details, name="asset_details"),
    path(r"api/v1/oei_chart_data/", oei_chart_data, name="oei_chart_data"),
    path(r"api/v1/oei_grid_data/", oei_tickets, name="oei_tickets"),
    path(r"api/v1/ticket_dropdown_data", ticket_dropdown_data, name="ticket_dropdown_data"),
    path(r"api/v1/ticket_details/", ticket_details, name="ticket_details"),
    path(r"api/v1/sla_dropdown_data", sla_dropdown_data, name="sla_dropdown_data"),
    path(r"api/v1/incident_close", incident_close, name="close")
]
