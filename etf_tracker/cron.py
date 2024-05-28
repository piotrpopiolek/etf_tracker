from django_cron import CronJobBase, Schedule
from order.models import Order, InvestmentCompany
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError


class CronJob(CronJobBase):
    # Ustawienie harmonogramu na raz dziennie
    RUN_AT_TIMES = ['00:00']  

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    
    code = 'addOrder'    # a unique code

    def do(self):
        # Sprawdzenie, czy dzisiaj jest dzień tygodnia od poniedziałku do piątku
        today = datetime.today().weekday()
        if today < 5:  # Poniedziałek to 0, Niedziela to 6
            self.run_job()
        else:
            print("Dziś jest weekend, zadanie cron nie zostanie wykonane.")

    def run_job(self):
        today = datetime.today().date()
        investmentCompanies = InvestmentCompany.objects.all()

        for company in investmentCompanies:
            try:
                order = Order.objects.filter(date_order=today, investmentcompany__name=company.name)
                if not order.exists():
                    new_order = Order(date_order=today, investmentcompany=company, amount=0)
                    new_order.save()
                    print(new_order)
            except ValidationError as e:
                print(f"Wystąpił błąd walidacji przy zapisie zamówienia dla firmy {company}: {e}")
            except Exception as e:
                print(f"Wystąpił ogólny błąd przy zapisie zamówienia dla firmy {company}: {e}")
