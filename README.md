# Advanced NetScanner & SYN Stealth Port Scanner Suite

Bu proje; yerel ağ haritalandırma, cihaz üreticisi analizi (Vendor Lookup), hedef işletim sistemi tahmini (OS Fingerprinting) ve güvenlik duvarlarını (Firewall) atlatarak açık kapıları tespit eden **Yarım Açık Tarama (SYN Stealth Scan)** özelliklerini tek bir çatıda birleştiren bağımsız bir siber güvenlik ve ağ keşif framework'üdür.

---

## Geliştirici Notu ve Projenin Amacı

Ben **14 yaşında bir Bilişim ve Ağ Teknolojileri öğrencisiyim**. Bu aracı, VirtualBox laboratuvarımda Kali Linux, Windows 11 ve siber güvenlik zafiyetli makineler (Metasploitable vb.) arasında sızma testleri (pentest) yaparken, standart tarayıcıların ağda bıraktığı gürültülü izleri (log) azaltmak, Firewall cihazlarının çalışma mantığını (Paket Drop/Filtreleme) ve ağ protokollerini pratik olarak anlamak için bağımsız bir script olarak geliştirdim.

**Dürüstlük Bildirimi:** Kullanıcı arayüzünü, hata yönetimini (`try-except`), sonsuz menü döngülerini, yerel ağ tarama mantığını, raporlama optimizasyonunu ve tüm portları (65.536 adet) tarama algoritmasını tamamen kendi zihnimle kodladım. Ancak standart `socket` kütüphanesinin yetersiz kaldığı donanım katmanında, ham TCP/ARP paketlerini manipüle etmek için **Scapy** kütüphanesinin entegrasyonu, bit maskeleme mimarisi ve harici API entegrasyonları konusunda yapay zekadan bir **mühendislik asistanı** gibi teknik destek aldım.

---

## Teknik Özellikler & Siber Güvenlik Anatomisi

### 1. Keşif Modülü (Yerel Ağ Tarayıcı)
*   **Asenkron ARP Sweep:** Belirlenen ağ bloğuna (Örn: `/24`) anlık asenkron ARP anonsları fırlatarak ağdaki tüm canlı cihazları, MAC adreslerini ve Hostname (Cihaz adı) bilgilerini 3 saniye gibi kısa bir sürede haritalandırır.
*   **Dinamik Vendor Lookup:** Bulunan cihazların MAC adreslerini anlık olarak ücretsiz MacVendors API'si üzerinden sorgulayarak cihazların fiziksel markalarını (Apple, Samsung, Intel, Huawei vb.) tespit eder.

### 2. Tarama Modülü (SYN Stealth Scan)
*   **Yarım Açık Tarama:** Standart 3 adımlı TCP el sıkışmasını (Three-Way Handshake) tamamlamaz. Hedef porttan `SYN-ACK` sinyali geldiği an portun **AÇIK** olduğunu anlar ve el sıkışmayı bitirmeden hemen bir `RST` (Reset) paketi fırlatarak kaçar. Bu sayede hedef sistemde uygulama seviyesinde log bırakmaz.
*   **Dinamik Gizlilik ve Hız Kademeleri:** 
    *   *Agresif Mod:* 0.1s timeout ile jet hızında tarama yapar.
    *   *Dengeli Mod:* Portları karıştırır, araya 0.5-2s rastgele gecikmeler koyar.
    *   *Sinsi Mod:* Portları tamamen çorba yapar (`shuffle`), araya 5-10s geniş ve ritmik olmayan rastgele gecikmeler koyarak modern Saldırı Tespit Sistemlerinin (IDS/IPS) ve Akıllı Firewall'ların `Rate Limiting` (Hız Sınırı) kurallarını bypass eder.
*   **Bit Maskeleme Teknolojisi:** Karşıdan dönen TCP bayraklarını string (metin) olarak değil, doğrudan işlemci seviyesinde çalışan **Bitwise AND (`bayraklar & 0x12`)** maskelemesiyle analiz eder. Bu sayede hatalı pozitif (false-positive) sonuçları sıfıra indirir.
*   **Döngü Dışı OS Fingerprinting:** Tarama başında hedefe tek bir SYN paketi atarak dönen **TTL (Time to Live)** değerini analiz eder. Port döngüsünü kirletmeden, hedefin Windows, Linux/macOS veya Cisco bir cihaz olduğunu en başta tek seferde tahmin eder.

### 3. Akıllı Raporlama & Kararlılık
*   **Gelişmiş I/O Optimizasyonu:** Rapor dosyasının şişmesini engellemek için ana başlıkları tarama başında tek sefer yazar, döngü içinde sadece port bulgularını alt alta ekler.
*   **Zaman Analizi:** Tarama bittiğinde projenin ne kadar sürdüğünü `00:02:15` (Saat:Dakika:Saniye) formatında profesyonelce raporun altına basar.
*   **Kurşun Geçirmezlik:** İçindeki yoğun istisna yönetimleri sayesinde ağ anlık olarak kopsa veya Scapy sistemsel thread hataları fırlatsa bile program kilitlenmez, akışı sürdürür.

---

## Dosya Yapısı

```text
└── Eğitim/
    ├── siber_panel.py              # Tüm sistemin birleşik ana kaynak kodu
    └── [Hedef_IP]_rapor.txt        # Masaüstünde anlık üretilen detaylı rapor dosyası
```

---

## Kurulum ve Çalıştırma Talimatı

Aracın ham ağ paketleri enjekte edebilmesi için bilgisayarınızın ağ kartına doğrudan erişmesi, yani **Yönetici (Administrator / Sudo)** yetkileriyle çalıştırılması şarttır.

### 1. Gerekli Kütüphanelerin Yüklenmesi
Terminal veya komut satırını açarak Scapy kütüphanesini yükleyin:
```bash
pip install scapy
```

### 2. İşletim Sistemine Göre Ön Gereksinimler

*   **Windows Kullanıcıları İçin:** Scapy'nin ham paket fırlatabilmesi için Windows arka planında bir paket yakalama motoruna ihtiyacı vardır. Eğer bilgisayarınızda yüklü değilse, ücretsiz ve güvenli olan **Npcap** yazılımını [buraya tıklayarak npcap.com üzerinden](https://npcap.com) indirip kurmanız gerekmektedir (Kurulum sırasında "Install Npcap in WinPcap API-compatible Mode" seçeneğinin işaretli olduğundan emin olun).
*   **Linux / Kali Linux Kullanıcıları İçin:** Ek bir yazılıma gerek yoktur, direkt terminalden çalıştırılabilir.

### 3. Aracın Başlatılması

*   **Windows:** PowerShell veya Komut İstemi'ni (CMD) **Yönetici Olarak Çalıştır** seçeneğiyle açın ve kodun olduğu dizine giderek başlatın:
    ```cmd
    python siber_panel.py
    ```
*   **Linux / macOS:** Terminali açın ve `sudo` yetkisiyle aracı tetikleyin:
    ```bash
    sudo python3 siber_panel.py
    ```

---

## Nasıl Kullanılır? (Kullanım Senaryoları)

1.  **Ağ Keşif Senaryosu:** Program başladığında size `Ağ taraması yapılsın mı? (e/h)` diye soracaktır. `e` diyerek kendi yerel ağ bloğunuzu (Örn: `192.168.1.0/24`) girip ağdaki tüm aktif cihazların IP, MAC, Cihaz Adı ve Üretici Marka (Apple, Samsung vb.) listesini görebilirsiniz. Çıkmak için `-1` yazmanız yeterlidir.
2.  **Hedef Odaklı Saldırı/Tarama Senaryosu:** Ağ tarayıcıdan çıktıktan sonra sizden hedef bir IP adresi istenecektir. Buraya sızma testi yapmak istediğiniz hedef makinenin IP'sini yazın.
3.  **Port ve Gizlilik Seçimi:** Karşınıza çıkan menüden taramak istediğiniz port aralığını seçin (Örn: En popüler 100 port). Ardından sızma operasyonunun gizliliğine göre `1`, `2` veya `3` modlarından birini seçerek taramayı başlatın.
4.  **Rapor İnceleme:** Tarama bittiğinde veya siz `CTRL+C` ile yarıda kestiğinizde, o ana kadar elde edilen tüm bulgular, işletim sistemi tahmini ve süre analiziyle birlikte **Masaüstünüzde** `{Hedef_IP}_rapor.txt` adıyla birikecektir.

---

> [!WARNING]
> **Yasal Uyarı (Legal Disclaimer)**
> Bu araç tamamen eğitim, akademik araştırma ve yerel siber güvenlik laboratuvarı testleri amacıyla geliştirilmiştir. Bu kodun, yasal izin belgesi veya yazılı sızma testi sözleşmesi olmayan harici ve yetkisiz sistemler üzerinde çalıştırılmasından doğacak tüm hukuki sorumluluk tamamen kullanıcıya aittir. Geliştirici hiçbir yasadışı faaliyetten ötürü sorumluluk kabul etmez.
