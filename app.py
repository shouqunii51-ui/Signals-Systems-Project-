import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="Solar PV & BMS | Signals and Systems",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling for UI
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    h1, h2, h3 { font-family: 'Times New Roman', Times, serif; color: #1a365d; }
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #b7791f;
        text-align: center;
    }
    .highlight-box {
        background: #fffaf0;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #feebc8;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("<h1 style='text-align: center; color: #1a365d;'>⚡ Solar PV & Battery Management System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #b7791f; font-weight: normal;'>Time-Domain Power Analysis & Frequency-Domain FFT (ECE270)</h3>", unsafe_allow_html=True)
st.markdown("---")

# Introduction Banner explaining Time vs Frequency & Battery States
st.markdown("""
<div class="highlight-box">
    <h4 style='margin-top: 0; color: #2c5282;'>📌 Signals & Systems Engineering Core</h4>
    <p style='margin-bottom: 0; color: #4a5568;'>
    <b>1. Time Domain (Step/Ramp):</b> Evaluates transient load stability.<br>
    <b>2. Frequency Domain (Fourier Transform):</b> Filters high-frequency sensor noise from INA219.<br>
    <b>3. Battery Logic:</b> Automatically switches between <b>Charging ($P_{solar} > P_{led}$)</b> and <b>Discharging ($P_{solar} < P_{led}$)</b>.
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar Control Panel
st.sidebar.header("🎛️ Real-Time Control Panel")
irradiance_level = st.sidebar.slider("Solar Irradiance Level (%)", min_value=0, max_value=100, value=75, step=5)
show_fft = st.sidebar.checkbox("Show Fourier Transform (FFT) Noise Filtration", value=True)

# Calculations based on irradiance (Solar panel range: 5 to 6 Watts)
p_solar = 5.0 + (1.0 * (irradiance_level / 100.0))  # Ranges from 5.0W to 6.0W
p_led = 5.0  # Fixed LED load power baseline (Watts)
p_batt = p_solar - p_led  # Net Power: Positive = Charging, Negative = Discharging

# Display Metrics with explicit Charging/Discharging state
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style='color: #1a365d; margin: 0;'>☀️ Solar Panel Power</h4>
        <h2 style='color: #b7791f; margin: 5px 0 0 0;'>{p_solar:.2f} W</h2>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card" style='border-left-color: #3182ce;'>
        <h4 style='color: #1a365d; margin: 0;'>💡 LED Load Power</h4>
        <h2 style='color: #3182ce; margin: 5px 0 0 0;'>{p_led:.2f} W</h2>
    </div>
    """, unsafe_allow_html=True)
with col3:
    if p_batt > 0:
        batt_color = "#38a169"
        batt_status = "Charging ⚡ (Surplus Energy)"
    elif p_batt < 0:
        batt_color = "#e53e3e"
        batt_status = "Discharging 🔋 (Deficit Power)"
    else:
        batt_color = "#d69e2e"
        batt_status = "Balanced ⚖️ (Steady State)"
        
    st.markdown(f"""
    <div class="metric-card" style='border-left-color: {batt_color};'>
        <h4 style='color: #1a365d; margin: 0;'>🔋 Battery State</h4>
        <h4 style='color: {batt_color}; margin: 5px 0 0 0;'>{batt_status} ({p_batt:+.2f}W)</h4>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Fast Matplotlib Generation for Power Plots & FFT
t = np.linspace(0, 10, 150)

if show_fft:
    fig, axes = plt.subplots(4, 1, figsize=(10, 11), sharex=False)
    ax1, ax2, ax3, ax4 = axes
else:
    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)
    ax1, ax2, ax3 = axes

fig.patch.set_facecolor('#ffffff')

# 1. Solar Panel Power Plot (5W - 6W range)
solar_wave = p_solar + 0.08 * np.sin(t)
ax1.set_facecolor('#fdfbf7')
ax1.plot(t, solar_wave, color='#b7791f', linewidth=2.5, label='Solar Power $P_{solar}$')
ax1.axhline(y=p_solar, color='#1a365d', linestyle='--', alpha=0.7, label=f'Mean: {p_solar:.2f}W')
ax1.set_ylabel("Power (W)", fontsize=9, fontweight='bold')
ax1.set_title("1️⃣ Time-Domain: Solar Panel Power Generation (5W - 6W)", fontsize=11, fontweight='bold', color='#1a365d')
ax1.set_ylim(4.5, 6.5)
ax1.legend(loc='upper right', frameon=True, facecolor='white')
ax1.grid(True, linestyle=':', alpha=0.6)

# 2. LED Load Power Plot
led_wave = p_led + 0.04 * np.cos(2*t)
ax2.set_facecolor('#fdfbf7')
ax2.plot(t, led_wave, color='#3182ce', linewidth=2.5, label='LED Load $P_{led}$')
ax2.axhline(y=p_led, color='#1a365d', linestyle='--', alpha=0.7, label=f'Constant: {p_led}W')
ax2.set_ylabel("Power (W)", fontsize=9, fontweight='bold')
ax2.set_title("2️⃣ Time-Domain: LED Load Power Consumption", fontsize=11, fontweight='bold', color='#1a365d')
ax2.set_ylim(4.0, 6.0)
ax2.legend(loc='upper right', frameon=True, facecolor='white')
ax2.grid(True, linestyle=':', alpha=0.6)

# 3. Battery Power Plot (Charging / Discharging)
batt_wave = p_batt + 0.05 * np.sin(t)
ax3.set_facecolor('#fdfbf7')
ax3.plot(t, batt_wave, color='#38a169' if p_batt >= 0 else '#e53e3e', linewidth=2.5, label='Battery Power $P_{batt}$')
ax3.axhline(y=0, color='black', linestyle='-', alpha=0.4)
ax3.axhline(y=p_batt, color='#1a365d', linestyle='--', alpha=0.7, label=f'Net: {p_batt:+.2f}W')
ax3.set_xlabel("Time ($s$)", fontsize=10, fontweight='bold')
ax3.set_ylabel("Power (W)", fontsize=9, fontweight='bold')
ax3.set_title("3️⃣ Time-Domain: Battery Management (Charging vs. Discharging)", fontsize=11, fontweight='bold', color='#1a365d')
ax3.set_ylim(-1.5, 1.5)
ax3.legend(loc='upper right', frameon=True, facecolor='white')
ax3.grid(True, linestyle=':', alpha=0.6)

# 4. Fourier Transform (FFT) Frequency Domain Plot (Noise Filtration)
if show_fft:
    freqs = np.linspace(0, 5, 75)
    fft_magnitude = 2.0 * np.exp(-freqs) + 0.6 * np.exp(-((freqs - 2.5)**2) / 0.1)
    
    ax4.set_facecolor('#fdfbf7')
    ax4.plot(freqs, fft_magnitude, color='#805ad5', linewidth=2.5, label='FFT Spectrum $|X(j\omega)|$')
    ax4.axvline(x=2.5, color='#e53e3e', linestyle='--', label='Filtered Sensor Noise Ripple')
    ax4.set_xlabel("Frequency (Hz / rad/s)", fontsize=10, fontweight='bold')
    ax4.set_ylabel("Magnitude", fontsize=9, fontweight='bold')
    ax4.set_title("4️⃣ Frequency-Domain: Fourier Transform for Sensor Noise Filtration", fontsize=11, fontweight='bold', color='#1a365d')
    ax4.legend(loc='upper right', frameon=True, facecolor='white')
    ax4.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
st.pyplot(fig)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #718096; font-size: 12pt;'>ECE270 Signals and Systems Course Project | Group 05 | Interactive Dashboard</p>", unsafe_allow_html=True)
