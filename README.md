# NFC Card Reader

A Python-based NFC card reader designed to read student card identifiers
using the ACS ACR122U USB reader.

This project provides a foundation for student identification and
attendance management. It uses the PC/SC
smart card interface through the `pyscard` Python library.

## Features

- **NFC Reader Detection** — Detects available smart card readers.
- **Card UID Reading** — Attempts to read the UID of a compatible card.
- **Real-Time Scanning** — Monitors the reader for card interactions.
- **CSV Logging** — Records card scans with timestamps and reader names.
- **Duplicate Scan Handling** — Reduces repeated logging while a card
  remains on the reader.
- **Windows Compatibility** — Designed for Windows environments
  supporting the PC/SC smart card interface.

## Technology Stack

- Python
- pyscard
- PC/SC Smart Card API
- ACS ACR122U USB NFC Reader
- CSV for scan logging

## Requirements

### Hardware

- Windows PC or laptop
- ACS ACR122U USB NFC Reader
- Compatible contactless student card

### Software

- Python 3.x
- Appropriate reader driver, if required
- Windows Smart Card service
- Python package: `pyscard`

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/N044/NFC-Card-Automation-or-Automation-Test
