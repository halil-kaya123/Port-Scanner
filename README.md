# Advanced NetScanner & SYN Port Scanner Suite

Bu proje; yerel ağ keşfi, TCP SYN port taraması, temel servis tanımlama, işletim sistemi tahmini ve anlaşılabilir TXT raporlamayı tek bir Python aracında birleştiren eğitim amaçlı bir ağ güvenliği ve keşif aracıdır.

> **Proje durumu:** Erken geliştirme aşamasında  
> **Geliştirici:** 14 yaşında Bilişim ve Ağ Teknolojileri öğrencisi  
> **Ana teknoloji:** Python + Scapy

---

## Geliştirici Notu ve Projenin Amacı

Ben **14 yaşında bir Bilişim ve Ağ Teknolojileri öğrencisiyim**.

Bu projeyi ağ protokollerini, TCP/IP yapısını, port taramasını, ARP keşfini, firewall davranışlarını ve temel siber güvenlik kavramlarını pratik olarak öğrenmek amacıyla geliştirmeye başladım.

Proje başlangıçta yaklaşık 70 satırlık basit bir SYN port tarayıcısıydı. Zaman içerisinde ağ keşfi, IP doğrulama, servis tespiti, TTL tabanlı işletim sistemi tahmini, banner alma, güvenlik tavsiyeleri, raporlama ve hata yönetimi gibi özellikler eklenmiştir.

Bazı teknik konularda yapay zekâdan bir mühendislik asistanı olarak destek alınmıştır. Özellikle Scapy kullanımı, ham paket işlemleri, hata yönetimi ve bazı Python uygulama ayrıntılarında AI desteğinden yararlanılmıştır.

Bu proje **Nmap'in alternatifi veya rakibi olarak tasarlanmamıştır**. Amacım, zaman içerisinde geliştirerek kullanıcıların ve siber güvenlik alanındaki kişilerin faydalı bulabileceği, sonuçları kolay anlaşılır şekilde sunan bir araç oluşturmaktır.

---

# Teknik Özellikler

## 1. Yerel Ağ Keşfi

ARP tabanlı ağ keşfi ile aynı yerel ağ üzerindeki cevap veren cihazlar tespit edilebilir.

Gösterilen bilgiler:

- IP adresi
- MAC adresi
- Hostname / cihaz adı

Örnek:

```text
IP ADRESİ         MAC ADRESİ          CİHAZ ADI
-------------------------------------------------------------
192.168.1.1       XX:XX:XX:XX:XX:XX   router
192.168.1.10      XX:XX:XX:XX:XX:XX   bilgisayar
192.168.1.20      XX:XX:XX:XX:XX:XX   Bilinmeyen cihaz
```

> ARP keşfi yerel ağ segmentleri için tasarlanmıştır.

---

## 2. TCP SYN Port Taraması

Araç TCP SYN paketleri göndererek hedef TCP portlarının durumunu belirlemeye çalışır.

Temel sonuçlar:

- `OPEN`
- `CLOSED`
- `NO_RESP / POSS_FILTERED`

SYN-ACK yanıtı alınması portun açık olduğunu gösterir.

RST veya RST-ACK yanıtı portun kapalı olduğunu gösterir.

Herhangi bir yanıt alınamaması ise portun kesin olarak filtrelendiği anlamına gelmez. Firewall, paket kaybı, ağ yapılandırması veya hedef sistemin davranışı gibi farklı sebepler olabilir.

---

## 3. Port Tarama Seçenekleri

Kullanıcı farklı tarama yöntemlerinden birini seçebilir:

```text
1 - İki port arasındaki aralık
2 - Belirli portlar
3 - Popüler port listesi
4 - 1-65535 arasındaki TCP portları
```

Port numaraları `1-65535` aralığında doğrulanır.

---

## 4. Tarama Hızı

Üç farklı tarama profili bulunmaktadır.

### Yüksek Trafik Ayarı

Daha kısa timeout değerleri kullanır.

Avantaj:

- Daha hızlı tarama

Dezavantaj:

- Daha fazla ağ trafiği oluşturabilir.
- Hedef sistem tarafından daha kolay fark edilebilir.

### Dengeli Ayar

Hız ve trafik miktarı arasında denge sağlamayı amaçlar.

Port sırası karıştırılabilir ve portlar arasında rastgele gecikmeler uygulanabilir.

### Düşük Trafik Ayarı

Daha uzun gecikmeler kullanarak taramayı daha yavaş gerçekleştirir.

Amaç:

- Trafik yoğunluğunu azaltmak
- Daha kontrollü tarama yapmak

> Bu mod herhangi bir IDS, IPS veya firewall sistemini kesin olarak aşmayı garanti etmez.

---

## 5. Servis Tanımlama

Açık veya cevap veren portlar için standart servis tablosundan muhtemel servis adı alınmaya çalışılır.

Örneğin:

```text
135  -> EPMAP
139  -> NETBIOS-SSN
443  -> HTTPS
445  -> MICROSOFT-DS
3306 -> MYSQL
3389 -> MS-WBT-SERVER
```

Bu bilgiler kesin servis tespiti değildir. Port numarasına göre yapılan bir tahmindir.

---

## 6. Banner Okuma

Açık TCP portlarına bağlantı kurulup başlangıç verisi okunmaya çalışılır.

Servis bir banner gönderirse rapora eklenir.

Örneğin:

```text
Apache/2.4.x
OpenSSH_9.x
Microsoft-IIS/10.0
```

Ancak birçok servis bağlantı kurulduğunda doğrudan banner göndermediği için:

```text
TCP bağlantısı başarılı; banner alınamadı
```

gibi bir sonuç alınması normaldir.

---

## 7. Temel İşletim Sistemi Tahmini

Tarama başlangıcında alınan IP paketindeki TTL değeri analiz edilerek işletim sistemi hakkında temel bir tahmin yapılır.

Örneğin:

```text
Tahmini İşletim Sistemi = Windows
```

veya:

```text
Tahmini İşletim Sistemi = Linux / Android / macOS
```

> TTL analizi kesin işletim sistemi tespiti değildir. NAT, proxy, ağ cihazları, özel yapılandırmalar veya değiştirilmiş TTL değerleri sonucu etkileyebilir.

---

# Güvenlik Referansları

Araç, tespit edilen bazı servisler için kısa ve anlaşılır güvenlik notları gösterebilir.

Örneğin:

```text
445/TCP OPEN

Windows SMB servisi aktif.
Güncel güvenlik yamalarının doğrulanması önerilir.
```

Bu bilgiler doğrudan güvenlik açığı tespiti anlamına gelmez.

Örneğin bir portun:

```text
445/TCP OPEN
```

olması yalnızca ilgili TCP servisinin erişilebilir olduğunu gösterir.

Gerçek bir güvenlik değerlendirmesi için servis sürümü, yapılandırma, erişim kontrolleri ve ilgili güvenlik kontrollerinin ayrıca incelenmesi gerekir.

---

# Raporlama

Tarama sonuçları kullanıcıların kolay okuyabileceği `.txt` formatında raporlanır.

Örnek:

```text
PERSONAL NETWORK SECURITY SCANNER REPORT

Hedef IP Adresi          = 192.168.1.140
Tahmini İşletim Sistemi  = Windows
Tarama Modu              = Mod 1

PORT      DURUM                    MUHTEMEL SERVİS
------------------------------------------------------------
135       OPEN                     EPMAP
139       OPEN                     NETBIOS-SSN
445       OPEN                     MICROSOFT-DS
```

Raporda ayrıca:

- Hedef IP
- Tahmini işletim sistemi
- Tarama modu
- Açık portlar
- Port durumları
- Muhtemel servisler
- Banner bilgileri
- Güvenlik tavsiyeleri
- Tarama süresi

gibi bilgiler bulunabilir.

---

# Dosya Yapısı

Mevcut sürümde proje basit ve tek dosyalı bir yapıya sahiptir:

```text
Eğitim/
│
├── siber_panel.py
│
└── [Hedef_IP]_rapor.txt
```

Proje büyüdükçe modüler yapıya geçirilmesi planlanmaktadır.

Örneğin gelecekte:

```text
project/
│
├── main.py
│
├── scanner/
│   ├── syn_scanner.py
│   ├── arp_scanner.py
│   └── service_detection.py
│
├── detection/
│   └── os_detection.py
│
├── reporting/
│   └── txt_report.py
│
├── database/
│   └── risk_database.py
│
└── utils/
    └── validators.py
```

şeklinde daha düzenli bir mimariye geçilebilir.

---

# Kurulum

## Gereksinimler

- Python 3.x
- Scapy

Scapy kurulumu:

```bash
pip install scapy
```

---

# Windows

Windows üzerinde Scapy'nin ham paket işlemleri için Npcap gerekebilir.

Npcap:

https://npcap.com/

Npcap kurulduktan sonra PowerShell veya CMD'yi yönetici olarak açarak:

```bash
python siber_panel.py
```

komutuyla program çalıştırılabilir.

---

# Linux / Kali Linux

Gerekli izinlerle:

```bash
sudo python3 siber_panel.py
```

komutuyla çalıştırılabilir.

---

# Kullanım

Program başlatıldığında öncelikle ağ keşfi yapmak isteyip istemediğinizi sorar.

Örneğin:

```text
Ağ keşif taraması yapılsın mı? (e/h)
=e
```

Ardından:

```text
Ağ Bloğu:
192.168.1.0/24
```

girilerek yerel ağdaki cihazlar keşfedilebilir.

Ağ keşfi atlandıktan sonra hedef IP adresi istenir:

```text
Taramak istediğin IP adresi:
192.168.1.140
```

Daha sonra port tarama yöntemi seçilir:

```text
1 - İki port arası
2 - Belirli portlar
3 - Popüler portlar
4 - Tüm TCP portları
```

Son olarak tarama profili seçilir:

```text
1 - Yüksek Trafik
2 - Dengeli
3 - Düşük Trafik
```

Tarama sonuçları masaüstünde:

```text
[Hedef_IP]_rapor.txt
```

formatında kaydedilir.

---

# Önerilen Test Ortamı

Geliştirme ve test işlemlerinin kontrollü bir laboratuvar ortamında yapılması önerilir.

Örneğin:

```text
Kali Linux
     │
     ├── Windows 11
     │
     └── Metasploitable / Test Makineleri
```

VirtualBox gibi sanallaştırma yazılımları kullanılarak izole bir test ağı oluşturulabilir.

---

# Mevcut Sınırlamalar

Bu proje halen erken geliştirme aşamasındadır.

Mevcut sürümün bazı sınırlamaları:

- Gelişmiş servis fingerprinting sınırlıdır.
- OS fingerprinting temel TTL analizine dayanır.
- Banner detection her serviste çalışmayabilir.
- UDP taraması bulunmamaktadır.
- IPv6 desteği bulunmamaktadır.
- Gelişmiş script sistemi bulunmamaktadır.
- Tarama motoru henüz gelişmiş paralel/asenkron mimariye sahip değildir.
- Gelişmiş firewall/IDS davranış analizi bulunmamaktadır.
- TXT raporlama sistemi geliştirilmeye devam etmektedir.
- Kod henüz tamamen modüler değildir.

Bu sınırlamalar projenin gelecekteki geliştirme planlarının bir parçasıdır.

---

# Gelecek Planları

Projenin ilerleyen sürümlerinde:

- [ ] Modüler mimariye geçiş
- [ ] Daha gelişmiş port tarama motoru
- [ ] Daha iyi servis tespiti
- [ ] Daha gelişmiş banner analizi
- [ ] Daha güvenilir OS fingerprinting
- [ ] UDP tarama desteği
- [ ] IPv6 desteği
- [ ] Gelişmiş TXT raporlama
- [ ] JSON ve CSV dışa aktarma
- [ ] Rapor filtreleme ve arama
- [ ] Daha kapsamlı güvenlik değerlendirmeleri
- [ ] Performans iyileştirmeleri
- [ ] Kullanıcı geri bildirimleriyle kullanılabilirlik geliştirmeleri
- [ ] Pentester geri bildirimleriyle teknik geliştirmeler

planlanmaktadır.

Uzun vadeli hedef yalnızca daha fazla özellik eklemek değildir.

Asıl hedef:

**Tarama sonuçlarını hem teknik kullanıcıların hem de normal kullanıcıların anlayabileceği şekilde sunan, güvenilir, düzenli ve geliştirilebilir bir ağ güvenliği aracı oluşturmaktır.**

---

# Proje Felsefesi

Bu proje büyük ve yıllardır geliştirilen ağ tarama araçlarıyla yarışmak amacıyla oluşturulmamıştır.

Projenin temel yaklaşımı:

```text
Öğren
  ↓
Geliştir
  ↓
Test et
  ↓
Hataları düzelt
  ↓
Geri bildirim al
  ↓
Tekrar geliştir
```

Proje küçük bir SYN scanner olarak başladı.

Zaman içerisinde daha kapsamlı bir ağ keşif ve güvenlik aracı haline getirilmesi hedeflenmektedir.

---

# Güvenlik ve Etik Kullanım

Bu araç yalnızca sahibi olduğunuz veya açıkça test etme izniniz bulunan sistemlerde kullanılmalıdır.

Önerilen kullanım alanları:

- Kişisel ağlar
- Sanal makineler
- CTF ortamları
- Siber güvenlik laboratuvarları
- Eğitim ortamları
- Yetkili pentest çalışmaları

Yetkisiz sistemlerde tarama yapmak yerine kontrollü test ortamları kullanılması önerilir.

---

# Yasal Uyarı

Bu yazılım yalnızca eğitim, araştırma, CTF ve yetkili güvenlik testleri amacıyla kullanılmalıdır.

Yalnızca sahibi olduğunuz veya açıkça test etme izniniz bulunan sistemleri tarayın.

İzinsiz sistemlerde port taraması yapmak veya elde edilen bilgileri kötüye kullanmak hukuki ve teknik sonuçlar doğurabilir.

Geliştirici, yazılımın yetkisiz kullanımından sorumlu değildir.

---

# Lisans

Bu proje eğitim ve araştırma amacıyla geliştirilmektedir.

Projeyi kullanmadan, değiştirmeden veya başka bir projeye dahil etmeden önce repository içerisinde belirtilen lisans koşullarını kontrol edin.

---

# Son Söz

Bu proje yaklaşık 70 satırlık basit bir SYN port tarayıcısı olarak başladı.

Hedef; bir anda büyük bir güvenlik platformu oluşturmak değil, projeyi adım adım geliştirmektir.

Öncelik sırası:

**Sağlam iskelet → daha iyi tarama → daha iyi tespit → daha iyi raporlama → geri bildirim → sürekli geliştirme**

Projenin gelecekte kullanıcılar ve siber güvenlik alanında çalışan kişiler tarafından gerçekten faydalı bulunan bir araca dönüşmesi hedeflenmektedir.
