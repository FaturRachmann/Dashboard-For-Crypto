📰 Bloomberg Crypto Lokal 🇮🇩
Bloomberg Crypto Lokal adalah dashboard real-time yang menampilkan informasi pasar kripto terupdate, termasuk:

Harga aset crypto populer

Transaksi besar dari wallet whale

Posisi long/short bernilai besar (≥ $10K)

Berita penting dari berbagai sumber kripto

Ringkasan AI otomatis menggunakan LLM

<p align="center"> <img src="https://github.com/namakamu/bloomberg-local/assets/preview-dashboard.png" alt="Bloomberg Crypto Lokal Screenshot" width="90%"> </p>
🚀 Fitur Utama
Fitur	Keterangan
📈 Harga Crypto	Harga BTC, ETH, SOL dengan perubahan %
🐋 Whale Transactions	Transaksi besar di blockchain dengan dampak & hash
📍 Posisi Long/Short	Posisi leverage besar dengan margin, PnL, dan liquidation
📰 Crypto News	Berita terbaru dari CoinTelegraph, Bitcoin.com, CryptoSlate
🧠 Ringkasan AI	Auto-summarize berita pakai LLM (bisa pakai Groq API atau open-source)
💬 Telegram Bot (opsional)	Kirim ringkasan otomatis ke Telegram (bisa ditambahkan)

🧱 Struktur Folder
perl
Salin
Edit
bloomberg-local/
├── main.py                # Entrypoint (opsional)
├── config.py              # Konfigurasi API Key
├── requirements.txt       # Dependensi
├── ai/
│   └── summarize.py       # Ringkasan berita AI
├── backend/
│   ├── whale_tracker.py   # Simulasi transaksi whale
│   ├── news_feed.py       # Fetch berita dari RSS
│   ├── price_feed.py      # Data harga real-time
│   ├── whale_position.py  # Simulasi posisi long/short
│   └── whale_position_binance.py # Posisi nyata dari Binance
└── dashboard/
    └── app.py             # Streamlit dashboard utama
🛠️ Cara Menjalankan
1. Clone Repositori
bash
Salin
Edit
git clone https://github.com/namakamu/bloomberg-local.git
cd bloomberg-local
2. Install Dependensi
bash
Salin
Edit
pip install -r requirements.txt
3. Jalankan Dashboard
bash
Salin
Edit
streamlit run dashboard/app.py
4. Buka di Browser
text
Salin
Edit
http://localhost:8501
📸 Screenshot


📦 Dependensi Utama
streamlit

pandas

requests

streamlit-autorefresh

📌 Catatan
Ringkasan berita menggunakan model LLM, bisa disesuaikan dengan Groq API, Ollama, atau local model.

Posisi long/short real menggunakan Binance Futures API.

Data whale transaction bersifat simulatif. Bisa diintegrasi dengan Arkham, Dexscreener, atau Etherscan jika diperlukan.

🤝 Kontribusi
Proyek ini open-source. Kamu bisa bantu dengan:

Menambahkan sumber data baru (misalnya CoinGecko, Arkham, Coinglass)

Integrasi AI lokal tanpa Groq

Menambahkan grafik Streamlit atau notifikasi Telegram
