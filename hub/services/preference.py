from SITAbackend.hub.models.preference import Preference


class PreferenceService:

    @staticmethod
    def preference_input(user,validated_data):

        queryset = Preference.objects.get(id=user)
        graph = validated_data.get("graph")
        graph_name = validated_data.get("graph_name")
        user_id = user
        value = validated_data.get("value")
        preference_kwargs = {
            "graph": graph,
            "graph_name": graph_name,
            "user_id": user_id,
            "value": value
        }
        for key, value in preference_kwargs.items():
            setattr(queryset, key, value)
        queryset.save()

        return queryset
