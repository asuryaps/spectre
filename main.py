#!/usr/bin/env python3
"""Asynchronous OSINT reconnaissance and digital footprint extraction tool."""

from __future__ import annotations

import argparse
import asyncio
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup

EMAIL_RE = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")
PHONE_RE = re.compile(r"(?:(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{3,4})")
URL_RE = re.compile(r"https?://[^\s'\"<>]+")


class Color:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


@dataclass(frozen=True)
class Platform:
    name: str
    url_template: str


PLATFORMS = [
    Platform("GitHub", "https://github.com/{username}"),
    Platform("X", "https://x.com/{username}"),
    Platform("Instagram", "https://www.instagram.com/{username}/"),
    Platform("Reddit", "https://www.reddit.com/user/{username}/"),
    Platform("TikTok", "https://www.tiktok.com/@{username}"),
    Platform("Medium", "https://medium.com/@{username}"),
    Platform("Pinterest", "https://www.pinterest.com/{username}/"),
]