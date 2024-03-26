from django.db import models

class InvestmentCompany(models.Model):
    date_add = models.TimeField()
    name = models.CharField(max_length=50)
    ticket = models.CharField(max_length=10)

    def __str__(self):
        return "{} {}".format(self.name, self.ticket)

    class Meta:
        managed = False
        db_table = 'investmentCompany'