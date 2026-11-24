"""
SISTEM KEUANGAN SEDERHANA
=========================
Project OOP Python - sesuai checklist tugas:

[v] Bahasa Python
[v] Konsep OOP
[v] Minimal 2 class        -> Akun, AkunTabungan, Transaksi, Bank
[v] Object dari class      -> dibuat di fungsi main()
[v] Constructor __init__() -> semua class
[v] Attribute & method     -> semua class
[v] Encapsulation          -> atribut private (__saldo, __pemilik)
[v] Property / setter      -> @property saldo, @property pemilik + @pemilik.setter
[v] Class method           -> Akun.dari_teks(), Akun.total_akun()
[v] Static method          -> Akun.validasi_nominal(), Bank.format_rupiah()
[+] Bonus: Inheritance & Polymorphism (AkunTabungan)
"""

from datetime import datetime


# ----------------------------------------------------------------
# CLASS 1: Transaksi
# ----------------------------------------------------------------
class Transaksi:
    def __init__(self, jenis, jumlah, saldo_akhir, keterangan=""):  # constructor
        self.waktu = datetime.now()          # attribute
        self.jenis = jenis
        self.jumlah = jumlah
        self.saldo_akhir = saldo_akhir
        self.keterangan = keterangan

    def tampilkan(self):                     # method
        return (f"{self.waktu:%d-%m-%Y %H:%M} | {self.jenis:<7} | "
                f"{Bank.format_rupiah(self.jumlah):>14} | "
                f"Saldo: {Bank.format_rupiah(self.saldo_akhir):>14} | {self.keterangan}")


# ----------------------------------------------------------------
# CLASS 2: Akun
# ----------------------------------------------------------------
class Akun:
    __jumlah_akun = 0                        # class attribute (private)

    def __init__(self, pemilik, saldo_awal=0):  # constructor
        Akun.__jumlah_akun += 1
        self.nomor = f"AKN-{Akun.__jumlah_akun:03d}"
        self.__pemilik = ""                  # private attribute (encapsulation)
        self.__saldo = 0                     # private attribute (encapsulation)
        self.riwayat = []
        self.pemilik = pemilik               # memanggil setter (ada validasi)
        if saldo_awal > 0:
            self.setor(saldo_awal, "Saldo awal")

    # ----- PROPERTY & SETTER -----
    @property
    def saldo(self):                         # getter: saldo hanya bisa dibaca
        return self.__saldo

    @property
    def pemilik(self):                       # getter
        return self.__pemilik

    @pemilik.setter
    def pemilik(self, nama):                 # setter dengan validasi
        if not nama or not nama.strip():
            raise ValueError("Nama pemilik tidak boleh kosong.")
        self.__pemilik = nama.strip().title()

    # ----- CLASS METHOD -----
    @classmethod
    def total_akun(cls):
        """Mengembalikan jumlah akun yang sudah dibuat."""
        return cls.__jumlah_akun

    @classmethod
    def dari_teks(cls, teks):
        """Alternative constructor. Format teks: 'nama,saldo_awal'."""
        nama, saldo = teks.split(",")
        return cls(nama, float(saldo))

    # ----- STATIC METHOD -----
    @staticmethod
    def validasi_nominal(jumlah):
        """Tidak butuh self/cls: hanya memeriksa nominal."""
        if jumlah <= 0:
            raise ValueError("Nominal harus lebih dari 0.")

    # ----- METHOD BIASA -----
    def batas_tarik(self):
        return self.__saldo                  # akun biasa: boleh tarik semua saldo

    def setor(self, jumlah, keterangan="Setor tunai"):
        Akun.validasi_nominal(jumlah)
        self.__saldo += jumlah
        self.riwayat.append(Transaksi("SETOR", jumlah, self.__saldo, keterangan))

    def tarik(self, jumlah, keterangan="Tarik tunai"):
        Akun.validasi_nominal(jumlah)
        if jumlah > self.batas_tarik():
            raise ValueError(
                f"Saldo tidak cukup. Maksimal tarik: "
                f"{Bank.format_rupiah(max(self.batas_tarik(), 0))}")
        self.__saldo -= jumlah
        self.riwayat.append(Transaksi("TARIK", jumlah, self.__saldo, keterangan))

    def info(self):
        return (f"[{self.nomor}] {self.jenis():<8} | {self.pemilik:<12} | "
                f"Saldo: {Bank.format_rupiah(self.saldo)}")

    def jenis(self):
        return "Biasa"


# ----------------------------------------------------------------
# CLASS 3: AkunTabungan  (Inheritance + Polymorphism)
# ----------------------------------------------------------------
class AkunTabungan(Akun):
    SALDO_MINIMUM = 50_000

    def __init__(self, pemilik, saldo_awal=0):
        super().__init__(pemilik, saldo_awal)

    def batas_tarik(self):                   # method overriding
        return self.saldo - self.SALDO_MINIMUM

    def jenis(self):                         # method overriding
        return "Tabungan"


# ----------------------------------------------------------------
# CLASS 4: Bank (mengelola banyak Akun)
# ----------------------------------------------------------------
class Bank:
    def __init__(self, nama):
        self.nama = nama
        self.__daftar_akun = {}              # private attribute

    def tambah_akun(self, akun):
        self.__daftar_akun[akun.nomor] = akun
        return akun

    def cari_akun(self, nomor):
        akun = self.__daftar_akun.get(nomor.upper())
        if akun is None:
            raise KeyError(f"Akun {nomor} tidak ditemukan.")
        return akun

    def transfer(self, dari, ke, jumlah):
        asal, tujuan = self.cari_akun(dari), self.cari_akun(ke)
        asal.tarik(jumlah, f"Transfer ke {tujuan.nomor}")
        tujuan.setor(jumlah, f"Transfer dari {asal.nomor}")

    def semua_akun(self):
        return list(self.__daftar_akun.values())

    def total_dana(self):
        return sum(a.saldo for a in self.__daftar_akun.values())

    @staticmethod
    def format_rupiah(angka):                # static method
        teks = f"{abs(angka):,.0f}".replace(",", ".")
        return f"-Rp{teks}" if angka < 0 else f"Rp{teks}"


# ----------------------------------------------------------------
# PROGRAM UTAMA
# ----------------------------------------------------------------
def tampilkan_menu():
    print("\n" + "=" * 46)
    print("      SISTEM KEUANGAN SEDERHANA")
    print("=" * 46)
    print("1. Buat akun baru")
    print("2. Setor tunai")
    print("3. Tarik tunai")
    print("4. Transfer")
    print("5. Ubah nama pemilik (setter)")
    print("6. Lihat semua akun")
    print("7. Riwayat transaksi")
    print("0. Keluar")


def main():
    bank = Bank("Bank Mini")

    # Membuat OBJECT dari class
    bank.tambah_akun(Akun("budi", 500_000))                     # via constructor
    bank.tambah_akun(AkunTabungan("siti", 1_000_000))           # via constructor (child)
    bank.tambah_akun(Akun.dari_teks("andi,250000"))             # via class method

    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu: ").strip()
        try:
            if pilihan == "1":
                jenis = input("Jenis (1=Biasa, 2=Tabungan): ")
                nama = input("Nama pemilik: ")
                saldo = float(input("Saldo awal: Rp"))
                kelas = AkunTabungan if jenis == "2" else Akun
                akun = bank.tambah_akun(kelas(nama, saldo))
                print("Akun dibuat ->", akun.info())
            elif pilihan == "2":
                akun = bank.cari_akun(input("Nomor akun: "))
                akun.setor(float(input("Jumlah setor: Rp")))
                print("Berhasil ->", akun.info())
            elif pilihan == "3":
                akun = bank.cari_akun(input("Nomor akun: "))
                akun.tarik(float(input("Jumlah tarik: Rp")))
                print("Berhasil ->", akun.info())
            elif pilihan == "4":
                dari = input("Dari akun: ")
                ke = input("Ke akun: ")
                bank.transfer(dari, ke, float(input("Jumlah: Rp")))
                print("Transfer berhasil.")
            elif pilihan == "5":
                akun = bank.cari_akun(input("Nomor akun: "))
                akun.pemilik = input("Nama baru: ")      # memanggil setter
                print("Berhasil ->", akun.info())
            elif pilihan == "6":
                print("\n--- DAFTAR AKUN ---")
                for a in bank.semua_akun():
                    print(a.info())
                print(f"Jumlah akun : {Akun.total_akun()}")   # class method
                print(f"Total dana  : {Bank.format_rupiah(bank.total_dana())}")
            elif pilihan == "7":
                akun = bank.cari_akun(input("Nomor akun: "))
                print(f"\n--- RIWAYAT {akun.nomor} ({akun.pemilik}) ---")
                for t in akun.riwayat:
                    print(t.tampilkan())
            elif pilihan == "0":
                print("Terima kasih!")
                break
            else:
                print("Menu tidak valid.")
        except (ValueError, KeyError) as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()