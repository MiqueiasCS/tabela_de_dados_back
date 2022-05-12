from rest_framework.test import APITestCase
from datetime import date
from reports.models import Vunerabilities
from accounts.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from reports.serializers import ReportSerializer
import ipdb

class VunerabilitiesRoutesTest(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(email='user@mail.com', password='123456')
        cls.token = Token.objects.create(user=cls.user)

        cls.vunerabilities = [
            Vunerabilities.objects.create(
                hostname = "WORKSTATION-3",
                ip_address =  "172.18.0.1",
                title = "VMSA-2019-0020 : Hypervisor-Specific Mitigations for Denial-of-Service and Speculative-Execution Vulnerabilities",
                severity = "Alto",
                cvss = 7.8,
                publication_date = date.fromisoformat("2018-07-19"),
                fixed = True
                ),
            Vunerabilities.objects.create(
                hostname = "SERVER-4",
                ip_address =  "172.20.0.4",
                title = "SSL Certificate Signed Using Weak Hashing Algorithm",
                severity = "Crítico",
                cvss = 9.5,
                publication_date = date.fromisoformat("2014-07-20"),
                fixed = False
                ),
            Vunerabilities.objects.create(
                hostname = "SERVER-3",
                ip_address =  "172.20.0.1",
                title = "SSL Certificate Signed Using Weak Hashing Algorithm",
                severity = "Crítico",
                cvss = 9.0,
                publication_date = date.fromisoformat("2016-07-20"),
                fixed = True
                ),
            Vunerabilities.objects.create(
                hostname = "SERVER-2",
                ip_address =  "172.20.0.2",
                title = "SSL Certificate Signed Using Weak Hashing Algorithm",
                severity = "Baixo",
                cvss = 3.0,
                publication_date = date.fromisoformat("2016-07-20"),
                fixed = False
                ),
                  Vunerabilities.objects.create(
                hostname = "SERVER-2",
                ip_address =  "172.20.0.2",
                title = "SSL Certificate Signed Using Weak Hashing Algorithm",
                severity = "Alto",
                cvss = 6.0,
                publication_date = date.fromisoformat("2016-07-20"),
                fixed = False
                )
        ]

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


    def test_can_list_all_vunerabilities(self):
            response = self.client.get("/api/reports/")

            self.assertEquals(status.HTTP_200_OK, response.status_code)
            self.assertEquals(len(self.vunerabilities),len(response.data["itens"]))

            for vunerability in self.vunerabilities:
                self.assertIn(ReportSerializer(instance=vunerability).data,response.data["itens"])


    def test_can_retrieve_a_specifc_vunerability(self):
        response = self.client.get(f"/api/reports/{self.vunerabilities[0].id}/")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(ReportSerializer(instance=self.vunerabilities[0]).data,response.data)


    def test_cannot_retrieve_a_specifc_vunerability_with_invalid_id(self):
        response = self.client.get(f"/api/reports/30/")

        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)


    def test_can_filter_by_severity(self):
        response = self.client.get(f"/api/reports/?severity=critico")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(2,len(response.data["itens"]))
        self.assertIn(ReportSerializer(instance=self.vunerabilities[2]).data,response.data["itens"])


    def test_can_filter_by_fixed(self):
        response = self.client.get(f"/api/reports/?fixed=corrigida")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(2,len(response.data["itens"]))
        self.assertIn(ReportSerializer(instance=self.vunerabilities[0]).data,response.data["itens"])


    def test_can_filter_by_severity_and_fixed(self):
        response = self.client.get(f"/api/reports/?severity=critico&fixed=corrigida")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(1,len(response.data["itens"]))
        self.assertIn(ReportSerializer(instance=self.vunerabilities[2]).data,response.data["itens"])


    def test_can_filter_by_hostname(self):
        response = self.client.get(f"/api/reports/?name=server-4")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        
        self.assertEquals(ReportSerializer(instance=self.vunerabilities[1]).data['hostname'],response.data["itens"][0]['hostname'])


    def test_return_empty_list_filter_by_invalid_hostname(self):
        response = self.client.get(f"/api/reports/?name=aaassdasd")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(0,len(response.data["itens"]))

    
    def test_can_sort_by_date(self):
        response = self.client.get(f"/api/reports/?date=desc")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.vunerabilities),len(response.data["itens"]))
        self.assertEquals(ReportSerializer(instance=self.vunerabilities[4]).data,response.data["itens"][3])
    

    def test_can_sort_by_cvss(self):
        response = self.client.get(f"/api/reports/?cvss=asc&date=desc")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.vunerabilities),len(response.data["itens"]))
        
        self.assertEquals(ReportSerializer(instance=self.vunerabilities[3]).data,response.data["itens"][0])


    def test_can_update_fixed_to_false(self):
        response = self.client.patch(f"/api/reports/{self.vunerabilities[0].id}/",{"fixed":False})

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertNotEquals(self.vunerabilities[0].fixed,response.data["fixed"])
        self.assertEquals(False,response.data["fixed"])


    def test_can_update_fixed_to_true(self):
        response = self.client.patch(f"/api/reports/{self.vunerabilities[1].id}/",{"fixed":True})

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertNotEquals(self.vunerabilities[1].fixed,response.data["fixed"])
        self.assertEquals(True,response.data["fixed"])


    def test_cannot_update_fixed_erro_404(self):
        response = self.client.patch(f"/api/reports/10/",{"fixed":True})
        
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)


    def test_cannot_update_fixed_erro_400(self):
        response = self.client.patch(f"/api/reports/{self.vunerabilities[1].id}/",{"fixed":"2016-07-20"})

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)


    def test_retrive_by_name_return_list(self):
        response = self.client.get(f"/api/reports/server-3/")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(1, len(response.data["itens"]))

    def test_retrive_by_name_route_name_not_found_return_empty_list(self):
        response = self.client.get(f"/api/reports/xxxxxxxxxxxx/")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(0, len(response.data["itens"]))