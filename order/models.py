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

class Summary(models.Model):
    date_order = models.DateField(primary_key=True)
    name = models.CharField(max_length=50)
    amount = models.FloatField()
    sum = models.FloatField()
    average = models.FloatField()

    def __str__(self):
        return "{} {} {} {} {}".format(self.date_order, self.name, self.amount, self.sum, self.average)

    class Meta:
        managed = False
        db_table = 'Summary'


class Sum(models.Model):
    date_order = models.DateField(primary_key=True)
    sum = models.FloatField()
    def __str__(self):
        return "{} {}".format(self.date_order, self.sum)

    class Meta:
        managed = False
        db_table = 'Sum'