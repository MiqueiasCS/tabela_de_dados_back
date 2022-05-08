from django.test import TestCase
from datetime import date
from reports.models import Vunerabilities

class VunerabiliteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hostname = "WORKSTATION-3"
        cls.ip_address =  "172.18.0.1"
        cls.title = "VMSA-2019-0020 : Hypervisor-Specific Mitigations for Denial-of-Service and Speculative-Execution Vulnerabilities"
        cls.severity = "Alto"
        cls.cvss = 7.8
        cls.publication_date = date.fromisoformat("2018-07-19")

        cls.vunerability = Vunerabilities.objects.create(
            hostname = cls.hostname,
            ip_address = cls.ip_address,
            title = cls.title,
            severity = cls.severity,
            cvss = cls.cvss,
            publication_date = cls.publication_date
        )
     

    def test_vunerab_has_information_fields(self):
        self.assertIsInstance(self.vunerability.ip_address,str)
        self.assertEqual(self.vunerability.ip_address,self.ip_address)

        self.assertIsInstance(self.vunerability.hostname,str)
        self.assertEqual(self.vunerability.hostname,self.hostname)

        self.assertIsInstance(self.vunerability.title,str)
        self.assertEqual(self.vunerability.title,self.title)

        self.assertIsInstance(self.vunerability.severity,str)
        self.assertEqual(self.vunerability.severity,self.severity)

        self.assertIsInstance(self.vunerability.cvss,float)
        self.assertEqual(self.vunerability.cvss,self.cvss)

        self.assertIsInstance(self.vunerability.publication_date,date)
        self.assertEqual(self.vunerability.publication_date,self.publication_date)