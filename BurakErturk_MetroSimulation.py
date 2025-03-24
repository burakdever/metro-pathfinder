from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:

    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları


    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))


class MetroAgi:

    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)


    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)


    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

# ==============================================================================================

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """
        BFS (Genişlik Öncelikli Arama) algoritmasını kullanarak,
        iki istasyon arasındaki en az aktarmalı (minimum transfer) rotayı bulur.

        Parametreler:
          - baslangic_id: Başlangıç istasyonunun id'si
          - hedef_id: Hedef istasyonunun id'si

        Dönen Değer:
          - Eğer bir rota bulunamazsa None
          - Rota bulunursa, rota üzerindeki istasyonların listesini döndürür
        """

        # Baslangic veya hedef istasyonlari agda yoksa, None dondur
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        # Baslangıc ve hedef istasyon nesnelerini al
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        # Ziyaret edilen istasyonlari tutmak icin set kullan
        ziyaret_edildi = set()

        # BFS icin kuyruk olustur. Her eleman (mevcut istasyon, o ana kadar olusturulan rota, mevcut hat) şeklindedir.
        kuyruk = deque([(baslangic, [baslangic], baslangic.hat)])

        # BFS algoritmasi: Kuyruk bosalana kadar her adimda kuyrugun basindaki istasyonu al
        while kuyruk:

            mevcut_istasyon, yol, mevcut_hat = kuyruk.popleft()
            ziyaret_edildi.add(mevcut_istasyon)

            # Hedef istasyona ulasildiysa, o ana kadar izlenen rotayi dondur
            if mevcut_istasyon is hedef:
                return yol

            # Mevcut istasyonun komsu istasyonlarini gez
            for komsu, komsu_sure in mevcut_istasyon.komsular:
                if komsu not in ziyaret_edildi:
                    yeni_hat = komsu.hat

                    # Ayni hat uzerinde ilerleyen istasyonlari öncelikli olarak kuyrugun basina ekle
                    if yeni_hat == mevcut_hat:
                        kuyruk.appendleft((komsu, yol + [komsu], mevcut_hat))

                    else:
                        # Hat degisikligi (aktarma) olanlari kuyrugun sonuna ekle
                        kuyruk.append((komsu, yol + [komsu], yeni_hat))

        # Rota bulunamazsa None dondur
        return None

# ==============================================================================================

# ==============================================================================================

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritması kullanarak en hızlı rotayı bulur

        Parametreler:
          - baslangic_id: Başlangıç istasyonunun id'si
          - hedef_id: Hedef istasyonunun id'si

        Dönen Değer:
          - Eğer rota bulunamazsa None
          - Bulunursa, (istasyon_listesi, toplam_sure) tuple'ı
        """
        # Baslangıc ve hedef istasyonlarin varligini kontrol et
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        # Ziyaret edilmis istasyonlari ve maliyet bilgilerini takip et
        ziyaret_edildi = set()
        g_maliyetler = {baslangic: 0}
        path = {}  # Rotayi yeniden insa etmek icin ebeveyn istasyonlari izle

        # Oncelik kuyrugu
        pq = [(0, id(baslangic), baslangic)]

        while pq:
            # En düşük f_maliyete sahip istasyonu sec
            f_maliyet, _, mevcut_istasyon = heapq.heappop(pq)

            # Zaten ziyaret edildiyse atla
            if mevcut_istasyon in ziyaret_edildi:
                continue

            # Hedef istasyona ulasildıysa rotayi olustur
            if mevcut_istasyon is hedef:
                # Rotayi ebeveynler dict'i kullanarak yeniden insa et
                rota = []
                while mevcut_istasyon:
                    rota.insert(0, mevcut_istasyon)
                    mevcut_istasyon = path.get(mevcut_istasyon)

                # Toplam sureyi hesapla
                toplam_sure = g_maliyetler[hedef]
                return (rota, toplam_sure)

            # Mevcut istasyonu ziyaret edildi olarak isaretle
            ziyaret_edildi.add(mevcut_istasyon)

            # Komsu istasyonlari kesfet
            for komsu, komsu_sure in mevcut_istasyon.komsular:
                if komsu in ziyaret_edildi:
                    continue

                # Mevcut yolun maliyetini hesapla
                g_maliyet = g_maliyetler.get(mevcut_istasyon, 0) + komsu_sure

                # Daha iyi bir yol bulunduysa guncelle
                if komsu not in g_maliyetler or g_maliyet < g_maliyetler[komsu]:
                    g_maliyetler[komsu] = g_maliyet

                    # f(n) = g(n) + h(n)
                    f_maliyet = g_maliyet + 0

                    # Ebeveyn bilgisini kaydet
                    path[komsu] = mevcut_istasyon

                    # Öncelik kuyruğuna ekle
                    heapq.heappush(pq, (f_maliyet, id(komsu), komsu))

        # Rota bulunamazsa None dondur
        return None
# ==============================================================================================

# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")  # Aktarma noktası
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")  # Aktarma noktası
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")  # Aktarma noktası
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))