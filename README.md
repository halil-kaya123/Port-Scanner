# Advanced SYN Stealth Port Scanner & Real-Time Logger

Bu proje, bilgisayar ağlarında güvenlik duvarlarını (Firewall) atlatarak açık kapıları tespit etmek amacıyla geliştirilmiş, **Yarım Açık Tarama (SYN Stealth Scan)** mantığıyla çalışan bağımsız bir siber güvenlik ve ağ keşif aracıdır.

---

## Geliştirici Notu ve Projenin Amacı

Ben **14 yaşında bir Bilişim ve Ağ Teknolojileri öğrencisiyim**. Bu aracı, VirtualBox laboratuvarımda Kali Linux ve Windows 11 işletim sistemleri arasında sızma testleri (pentest) yaparken, standart tarayıcıların ağda bıraktığı gürültülü izleri (log) azaltmak ve Firewall cihazlarının çalışma mantığını (Paket Drop/Filtreleme) pratik olarak anlamak için tek bir bağımsız script olarak geliştirdim.

**Dürüstlük Bildirimi:** Kullanıcı arayüzünü, hata yönetimini (`try-except`), sonsuz menü döngüsünü ve tüm portları (65.536 adet) tarama mantığını tamamen kendi zihnimle kodladım. Ancak standart `socket` kütüphanesinin yetersiz kaldığı donanım katmanında, ham TCP paketlerini manipüle etmek için **Scapy** kütüphanesinin entegrasyonu ve SYN bayrak yapısı (`flags="S"`) konusunda yapay zekadan bir **mühendislik asistanı** gibi teknik destek aldım.

---

## Teknik Özellikler & Siber Güvenlik Anatomisi

*   **SYN Stealth Scan (Yarım Açık Tarama):** Standart 3 adımlı el sıkışmayı (Three-Way Handshake) tamamlamaz. Hedef porttan `SYN-ACK` (Onay) sinyali geldiği an portun **AÇIK** olduğunu anlar ve el sıkışmayı bitirmeden hemen bir `RST` (Reset) paketi fırlatarak kaçar. Bu sayede hedef sistemdeki Firewall loglarında yakalanmamayı hedefler.
*   **Anlık Loglama (Real-Time Logging):** Powershell veya terminal pencerelerinin satır sınırı (buffer limit) sorununu aşmak ve veri kaybını önlemek için tarama sonuçları **anlık olarak** saliseler içinde diskteki `[Hedef_IP]_rapor.txt` dosyasına yazılır. Tarama CTRL+C ile yarıda kesilse bile o ana kadar bulunan tüm veriler korunur.
*   **Firewall Teşhisi (Filtrelendi):** Eğer hedef porttan belirlenen süre boyunca hiçbir cevap gelmezse (Sessiz drop durumu), sistemin kapalı olduğunu varsaymaz; orada aktif bir **Güvenlik Duvarı (Firewall)** olduğunu tespit eder.
*   **Full Range Scanning:** 0 ile 65535 arasındaki tüm olası portları (65.536 adet) tarayabilecek tam kapsama alanına sahiptir.

---

## Dosya Konumu

Çalışma alanında bağımsız bir siber güvenlik aracı olarak konumlandırılmıştır:
```text
└── Eğitim/
    ├── port_tarayıcı.py            # Tarayıcının ana kaynak kodu
    └── [Hedef_IP]_rapor.txt        # Tarama sonrası anlık üretilen rapor dosyası
```

---

## Çalıştırma Talimatı

Scapy kütüphanesi doğrudan bilgisayarın ağ kartına (donanıma) paket enjekte ettiği için bu aracın **Yönetici (Administrator)** yetkileriyle çalıştırılması şarttır.

1. Gerekli kütüphaneyi yükleyin:
   ```bash
   pip install scapy
   ```
2. Terminalinizi veya VS Code'u **Yönetici Olarak Çalıştırın** ve aracı başlatın:
   ```bash
   python port_tarayıcı.py
   ```

---

## ⚠️ Yasal Uyarı (Legal Disclaimer)

Bu araç tamamen eğitim, akademik araştırma ve yerel siber güvenlik laboratuvarı testleri amacıyla geliştirilmiştir. Bu kodun, yasal izin belgesi olmayan harici ve yetkisiz sistemler üzerinde çalıştırılmasından doğacak tüm hukuki sorumluluk tamamen kullanıcıya aittir. Geliştirici hiçbir sorumluluk kabul etmez.
