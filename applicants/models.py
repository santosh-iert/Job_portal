from django.db import models
# Create your models here.
from django.db import models
from django.db.models import UniqueConstraint

from job_function.models import PostedJobs
from users.models import CustomUser


class AppliedJobs(models.Model):
    """
    Applied Jobs model to track individual applied Jobs
    """
    jobId = models.ForeignKey(PostedJobs, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'jobId'], name='unique_user_job')]
        ordering = ['-applied_date']
    def __str__(self):
        return f"{self.jobId}"