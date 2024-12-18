from rest_framework import serializers
from job_function.models import PostedJobs


class PostedJobsSerializer(serializers.ModelSerializer):
    """
    Serializer for Jobs Posted creation and management
    """

    class Meta:
        model = PostedJobs
        fields = ['job_title', 'postedBy', 'job_description', 'posted_date', 'status']

    def validate_postedBy(self, value):
        if value.user_type != 'RECRUITER':
            raise ValueError("Only Recruiters can only post jobs")
        return value
