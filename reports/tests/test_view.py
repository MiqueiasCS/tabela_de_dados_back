from rest_framework.test import APITestCase
from datetime import date
from reports.models import Vunerabilities
from rest_framework import status
from reports.serializers import ReportSerializer
import ipdb

class VunerabilitiesRoutesTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
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
                )
        ]


    def test_can_list_all_vunerabilities(self):
            response = self.client.get("/api/reports/")

            self.assertEquals(status.HTTP_200_OK, response.status_code)
            self.assertEquals(len(self.vunerabilities),len(response.data))

            for vunerability in self.vunerabilities:
                self.assertIn(ReportSerializer(instance=vunerability).data,response.data)


    def test_can_retrieve_a_specifc_vunerability(self):
        response = self.client.get(f"/api/reports/{self.vunerabilities[0].id}/")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(ReportSerializer(instance=self.vunerabilities[0]).data,response.data)


    def test_cannot_retrieve_a_specifc_vunerability_with_invalid_id(self):
        response = self.client.get(f"/api/reports/30/")

        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)


    def test_can_apply_severity_filter(self):
        response = self.client.get(f"/api/reports/?severity=critico")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(2,len(response.data))
        self.assertIn(ReportSerializer(instance=self.vunerabilities[2]).data,response.data)


    def test_can_apply_fixed_filter(self):
        response = self.client.get(f"/api/reports/?fixed=corrigida")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(2,len(response.data))
        self.assertIn(ReportSerializer(instance=self.vunerabilities[0]).data,response.data)


    def test_can_apply_severity_filter_and_fixed_filter(self):
        response = self.client.get(f"/api/reports/?severity=critico&fixed=corrigida")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(1,len(response.data))
        self.assertIn(ReportSerializer(instance=self.vunerabilities[2]).data,response.data)

    
    def test_can_sort_by_date(self):
        response = self.client.get(f"/api/reports/?date=desc")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.vunerabilities),len(response.data))
        self.assertEquals(ReportSerializer(instance=self.vunerabilities[0]).data,response.data[0])
    

    def test_can_sort_by_cvss(self):
        response = self.client.get(f"/api/reports/?cvss=asc&date=desc")

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.vunerabilities),len(response.data))

        self.assertEquals(ReportSerializer(instance=self.vunerabilities[3]).data,response.data[1])


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