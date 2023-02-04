from django_cassandra_engine.rest.serializers import \
    DjangoCassandraModelSerializer
from rest_framework import serializers
from apiApp.models import BaseModel, UserInquirySearchHistory, StellarCreatorAccountLineage


class BaseModelSerializer(DjangoCassandraModelSerializer):
    class Meta:
        model = BaseModel
        fields = "__all__"

class UserInquirySearchHistorySerializer(BaseModelSerializer):
    class Meta:
        model = UserInquirySearchHistory
        fields = "__all__"

class StellarCreatorAccountLineageSerializer(BaseModelSerializer):
    xlm_balance = serializers.FloatField()

    class Meta:
        model = StellarCreatorAccountLineage
        fields = "__all__"
