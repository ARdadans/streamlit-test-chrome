import os
import sys
import time
from pathlib import Path
import streamlit as st

# Ensure local package can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from streamlit_test_chrome.browser import capture_page_screenshot, get_browser_launch_config

# Page configuration
st.set_page_config(
    page_title="Streamlit + Patchright Browser Automation",
    page_icon="🦆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #DE5833, #FF8A00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .badge-info {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        background: rgba(222, 88, 51, 0.15);
        color: #FF8A00;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Detect Environment
is_linux = sys.platform.startswith("linux")
env_name = "Linux (Streamlit Cloud / Docker)" if is_linux else f"Local Dev ({sys.platform})"
browser_strategy = (
    "Patchright Chromium (Auto-installed)" if is_linux else "Google Chrome Lokal (channel='chrome')"
)

# Sidebar
with st.sidebar:
    st.image("https://duckduckgo.com/assets/logo_homepage.alt.v108.svg", width=180)
    st.markdown("### ⚙️ Pengaturan Browser")
    st.markdown(f"**Lingkungan:** `{env_name}`")
    st.markdown(f"**Browser Target:** `{browser_strategy}`")
    st.markdown("---")

    headless_mode = st.checkbox(
        "Headless Mode",
        value=True,
        help="Hilangkan centang jika ingin melihat jendela browser terbuka saat pengujian di PC lokal.",
    )

    wait_seconds = st.slider(
        "Waktu Tunggu JS (Detik)",
        min_value=1,
        max_value=15,
        value=4,
        help="Beri waktu beberapa detik agar konten dinamis JavaScript Duck.ai selesai dimuat.",
    )

    resolution_choice = st.selectbox(
        "Resolusi Viewport",
        ["1280 x 800 (HD)", "1920 x 1080 (FHD)", "1024 x 768 (Standar)"],
        index=0,
    )
    if "1920" in resolution_choice:
        vw, vh = 1920, 1080
    elif "1024" in resolution_choice:
        vw, vh = 1024, 768
    else:
        vw, vh = 1280, 800

    st.markdown("---")
    st.caption("⚡ Didukung oleh **Patchright** (Anti-detection Playwright fork)")

# Header
st.markdown('<div class="main-header">🦆 Duck.ai Browser Screenshot with Patchright</div>', unsafe_allow_html=True)
st.markdown(
    '<div><span class="badge-info">Patchright Stealth</span>'
    f'<span class="badge-info">{env_name}</span>'
    '<span class="badge-info">Zero-Download on Dev</span></div>',
    unsafe_allow_html=True,
)
st.markdown("")

# URL Input
col_url, col_btn = st.columns([4, 1])
with col_url:
    target_url = st.text_input(
        "Target URL:",
        value="https://duck.ai/",
        placeholder="https://duck.ai/",
        label_visibility="collapsed",
    )
with col_btn:
    trigger_btn = st.button("📸 Ambil Screenshot", type="primary", use_container_width=True)

st.markdown("---")

# Session state to hold screenshot results
if "screenshot_data" not in st.session_state:
    st.session_state.screenshot_data = None
if "page_title" not in st.session_state:
    st.session_state.page_title = None
if "meta_info" not in st.session_state:
    st.session_state.meta_info = None

# Action execution
if trigger_btn:
    with st.status("🚀 Menjalankan browser dengan Patchright...", expanded=True) as status:
        st.write("1. Menginisialisasi browser engine (memakai Chrome lokal di dev)...")
        start_time = time.time()

        try:
            st.write(f"2. Mengarahkan browser ke `{target_url}`...")
            title, browser_info, img_bytes = capture_page_screenshot(
                url=target_url,
                output_path="duck_ai_screenshot.png",
                wait_seconds=wait_seconds,
                viewport_width=vw,
                viewport_height=vh,
                headless=headless_mode,
            )

            duration = round(time.time() - start_time, 2)
            st.session_state.screenshot_data = img_bytes
            st.session_state.page_title = title
            st.session_state.meta_info = {
                "title": title,
                "browser": browser_info,
                "duration": f"{duration}s",
                "resolution": f"{vw}x{vh}",
                "size_kb": f"{round(len(img_bytes) / 1024, 1)} KB",
            }

            status.update(
                label=f"✅ Berhasil! Halaman dimuat dalam {duration} detik.",
                state="complete",
                expanded=False,
            )
        except Exception as e:
            status.update(label="❌ Gagal mengambil screenshot.", state="error")
            st.error(f"Terjadi kesalahan saat menjalankan browser: {e}")

# Display Results
if st.session_state.screenshot_data:
    meta = st.session_state.meta_info

    # Info summary
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Judul Halaman", meta["title"][:28] + "..." if len(meta["title"]) > 28 else meta["title"])
    with m2:
        st.metric("Browser Digunakan", meta["browser"])
    with m3:
        st.metric("Resolusi", meta["resolution"])
    with m4:
        st.metric("Ukuran & Waktu", f"{meta['size_kb']} ({meta['duration']})")

    st.markdown("### 🖼️ Hasil Tangkapan Layar:")
    st.image(
        st.session_state.screenshot_data,
        caption=f"Screenshot dari {target_url} — {meta['title']}",
        use_container_width=True,
    )

    # Download Button
    st.download_button(
        label="⬇️ Unduh Screenshot (PNG)",
        data=st.session_state.screenshot_data,
        file_name="duck_ai_screenshot.png",
        mime="image/png",
    )
else:
    # Initial state / guide
    st.info("💡 Klik tombol **'📸 Ambil Screenshot'** di atas untuk mulai mengambil screenshot dari https://duck.ai/ menggunakan Patchright.")

# Cloud compatibility footer
with st.expander("☁️ Informasi Kompatibilitas Streamlit Cloud"):
    st.markdown("""
    **Proyek ini telah dikonfigurasi 100% kompatibel dengan Streamlit Cloud:**
    
    1. **Bebas Error APT:** Tidak menggunakan `packages.txt` sehingga terhindar dari error repository Debian yang expired di Streamlit Cloud.
    2. **Self-Contained Chromium:** Di Streamlit Cloud (Linux), browser Chromium diunduh secara mandiri oleh Patchright ke direktori cache user via Python tanpa butuh akses root/apt.
    3. **Local Development (Windows):** Tetap menggunakan Google Chrome lokal (`channel="chrome"`) tanpa download tambahan.
    4. **Anti-Detection:** Menembus proteksi Cloudflare dan bot detection secara *out-of-the-box*.
    """)
