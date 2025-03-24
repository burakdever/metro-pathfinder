
# metro-pathfinder 🚇

Bu proje, bir metro ağında en az aktarmalı ve en hızlı rotayı bulmak için **BFS** ve **A*** algoritmalarını kullanan bir Python uygulamasıdır.  
<br>
## Kullanılan Teknolojiler ve Kütüphaneler  

- **Python**: Ana programlama dili.
- **collections**: `defaultdict`, `deque` veri yapıları için.
- **heapq**: A* algoritması öncelik kuyruğu için.

<br>

## Algoritmaların Çalışma Mantığı  

### 1. En Az Aktarmalı Rota (BFS)  
- **BFS (Genişlik Öncelikli Arama)** algoritması kullanılarak, bir istasyondan diğerine **en az aktarma** ile nasıl gidileceği bulunur.  
- Kuyruk (queue) veri yapısı ile genişlik öncelikli tarama yapılır.

### 2. En Hızlı Rota (A*)  

- **A* algoritması**, en kısa süreli rotayı bulmak için **öncelik kuyruğu** (heapq) kullanır.  
- **G maliyeti** (şu ana kadar kat edilen mesafe) takip edilir ve en hızlı yol hesaplanır.  

<br>

## Örnek Kullanım ve Test Senaryoları  

Python kodu çalıştırıldığında aşağıdaki gibi testler yapılabilir:  

```python
metro.en_az_aktarma_bul("M1", "K4")  # En az aktarma ile en kısa rota
metro.en_hizli_rota_bul("M1", "K4")  # En hızlı rota hesaplama
```

<br>

## Çıktı örneği:

En az aktarmalı rota: AŞTİ -> Kızılay -> Kızılay -> Ulus -> Demetevler -> OSB

En hızlı rota (25 dakika): AŞTİ -> Kızılay -> Kızılay -> Ulus -> Demetevler -> OSB

<br>

## 🚀 Geliştirme Fikirleri

- 🎨 **Grafik Arayüz (GUI) entegrasyonu**  
  Kullanıcı dostu bir arayüz için **Kivy** veya diğer GUI framework'leri ile entegrasyon.

- 🔍 **Farklı Grafik Arama Algoritmaları**  
  Projeye **Dijkstra Algoritması**, **DFS Algoritması** gibi farklı algoritmalar eklenebilir.
