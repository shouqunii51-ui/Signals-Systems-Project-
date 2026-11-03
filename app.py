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

# Custom CSS Styling for High-Speed & Modern UI
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    h1, h2, h3 { font-family: 'Times New Roman', Times, serif; color: #1a365d; }
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
st.markdown("<h3 style='text-align: center; color: #b7791f; font-weight: normal;'>Interactive 3-State Solar Irradiance & BMS Simulation (ECE270)</h3>", unsafe_allow_html=True)
st.markdown("---")

# Introduction Banner
st.markdown("""
<div class="highlight-box">
    <h4 style='margin-top: 0; color: #2c5282;'>📌 Dynamic 3-State Irradiance Control</h4>
    <p style='margin-bottom: 0; color: #4a5568;'>
    Move the slider to simulate <b>3 distinct solar intensity states</b> (Low / Medium / High). Notice how the system's power generation ($P_{solar}$), LED consumption ($P_{led}$), and Battery State instantly adapt in real-time.
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar Control Panel with Instant Response
st.sidebar.header("🎛️ Real-Time Control Panel")
st.sidebar.markdown("Select Solar Irradiance Level:")

# 3 States Slider / Radio mapped instantly
irradiance_state = st.sidebar.select_slider(
    "Solar Irradiance State",
    options=["State 1: Low (Cloudy / Morning)", "State 2: Medium (Partial Sun)", "State 3: High (Peak Sunlight)"],
    value="State 2: Medium (Partial Sun)"
)

# Define parameters based on the selected state for instant calculation
if "Low" in irradiance_state:
    p_solar = 1.2  # Watts
    p_led = 2.5    # Watts
    batt_state = "Discharging 🔋 (Deficit Power)"
    state_color = "#e53e3e"
    voltage_factor = 3.5
elif "Medium" in irradiance_state:
    p_solar = 3.0  # Watts
    p_led = 2.0    # Watts
    batt_state = "Balanced ⚖️ (Stable)"
    state_color = "#d69e2e"
    voltage_factor = 4.5
else:
    p_solar = 5.5  # Watts
    p_led = 1.5    # Watts
    batt_state = "Charging ⚡ (Surplus Energy)"
    state_color = "#38a169"
    voltage_factor = 5.0

# Display Instant Metrics in Columns
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style='color: #1a365d; margin-top: 0;'>☀️ P Solar Panel</h4>
        <h2 style='color: #b7791f; margin: 0;'>{p_solar} W</h2>
    </div>
    """, unsafe_allow_html=True)
with col_m2:
    st.markdown(f"""
    <div class="metric-card" style='border-left-color: #3182ce;'>
        <h4 style='color: #1a365d; margin-top: 0;'>💡 P LED Load</h4>
        <h2 style='color: #3182ce; margin: 0;'>{p_led} W</h2>
    </div>
    """, unsafe_allow_html=True)
with col_m3:
    st.markdown(f"""
    <div class="metric-card" style='border-left-color: {state_color};'>
        <h4 style='color: #1a365d; margin-top: 0;'>🔋 Battery State</h4>
        <h4 style='color: {state_color}; margin: 0;'>{batt_state}</h4>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Fast Matplotlib Plotting responding instantly to the state
t = np.linspace(0, 10, 200)
fig, ax = plt.subplots(figsize=(10, 4.2))
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#fdfbf7')

# Dynamic response curve adjusting instantly to voltage_factor
y = voltage_factor * (1 - np.exp(-1.5 * t) * np.cos(t))

ax.plot(t, y, label=f'System Voltage Response ($P_{{solar}}$ = {p_solar}W)', color=state_color, linewidth=3)
ax.axhline(y=voltage_factor, color='#1a365d', linestyle='--', label=f'Operating Level ({voltage_factor}V)', linewidth=2)

ax.set_title(f"Real-Time System Response under {irradiance_state}", fontsize=12, fontweight='bold', color='#1a365d')
ax.set_xlabel("Time ($s$)", fontsize=10, fontweight='bold')
ax.set_ylabel("Voltage (V)", fontsize=10, fontweight='bold')
ax.set_ylim(0, 6.0)
ax.legend(loc='lower right', frameon=True, facecolor='white', edgecolor='none')
ax.grid(True, linestyle=':', alpha=0.6, color='#cbd5e0')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
st.pyplot(fig)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #718096; font-size: 13pt;'>ECE270 Signals and Systems Course Project | Group 05 | High-Speed Interactive Dashboard</p>", unsafe_allow_html=True)



