from datetime import datetime
from decimal import *
from django.core.exceptions import ValidationError
from django_cron import CronJobBase, Schedule
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from order.models import Order, InvestmentCompany
import os
import requests
import smtplib
import time


class CronJob(CronJobBase):
    
    code = 'addOrder'    # a unique code

    def do(self):
        # Sprawdzenie, czy dzisiaj jest dzień tygodnia od poniedziałku do piątku
        today = datetime.today().weekday()
        if today < 5:  # Poniedziałek to 0, Niedziela to 6
            self.run_job()
        else:
            print("Dziś jest weekend, zadanie cron nie zostanie wykonane.")
        self.football()

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


    def football(self):
        # Dane nadawcy i odbiorcy
        from_address = os.getenv('FROM_ADDRESS')
        to_address = os.getenv('TO_ADDRESS')

        # Dane logowania
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')

        headers = {
            'x-rapidapi-key': os.getenv('API_FOOTBALL_KEY')
            }

        link = os.getenv('API_FOOTBALL')+'?live=all'
        res = requests.get(link, headers=headers).json()
        
        fixtures = res.get('response')
        for match in fixtures:
            goals = match.get('goals')
            status = match.get('fixture').get('status')
            if (goals.get('home') + 1 == goals.get('away') or goals.get('home') == goals.get('away') + 1) and goals.get('home') + goals.get('away') < 4 and status.get('elapsed')>50 and status.get('elapsed')<80:
                link = 'https://api-football-v1.p.rapidapi.com/v3/odds?fixture=' + str(match.get('fixture').get('id'))
                teams = match.get('teams')
                home = teams.get('home').get('name')
                away = teams.get('away').get('name')
                print(home + ' ' + away)
                bookmakers = requests.get(link, headers=headers).json().get('response')
                for bookmaker in bookmakers:
                    odds = bookmaker.get('bookmakers')
                    odds_list = odds[0].get('bets')[0].get('values')

                    home_odd = next((item['odd'] for item in odds_list if item['value'] == 'Home'), None)
                    away_odd = next((item['odd'] for item in odds_list if item['value'] == 'Away'), None)

                    # Przekształcanie kursów na Decimal
                    home_odd_decimal = Decimal(home_odd)
                    away_odd_decimal = Decimal(away_odd)

                    send = False

                    # Logika porównywania
                    if goals.get('home') + 1 == goals.get('away') and home_odd_decimal +  Decimal('1.0') < away_odd_decimal:
                        send = True

                    if goals.get('home') == goals.get('away') + 1 and home_odd_decimal > away_odd_decimal + Decimal('2.0'):
                        send = True

                    if send:
                        # Treść e-maila
                        subject = 'Kandydat'
                        body = home + ' ' + away

                        # Tworzenie wiadomości
                        msg = MIMEMultipart()
                        msg['From'] = from_address
                        msg['To'] = to_address
                        msg['Subject'] = subject

                        # Dodanie treści wiadomości
                        msg.attach(MIMEText(body, 'plain'))

                        # Wysyłanie wiadomości
                        try:
                            # Połączenie z serwerem SMTP
                            server = smtplib.SMTP(os.getenv('SERVER_NAME'), 587)
                            server.starttls()

                            # Logowanie do serwera
                            server.login(username, password)

                            # Wysyłanie wiadomości
                            text = msg.as_string()
                            server.sendmail(from_address, to_address, text)

                            print('Wiadomość została wysłana pomyślnie')
                        except Exception as e:
                            print(f'Błąd podczas wysyłania wiadomości: {e}')
                        finally:
                        # Zamknięcie połączenia z serwerem
                            server.quit()
