from scapy.all import IP, TCP, sr1, send
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
from datetime import timedelta
import ipaddress
import random
import socket
import time
import sys
import os

# Windows işletim sistemlerinde gerçek Masaüstü yolunu Registry üzerinden çeken kurumsal koruma
def get_windows_desktop_path():
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
        path, _ = winreg.QueryValueEx(key, "Desktop")
        return os.path.expandvars(path)
    except Exception:
        # Windows dışı işletim sistemleri (Linux/macOS) için evrensel yedek yol
        ana_dizin = os.path.expanduser("~")
        yedek_yol = os.path.join(ana_dizin, "Desktop")
        if not os.path.exists(yedek_yol):
            yedek_yol = os.path.join(ana_dizin, "Masaüstü")
        return yedek_yol

def agi_tara(hedef_blok):
    print(f"\n{hedef_blok} ağı taranıyor, lütfen bekleyin...")
    try:
        # Girdinin geçerli bir network bloğu olup olmadığını endüstri standartlarında doğruluyoruz
        ipaddress.ip_network(hedef_blok, strict=False)
        
        arp_istegi = ARP(pdst=hedef_blok)
        yayin_katmani = Ether(dst="ff:ff:ff:ff:ff:ff")
        tam_paket = yayin_katmani / arp_istegi
        cevaplanan_listesi = srp(tam_paket, timeout=3, verbose=False)[0] # Sadece cevaplanan paket havuzunu alıyoruz
    except ValueError:
        print("HATA: Geçersiz ağ bloğu formatı! (Örn: 192.168.1.0/24)")
        return
    except socket.error as e:
        print(f"Ağ soket hatası oluştu: {e}")
        return
    except Exception as e:
        print(f"Tarama sırasında beklenmedik bir sistem hatası oluştu: {e}")
        return

    print(f"\n{'IP ADRESİ':<18}{'MAC ADRESİ':<20}{'CİHAZ ADI (HOSTNAME)'}")
    print("-" * 65)

    cihaz_sayisi = 0
    for gonderilen, alinan in cevaplanan_listesi:
        ip_adresi = alinan.psrc
        mac_adresi = alinan.hwsrc

        try:
            isim_cozumleme = socket.gethostbyaddr(ip_adresi)
            cihaz_ismi = isim_cozumleme[0]
        except (socket.herror, socket.gaierror):
            cihaz_ismi = "Bilinmeyen cihaz"

        print(f"{ip_adresi:<18}{mac_adresi:<20}{cihaz_ismi}")
        cihaz_sayisi += 1

    print(f"\nTarama tamamlandı. Ağda {cihaz_sayisi} tane aktif cihaz bulundu.\n")

def baslat():
    print("\nAğ Keşifi")
    while True:
        try:
            print("Taramak istediğiniz ağ bloğunu girin.")
            print("Örnek formatlar: 192.168.1.0/24 veya 10.0.0.0/24.")
            hedef_blok = input("Ağ Bloğu (Çıkış için -1): ").strip()

            if hedef_blok == "-1":
                print("Ağ tarayıcıdan çıkış yapılıyor...")
                break

            if not hedef_blok:
                print("Lütfen boş bırakmayın!")
                continue

            agi_tara(hedef_blok)

        except KeyboardInterrupt:
            print("\nKullanıcı tarafından kesildi.")
            break
        except Exception as e:
            print(f"Hata: {e}. Lütfen kontrol edin.")
            continue

def stealth_scan():
    while True:
        print("Ağ keşif taraması yapılsın mı? (e/h)")
        secim = input("=").lower().strip()
        if secim=="e" or secim=="evet" or secim=="yes" or secim=="y" or secim=="1":
            baslat()
            break
        elif secim=="h" or secim=="hayır" or secim=="n" or secim=="no" or secim=="0":
            print("Ağ keşfi atlandı, doğrudan port taramaya geçiliyor.\n")
            break
        else:
            print("Geçersiz seçim, lütfen e veya h giriniz.")
            
    print("\nPersonal Network Security Scanner")
    
    while True:
        portlar = []
        try:
            hedef_input = input("\nTaramak istediğin IP adresi (Çıkış için -1): ").strip()

            if hedef_input == "-1":
                print("Çıkış yapılıyor...")
                break

            if not hedef_input:
                print("Lütfen geçerli bir IP girin!")
                continue

            # Gelişmiş IP Doğrulama (ipaddress entegrasyonu)
            hedef_ip = str(ipaddress.ip_address(hedef_input))

        except ValueError:
            print("HATA: Geçersiz IP adresi formatı! Lütfen tekrar deneyin.")
            continue
        except Exception as e:
            print(f"Hata = {e}. Lütfen geçerli bir IP girin!")
            continue

        # KORUMALI MASAÜSTÜ YOLU YÜKLEMESİ
        dosya_adi = f"{hedef_ip}_rapor.txt"
        desktop_path = get_windows_desktop_path()
        dosya_yeri = os.path.join(desktop_path, dosya_adi)

        if os.path.exists(dosya_yeri):
            os.remove(dosya_yeri)

        while True:
            print("\nPort Tarama Seçeneği\n")
            print("2 port arası tarama (1)")
            print("Belirli portları tarama (2)")
            print("En popüler 100 portu tarama (3)")
            print("Tüm portları tarama (4)")

            try:
                secim = int(input("="))
            except ValueError:
                print("Lütfen sayısal veri giriniz.")
                continue

            if secim == 1:
                try:
                    ilk_port = int(input("İlk portu giriniz: "))
                    ikinci_port = int(input("İkinci portu giriniz: "))

                    if ilk_port < 1 or ikinci_port < 1:
                        print("Port numaraları en az 1 olmalıdır!")
                        continue
                    elif ilk_port>65535 or ikinci_port>65535:
                        print("Port numarası maksimum 65535 olmalıdır!")
                        continue
                except ValueError:
                    print("Lütfen sayısal veri giriniz.")
                    continue

                min_port = min(ilk_port, ikinci_port)
                max_port = max(ilk_port, ikinci_port)

                for port in range(min_port, max_port + 1):
                    portlar.append(port)
                break

            elif secim == 2:
                while True:
                    try:
                        belirli_portlar = int(input("Taranacak belirli portları girin (Çıkış için -1): "))

                        if belirli_portlar == -1 and len(portlar) == 0:
                            print("Henüz port girilmemiş!")
                            continue
                        elif belirli_portlar == -1 and len(portlar) > 0:
                            print("Port girişleri tamamlandı.")
                            break
                        elif belirli_portlar < 1 or belirli_portlar > 65535:
                            print("Port numaraları 1-65535 arasında olmalı!")
                            continue
                        else:
                            portlar.append(belirli_portlar)
                    except ValueError:
                        print("Lütfen sayısal veri giriniz.")
                        continue
                break

            elif secim == 3:
                # Tam olarak 100 adet endüstri standardı popüler port listesi
                portlar += [
                    1, 5, 7, 9, 11, 13, 17, 18, 19, 20, 
                    21, 22, 23, 25, 37, 42, 43, 49, 53, 67, 
                    68, 69, 70, 79, 80, 88, 101, 102, 107, 109, 
                    110, 111, 113, 115, 117, 118, 119, 123, 135, 137, 
                    138, 139, 143, 156, 161, 162, 179, 194, 201, 220, 
                    389, 443, 444, 445, 464, 465, 500, 513, 514, 515, 
                    520, 530, 543, 544, 546, 547, 554, 587, 631, 636, 
                    873, 990, 992, 993, 995, 1080, 1433, 1434, 1521, 2049, 
                    2375, 2376, 3306, 3389, 3690, 4444, 5000, 5060, 5432, 5672, 
                    5900, 6379, 8000, 8080, 8443, 8888, 9000, 9200, 9300, 27017
                ]
                break

            elif secim == 4:
                # Endüstri standardı olan 1-65535 aralığı (Port 0 taranmaz)
                for i in range(1, 65536):
                    portlar.append(i)
                break
            else:
                print("Seçenek bulunamadı!")
                continue

        while True:
            print("\nGizlilik ve Hız Ayarı\n")
            print("1-) Yüksek Trafik Ayarı (Hızlı ancak ağda gürültülü)")
            print("2-) Dengeli Ayar (Normal hız, orta derece gecikmeli)")
            print("3-) Düşük Trafik Ayarı (Çok yavaş, güvenlik mekanizmalarını atlatmaya yönelik)")

            try:
                gizlilik_ayari = int(input("="))

                if gizlilik_ayari < 1 or gizlilik_ayari > 3:
                    print("1-3 arası değer giriniz lütfen")
                    continue
                elif gizlilik_ayari > 1:
                    random.shuffle(portlar)
                break
            except ValueError:
                print("Lütfen sayısal veri giriniz.")
                continue
        
        print(f"\n{hedef_ip} için tarama başlatıldı...")
        print(f"Sonuçlar anlık olarak '{dosya_adi}' dosyasına kaydediliyor.\n")
        simdi = time.time()

        # TEK SEFERLİK İŞLETİM SİSTEMİ TESPİTİ (TTL ANALİZİ)
        tahmini_os = "Belirlenemedi (Yanıt Alınamadı)"
        try:
            os_paketi = IP(dst=hedef_ip) / TCP(dport=80, flags="S")
            os_cevabi = sr1(os_paketi, timeout=1.0, verbose=0)
            
            if os_cevabi and os_cevabi.haslayer(IP):
                ttl_degeri = os_cevabi.getlayer(IP).ttl
                if ttl_degeri <= 64:
                    tahmini_os = "Linux / Android / macOS"
                elif 64 < ttl_degeri <= 128:
                    tahmini_os = "Windows"
                elif 128 < ttl_degeri <= 255:
                    tahmini_os = "Cisco / Network Cihazı (Unix tabanlı)"
        except Exception:
            pass

        # TARAFSIZ SİBER GÜVENLİK REFERANS VERİTABANI
        risk_veritabanı = {
            21:   "Servis aktif. Kimlik doğrulama verilerinin şifresiz iletildiği bilinmektedir.",
            22:   "Servis aktif. Kaba kuvvet (Brute Force) girişimlerine karşı önlem alınması önerilir.",
            23:   "Servis aktif. Güvenli olmayan protokol kullanımı; SSH geçişi önerilir.",
            25:   "E-posta servisi aktif. Açık röle (Open Relay) yapılandırması kontrol edilmelidir.",
            53:   "DNS servisi aktif. Bölge transferi (Zone Transfer) izinleri incelenmelidir.",
            80:   "HTTP web sunucusu aktif. Yazılım sürüm zafiyetleri kontrol edilmelidir.",
            110:  "POP3 e-posta servisi aktif. Şifrelerin temiz metin geçişi incelenmelidir.",
            135:  "Windows RPC servisi aktif. Ağ içi erişim izinleri sınırlandırılmalıdır.",
            139:  "NetBIOS servisi aktif. Dosya paylaşım izinleri denetlenmelidir.",
            443:  "HTTPS güvenli web sunucusu aktif. SSL/TLS sertifika ve şifreleme algoritmaları incelenmelidir.",
            445:  "Windows SMB servisi aktif. Güncel güvenlik yamalarının (MS17-010 vb.) doğrulanması önerilir.",
            1433: "MSSQL veritabanı servisi aktif. Varsayılan yetkili hesap şifreleri gözden geçirilmelidir.",
            3306: "MySQL veritabanı servisi aktif. Dış ağ erişim kuralları sınırlandırılmalıdır.",
            3389: "Windows RDP (Uzak Masaüstü) aktif. Ağ seviyesinde kimlik doğrulama (NLA) önerilir.",
            8080: "Alternatif HTTP sunucusu aktif. Test veya yönetim panellerinin varlığı incelenmelidir."
        }

        # RAPOR BAŞLIĞI VE ÖNEMLİ YASAL UYARI MANTIĞI
        with open(dosya_yeri, "w", encoding="utf-8") as f:
            f.write(f"PERSONAL NETWORK SECURITY SCANNER REPORT\n")
            f.write(f"ÖNEMLİ NOT: Bu rapor yalnızca hedef sistem üzerindeki açık veya aktif\n")
            f.write(f"servisleri listeler. Bir portun 'OPEN' (Açık) olması doğrudan bir siber güvenlik açığı\n")
            f.write(f"olduğu anlamına gelmez. Yapılandırma detayları ayrıca incelenmelidir.\n")
            f.write(f"---------------------------------------------------------------------------------\n")
            f.write(f"Hedef IP Adresi          = {hedef_ip}\n")
            f.write(f"Tahmini İşletim Sistemi  = {tahmini_os} (TTL tabalı tahmin)\n")
            f.write(f"Tarama Başlangıç Zamanı  = {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Tarama Modu              = Mod {gizlilik_ayari}\n")
            f.write("-" * 135 + "\n")
            f.write(f"{'PORT':<10}{'DURUM':<24}{'MUHTEMEL SERVİS':<18}{'CANLI BANNER (YAZILIM SÜRÜMÜ)':<35}{'GÜVENLİK TAVSİYESİ / NOTU'}\n")
            f.write("-" * 135 + "\n")

        # PORT TARAMA DÖNGÜSÜ
        for port in portlar:
            try:
                if gizlilik_ayari == 2:
                    time.sleep(random.uniform(0.5, 2.0))
                elif gizlilik_ayari == 3:
                    time.sleep(random.uniform(5.0, 10.0))

                timeout_ayari = 0.1 if gizlilik_ayari == 1 else (0.5 if gizlilik_ayari == 2 else 1.0)

                syn_paketi = IP(dst=hedef_ip) / TCP(dport=port, flags="S")
                cevap = sr1(syn_paketi, timeout=timeout_ayari, verbose=0)
                
                durum = "NO RESPONSE / POSSIBLY FILTERED"
                muhtemel_servis = "Bilinmiyor"
                canlı_banner = "Alınamadı / Yanıt Yok"
                tavsiye_notu = risk_veritabanı.get(port, "Servis yapılandırmasının ve erişim izinlerinin incelenmesi önerilir.")
                
                try:
                    muhtemel_servis = socket.getservbyport(port).upper()
                except (OSError, socket.error):
                    pass

                # SENARYO A: YANIT YOK (FILTERED OLABİLİR)
                if cevap is None:
                    durum = "NO_RESP / POSS_FILTERED"
                    tavsiye_notu = "Paket yanıtı alınamadı; ağ engeli, drop durumu veya host durumu kontrol edilmelidir."
                
                # SENARYO B: YANIT GELDİ
                elif cevap.haslayer(TCP):
                    bayraklar = int(cevap.getlayer(TCP).flags)
                    
                    # PORT AÇIK (SYN-ACK ALINDI)
                    if (bayraklar & 0x12) == 0x12:
                        durum = "OPEN"
                        canlı_banner = "Banner Alınamadı"
                        
                        # Banner Grabbing (Sürüm Yakalama) Alanı
                        try:
                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s.settimeout(1.0)
                            s.connect((hedef_ip, port))
                            banner = s.recv(1024)
                            if banner:
                                canlı_banner = banner.decode('utf-8', errors='ignore').strip().replace('\r', '').replace('\n', ' ')
                            s.close()
                        except (socket.timeout, socket.error) as e:
                            canlı_banner = f"TCP bağlantısı başarılı; banner alınamadı"

                        # El sıkışmayı sonlandırıp kaçıyoruz (Stealth)
                        rst_paketi = IP(dst=hedef_ip) / TCP(dport=port, flags="R")
                        send(rst_paketi, verbose=0)
                        
                    # PORT KAPALI (RST-ACK ALINDI)
                    elif (bayraklar & 0x04):
                        durum = "CLOSED"
                        tavsiye_notu = "Port kapalı durumdadır."

                # Konsol ekranına basma kuralları (Kapalı portlar süzülür)
                if durum != "CLOSED":
                    print(f"-> Port {port:<5} | Durum: {durum:<24} | Service: {muhtemel_servis:<12} | Banner: {canlı_banner[:25]}")

                    # Sütun hizalamalı TXT rapor satırı oluşturma
                    log_satiri = f"{port:<10}{durum:<24}{muhtemel_servis:<18}{canlı_banner:<35}{tavsiye_notu}"
                    
                    with open(dosya_yeri, "a", encoding="utf-8") as f:
                        f.write(log_satiri + "\n")

            except KeyboardInterrupt:
                print("\nTarama Kullanıcı Tarafından Durduruldu.")
                break
            except socket.error as se:
                print(f"Port {port} için ağ hatası: {se}")
                continue
            except Exception as e:
                print(f"Port {port} taranırken beklenmedik hata oluştu: {e}")
                continue

        bitis = time.time()
        aradaki_fark = bitis - simdi
        gecen_sure = str(timedelta(seconds=int(aradaki_fark)))
        
        print(f"\nTarama Tamamlandı. Tüm sonuçlar masaüstünde '{dosya_adi}' dosyasına kaydedildi.")
        print(f"Tahmini işletim sistemi = {tahmini_os}")
        print(f"Tarama süresi = {gecen_sure}")

        # Rapor sonu özeti ekleme
        with open(dosya_yeri, "a", encoding="utf-8") as f:
            f.write("-" * 125 + "\n")
            f.write(f"Tarama Tamamlanma Süresi = {gecen_sure}\n")

if __name__ == "__main__":
    # Windows platform kontrolü ve yönetici yetki sorgusu
    if os.name == 'nt':
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("\nHATA: Bu programı çalıştırmak için lütfen terminali YÖNETİCİ (Administrator) olarak açın!")
            sys.exit()
    stealth_scan()
