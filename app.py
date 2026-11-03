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

# Custom CSS Styling for an Extraordinary UI
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stSidebar {
        background-color: #1e293b;
    }
    h1, h2, h3 {
        font-family: 'Times New Roman', Times, serif;
        color: #1a365d;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #b7791f;
        text-align: center;
    }
    .highlight-box {
        background: #fffaf0;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #feebc8;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("<h1 style='text-align: center; color: #1a365d;'>⚡ Solar PV & Battery Management System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #b7791f; font-weight: normal;'>Dynamic Signal Analysis & Simulation (ECE270 Course Project)</h3>", unsafe_allow_html=True)
st.markdown("---")

# Introduction Banner
st.markdown("""
<div class="highlight-box">
    <h4 style='margin-top: 0; color: #2c5282;'>📌 Project Core Architecture</h4>
    <p style='margin-bottom: 0; color: #4a5568;'>
    This interactive dashboard bridges theoretical <b>Signals and Systems</b> concepts with practical renewable energy hardware. 
    Using standardized test signals (Unit Step & Ramp), we evaluate the transient stability and tracking accuracy of the <b>BQ25185</b> power-path management IC integrated with an <b>INA219</b> sensor.
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar Control Panel
st.sidebar.header("🎛️ Simulation Control Panel")
st.sidebar.markdown("Configure system parameters and test signals interactively:")

signal_type = st.sidebar.selectbox(
    "Select Test Signal", 
    ["Unit Step Response (Sudden Load Change)", "Ramp Response (Gradual Solar Irradiance)"]
)

system_speed = st.sidebar.slider("System Damping / Speed Factor ($\omega_n / \zeta$)", 0.5, 3.0, 1.2)

# Main Computation
t = np.linspace(0, 10, 400)

fig, ax = plt.subplots(figsize=(10, 4.8))
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#fdfbf7')

if "Step" in signal_type:
    # Unit Step Response Calculation
    y = 5.0 * (1 - np.exp(-system_speed * t) * np.cos(2 * t))
    ax.plot(t, y, label='Battery Voltage Output $y(t)$', color='#1f77b4', linewidth=3)
    ax.axhline(y=5.0, color='#e53e3e', linestyle='--', label='Target Stable Voltage (5.0V)', linewidth=2)
    ax.set_title("1️⃣ Unit Step Response: Transient Load Switching Analysis", fontsize=12, fontweight='bold', color='#1a365d')
    ax.set_ylabel("Voltage (V)", fontsize=10, fontweight='bold')
else:
    # Ramp Response Calculation
    input_ramp = 0.5 * t
    output_response = 0.5 * (t - (1/system_speed) * (1 - np.exp(-system_speed * t)))
    ax.plot(t, input_ramp, label='Input Solar Energy Ramp $r(t)$', color='#dd6b20', linestyle='--', linewidth=2.5)
    ax.plot(t, output_response, label='System Tracked Response $y(t)$', color='#38a169', linewidth=3)
    ax.set_title("2️⃣ Ramp Response: Solar Irradiance Tracking Accuracy", fontsize=12, fontweight='bold', color='#1a365d')
    ax.set_ylabel("Amplitude / Voltage", fontsize=10, fontweight='bold')

ax.set_xlabel("Time ($s$)", fontsize=10, fontweight='bold')
ax.legend(loc='lower right', frameon=True, facecolor='white', edgecolor='none')
ax.grid(True, linestyle=':', alpha=0.6, color='#cbd5e0')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
st.pyplot(fig)

st.markdown("---")

# Metric / Info Cards Columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h4 style='color: #1a365d; margin-top: 0;'>📈 Transient Stability (Step Test)</h4>
        <p style='text-align: justify; color: #4a5568;'>
        Demonstrates how the BQ25185 power management IC absorbs sudden load applications, ensuring the output voltage stabilizes rapidly at 5.0V with minimal overshoot and controlled damping.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card" style='border-left-color: #38a169;'>
        <h4 style='color: #1a365d; margin-top: 0;'>📉 Tracking Efficiency (Ramp Test)</h4>
        <p style='text-align: justify; color: #4a5568;'>
        Evaluates the Arduino and INA219 sensor loop's ability to track continuous, gradual environmental shifts (like morning sunrise) without phase lagging or steady-state errors.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #718096; font-size: 13pt;'>ECE270 Signals and Systems Course Project | Group 05 | Developed with Streamlit & Python</p>", unsafe_allow_html=True)


