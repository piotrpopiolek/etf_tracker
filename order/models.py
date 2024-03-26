from django.db import models
from investmentCompany.models import InvestmentCompany

class Order(models.Model):
    date_add = models.TimeField()
    date_order = models.DateField()
    investmentcompany = models.ForeignKey(InvestmentCompany, models.DO_NOTHING, db_column='investmentCompany_id')
    amount = models.FloatField()

    def __str__(self):
        return "{} {} {}".format(self.date_order, self.investmentcompany, self.amount)

    class Meta:
        managed = False
        db_table = 'order'