from core.models import Application as Image, BootScript
from core.metrics import _get_application_metrics
from rest_framework import serializers
from dateutil import rrule
from api.v2.serializers.summaries import UserSummarySerializer
from api.v2.serializers.fields import (
        ImageVersionRelatedField, TagRelatedField)
from api.v2.serializers.fields.base import UUIDHyperlinkedIdentityField


class SwapBooleanField(serializers.BooleanField):
    def to_internal_value(self, data):
        truth_value = super(SwapBooleanField, self).to_internal_value(data)
        swap_value = not truth_value
        return swap_value

    def to_representation(self, value):
        truth_value = super(SwapBooleanField, self).to_representation(value)
        swap_value = not truth_value
        return swap_value


class ImageMetricSerializer(serializers.HyperlinkedModelSerializer):
    url = UUIDHyperlinkedIdentityField(
        view_name='api:v2:applicationmetric-detail',
    )
    metrics = serializers.SerializerMethodField()

    def get_metrics(self, application):
        request = self.context.get('request', None)
        interval = rrule.MONTHLY
        limit = 3
        if request and 'interval' in request.query_params:
            interval_str = request.query_params.get('interval', '').lower()
            if 'week' in interval_str:
                interval = rrule.WEEKLY
                limit = 12
            elif 'day' in interval_str or 'daily' in interval_str:
                interval = rrule.DAILY
                limit = 90
        return _get_application_metrics(application, interval=interval, limit=limit, read_only=True)

    class Meta:
        model = Image
        fields = (
            'id',
            'url',
            'uuid',
            'name',
            # Adtl. Fields
            'metrics',
        )
