# Userbot Telegram

Userbot Telegram ini menggunakan **Telethon** & **Flask** untuk berjalan di Railway. Mendukung manajemen produk, VIP link, DANA & QRIS, auto-reply, dan utilitas bot.

---

## Fitur Utama

- 🏪 Produk & VIP  
  - Tambah, edit, hapus produk  
  - Tambah/hapus VIP link  
  - Lihat daftar produk & link VIP  
- 💳 Pembayaran  
  - DANA & QRIS (bisa menampilkan foto/QRIS)  
- 🤖 Auto Reply  
  - Tambah, hapus, list auto reply  
- ⚡ Utilitas & Status  
  - Ping, Alive, Shutdown, Reload, Restart, Cache, Broadcast  

---

## Deploy ke Railway

[![Deploy to Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/s3xdes/userbot)

**Langkah:**

1. Klik tombol **Deploy to Railway** di atas.  
2. Login ke Railway (atau daftar baru).  
3. Railway otomatis fork & deploy repo ini.  
4. Tambahkan **Environment Variables**:  

   | Key       | Value                       |
   |-----------|-----------------------------|
   | API_ID    | Dari my.telegram.org         |
   | API_HASH  | Dari my.telegram.org         |
   | OWNER_ID  | User ID Telegram kamu        |
   | PORT      | 5000 (Railway otomatis)     |

5. Klik **Deploy** dan tunggu hingga status “Deployed” ✅  

---

## Contoh Command

- `!addproduk <nama> <harga>` → Tambah produk  
- `!editproduk <nama_lama> <nama_baru> <harga_baru>` → Edit produk  
- `!rmproduk <nama>` → Hapus produk  
- `!pricelist` → Lihat daftar harga  
- `!setlink <nama> <link>` → Tambah link VIP  
- `!listlink` → Lihat semua link VIP  
- `!rmlink <nama>` → Hapus link VIP  
- `!sendvip <nama>` → Kirim produk VIP  
- `!takeall` → Ambil semua produk sekaligus  
- `!dana <nama>` → Pembayaran via DANA  
- `!qris <nama>` → Pembayaran via QRIS  
- `!addreply <kata> <balasan>` → Tambah auto reply  
- `!delreply <kata>` → Hapus auto reply  
- `!listreply` → Lihat daftar auto reply  
- `!ping` → Cek bot aktif  
- `!alive` → Info bot aktif  
- `!shutdown` → Matikan bot  
- `!reload` / `!restart` → Restart bot  
- `!cache` → Bersihkan cache internal  
- `!broadcast <pesan>` → Broadcast ke semua grup  

---

## Catatan

- QRIS & DANA bisa menampilkan gambar & nomor agar mudah disalin  
- Produk `take all` akan otomatis mengirim semua produk  
- Pastikan folder `session/` sudah ada untuk Telethon  
- Flask menjaga bot tetap berjalan di Railway  

---

## Support

Kontak Owner Telegram: `@username`
