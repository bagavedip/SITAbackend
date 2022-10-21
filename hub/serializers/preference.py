from rest_framework import serializers
from hub.models.preference import Preference


class PreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preference
        fields = (
            'graph',
            'graph_name',
            'user_id',
            'value'
        )
    #
    # def preference_input(self, data):
    #     pass

