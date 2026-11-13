# CMOS Electromagnetic Side-Channel Analysis
> **MSc Research Project** • Department of Computer Science, University of Colombo (UoC 24440086)  
> **Author:** Sanjey Asirvatham | **Timeline:** 01 Apr 2026 – 15 Feb 2027

[![Progress](https://img.shields.io/badge/Project_Progress-70.5%25_(Week_33)-brightgreen.svg)](index.html)
[![Live Timeline](https://img.shields.io/badge/Timeline_Dashboard-index.html-blue.svg)](index.html)
[![Hardware](https://img.shields.io/badge/Hardware-HackRF_One_SDR-orange.svg)](https://greatscottgadgets.com/hackrf/one/)

---

## 📌 What is this project?

When digital chips process data, transistor switching draws sudden bursts of current from the power rail. These current spikes radiate subtle electromagnetic (EM) signals that can be picked up nearby with an antenna—a phenomenon known as an **EM side-channel**.

In this project, we:
1. **Simulate** CMOS inverter switching across 4 transistor models (**Level 1, Level 2, BSIM3, and BSIM4**) using LTspice.
2. **Measure** real physical RF emissions at **40 MHz** using an inductive near-field probe and a **HackRF One Software Defined Radio (SDR)**.
3. **Reconcile** the differences between computer simulation models and physical hardware measurements.

---

## 🚀 Project Timeline & Current Progress

We have built an interactive single-page dashboard tracking the full 46-week research plan:

👉 **[Open Interactive Project Timeline (`index.html`)](index.html)**

- **Current Status (13 Nov 2026):** **Week 33 of 46** (Phase 6: IQ Processing & Spectral Analysis)
- **Current Completion:** **70.5%** (~1,068 of 1,514 planned research hours completed)
- **Next Milestone:** Week 35 (IQ processing and spectral evaluation complete)

---

## 💡 Key Findings at a Glance

1. **Directional Switching Asymmetry:**
   CMOS circuits only draw significant power when outputs switch from **$0 \to 1$** (PMOS charging load capacitors from $V_{DD}$). Falling transitions ($1 \to 0$) simply discharge stored charge to ground without drawing current from the supply rail. EM leakage correlates with **rising output bits**, not simple Hamming distance.

2. **The Hardware Ringing Effect (40–50 MHz):**
   While idealized SPICE schematics show clean switching pulses, physical breadboard wiring and IC pins introduce **parasitic inductance** ($\approx 12\ \text{nH}$). Combined with the bus capacitance ($20\ \text{pF}$), this forms an unintended resonant tank that rings at **$\approx 46\ \text{MHz}$**, matching our physical HackRF SDR measurements.

---

## ⚡ Quickstart

### 1. Requirements
```bash
pip install numpy scipy matplotlib python-docx
```

### 2. Run the SDR Signal Processing Pipeline
Processes 5 raw SDR recordings, detects switching bursts, and plots the emission spectra:
```powershell
python "Raw_IQ\run_iq_fft_analysis.py"
```

---

## 📁 Repository Overview

- **[`index.html`](index.html)** — Interactive project timeline dashboard (GitHub Pages ready)
- **[`Methodology/`](../Methodology/)** — In-depth methodology report and Word document (`.docx`)
- **[`Raw_IQ/`](../Raw_IQ/)** — HackRF SDR captures (80 MB binary IQ files) and DSP Python scripts
- **[`Model 1` to `BSIM4`](../)** — LTspice circuit simulation models and current waveforms
- **[`Arduino Code...`](../Arduino%20Code%20for%20Nano%20Hamming%20Distance/)** — Arduino Nano code generating the 4-bit Hamming sequence
