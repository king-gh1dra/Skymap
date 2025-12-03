<div align="center">

# 🐉 Skyrim Nmap GUI


<img src="https://github.com/user-attachments/assets/943ad9c2-630a-47e0-b20b-38d01f538734" width="500" alt="Skyrim Scanner Logo">

<br/>

**A fantasy-themed graphical interface for Nmap port scanning, inspired by The Elder Scrolls UI.**
*Reconnaissance should feel like a quest.*

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Nmap](https://img.shields.io/badge/Tool-Nmap-blueviolet?style=for-the-badge)](https://nmap.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## 📜 Overview

**Skyrim Nmap GUI** (The Elder Scans) is a Python-based graphical frontend for the Nmap port scanner. It replaces complex command-line flags with themed scan presets and a UI that mimics the "System Menu" from Skyrim.

This project was built for cybersecurity practice, UI creativity, and to make network enumeration feel less like work and more like delving into a Dwemer ruin.

<div align="center">
  
</div>

## ✨ Features

### ⚔️ Immersive Interface
- **Parchment-Style Output:** Scan results appear on an aged scroll background with "ink" typography.
- **Themed UI Elements:** Labels like *THU'UM SCANNER*, *Active Runes*, and *Custom Spells*.
- **Atmospheric Feedback:** Scan status updates range from "Focusing Magicka..." to "Ritual Complete."

### 🔮 Sorcerous Functionality
- **Live Nmap Control:** Runs real `nmap` scans in the background using threading (non-blocking UI).
- **Runes (Toggles):** Quickly enable common flags:
    - `Version (-sV)`
    - `Scripts (-sC)`
    - `OS Detect (-O)`
- **Custom Spells:** A dedicated input field for raw Nmap arguments (e.g., `-p- -T4 --script vuln`).

### 🔗 Magic Hyperlinks
- **Interactive Scroll:** The scroll is not just text—it is alive.
- **Auto-Linking:** Regex automatically detects open ports (`80/tcp`) and URLs found in script output.
- **One-Click Access:** Clicking a port automatically launches Firefox (or your default browser) to `http://<target>:<port>`.

---

## 🛠️ Prerequisites

To cast these spells, you must have the following installed on your system:

1.  **Python 3.x** (with `tkinter` included, which is standard).
2.  **Nmap** must be installed and in your system PATH.

**Installing Nmap:**
- **Linux:** `sudo apt install nmap`
- **MacOS:** `brew install nmap`


## 📥 Installation

```bash
# 1. Clone the repository
git clone https://github.com/king-gh1dra/Skymap

# 2. Enter the dungeon
cd Skymap

# 3. Cast the spell
python3 skymap.py
