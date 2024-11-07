import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
    
    def test_rahaa_on_1000e_kun_lounaita_ei_ole_myyty(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)

    # Maukkaat käteisostot

    def test_kassa_kasvaa_maukkaalla_kateisostolla(self):
        self.kassapaate.syo_maukkaasti_kateisella(5423)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004.0)

    def test_kassa_palauttaa_vaihtorahan_maukkaalla_kateisostolla(self):
        maksu = 5423

        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(maksu)

        self.assertEqual(vaihtoraha, maksu - 400.0)

    def test_maukkaiden_maara_kasvaa_oston_jalkeen(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

        self.kassapaate.syo_maukkaasti_kateisella(5423)
        self.kassapaate.syo_maukkaasti_kateisella(432)
        self.kassapaate.syo_maukkaasti_kateisella(400)

        self.assertEqual(self.kassapaate.maukkaat, 3)

    def test_kassan_rahamaara_ei_muutu_jos_maksu_ei_ole_riittava_maukkaaseen(self):
        self.kassapaate.syo_maukkaasti_kateisella(399)
        
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)

    def test_raha_palautetaan_jos_maksu_ei_riita_maukkaaseen_kateisostoon(self):
        palautettu_raha = self.kassapaate.syo_maukkaasti_kateisella(399)

        self.assertEqual(palautettu_raha, 399)

    def test_maukkaiden_myyntien_maara_ei_muutu_jos_raha_ei_riita_ostoon(self):
        maukkaat_myynnit_alussa = self.kassapaate.maukkaat
        self.kassapaate.syo_maukkaasti_kateisella(399)
        
        self.assertEqual(self.kassapaate.maukkaat, maukkaat_myynnit_alussa)

    # Edulliset käteisostot

    def test_kassa_kasvaa_edullisella_kateisostolla(self):
        self.kassapaate.syo_edullisesti_kateisella(12345)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.4)

    def test_kassa_palauttaa_vaihtorahan_edullisella_kateisostolla(self):
        maksu = 12341

        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(maksu)

        self.assertEqual(vaihtoraha, maksu - 240.0)

    def test_edullisten_maara_kasvaa_oston_jalkeen(self):
        self.assertEqual(self.kassapaate.edulliset, 0)

        self.kassapaate.syo_edullisesti_kateisella(5423)
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.kassapaate.syo_edullisesti_kateisella(2400)

        self.assertEqual(self.kassapaate.edulliset, 3)

    def test_kassan_rahamaara_ei_muutu_jos_maksu_ei_ole_riittava_edulliseen(self):
        self.kassapaate.syo_edullisesti_kateisella(239)
        
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)

    def test_raha_palautetaan_jos_maksu_ei_riita_edulliseen_kateisostoon(self):
        palautettu_raha = self.kassapaate.syo_edullisesti_kateisella(238)

        self.assertEqual(palautettu_raha, 238)

    def test_edullisten_myyntien_maara_ei_muutu_jos_raha_ei_riita_ostoon(self):
        edulliset_myynnit_alussa = self.kassapaate.edulliset
        
        self.kassapaate.syo_edullisesti_kateisella(237)
        self.kassapaate.syo_edullisesti_kateisella(-1)
        self.kassapaate.syo_edullisesti_kateisella(199)
        
        self.assertEqual(self.kassapaate.edulliset, edulliset_myynnit_alussa)

    # Korttiostot
    
    def test_maukas_osto_veloittaa_summan_maksukortilta(self):
        maksukortti = Maksukortti(1000)
        vastaus = self.kassapaate.syo_maukkaasti_kortilla(maksukortti)
        self.assertEqual(maksukortti.saldo_euroina(), 6.0)
        self.assertEqual(vastaus, True)

    def test_edullinen_osto_veloittaa_summan_maksukortilta(self):
        maksukortti = Maksukortti(1000)
        vastaus = self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        self.assertEqual(maksukortti.saldo_euroina(), 7.6)
        self.assertEqual(vastaus, True)

    def test_maukas_osto_maksukortilla_kasvattaa_maukkaiden_maaraa_kassapaatteessa(self):
        maksukortti = Maksukortti(1000)
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti)
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 2)

    def test_edullinen_osto_maksukortilla_kasvattaa_edullisten_maaraa_kassapaatteessa(self):
        maksukortti = Maksukortti(1000)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 3)

    def test_jos_raha_ei_riita_maukkaaseen_ostoon_kortin_rahamaara_ei_muutu(self):
        maksukortti = Maksukortti(100)
        vastaus = self.kassapaate.syo_maukkaasti_kortilla(maksukortti)
        
        self.assertEqual(maksukortti.saldo_euroina(), 1.0)
        self.assertEqual(vastaus, False)

    def test_jos_raha_ei_riita_maukkaaseen_ostoon_kassan_maukkaat_ei_muutu(self):
        maksukortti = Maksukortti(100)
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti)
        
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_jos_raha_ei_riita_edulliseen_ostoon_kortin_rahamaara_ei_muutu(self):
        maksukortti = Maksukortti(123)
        vastaus = self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        
        self.assertEqual(maksukortti.saldo_euroina(), 1.23)
        self.assertEqual(vastaus, False)

    def test_jos_raha_ei_riita_edulliseen_ostoon_kassan_maukkaat_ei_muutu(self):
        maksukortti = Maksukortti(99)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_maukas_osto_kortilla_ei_muuta_kassan_rahamaaraa(self):
        maksukortti = Maksukortti(500)
        alkuperainen_rahamaara_kassassa = self.kassapaate.kassassa_rahaa_euroina()
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), alkuperainen_rahamaara_kassassa)

    def test_edullinen_osto_kortilla_ei_muuta_kassan_rahamaaraa(self):
        maksukortti = Maksukortti(500)
        alkuperainen_rahamaara_kassassa = self.kassapaate.kassassa_rahaa_euroina()
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), alkuperainen_rahamaara_kassassa)

    def test_rahaa_ladattaessa_kortin_saldo_muuttuu(self):
        maksukortti = Maksukortti(0)

        self.kassapaate.lataa_rahaa_kortille(maksukortti, 101)

        self.assertEqual(maksukortti.saldo_euroina(), 1.01)

    def test_rahaa_ladattaessa_kassan_rahamaara_muuttuu(self):
        maksukortti = Maksukortti(0)

        kassa_ennen_latausta_euroa = self.kassapaate.kassassa_rahaa_euroina()
        self.kassapaate.lataa_rahaa_kortille(maksukortti, 101)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), kassa_ennen_latausta_euroa + 1.01)

    def test_negatiivinen_lataus_kortille_ei_muuta_kortin_saldoa(self):
        maksukortti = Maksukortti(50)
        self.kassapaate.lataa_rahaa_kortille(maksukortti, -23)
        self.assertEqual(maksukortti.saldo_euroina(), 0.5)