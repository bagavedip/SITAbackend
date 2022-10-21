from hub.models.preference import Preference


class PreferenceService:

    @staticmethod
    def preference_input(graph,graph_name, user_id,value):
        print("inside service")
        save_preference = Preference(
            graph=graph,
            graph_name=graph_name,
            user_id=user_id,
            value=value
        )
        save_preference.save()
        print("preference saved successfully")
        return "Update Added Successfully !!"

        #
        # queryset = Preference.objects.get(id=user)
        # graph = validated_data.get("graph")
        # graph_name = validated_data.get("graph_name")
        # user_id = user
        # value = validated_data.get("value")
        # preference_kwargs = {
        #     "graph": graph,
        #     "graph_name": graph_name,
        #     "user_id": user_id,
        #     "value": value
        # }
        # for key, value in preference_kwargs.items():
        #     setattr(queryset, key, value)
        # queryset.save()
        # asset = queryset
        # return asset
