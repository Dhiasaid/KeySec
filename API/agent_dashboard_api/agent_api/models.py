from django.db import models

class Agent(models.Model):
    agent_id = models.CharField(max_length=50)
    desktop_name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=15)
    vlan = models.CharField(max_length=50)

    def __str__(self):
        return self.desktop_name
