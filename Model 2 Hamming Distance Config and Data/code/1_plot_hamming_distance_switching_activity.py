import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.signal as signal

# ==============================================================================
# 1. LOAD DATASET (LEVEL 2 MOSFET MODELS)
# ==============================================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.dirname(script_dir)
data_dir = os.path.join(model_dir, 'data')
images_dir = os.path.join(model_dir, 'images')
os.makedirs(images_dir, exist_ok=True)
data_file = os.path.join(data_dir, 'Hamming.txt')
if not os.path.exists(data_file):
    data_file = os.path.join(data_dir, '4bit-hamming-distance')
if not os.path.exists(data_file):
    data_file = os.path.join(model_dir, 'Hamming.txt')

df = pd.read_csv(data_file, sep='\t')
df.columns = [c.strip() for c in df.columns]

# Ensure robust numeric conversion (filtering any trailing non-numeric rows)
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df = df.dropna().reset_index(drop=True)

# Locate signals
time_s = df['time'].values
time_us = time_s * 1e6
v_hd = df['V(hd)'].values
v_y0 = df['V(y0)'].values
v_y1 = df['V(y1)'].values
v_y2 = df['V(y2)'].values
v_y3 = df['V(y3)'].values

# LTspice supply current leaving VDD source into the 4-bit inverter bank is -I(VDD)
idd_a = df['-I(VDD)'].values
idd_ma = idd_a * 1e3


# ==============================================================================
# PLOT 1: TIME-DOMAIN SWITCHING ACTIVITY ACROSS 4 INVERTERS (Outputs & IDD)
# ==============================================================================
fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(10.5, 6.5), sharex=True, dpi=300)

# Panel 1: Voltages (Hamming Distance Reference & Inverter Outputs Y0-Y3)
ax1.plot(time_us, v_hd, 'k-', linewidth=2.0, label='Hamming Distance Reference V(hd)')
ax1.plot(time_us, v_y0, color='tab:blue', linewidth=1.2, linestyle='--', label='Inverter 0 Output V(y0)')
ax1.plot(time_us, v_y1, color='tab:orange', linewidth=1.2, linestyle=':', label='Inverter 1 Output V(y1)')
ax1.plot(time_us, v_y2, color='tab:green', linewidth=1.2, linestyle='-.', label='Inverter 2 Output V(y2)')
ax1.plot(time_us, v_y3, color='tab:purple', linewidth=1.2, label='Inverter 3 Output V(y3)')
ax1.set_ylabel('Voltage (V)', fontsize=10.5)
ax1.set_ylim(-0.3, 5.5)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(bbox_to_anchor=(1.02, 1.0), loc='upper left', frameon=True, borderaxespad=0, fontsize=9)

# Panel 2: Overall Supply Current IDD across all 4 Inverters
ax2.plot(time_us, idd_ma, color='tab:red', linewidth=1.5, label=r'Overall Supply Current $I_{DD}$ ($-I(VDD)$)')
ax2.set_ylabel('Supply Current (mA)', fontsize=10.5)
ax2.set_xlabel('Time ($\\mu$s)', fontsize=10.5)
ax2.set_xlim(0, 6.0)
ax2.set_ylim(-0.5, 17.5)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(bbox_to_anchor=(1.02, 1.0), loc='upper left', frameon=True, borderaxespad=0, fontsize=9.5)

output_time_domain = os.path.join(images_dir, '1_hamming_switching_activity_with_idd.png')
fig1.savefig(output_time_domain, dpi=300, bbox_inches='tight')
plt.close(fig1)
print(f"[1] Model 2 Hamming switching activity plot saved to: {output_time_domain}")


# ==============================================================================
# PHYSICAL MODEL: BIOT-SAVART TWO-CONDUCTOR LAYOUT MODEL & dB/dt
# ==============================================================================
# Physical Model Assumptions:
# 1. Biot-Savart Law for straight conductors: B = (mu * I) / (2 * pi * r)
# 2. Two straight parallel conducting lines:
#    - Conductor 1: Outgoing line (VDD rail) at distance r1 carrying I(t)
#    - Conductor 2: Return line (GND rail) at distance r2 carrying -I(t)
#    Net magnetic field: B(t) = (mu / 2pi) * (1/r1 - 1/r2) * I(t)
# 3. Induced EMF / Probe voltage: Proportional to dB/dt (Faraday's Law)
# 4. FFT of dB/dt: F{dB/dt}(f) = j * 2*pi*f * F{B}(f)

mu_0 = 4.0 * np.pi * 1e-7      # Vacuum permeability (H/m)
mu_r = 1.0                     # Relative permeability of surrounding dielectric/air
mu = mu_0 * mu_r

r1 = 100e-6                    # Distance to outgoing VDD line (100 um)
d = 20e-6                      # Line separation (20 um)
r2 = r1 + d                    # Distance to return GND line (120 um)

geom_factor = (mu / (2.0 * np.pi)) * (1.0 / r1 - 1.0 / r2)

# Resample transient data onto uniform sub-nanosecond grid (0.1 ns step, 10 GHz sampling)
num_samples = 60000
t_uniform = np.linspace(0, 6e-6, num_samples)
dt = t_uniform[1] - t_uniform[0]  # 0.1 ns
fs = 1.0 / dt                     # 10.0 GHz

i_uniform = np.interp(t_uniform, time_s, idd_a)

# Calculate B(t) and rate of change dB(t)/dt
B_t = geom_factor * i_uniform
dB_dt = np.gradient(B_t, dt)


# ==============================================================================
# PLOT 2: SEPARATE FFT OF dB/dt (FREQUENCY CHARACTERISTICS)
# ==============================================================================
fft_vals = np.fft.rfft(dB_dt)
freqs = np.fft.rfftfreq(num_samples, dt)
fft_mag = 2.0 * np.abs(fft_vals) / num_samples

# State transition rate: 1.0 us per state -> fundamental repetition f0 = 1.0 MHz
f_0 = 1e6
f_peak_idx = np.argmax(fft_mag[1:]) + 1
f_peak = freqs[f_peak_idx]

fig2, (ax_t, ax_f) = plt.subplots(2, 1, figsize=(10.5, 6.5), dpi=300)

# Subplot 1: Time-domain rate of change dB/dt (0 to 6 us window) - No title
ax_t.plot(t_uniform * 1e6, dB_dt / 1e3, color='tab:purple', linewidth=1.2, label=r'$\frac{dB}{dt}$ (Rate of Change)')
ax_t.set_ylabel('dB/dt (kT/s)', fontsize=10.5)
ax_t.set_xlabel('Time ($\\mu$s)', fontsize=10.5)
ax_t.set_xlim(0, 6.0)
ax_t.grid(True, linestyle='--', alpha=0.5)
ax_t.legend(bbox_to_anchor=(1.02, 1.0), loc='upper left', frameon=True, borderaxespad=0, fontsize=9.5)

# Subplot 2: Frequency Spectrum (FFT of dB/dt up to 200 MHz) - No title, No arrow
freq_limit = 200e6             # 200 MHz
f_mask = (freqs >= 0) & (freqs <= freq_limit)

ax_f.plot(freqs[f_mask] / 1e6, fft_mag[f_mask], color='tab:blue', linewidth=1.2, label=r'FFT Magnitude $\left|\mathcal{F}\left\{\frac{dB}{dt}\right\}\right|$')
ax_f.axvline(f_peak / 1e6, color='tab:red', linestyle='--', linewidth=1.2, label=f'Peak Resonance: {f_peak/1e6:.1f} MHz')

ax_f.set_ylabel('Amplitude (T/s)', fontsize=10.5)
ax_f.set_xlabel('Frequency (MHz)', fontsize=10.5)
ax_f.set_xlim(0, 200)
ax_f.grid(True, linestyle='--', alpha=0.5)
ax_f.legend(bbox_to_anchor=(1.02, 1.0), loc='upper left', frameon=True, borderaxespad=0, fontsize=9.5)

output_fft = os.path.join(images_dir, '2_fft_hamming_biot_savart.png')
fig2.savefig(output_fft, dpi=300, bbox_inches='tight')
plt.close(fig2)
print(f"[2] Model 2 FFT frequency characteristics plot saved to: {output_fft}")


# ==============================================================================
# PLOT 3: SEPARATE SPECTROGRAM OF dB/dt (GRIDSPEC DEDICATED CAX, ZERO OVERLAP)
# ==============================================================================
# High-resolution Short-Time Fourier Transform (STFT) for megahertz-band transient emissions
nperseg = 1024
noverlap = 960
nfft = 4096

f_spec, t_spec, Sxx = signal.spectrogram(
    dB_dt,
    fs=fs,
    nperseg=nperseg,
    noverlap=noverlap,
    nfft=nfft,
    window='hann'
)

# Convert power spectral density to normalized decibels (dB)
Sxx_db = 10.0 * np.log10(np.maximum(Sxx, 1e-25))
max_psd = np.max(Sxx_db)
Sxx_norm = Sxx_db - max_psd    # Normalized to 0 dB peak

# Filter visualization window (0 to 6 us, 0 to 200 MHz)
t_mask_spec = t_spec <= 6e-6
f_mask_spec = f_spec <= 200e6

fig3 = plt.figure(figsize=(11, 7), dpi=300)
gs = fig3.add_gridspec(
    2, 2,
    width_ratios=[1, 0.03],
    height_ratios=[1, 2],
    wspace=0.06,
    hspace=0.15
)

ax_w = fig3.add_subplot(gs[0, 0])
ax_s = fig3.add_subplot(gs[1, 0], sharex=ax_w)
cax = fig3.add_subplot(gs[:, 1])

# Top Subplot: Synchronized time-domain dB/dt signal - No title
ax_w.plot(t_uniform * 1e6, dB_dt / 1e3, color='tab:purple', linewidth=1.2, label=r'$\frac{dB}{dt}$')
ax_w.set_ylabel('dB/dt (kT/s)', fontsize=10.5)
ax_w.grid(True, linestyle='--', alpha=0.5)
ax_w.legend(loc='upper right', framealpha=0.9, fontsize=9.5)

# Bottom Subplot: Spectrogram heatmap - No title
t_grid_us = t_spec[t_mask_spec] * 1e6
f_grid_mhz = f_spec[f_mask_spec] / 1e6
Sxx_sub = Sxx_norm[np.ix_(f_mask_spec, t_mask_spec)]

pcol = ax_s.pcolormesh(
    t_grid_us,
    f_grid_mhz,
    Sxx_sub,
    shading='gouraud',
    cmap='inferno',
    vmin=-60,
    vmax=0
)

ax_s.set_ylabel('Frequency (MHz)', fontsize=10.5)
ax_s.set_xlabel('Time ($\\mu$s)', fontsize=10.5)
ax_s.set_xlim(0, 6.0)
ax_s.set_ylim(0, 200)
ax_s.grid(True, linestyle='--', alpha=0.3)

# Colorbar in dedicated isolated cax with independent positioning
cbar = fig3.colorbar(pcol, cax=cax)
cbar.set_label('Normalized Power Spectral Density (dB)', fontsize=9.5)

fig3.subplots_adjust(top=0.96, bottom=0.10, left=0.10, right=0.90)

output_spectrogram = os.path.join(images_dir, '3_spectrogram_hamming_biot_savart.png')
fig3.savefig(output_spectrogram, dpi=300, bbox_inches='tight')
plt.close(fig3)
print(f"[3] Model 2 Spectrogram plot saved to: {output_spectrogram}")


# ==============================================================================
# SUMMARY CONSOLE METRICS
# ==============================================================================
print("\n" + "="*70)
print("MODEL 2: FREQUENCY & TIME-FREQUENCY CHARACTERISTICS (Level 2 dB/dt)")
print("="*70)
print(f"• State Duration / Transition Interval: 1.0 us")
print(f"• State Switching Repetition Rate:       {f_0/1e6:.1f} MHz")
print(f"• Peak Supply Current (IDD,max):        {np.max(idd_a)*1e3:.2f} mA (at t = 5.0 us, HD = 4)")
print(f"• Peak Magnetic Field B(t) Amplitude:    {np.max(B_t)*1e6:.2f} uT")
print(f"• Peak Rate of Change |dB/dt|:          {np.max(np.abs(dB_dt))/1e3:.2f} kT/s ({np.max(np.abs(dB_dt)):.1f} T/s)")
print(f"• Peak Spectral Resonance Frequency:    {f_peak/1e6:.1f} MHz")
print(f"• Spectrogram STFT Window (nperseg):    {nperseg} samples ({nperseg*dt*1e9:.1f} ns)")
print(f"• Spectrogram Overlap:                  {noverlap/nperseg*100:.1f}% ({noverlap} samples)")
print("="*70)

