import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_on_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_rahan_lataaminen_kasvattaa_saldoa(self):
        self.maksukortti.lataa_rahaa(1234)
        
        self.assertEqual(self.maksukortti.saldo_euroina(), 22.34)

    def test_saldo_vahenee_jos_rahaa_on_tarpeeksi_ottoon(self):
        self.maksukortti.ota_rahaa(525)
        self.assertEqual(self.maksukortti.saldo_euroina(), 4.75)

    def test_saldo_ei_muutu_jos_rahaa_ei_ole_tarpeeksi_ottoon(self):
        self.maksukortti.ota_rahaa(1002)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_ota_rahaa_metodi_palauttaa_true_jos_rahat_riittivat(self):
        vastaus = self.maksukortti.ota_rahaa(777)
        self.assertEqual(vastaus, True)

    def test_ota_rahaa_metodi_palauttaa_false_jos_rahat_ei_riitä(self):
        vastaus = self.maksukortti.ota_rahaa(2123)
        self.assertEqual(vastaus, False)

    def test_kortin_merkkijonomuoto_on_oikein(self):
        oletettu = "Kortilla on rahaa 10.00 euroa"
        self.assertEqual(str(self.maksukortti), oletettu)
