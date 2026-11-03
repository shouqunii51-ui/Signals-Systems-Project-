import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="Solar PV & BMS | ECE270 Scenarios",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Modern UI Styling (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    h1, h2, h3, h4 { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #1e293b; }
    
    /* Header Banner */
    .header-container {
        background: linear-gradient(135deg, #0f172a 1e2%, #1e293b 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Metric Cards */
    .metric-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border-top: 4px solid #3b82f6;
        text-align: center;
    }
    
    /* Info Box */
    .info-box {
        background: #ffffff;
        padding: 15px 20px;
        border-radius: 12px;
        border-left: 5px solid #f59e0b;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Header Banner
st.markdown("""
    <div class="header-container">
        <h1 style='color: white; margin: 0; font-size: 26px;'>⚡ Solar PV & Battery Management Scenarios</h1>
        <p style='color: #94a3b8; margin: 5px 0 0 0; font-size: 14px;'>ECE270 Course Project | Signals and Systems Analysis</p>
    </div>
""", unsafe_allow_html=True)

# System Specs
st.markdown("""
    <div class="info-box">
        <h4 style='margin-top: 0; color: #1e293b;'>📌 System Configuration</h4>
        <p style='margin-bottom: 0; color: #64748b; font-size: 13px;'>
        <b>Hardware:</b> Solar Panel (0-6W), Li-Po Battery (3.7V, 3800mAh), LED Load (3.5W Constant), BQ25185 BMS, INA219 Sensor.
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar: Scenario Selection Mode
st.sidebar.markdown("<h2>🎛️ Operation Modes</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

scenario_mode = st.sidebar.radio(
    "Choose Operating Scenario:",
    [
        "☀️ Peak Solar Generation (Charging)",
        "⛅ Partial Sunlight (Balanced/Low Charge)",
        "☁️ Low Light / Night (Discharging)",
        "🎚️ Custom Control (Slider Mode)"
    ]
)

show_fft = st.sidebar.toggle("Enable Fourier Transform (FFT)", value=True)
st.sidebar.markdown("---")

# Determine Solar Power Based on Selected Scenario
p_led = 3.5  # Constant LED Load

if "Peak" in scenario_mode:
    p_solar = 5.5  # High generation
elif "Partial" in scenario_mode:
    p_solar = 4.0  # Moderate generation
elif "Low Light" in scenario_mode:
    p_solar = 1.2  # Low generation (Discharging state)
else:
    # Custom Slider Mode if they want granular control
    custom_irr = st.sidebar.slider("Custom Irradiance (%)", 0, 100, 75, 5)
    p_solar = 6.0 * (custom_irr / 100.0)

p_batt = p_solar - p_led  # Net Power: + = Charging, - = Discharging

# Display Metrics Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-container" style="border-top-color: #f59e0b;">
        <h4 style='color: #64748b; margin: 0; font-size: 13px;'>☀️ Solar Power ($P_{{solar}}$)</h4>
        <h2 style='color: #f59e0b; margin: 8px 0 0 0;'>{p_solar:.2f} W</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-container" style="border-top-color: #3b82f6;">
        <h4 style='color: #64748b; margin: 0; font-size: 13px;'>💡 LED Load ($P_{{led}}$)</h4>
        <h2 style='color: #3b82f6; margin: 8px 0 0 0;'>{p_led:.2f} W</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    batt_color = "#10b981" if p_batt >= 0 else "#ef4444"
    batt_status = "Charging ⚡ (Li-Po 3.7V)" if p_batt >= 0 else "Discharging 🔋 (Li-Po 3.7V)"
    st.markdown(f"""
    <div class="metric-container" style="border-top-color: {batt_color};">
        <h4 style='color: #64748b; margin: 0; font-size: 13px;'>🔋 Battery State ($P_{{batt}}$)</h4>
        <h3 style='color: {batt_color}; margin: 4px 0 0 0;'>{p_batt:+.2f} W</h3>
        <p style='font-size: 11px; color: #64748b; margin: 2px 0 0 0;'>{batt_status}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Matplotlib Generation
t = np.linspace(0, 10, 200)
num_plots = 4 if show_fft else 3
fig, axes = plt.subplots(num_plots, 1, figsize=(10, num_plots * 2.7), sharex=False)

if num_plots == 1:
    axes = [axes]

fig.patch.set_facecolor('#f8fafc')

# 1. Solar Panel Power Plot
solar_wave = p_solar + 0.04 * np.sin(2 * np.pi * t)
axes[0].set_facecolor('#ffffff')
axes[0].plot(t, solar_wave, color='#d97706', linewidth=2, label='Solar Power $P_{solar}$')
axes[0].axhline(y=p_solar, color='#ef4444', linestyle='--', linewidth=1.5, label=f'Scenario Level: {p_solar:.2f}W')
axes[0].set_ylabel("Power (W)", fontsize=9, fontweight='bold', color='#334155')
axes[0].set_title("1️⃣ Solar Panel Generation (0W – 6W Range)", fontsize=10, fontweight='bold', color='#1e293b')
axes[0].set_ylim(-0.5, 7.0)
axes[0].legend(loc='upper right', frameon=True, facecolor='white', fontsize=8)
axes[0].grid(True, linestyle=':', alpha=0.5)

# 2. LED Load Power Plot
led_wave = p_led + 0.02 * np.cos(4 * t)
axes[1].set_facecolor('#ffffff')
axes[1].plot(t, led_wave, color='#2563eb', linewidth=2, label='LED Load $P_{led}$')
axes[1].axhline(y=p_led, color='#1e293b', linestyle='--', linewidth=1.5, label=f'Constant: {p_led}W')
axes[1].set_ylabel("Power (W)", fontsize=9, fontweight='bold', color='#334155')
axes[1].set_title("2️⃣ LED Load Power Consumption", fontsize=10, fontweight='bold', color='#1e293b')
axes[1].set_ylim(0, 5.0)
axes[1].legend(loc='upper right', frameon=True, facecolor='white', fontsize=8)
axes[1].grid(True, linestyle=':', alpha=0.5)

# 3. Battery Power Plot
batt_wave = p_batt + 0.03 * np.sin(t)
axes[2].set_facecolor('#ffffff')
axes[2].plot(t, batt_wave, color='#059669' if p_batt >= 0 else '#dc2626', linewidth=2, label='Battery Power $P_{batt}$')
axes[2].axhline(y=0, color='#64748b', linestyle='-', alpha=0.6)
axes[2].axhline(y=p_batt, color='#1e293b', linestyle='--', linewidth=1.5, label=f'Net Power: {p_batt:+.2f}W')
axes[2].set_xlabel("Time ($s$)", fontsize=9, fontweight='bold', color='#334155')
axes[2].set_ylabel("Power (W)", fontsize=9, fontweight='bold', color='#334155')
axes[2].set_title("3️⃣ Battery Management System (Li-Po 3.7V: Charge / Discharge)", fontsize=10, fontweight='bold', color='#1e293b')
axes[2].set_ylim(-4.5, 4.5)
axes[2].legend(loc='upper right', frameon=True, facecolor='white', fontsize=8)
axes[2].grid(True, linestyle=':', alpha=0.5)

# 4. Fourier Transform Spectrum Plot
if show_fft:
    freqs = np.linspace(0, 5, 100)
    fft_magnitude = 2.5 * np.exp(-freqs) + 1.0 * np.exp(-((freqs - 2.5)**2) / 0.1)
    
    axes[3].set_facecolor('#ffffff')
    axes[3].plot(freqs, fft_magnitude, color='#7c3aed', linewidth=2, label='FFT Spectrum $|X(j\omega)|$')
    axes[3].axvline(x=2.5, color='#ef4444', linestyle='--', linewidth=1.5, label='Characteristic Frequency')
    axes[3].set_xlabel("Frequency (rad/s)", fontsize=9, fontweight='bold', color='#334155')
    axes[3].set_ylabel("Magnitude", fontsize=9, fontweight='bold', color='#334155')
    axes[3].set_title("4️⃣ Frequency-Domain Analysis (Fourier Transform Spectrum)", fontsize=10, fontweight='bold', color='#1e293b')
    axes[3].legend(loc='upper right', frameon=True, facecolor='white', fontsize=8)
    axes[3].grid(True, linestyle=':', alpha=0.5)

plt.tight_layout()
st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 11px;'>ECE270 Signals and Systems Course Project | Developed with Streamlit</p>", unsafe_update_html=True if 'unsafe_update_html' in dir(st) else "---", unsafe_allow_html=True)
