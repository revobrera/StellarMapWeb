from rest_framework import serializers
from apiApp.models import StellarAccountInquiryHistory, StellarAccountLineage


class BaseModelSerializer(serializers.Serializer):
    # Re-declaring fields for Serializer
    id = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    class Meta:
        fields = ['id', 'created_at', 'updated_at']

class StellarAccountInquiryHistorySerializer(BaseModelSerializer):
    """
    Serializer for the StellarAccountInquiryHistory model.

    Notes:
        To use the StellarAccountInquiryHistory model, a regular Serializer
        class must be used instead of ModelSerializer because the model's
        parent class is an abstract model. This means that the fields and
        their validation rules have to be defined manually in the Serializer.
    """

    # Re-declaring fields for Serializer
    # validating data type and character length
    stellar_account = serializers.CharField(max_length=56)
    network_name = serializers.CharField(max_length=9)
    status = serializers.CharField(max_length=20)

    class Meta:
        model = StellarAccountInquiryHistory
        fields = BaseModelSerializer.Meta.fields + ['stellar_account', 'network_name', 'status']

class StellarAccountLineageSerializer(BaseModelSerializer):
    # Re-declaring fields for Serializer
    account_active = serializers.CharField(max_length=30)
    stellar_creator_account = serializers.CharField(max_length=56)
    stellar_account = serializers.CharField(max_length=56)
    stellar_account_created_at = serializers.DateTimeField()
    network_name = serializers.CharField(max_length=9)
    home_domain = serializers.CharField(max_length=71)
    xlm_balance = serializers.FloatField()
    horizon_accounts_doc_api_href = serializers.CharField()
    horizon_accounts_operations_doc_api_href = serializers.CharField()
    horizon_accounts_effects_doc_api_href = serializers.CharField()
    stellar_expert_explorer_account_doc_api_href = serializers.CharField()
    status = serializers.CharField(max_length=36)

    class Meta:
        model = StellarAccountLineage
        fields = BaseModelSerializer.Meta.fields + [
            'account_active',
            'stellar_creator_account',
            'stellar_account',
            'stellar_account_created_at',
            'network_name',
            'home_domain',
            'xlm_balance',
            'horizon_accounts_doc_api_href',
            'horizon_accounts_operations_doc_api_href',
            'horizon_accounts_effects_doc_api_href',
            'stellar_expert_explorer_account_doc_api_href',
            'status'
        ]