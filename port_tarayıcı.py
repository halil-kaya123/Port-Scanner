from scapy.all import IP, TCP, sr1, send
import sys
import os

def stealth_scan():
    print("=== PROFESYONEL SYN STEALTH SCANNER ===")
    
    while True:
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
        
        # Eğer dosya zaten varsa eski verilerle karışmasın diye siliyoruz, temiz bir sayfa açıyoruz
        if os.path.exists(dosya_adi):
            os.remove(dosya_adi)

        # 65535 portun hepsini listeye ekliyoruz
        portlar = []
        for i in range(65536):
            portlar.append(i)
        
        print(f"\n[+] {hedef_ip} için sinsi tarama başlatıldı...")
        print(f"[+] Sonuçlar anlık olarak '{dosya_adi}' dosyasına kaydediliyor.\n")

        for port in portlar:
            try:
                syn_paketi = IP(dst=hedef_ip) / TCP(dport=port, flags="S")
                cevap = sr1(syn_paketi, timeout=0.1, verbose=0) # Hız için timeout 0.1 yapıldı

                log_satiri = "" # Dosyaya yazılacak metni tutacak değişken

                if cevap is None:
                    log_satiri = f"Port {port} | FİLTRELENDİ (FİREWALL VAR) 🛡️"
                    print(f"-> {log_satiri}")
                
                elif cevap.haslayer(TCP):
                    if cevap.getlayer(TCP).flags == "SA":
                        log_satiri = f"Port {port} | AÇIK 🟢"
                        print(f"-> {log_satiri}")
                        
                        rst_paketi = IP(dst=hedef_ip) / TCP(dport=port, flags="R")
                        send(rst_paketi, verbose=0)
                        
                    elif cevap.getlayer(TCP).flags == "RA" or cevap.getlayer(TCP).flags == "R":
                        log_satiri = f"Port {port} | KAPALI 🔴"
                        print(f"-> {log_satiri}")

                # 🔥 ANLIK LOGLAMA SİHRİ (Zurnanın Zırt Dediği Yer)
                # Her port işleminde dosyayı "a" (append - sonuna ekle) modunda açıyoruz.
                # "with open" bloğu işi bittiği mikro saniyede dosyayı kaydeder ve kapatır.
                # Sen terminali CTRL+C ile kapatsan bile o saliseye kadar yazılanlar asla silinmez!
                if log_satiri:
                    with open(dosya_adi, "a", encoding="utf-8") as f:
                        f.write(log_satiri + "\n")

            except Exception as e:
                continue

        print(f"\n[+] --- Sinsi Tarama Tamamlandı. Tüm sonuçlar '{dosya_adi}' dosyasına kaydedildi. ---")

if __name__ == "__main__":
    try:
        stealth_scan()
    except PermissionError:
        print("\n[!] HATA: Bu programı çalıştırmak için lütfen terminali YÖNETİCİ (Administrator) olarak açın!")
