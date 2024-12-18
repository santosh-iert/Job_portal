# Serializer for User Registration
import re

from rest_framework import serializers

from applicants.models import AppliedJobs


class AppliedJobsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppliedJobs
        fields = ['jobId', 'user']
