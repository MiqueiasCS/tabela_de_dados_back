from accounts.models import User
from reports.models import Vunerabilities
import csv


def register_user():
    user = {"email":"testador@mail.com","password":"123asd"}

    User.objects.all().delete()

    new_user = User.objects.create_user(**user)
    new_user.save()


def read_file_cvs():
    reports_list = []

    with open('./scripts/asset_vulnerability.csv') as file:
        reader = csv.DictReader(file)

        ob = {}
        for row in reader:
            ob['hostname'] = row['ASSET - HOSTNAME']
            ob['ip_address'] = row['ASSET - IP_ADDRESS']
            ob['title'] = row['VULNERABILITY - TITLE']
            ob['severity'] = row['VULNERABILITY - SEVERITY']
            ob['cvss'] = row['VULNERABILITY - CVSS']
            ob['publication_date'] = row['VULNERABILITY - PUBLICATION_DATE']

            if(not ob['cvss']):
                ob.pop('cvss')
            
            if(not ob['publication_date']):
                ob.pop('publication_date')

            report = Vunerabilities(**ob)
            reports_list.append(report)
    
    return reports_list



def run():
    print("registrando usuario...")
    register_user()
    reports = read_file_cvs()

    print("Verificando se existem dados na tabela de vunerabilidades...")
    Vunerabilities.objects.all().delete()

    print("carregado dados do csv...")
    Vunerabilities.objects.bulk_create(reports)

    print("Finalizado")