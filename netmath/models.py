from django.db import models

class SubnetCalculation(models.Model):
    cidr_input = models.CharField(max_length=18)
    binary_num = models.TextField(max_length=32, null=True, blank=True)
    subnet_mask = models.CharField(max_length=18)
    total_ip = models.IntegerField()
    usable_host = models.IntegerField()
    network_address = models.GenericIPAddressField(null=True, blank=True)
    broadcast_address = models.GenericIPAddressField(null=True, blank=True)
    first_host = models.GenericIPAddressField(null=True, blank=True)
    last_host = models.GenericIPAddressField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cidr_input} with total {self.total_ip} ip related Data created on {self.created_on}"
