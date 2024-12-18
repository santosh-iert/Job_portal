from django.db import models
from users.models import CustomUser

# Create your models here.


class PostedJobs(models.Model):
    """
    Posted Jobs model
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'active'),
        ('CLOSED', 'closed')
    ]

    job_title = models.CharField(max_length=20, unique=True, )
    postedBy = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='incidents')
    job_description = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    def __str__(self):
        return f"{self.job_title}"

    class Meta:
        ordering = ['-posted_date']