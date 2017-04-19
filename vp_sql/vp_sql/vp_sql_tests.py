#!/usr/bin/env python3

import os
import requests
import unittest


class Vp_SqlTestCase(unittest.TestCase):

    def setUp(self):
        self.url = "http://localhost:8080"
        self.user = "sa"
        self.password = "sqlservp4sSw0rd"
        self.dbname = "TestVP"
        self.server = "localhost"
        self.headers = {'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXJ2ZXIiOiJsb2NhbGhvc3QiLCJwYXNzd29yZCI6InNxbHNlcnZwNHNTdzByZCIsImRibmFtZSI6IlRlc3RWUCIsInVzZXIiOiJzYSJ9.E-r4hl8eY2-glLNBK6YdTwG3sKU996wSyn7mqLnFs6A"}


    def test_connection(self):
        r = requests.post(self.url + "/change_credz", headers=self.headers, data={'user': self.user, 'password': self.password, 'dbname': self.dbname, 'server': self.server})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['success'], True)


    def test_table(self):
        r = requests.get(self.url + "/Rois_de_France", headers=self.headers)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 4)


    def test_where(self):
        r = requests.get(self.url + "/Rois_de_France?select=Id&Nom=Charlemagne", headers=self.headers)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)
        self.assertEqual(r.json()[0]['Id'], 2)


    def test_limit(self):
        r = requests.get(self.url + "/Rois_de_France?select=Nom&limit=3", headers=self.headers)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 3)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Vp_SqlTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
