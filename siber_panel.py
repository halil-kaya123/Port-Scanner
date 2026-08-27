from scapy.all import IP, TCP, sr1, send
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
from datetime import timedelta
import urllib.request
import random
import socket
import time
import sys
import os

def agi_tara(hedef_blok):
    print(f"\n{hedef_blok} ağı taranıyor, lütfen bekleyin...")
    try:
        arp_istegi = ARP(pdst=hedef_blok)
        yayin_katmani = Ether(dst="ff:ff:ff:ff:ff:ff")
        tam_paket = yayin_katmani / arp_istegi
        cevaplanan_listesi = srp(tam_paket, timeout=3, verbose=False)[0]
    except Exception:
        print("Tarama sırasında sistemsel hata oldu.")
        return

    # Sütunları genişleterek ÜRETİCİ bilgisi tabloya eklendi
    print(f"\n{'IP ADRESİ':<18}{'MAC ADRESİ':<20}{'CİHAZ ADI (HOSTNAME)':<22}{'ÜRETİCİ'}")
    print("-" * 85)

    cihaz_sayisi = 0
    for gonderilen, alinan in cevaplanan_listesi:
        ip_adresi = alinan.psrc
        mac_adresi = alinan.hwsrc

        # 1. ADIM: Hostname Çözümleme
        try:
            isim_cozumleme = socket.gethostbyaddr(ip_adresi)
            cihaz_ismi = isim_cozumleme[0]
        except (socket.herror, socket.gaierror):
            cihaz_ismi = "Bilinmeyen cihaz"

        # 2. ADIM: MAC Adresinden Marka Bulma
        ureti_firma = "Bilinmiyor"
        try:
            # macvendors.com API'sine istek atıyoruz (Kayıt/Key gerektirmez)
            url = f"https://api.macvendors.com/{mac_adresi}"
            istek = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            # API saniyede en fazla 1 isteğe izin verdiği için ağı yormadan hızlıca okuyoruz
            with urllib.request.urlopen(istek, timeout=2) as response:
                ureti_firma = response.read().decode('utf-8')
        except Exception:
            # API sınırına takılırsa veya MAC adresi yerel/özel ise "Bilinmiyor" olarak kalır
            ureti_firma = "Bilinmeyen Marka"

        # Bulguları yeni sütun düzenine göre ekrana basıyoruz
        print(f"{ip_adresi:<18}{mac_adresi:<20}{cihaz_ismi:<22} {ureti_firma}")
        cihaz_sayisi += 1
        
        # API'nin saniye sınırına takılmamak için her cihaz arasında çok küçük bir duraklama koyuyoruz
        time.sleep(0.5)

    print(f"\nTarama tamamlandı. Ağda {cihaz_sayisi} tane aktif cihaz bulundu.\n")


def baslat():
    print("\nYEREL AĞ TARAYICI\n")
    while True:
        try:
            print("Taramak istediğiniz ağ bloğunu girin.")
            print("Örnek formatlar: 192.168.1.0/24 veya 10.0.0.0/24.")
            hedef_blok = input("Ağ Bloğu (çıkış için -1):").strip()

            if hedef_blok=="-1":
                print("Çıkış yapılıyor...\n")
                break

            if not hedef_blok:
                print("Lütfen boş bırakmayın!")
                continue

            agi_tara(hedef_blok)

        except KeyboardInterrupt:
            print("Kullanıcı tarafından kesildi.")
            break
        except Exception as e:
            print(f"Hata: {e}. Lütfen kontrol edin.")
            continue

def stealth_scan():
    while True:
        print("Ağ taraması yapılsın mı? (e/h)")
        secim=input("=").lower()
        if secim=="e" or secim=="evet" or secim=="yes" or secim=="1":
            baslat()
            break
        elif secim=="h" or secim=="hayır" or secim=="no" or secim=="0":
            print("Ağ taraması yapılmayacak\n")
            break
        else:
            print("Seçim bulunamadı")

    print("PROFESYONEL SYN STEALTH SCANNER")
    
    while True:
        portlar = []
        try:
            hedef_ip = input("\nTaramak istediğin IP adresi (Çıkış için -1): ")

            if hedef_ip == "-1":
                print("Çıkış yapılıyor...")
                break

        except Exception as e:
            print(f"Hata = {e}. Lütfen geçerli bir IP girin!")
            continue

        # LOG DOSYASI HAZIRLIĞI
        # Girilen IP adına göre bir dosya ismi oluşturuyoruz (Örn: 127.0.0.1_rapor.txt)
        dosya_adi = f"{hedef_ip}_rapor.txt"
        ana_dizin = os.path.expanduser("~")
        dosya_yeri=os.path.join(ana_dizin, "Desktop",dosya_adi)

        if not os.path.exists(os.path.join(ana_dizin, "Desktop")):
            dosya_yeri = os.path.join(ana_dizin, "Masaüstü", dosya_adi)

        # Eğer dosya zaten varsa eski verilerle karışmasın diye siliyoruz, temiz bir sayfa açıyoruz
        if os.path.exists(dosya_yeri):
            os.remove(dosya_yeri)

        while True:
            print("\nPort Tarama Seçeneği\n")
            print("2 port arası tarama (1)")
            print("Belirli portları tarama (2)")
            print("En popüler 100 portu tarama (3)")
            print("Tüm portları tarama (4)")

            try:
                secim=int(input("="))
            except ValueError:
                print("Lütfen sayısal veri giriniz.")
                continue

            if secim == 1:
                try:

                    ilk_port=int(input("İlk portu giriniz:"))
                    ikinci_port=int(input("İkinci portu giriniz:"))

                    if ilk_port<0 or ikinci_port<0:
                        print("Seçim en az 0 olmalıdır!")
                        continue

                except ValueError:
                    print("Lütfen sayısal veri giriniz.")
                    continue

                min_port=min(ilk_port, ikinci_port)
                max_port=max(ilk_port, ikinci_port)

                for port in range(min_port, max_port+1):
                    portlar.append(port)

                break

            elif secim == 2:
                while True:
                    try:
                        belirli_portlar=int(input("Taranacak belirli portları girin (çıkış için -1):"))

                        if belirli_portlar == -1 and len(portlar)==0:
                            print("Henüz port girilmemiş!")
                            continue

                        elif belirli_portlar == -1 and len(portlar)>0:
                            print("Çıkış yapılıyor...")
                            break

                        elif belirli_portlar<0 or belirli_portlar>65535:
                            print("Port numaraları 0-65535 arasında olmalı!")
                            continue

                        else:
                            portlar.append(belirli_portlar)
                            continue

                    except ValueError:
                        print("Lütfen sayısal veri giriniz.")
                        continue
                break

            elif secim == 3:
                portlar+=[
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
                for i in range(65536):
                    portlar.append(i)
                break

            else:
                print("Seçenek bulunamadı!")
                continue

        while True:

            print("\nGizlilik ve Hız Ayarı\n")
            print("1-) Agresif ayar (Hızlı ancak aşırı gürültülü)")
            print("2-) Dengeli ayar (Normal hız, orta gürültülü)")
            print("3-) Sinsi ayar (Çok yavaş ancak aşırı gizli ve az gürültülü)")

            try:
                gizlilik_ayari=int(input("="))

                if gizlilik_ayari < 1 or gizlilik_ayari > 3:
                    print("1-3 arası değer giriniz lütfen")
                    continue
                
                elif gizlilik_ayari>1:
                    random.shuffle(portlar)

                break
            
            except ValueError:
                print("Lütfen sayısal veri giriniz.")
                continue
        
        print(f"\n[+] {hedef_ip} için sinsi tarama başlatıldı...")
        print(f"[+] Sonuçlar anlık olarak '{dosya_adi}' dosyasına kaydediliyor.\n")
        simdi=time.time()

        tahmini_os = "Bilinmiyor (Yanıt Alınamadı)"
        try:
            # Hedefin durumunu anlamak için hızlıca tek bir SYN paketi fırlatıyoruz
            os_paketi = IP(dst=hedef_ip) / TCP(dport=80, flags="S")
            os_cevabi = sr1(os_paketi, timeout=1.0, verbose=0)
            
            # Eğer karşıdan bir cevap (SYN-ACK veya RST) dönerse TTL değerini okuyoruz
            if os_cevabi and os_cevabi.haslayer(IP):
                ttl_degeri = os_cevabi.getlayer(IP).ttl
                
                # Standart TTL imza analizleri:
                if ttl_degeri <= 64:
                    tahmini_os = "Linux / Android / macOS"
                elif 64 < ttl_degeri <= 128:
                    tahmini_os = "Windows"
                elif 128 < ttl_degeri <= 255:
                    tahmini_os = "Cisco / Network Cihazı (Unix tabanlı)"
        except Exception:
            # Ağda anlık bir kopma veya engel olursa taramayı çökertmesin diye sessizce geçiyoruz
            pass

        with open(dosya_yeri, "w", encoding="utf-8") as rapor:
            rapor.write(f"Tahmini İşletim Sistemi = {tahmini_os}")

        for port in portlar:
            
            try:

                if gizlilik_ayari == 2:
                    time.sleep(random.uniform(0.5,2.0))

                elif gizlilik_ayari == 3:
                    time.sleep(random.uniform(5.0,10.0))


                if gizlilik_ayari == 1:
                    timeout_ayari=0.1

                elif gizlilik_ayari == 2:
                    timeout_ayari=0.5

                elif gizlilik_ayari == 3:
                    timeout_ayari=1.0

                syn_paketi = IP(dst=hedef_ip) / TCP(dport=port, flags="S")
                cevap = sr1(syn_paketi, timeout=timeout_ayari, verbose=0)
                
                log_satiri = "" # Dosyaya yazılacak metni tutacak değişken

                if cevap is None:
                    log_satiri = f"Port {port} | FİLTRELENDİ (FİREWALL VAR) 🛡️"
                    print(f"-> {log_satiri}")
                
                elif cevap.haslayer(TCP):
                    bayraklar = int(cevap.getlayer(TCP).flags)
                    if (bayraklar & 0x12) == 0x12:
                        log_satiri = f"Port {port} | AÇIK 🟢"
                        print(f"-> {log_satiri}")
                        
                        rst_paketi = IP(dst=hedef_ip) / TCP(dport=port, flags="R")
                        send(rst_paketi, verbose=0)
                        
                    elif (bayraklar & 0x04):
                        log_satiri = f"Port {port} | KAPALI 🔴"
                        print(f"-> {log_satiri}")

                # Her port işleminde dosyayı "a" (append - sonuna ekle) modunda açıyoruz.
                # "with open" bloğu işi bittiği mikro saniyede dosyayı kaydeder ve kapatır.
                if log_satiri:
                    with open(dosya_yeri, "a", encoding="utf-8") as f:
                        f.write(f"Tahmini İşletim Sistemi = {tahmini_os}")
                        f.write(log_satiri + "\n")
            except KeyboardInterrupt:
                print("Tarama Kullanıcı Tarafından Durduruldu.")
                break
            
            except Exception as e:
                continue

        bitis=time.time()
        aradaki_fark=bitis-simdi
        gecen_sure=str(timedelta(seconds=int(aradaki_fark)))
        print(f"\nSinsi Tarama Tamamlandı. Tüm sonuçlar masaüstünde '{dosya_adi}' dosyasına kaydedildi. ---")
        print(f"Tahmini işletim sistemi = {tahmini_os}")
        print(f"Tarama süresi = {gecen_sure}")

if __name__ == "__main__":
    try:
        stealth_scan()
    except PermissionError:
        print("\nHATA: Bu programı çalıştırmak için lütfen terminali YÖNETİCİ (Administrator) olarak açın!")
