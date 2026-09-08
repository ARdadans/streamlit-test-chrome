# Streamlit + Patchright Browser Automation

Aplikasi Streamlit untuk otomasi browser menggunakan **[Patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright)** (patched undetected Playwright).

---

## ✨ Fitur Utama

- **Zero-Download pada Local Dev:** Di Windows / macOS, otomatis memakai Google Chrome yang sudah terpasang di PC Anda (`channel="chrome"`).
- **100% Kompatibel dengan Streamlit Cloud:** Menggunakan [`packages.txt`](packages.txt) untuk instalasi otomatis `chromium` dan `chromium-driver` di Linux container.
- **Stealth / Anti-Bot Detection:** Bypass proteksi bot dan Cloudflare secara bawaan tanpa konfigurasi rumit.
- **Target Demo:** Mengambil screenshot lengkap dari [https://duck.ai/](https://duck.ai/) dan menyediakannya untuk diunduh langsung via UI Streamlit.

---

## 🚀 Cara Menjalankan Secara Lokal

```bash
uv run streamlit run app.py
```

Aplikasi akan terbuka di browser Anda: `http://localhost:8501`.

---

## ☁️ Deployment ke Streamlit Community Cloud

1. Push repository ini ke GitHub.
2. Buka [share.streamlit.io](https://share.streamlit.io/) dan pilih repository ini.
3. Set file utama ke `app.py`.
4. Streamlit Cloud akan otomatis membaca [`packages.txt`](packages.txt) untuk memasang Chromium Linux, dan script Python akan otomatis mendeteksi environment cloud tersebut.

---

## 📁 Struktur File

```
streamlit-test-chrome/
├── .streamlit/
│   └── config.toml          # Konfigurasi Streamlit
├── src/
│   └── streamlit_test_chrome/
│       ├── __init__.py      # Script entrypoint
│       └── browser.py       # Engine Patchright dengan deteksi Local/Cloud
├── app.py                   # Dashboard interaktif Streamlit
├── packages.txt             # Dependensi sistem Linux untuk Streamlit Cloud
├── pyproject.toml           # Dependensi Python uv
└── uv.lock
```
