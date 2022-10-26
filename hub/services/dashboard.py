import logging
from operator import itemgetter

from hub.models import SecurityPulse,CyFeeds,Perspective

logger = logging.getLogger(__name__)


class DashboardService:
    @staticmethod
    def dashboard_grid_data():
        cyfeed = CyFeeds.objects.all().order_by('-timestamp')
        feeds = []
        # using for loop to store the data
        for data in cyfeed:
            url = data.informationSource_references_references
            url = url.strip("[").strip("]").replace("'","")
            urls = url.split(",")
            date = data.vulnerabilities
            for data in list(date):
                time = data.get("publishedDateTime").get("value")
            new_feed = {
                "title": data.title,
                "description": data.descriptions,
                "IsExternal": True,
                "links": urls,
                "published_date": time.date()
            }
            feeds.append(new_feed)
        analysis = Perspective.objects.all().order_by('-updated_at')
        analysis_list = []
        for data in analysis:
            new_feed = {
                "title": data.perspective_title,
                "type": "analysis",
                "id": data.id,
                "IsExternal": False,
                "published_date": data.updated_at.date()
            }
            analysis_list.append(new_feed)
        security_pulse = SecurityPulse.objects.all().order_by('-updated_at')
        security_pulse_list = []
        for data in security_pulse:
            new_feed = {
                "title": data.security_pulse_title,
                "type": "analysis",
                "id": data.id,
                "IsExternal": False,
                "published_date": data.updated_at.date()
            }
            security_pulse_list.append(new_feed)
        query_data = analysis_list + security_pulse_list + feeds
        query_data = sorted(query_data, key=itemgetter('published_date'), reverse=True)
        return query_data