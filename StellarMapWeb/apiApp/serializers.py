from django_cassandra_engine.rest.serializers import \
    DjangoCassandraModelSerializer
from rest_framework import serializers
from apiApp.models import BaseModel, StellarAccountInquiryHistory, StellarAccountLineage


class BaseModelSerializer(DjangoCassandraModelSerializer):
    class Meta:
        model = BaseModel
        fields = "__all__"

class StellarAccountInquiryHistorySerializer(BaseModelSerializer):
    class Meta:
        model = StellarAccountInquiryHistory
        fields = "__all__"

class StellarAccountLineageSerializer(BaseModelSerializer):
    xlm_balance = serializers.FloatField()

    class Meta:
        model = StellarAccountLineage
        fields = "__all__"
