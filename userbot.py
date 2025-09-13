import asyncio
import random
import json
import time
import os
from telethon import TelegramClient, events
from flask import Flask

# --------------------------
# CONFIG TELEGRAM USERBOT
# --------------------------
api_id = int(os.environ.get("API_ID", 19186443))
api_hash = os.environ.get("API_HASH", "8d60cedbb97c6bc03b20376ce8ef3b30")
session_name = 'session/userbot'
OWNER_ID = int(os.environ.get("OWNER_ID", 8081631178))

client = TelegramClient(session_name, api_id, api_hash)

# --------------------------
# DATA FILES
# --------------------------
KODE_FILE = "data/kode.json"
PRODUK_FILE = "data/produk.json"
REPLY_FILE = "data/reply.json"
LINK_FILE = "data/link.json"
START_TIME = time.time()

internal_cache = {
    "temp_transaksi": {},
    "temp_messages": [],
    "session_data": {}
}

# --------------------------
# HELPERS
# --------------------------
def load_json(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def get_uptime():
    seconds = int(time.time() - START_TIME)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"

def get_latency():
    return 100

async def auto_delete(event, delay=2):
    try:
        await asyncio.sleep(delay)
        await event.delete()
    except:
        pass

async def only_owner(event):
    if event.sender_id != OWNER_ID:
        await event.reply("❌ Command ini hanya bisa diakses oleh owner.")
        await auto_delete(event)
        return False
    return True

# --------------------------
# FLASK WEBHOOK
# --------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Babu aktif! 👍"

# --------------------------
# COMMANDS
# --------------------------

# Ping & Alive
@client.on(events.NewMessage(pattern="^!ping$"))
async def ping_handler(event):
    if not await only_owner(event): return
    await event.reply(f"🏓 Pong! Babu aktif.\n⏱ Latency: {get_latency()} ms")
    await auto_delete(event)

@client.on(events.NewMessage(pattern="^!alive$"))
async def alive_handler(event):
    if not await only_owner(event): return
    banner = "╔═════════════════════╗\n      🌟 BABU SEXDES 🌟      \n╚═════════════════════╝"
    info = f"\n🤖 Bot Status : ✅ Aktif\n📦 Versi : 1.0\n⏰ Uptime : {get_uptime()}\n⚡ Latency : {get_latency()} ms"
    await event.reply(f"{banner}{info}")
    await auto_delete(event)

# Shutdown / Reload / Cache
@client.on(events.NewMessage(pattern="^!shutdown$"))
async def shutdown_handler(event):
    if not await only_owner(event): return
    await event.reply("⚠️ Userbot akan dimatikan...")
    await auto_delete(event)
    await client.disconnect()
    import sys; sys.exit(0)

@client.on(events.NewMessage(pattern="^!(reload|restart)$"))
async def restart_handler(event):
    if not await only_owner(event): return
    await event.reply("♻️ Userbot direstart...")
    await auto_delete(event)
    await client.disconnect()
    import sys, os; os.execv(sys.executable, ['python'] + sys.argv)

@client.on(events.NewMessage(pattern="^!cache$"))
async def cache_handler(event):
    if not await only_owner(event): return
    internal_cache["temp_transaksi"].clear()
    internal_cache["temp_messages"].clear()
    internal_cache["session_data"].clear()
    await event.reply("🧹 Sampah internal dibersihkan!")
    await auto_delete(event)

# --------------------------
# Produk Commands
# --------------------------
@client.on(events.NewMessage(pattern="^!addproduk (.+) (.+)"))
async def addproduk(event):
    if not await only_owner(event): return
    nama, harga = event.pattern_match.group(1), event.pattern_match.group(2)
    produk = load_json(PRODUK_FILE)
    produk[nama] = harga
    save_json(PRODUK_FILE, produk)
    await event.reply(f"✅ Produk *{nama}* berhasil ditambahkan!")
    await auto_delete(event)

@client.on(events.NewMessage(pattern="^!rmproduk (.+)"))
async def rmproduk(event):
    if not await only_owner(event): return
    nama = event.pattern_match.group(1)
    produk = load_json(PRODUK_FILE)
    if nama in produk:
        del produk[nama]
        save_json(PRODUK_FILE, produk)
        await event.reply(f"🗑️ Produk *{nama}* berhasil dihapus!")
    else:
        await event.reply("❌ Produk tidak ditemukan!")
    await auto_delete(event)

@client.on(events.NewMessage(pattern="^!pricelist$"))
async def pricelist(event):
    if not await only_owner(event): return
    produk = load_json(PRODUK_FILE)
    msg = "💰 Daftar Harga Produk:\n"
    for nama, harga in produk.items():
        msg += f"{nama} → Rp {harga}\n"
    await event.reply(msg)
    await auto_delete(event)

# --------------------------
# VIP Link Commands
# --------------------------
@client.on(events.NewMessage(pattern="^!setlink (.+) (.+)"))
async def setlink(event):
    if not await only_owner(event): return
    nama, link = event.pattern_match.group(1), event.pattern_match.group(2)
    data = load_json(LINK_FILE)
    data[nama] = link
    save_json(LINK_FILE, data)
    await event.reply(f"✅ Link VIP untuk *{nama}* berhasil disimpan!")
    await auto_delete(event)

@client.on(events.NewMessage(pattern="^!listlink$"))
async def listlink(event):
    if not await only_owner(event): return
    data = load_json(LINK_FILE)
    if data:
        msg = "🔗 Daftar Link VIP:\n"
        for nama, link in data.items():
            msg += f"{nama} → {link}\n"
    else:
        msg = "Belum ada link VIP."
    await event.reply(msg)
    await auto_delete(event)

@client.on(events.NewMessage(pattern="^!rmlink (.+)"))
async def rmlink(event):
    if not await only_owner(event): return
    nama = event.pattern_match.group(1)
    data = load_json(LINK_FILE)
    if nama in data:
        del data[nama]
        save_json(LINK_FILE, data)
        await event.reply(f"🗑️ Link VIP untuk *{nama}* berhasil dihapus!")
    else:
        await event.reply("❌ Link tidak ditemukan!")
    await auto_delete(event)

# --------------------------
# Send VIP Product
# --------------------------
@client.on(events.NewMessage(pattern="^!sendvip (.+)"))
async def sendvip(event):
    if not await only_owner(event): return
    target = event.pattern_match.group(1)
    produk = load_json(PRODUK_FILE)
    links = load_json(LINK_FILE)
    if target.lower() == "take all":
        msg = "💎 Take All VIP:\n\n"
        for nama in produk:
            link = links.get(nama, "Link belum tersedia")
            harga = produk[nama]
            msg += f"*{nama}*\nHarga: Rp `{harga}`\nLink VIP: {link}\n\n"
        await event.reply(msg)
    else:
        if target in produk:
            link = links.get(target, "Link belum tersedia")
            harga = produk[target]
            msg = f"🎉 Produk VIP: *{target}*\nHarga: Rp `{harga}`\nLink VIP: {link}"
            await event.reply(msg)
        else:
            await event.reply("❌ Produk tidak ditemukan!")
    await auto_delete(event)

# --------------------------
# Payment Commands
# --------------------------
@client.on(events.NewMessage(pattern="^!dana (.+)"))
async def dana(event):
    if not await only_owner(event): return
    nama = event.pattern_match.group(1)
    produk = load_json(PRODUK_FILE)
    if nama in produk:
        total = int(produk[nama]) + random.randint(0,999)
        nomor = os.environ.get("NO_DANA", "083820469781")
        pemilik = os.environ.get("NAMA_DANA", "Surya Lesmana")
        await event.reply(
            f"💳 *Pembayaran via DANA*\n\n"
            f"Produk: *{nama}*\n"
            f"Total: Rp `{total}`\n"
            f"Nomor: `{nomor}`\n"
            f"Atas Nama: `{pemilik}`"
        )
    else:
        await event.reply("❌ Produk tidak ditemukan!")
    await auto_delete(event)

@client.on(events.NewMessage(pattern="^!qris (.+)"))
async def qris(event):
    if not await only_owner(event):
        return

    nama = event.pattern_match.group(1)
    produk = load_json(PRODUK_FILE)
    
    if nama in produk:
        total = int(produk[nama]) + random.randint(0, 999)
        # URL gambar QRIS
        qris_image_url = "data/qris.png"  # ganti dengan link QRIS kamu

        msg_text = (
            f"💳 Bayar via QRIS\n"
            f"Produk: *{nama}*\n"
            f"Total: Rp `{total}`"
        )
        # Kirim teks + gambar
        await event.reply(msg_text, file=qris_image_url)
    else:
        await event.reply("❌ Produk tidak ditemukan!")

    await auto_delete(event)

# --------------------------
# Auto Reply
# --------------------------
@client.on(events.NewMessage)
async def auto_reply(event):
    if not await only_owner(event): return
    reply_data = load_json(REPLY_FILE)
    text = event.raw_text.lower()
    if text in reply_data:
        await event.reply(reply_data[text])

# --------------------------
# Help Command
# --------------------------
@client.on(events.NewMessage(pattern="^!help$"))
async def help_handler(event):
    if not await only_owner(event): return
    commands = [
        "🏪 Produk",
        "!addproduk <nama> <harga>",
        "!rmproduk <nama>",
        "!pricelist",
        "",
        "💳 Pembayaran",
        "!dana <nama>",
        "!qris <nama>",
        "",
        "🔗 Link VIP",
        "!setlink <nama> <link>",
        "!listlink",
        "!rmlink <nama>",
        "!sendvip <nama_produk/take all>",
        "",
        "🤖 Auto Reply",
        "!addreply <kata> <balasan>",
        "!delreply <kata>",
        "!listreply",
        "",
        "⚡ Utilitas & Status",
        "!ping",
        "!alive",
        "!shutdown",
        "!reload",
        "!cache",
        "!broadcast <pesan>",
        "!help"
    ]
    await event.reply("📜 Daftar Command Babu Sexdes:\n\n" + "\n".join(commands))
    await auto_delete(event)

# --------------------------
# Start Client for Railway
# --------------------------
async def start_client():
    await client.start()
    print("Userbot siap!")
    await asyncio.Event().wait()  # agar tetap berjalan

loop = asyncio.get_event_loop()
loop.create_task(start_client())

# Flask app siap untuk Railway
PORT = int(os.environ.get("PORT", 5000))