from django.db import models
import json

class Academia(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.TextField(null=True, blank=True)
    major = models.TextField(null=True, blank=True)
    interests = models.TextField(null=True, blank=True)  # Store interests as JSON string

    def set_interests(self, interests_list):
        self.interests = json.dumps(interests_list)

    def get_interests(self):
        if self.interests:
            return json.loads(self.interests)
        return []

    def __str__(self):
        return self.email
