import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.signal as signal

# ==============================================================================
# 1. LOAD DATASET (MODEL 1 - LEVEL 1 MOSFETS)
# ==============================================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.dirname(script_dir)
data_dir = os.path.join(model_dir, 'data')
images_dir = os.path.join(model_dir, 'images')
os.makedirs(images_dir, exist_ok=True)
txt_file = os.path.join(data_dir, 'Hamming.txt')
if not os.path.exists(txt_file):
    txt_file = os.path.join(data_dir, '4bit-hamming-distance')
if not os.path.exists(txt_file):
    txt_file = os.path.join(model_dir, 'Hamming.txt')
if not os.path.exists(txt_file):
    txt_file = os.path.join(model_dir, '4bit-hamming-distance')

df = pd.read_csv(txt_file, sep='\t')
for c in df.columns:
    df[c] = pd.to_numeric(df[c], errors='coerce')
df = df.dropna().reset_index(drop=True)

time_s = df['time'].values
idd_a = df['-I(VDD)'].values

# ==============================================================================
# 2. PHYSICAL BIOT-SAVART COUPLING & DERIVATIVE dB/dt
# ==============================================================================
mu_0 = 4.0 * np.pi * 1e-7      # Vacuum permeability (H/m)
mu_r = 1.0
mu = mu_0 * mu_r

r1 = 100e-6                    # Outgoing rail distance (100 um)
d = 20e-6                      # Rail separation (20 um)
r2 = r1 + d                    # Return rail distance (120 um)

geom_factor = (mu / (2.0 * np.pi)) * (1.0 / r1 - 1.0 / r2)

num_samples = 60000
t_uniform = np.linspace(0, 6e-6, num_samples)
dt = t_uniform[1] - t_uniform[0]
fs = 1.0 / dt

i_uniform = np.interp(t_uniform, time_s, idd_a)
B_t = geom_factor * i_uniform
dB_dt = np.gradient(B_t, dt)

# ==============================================================================
# 3. FFT ANALYSIS & DOMINANT FREQUENCIES IDENTIFICATION
# ==============================================================================
fft_vals = np.fft.rfft(dB_dt)
freqs = np.fft.rfftfreq(num_samples, dt)
fft_mag = 2.0 * np.abs(fft_vals) / num_samples

mask = (freqs >= 0) & (freqs <= 200e6)
f_sub = freqs[mask]
mag_sub = fft_mag[mask]

# Find prominent spectral peaks
peaks, _ = signal.find_peaks(mag_sub, distance=5, height=np.max(mag_sub) * 0.05)
peak_freqs = f_sub[peaks]
peak_mags = mag_sub[peaks]

# Sort by amplitude to identify top dominant frequencies
sorted_idx = np.argsort(peak_mags)[::-1]
top_n = min(5, len(sorted_idx))
top_f = peak_freqs[sorted_idx][:top_n]
top_m = peak_mags[sorted_idx][:top_n]

# ==============================================================================
# 4. PLOT: DOMINANT FREQUENCIES (WIDEBAND & ZOOMED HARMONIC BAND)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7.5), dpi=300)

# Subplot 1: Wideband Spectrum (0 to 200 MHz) - No Title
ax1.plot(f_sub / 1e6, mag_sub, color='tab:blue', linewidth=1.2, label=r'FFT Spectrum $\left|\mathcal{F}\left\{\frac{dB}{dt}\right\}\right|$')
for i, (pf, pm) in enumerate(zip(top_f, top_m)):
    ax1.plot(pf / 1e6, pm, 'o', color='tab:red', markersize=4 if i > 0 else 7)
ax1.axvline(top_f[0] / 1e6, color='tab:red', linestyle='--', linewidth=1.2, label=f'Peak Dominant: {top_f[0]/1e6:.1f} MHz')
ax1.set_ylabel('Amplitude (T/s)', fontsize=10.5)
ax1.set_xlabel('Frequency (MHz)', fontsize=10.5)
ax1.set_xlim(0, 200)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(bbox_to_anchor=(1.02, 1.0), loc='upper left', frameon=True, borderaxespad=0, fontsize=9.5)

# Subplot 2: Zoomed-in Dominant Frequency Band (Resolving Discrete Harmonics) - No Title
zoom_center = top_f[0] / 1e6
zoom_span = 15.0
zoom_min = max(0, zoom_center - zoom_span)
zoom_max = zoom_center + zoom_span
zoom_mask = (f_sub / 1e6 >= zoom_min) & (f_sub / 1e6 <= zoom_max)

ax2.plot(f_sub[zoom_mask] / 1e6, mag_sub[zoom_mask], color='tab:blue', linewidth=1.2, alpha=0.4, label='Spectrum Envelope')

colors = ['tab:red', 'tab:orange', 'tab:green', 'tab:purple', 'tab:brown']
for rank, (pf, pm, col) in enumerate(zip(top_f, top_m, colors), 1):
    db_c = 20 * np.log10(pm / top_m[0])
    label = f'Dominant {rank}: {pf/1e6:.1f} MHz ({pm:.3f} T/s, {db_c:.2f} dBc)'
    markerline, stemlines, _ = ax2.stem([pf / 1e6], [pm], basefmt=' ', label=label)
    plt.setp(markerline, color=col, markersize=6)
    plt.setp(stemlines, color=col, linewidth=1.5)

ax2.set_ylabel('Amplitude (T/s)', fontsize=10.5)
ax2.set_xlabel('Frequency (MHz)', fontsize=10.5)
ax2.set_xlim(zoom_min, zoom_max)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(bbox_to_anchor=(1.02, 1.0), loc='upper left', frameon=True, borderaxespad=0, fontsize=9.0)

plt.subplots_adjust(hspace=0.28)
output_file = os.path.join(images_dir, '4_dominant_frequencies_biot_savart.png')
fig.savefig(output_file, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"[Model 1] Dominant frequencies plot successfully saved to: {output_file}")

# Print dominant frequencies summary
print("\nTop Dominant Frequencies for Model 1:")
for rank, (pf, pm) in enumerate(zip(top_f, top_m), 1):
    db_c = 20 * np.log10(pm / top_m[0])
    print(f"  Rank {rank}: {pf/1e6:6.2f} MHz | Amplitude: {pm:.4f} T/s | Relative: {db_c:6.2f} dBc")

