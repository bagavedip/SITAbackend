from rest_framework.response import Response
from hub.models.cy_feeds import CyFeeds

class Cy_FeedsService:
    
    @staticmethod
    def get_cy_feeds():
        """Function to get all feeds of cy pharma"""

        # Query for get all data of CY
        query_data = CyFeeds.objects.all().order_by('-timestamp')
        feeds = []

        #using for loop to store the data
        for data in query_data:
            new_feed = {
            "title": data.title,
            "description" :data.descriptions,
            "iconclass" :"fa-solid fa-display",
            "linkurl" : data.informationSource_references_references 
            }
            feeds.append(new_feed)
        return Response({
            "FeedHeader":"CY Pharma",
            "Feed": feeds
        })
