from rest_framework import serializers
from hub.models.preference import Preference


class PreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preference
        fields = (
            'user',
            'session',
        )
