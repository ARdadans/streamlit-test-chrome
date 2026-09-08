import os
import sys
import subprocess
import logging
from typing import Dict, Any, Tuple
from patchright.sync_api import sync_playwright

logger = logging.getLogger(__name__)


def ensure_linux_browser() -> str:
    """
    Ensures a working Chromium browser is available on Linux (Streamlit Cloud).
    Checks for system-installed binaries first. If none are found, installs
    Patchright's self-contained Chromium via Python without requiring apt or root.
    """
    candidate_paths = [
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
    ]
    for path in candidate_paths:
        if os.path.exists(path) and os.access(path, os.X_OK):
            return path

    # Auto-install Patchright Chromium without apt-get
    try:
        subprocess.run(
            [sys.executable, "-m", "patchright", "install", "chromium"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception as e:
        logger.warning(f"Could not run patchright install chromium: {e}")
    return ""


def get_browser_launch_config() -> Dict[str, Any]:
    """
    Returns the launch configuration for Patchright:
    - Windows / macOS (local dev): Uses locally installed Chrome (channel='chrome', zero download).
    - Linux (Streamlit Cloud): Uses system Chromium or Patchright's self-contained browser.
    """
    is_linux = sys.platform.startswith("linux")

    if is_linux:
        executable = ensure_linux_browser()
        linux_args = [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--no-first-run",
            "--no-zygote",
        ]
        config: Dict[str, Any] = {"args": linux_args}
        if executable:
            config["executable_path"] = executable
        return config
    else:
        # Local Development (Windows / macOS)
        return {
            "channel": "chrome",
        }


def capture_page_screenshot(
    url: str = "https://duck.ai/",
    output_path: str = "duck_ai_screenshot.png",
    wait_seconds: int = 4,
    viewport_width: int = 1280,
    viewport_height: int = 800,
    headless: bool = True,
) -> Tuple[str, str, bytes]:
    """
    Loads a URL and captures a screenshot using Patchright.

    Returns:
        (page_title, browser_info, screenshot_bytes)
    """
    config = get_browser_launch_config()
    config["headless"] = headless

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(**config)
            browser_info = config.get("executable_path") or f"channel: {config.get('channel', 'patchright-chromium')}"
        except Exception as err:
            # Fallback for local Windows if Chrome channel isn't registered: try Edge
            if not sys.platform.startswith("linux"):
                config.pop("channel", None)
                config["channel"] = "msedge"
                browser = p.chromium.launch(**config)
                browser_info = "channel: msedge (fallback)"
            else:
                raise err

        context = browser.new_context(
            viewport={"width": viewport_width, "height": viewport_height},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        )
        page = context.new_page()

        # Navigate to target
        page.goto(url, timeout=45000, wait_until="domcontentloaded")

        # Wait for dynamic elements / JavaScript rendering
        if wait_seconds > 0:
            page.wait_for_timeout(wait_seconds * 1000)

        title = page.title()
        screenshot_bytes = page.screenshot(path=output_path, full_page=False)

        browser.close()
        return title, browser_info, screenshot_bytes
