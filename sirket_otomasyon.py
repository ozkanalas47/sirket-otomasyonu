from datetime import datetime

class Sirket:
    def __init__(self, ad):
        self.ad = ad
        self.calisma = True

    def program(self):
        secim = self.menuSecim()

        if secim == 1:
            self.calisanEkle()
        elif secim == 2: 
            self.calisanCikar()
        elif secim == 3:
            ay_yil_secim = input("Yıllık bazda görmek ister misiniz? (e/h): ")
            if ay_yil_secim == "e": 
                self.verilecekmaasGoster(hesap="y")
            else:
                self.verilecekmaasGoster()
        elif secim == 4:
            self.maaslarVer()
        elif secim == 5:
            self.masrafGir()
        elif secim == 6:
            self.gelirGir()

    def menuSecim(self):
        secim = int(input(f"**** {self.ad} otomasyona hoş geldiniz ****\n\n"
                          "1-Çalışan Ekle \n2-Çalışan Çıkar\n3-Verilen maaşları Göster\n4-Maaşları Ver\n"
                          "5-Masraf Gir\n6-Gelir Gir\n\nSeçiminizi Giriniz: "))
        while secim < 1 or secim > 6:
            secim = int(input("Lütfen 1 - 6 arasında belirtilen seçeneklerden birini giriniz: "))
        return secim

    def calisanEkle(self):
        ad = input("Çalışan adını giriniz: ")
        soyad = input("Çalışan soyadını giriniz: ")
        yas = input("Çalışanın yaşını giriniz: ")
        cinsiyet = input("Çalışanın cinsiyetini giriniz: ")
        maas = input("Çalışanın maaşını giriniz: ")

        with open("calisanlar.txt", "r") as dosya:
            calisanlarListesi = dosya.readlines()
        
        if len(calisanlarListesi) == 0:
            id = 1
        else:
            id = int(calisanlarListesi[-1].split(")")[0]) + 1

        with open("calisanlar.txt", "a") as dosya:
            dosya.write(f"{id}){ad}-{soyad}-{yas}-{cinsiyet}-{maas}\n")
    
    def calisanCikar(self):
        with open("calisanlar.txt", "r") as dosya:
            calisanlar = dosya.readlines()

        gcalisanlar = [calisan[:-1].replace("-", " ") for calisan in calisanlar]

        for i, calisan in enumerate(gcalisanlar, 1):
            print(f"{i}) {calisan}")

        secim = int(input(f"Lütfen çıkarmak istediğiniz çalışanın numarasını giriniz (1-{len(gcalisanlar)}): "))
        while secim < 1 or secim > len(gcalisanlar):
            secim = int(input(f"Lütfen 1 - {len(gcalisanlar)} arasında bir numara giriniz: "))

        calisanlar.pop(secim - 1)

        with open("calisanlar.txt", "w") as dosya:
            for sayac, calisan in enumerate(calisanlar, 1):
                dosya.write(f"{sayac}){calisan.split(')')[1]}")

    def verilecekmaasGoster(self, hesap="a"):
        with open("calisanlar.txt", "r") as dosya:
            calisanlar = dosya.readlines()

        maaslar = [int(calisan.split("-")[-1]) for calisan in calisanlar]

        if hesap == "a": 
            print(f"Bu ay toplam verilmesi gereken maaş: {sum(maaslar)}")
        else:
            print(f"Bu yıl toplam verilmesi gereken maaş: {sum(maaslar) * 12}")

    def maaslarVer(self):
        with open("calisanlar.txt", "r") as dosya:
            calisanlar = dosya.readlines()

        maaslar = [int(calisan.split("-")[-1]) for calisan in calisanlar]
        topMaas = sum(maaslar)

        with open("butce.txt", "r") as dosya:
            tbutce = int(dosya.readline().strip())

        tbutce -= topMaas

        with open("butce.txt", "w") as dosya:
            dosya.write(str(tbutce))

    def masrafGir(self):
        masraf = int(input("Girmek istediğiniz masraf tutarını yazınız: "))
        masraf_turu = input("Masraf türünü belirtiniz: ")
        aciklama = input("Masraf ile ilgili açıklama giriniz: ")

        with open("butce.txt", "r") as dosya:
            mevcut_butce = int(dosya.readline().strip())

        mevcut_butce -= masraf

        with open("butce.txt", "w") as dosya:
            dosya.write(str(mevcut_butce))

        tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("masraflar.txt", "a") as masraf_dosya:
            masraf_dosya.write(f"{tarih} - {masraf_turu} - {masraf} TL - {aciklama}\n")

        print(f"Yeni bütçe: {mevcut_butce}")
        print(f"Masraf kaydedildi: {masraf_turu} için {masraf} TL - {aciklama}")
        
    def gelirGir(self):
        gelir = int(input("Girmek istediğiniz gelir tutarını yazınız: "))
        gelir_turu = input("Gelir türünü belirtiniz: ")
        aciklama = input("Gelir ile ilgili açıklama giriniz: ")

        with open("butce.txt", "r") as dosya:
            mevcut_butce = int(dosya.readline().strip())

        mevcut_butce += gelir

        with open("butce.txt", "w") as dosya:
            dosya.write(str(mevcut_butce))

        tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("gelir_detay.txt", "a") as gelir_dosya:
            gelir_dosya.write(f"{tarih} - {gelir_turu} - {gelir} TL - {aciklama}\n")

        print(f"Yeni bütçe: {mevcut_butce}")
        print(f"Gelir kaydedildi: {gelir_turu} için {gelir} TL - {aciklama}")

sirket = Sirket("Özkan Yazılım")

while sirket.calisma:
    sirket.program()