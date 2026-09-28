import os
import re
import json
import hashlib
import requests
from playwright.sync_api import sync_playwright

PAGE_NAME = "เทรดเดอร์หน้าหมีแต่ชอบหมา"
PAGE_URL = "https://www.facebook.com/BearFaceTrader"
STORAGE_FILE = "last_post.json"
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
FB_COOKIES_RAW = os.environ.get("FB_COOKIES")

def clean_and_deduplicate_text(raw_text):
    lines = raw_text.split("\n")
    cleaned_lines = []
    
    garbage_keywords = [
        "view more comments", "ดูความคิดเห็นเพิ่มเติม", "เทรดเดอร์หน้าหมีแต่ชอบหมา",
        "like", "comment", "share", "top fan", "see more", "see less", "just now", "all reactions",
        "ผู้ติดตาม", "ถูกใจ", "แชร์", "ความคิดเห็น", "ดูเพิ่มเติม", "all reactions:",
        "เขียนความคิดเห็น...", "write a comment...", "subscriber", "ผู้ติดตามตัวยง",
        "ดูน้อยลง", "แก้ไขแล้ว"
    ]
    
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped == "-":
            continue
        lower = stripped.lower()
        if stripped.isdigit():
            continue
        if re.match(r"^(\d+\s*(m|h|d|min|mins|minutes|hours|days|ชม\.|นาที|ชั่วโมง)|about an hour ago|yesterday|เมื่อสักครู่).*$", lower):
            continue
        if any(c in lower for c in
