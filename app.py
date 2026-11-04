import streamlit as st
import numpy as np
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="Renewable Energy & FFT Analysis", layout="wide")

def show_three_powers_analysis():
    # تصميم مخصص للواجهة عبر CSS
    st.markdown("""
        <style>
        .main-title {
            font-size: 26px;
            font-weight: bold;
            color: #1E3A8A;
            text-align: center;
            padding-bottom: 10px;
        }
        .section-box {
            background-color: #F8FAFC;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # العنوان الرئيسي
    st.markdown("<div class='main-title'>⚡ System-Wide Power & Magnitude Spectrum Analysis</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #64748B; margin-bottom: 25px;'>
        Analyzing how changing <b>Solar Irradiance</b> dynamically impacts power generation, storage response, and load regulation 
        across <b>Solar Panel</b>, <b>Battery</b>, and <b>LED Load</b> alongside their FFT Magnitude Spectra.
    </div>
    """, unsafe_allow_html=True)

    # لوحة التحكم بسلايدر واحد لشدة الإضاءة يتحكم بالنظام كاملاً
    with st.container():
        st.markdown("<div class='section-box'>", unsafe_allow_html=True)
        st.markdown("### 🎛️ System Control Panel")
        
        irradiance = st.slider(
            "Solar Irradiance / Light Intensity Level:", 
            min_value=0.5, max_value=3.0, value=1.5, step=0.1,
            help="Controls the primary light intensity hitting the solar panel and affects the entire system."
        )
        
        st.markdown("</div>", unsafe_allow_html=True)

    # إعدادات الزمن ومعدل أخذ العينات
    fs = 200  
    T = 2.0   
    t = np.linspace(0, T, int(fs * T), endpoint=False)
    n = len(t)
    fft_freqs = np.fft.fftfreq(n, 1/fs)
    positive_mask = fft_freqs >= 0
    f_axis = fft_freqs[positive_mask]

    # --- 1. Solar Panel Power ($P_{solar}$) ---
    solar_transition = np.where(t < 1.0, 1.0 * irradiance, 1.8 * irradiance)
    solar_noise = 0.1 * np.random.normal(0, 1, n)
    p_solar = solar_transition + solar_noise

    # --- 2. Battery Storage Power ($P_{battery}$) ---
    # البطارية تتفاعل عكسياً أو تدعم النظام عند تغير الإشعاع لتخفيف التذبذبات
    battery_transition = np.where(t < 1.0, 0.8 / irradiance, 0.5 * irradiance)
    p_battery = battery_transition + (0.5 * solar_noise)

    # --- 3. LED Load Power ($P_{load}$) ---
    # الحمل يظل مستقراً ومُنظماً قدر الإمكان بفضل المنظم
    load_transition = np.where(t < 1.0, 2.0, 2.3)
    p_load = load_transition + 0.05 * np.sin(2 * np.pi * 15 * t)

    # دالة لحساب Magnitude Spectrum
    def compute_magnitude_spectrum(signal):
        fft_vals = np.fft.fft(signal)
        return (2.0 / n) * np.abs(fft_vals[positive_mask])

    mag_solar = compute_magnitude_spectrum(p_solar)
    mag_battery = compute_magnitude_spectrum(p_battery)
    mag_load = compute_magnitude_spectrum(p_load)

    # --- دالة عرض كل مكون بتصميم منظم ---
    def render_signal_section(title, icon, p_signal, m_signal, desc_time, desc_fft):
        st.markdown(f"### {icon} {title}")
        st.markdown("<div class='section-box'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**📉 Time Domain:** `{desc_time}`")
            df_time = pd.DataFrame({"Power (W)": p_signal}, index=t)
            st.line_chart(df_time, height=200)
            
        with col2:
            st.markdown(f"**📊 Magnitude Spectrum:** `{desc_fft}`")
            df_fft = pd.DataFrame({"Magnitude": m_signal}, index=f_axis)
            st.line_chart(df_fft, height=200)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # عرض الأقسام الثلاثة بالترتيب
    render_signal_section(
        "1. Solar Panel Power Source ($P_{solar}$)", 
        "☀️", 
        p_solar, mag_solar, 
        "Scaled by Irradiance Level + Environmental Noise", 
        "Source Frequency Spectrum & Harmonics"
    )

    render_signal_section(
        "2. Battery Storage Response ($P_{battery}$)", 
        "🔋", 
        p_battery, mag_battery, 
        "Buffer & Damping Response to Irradiance Changes", 
        "Storage Spectrum & Smoothed Ripples"
    )

    render_signal_section(
        "3. LED Load Output ($P_{load}$)", 
        "💡", 
        p_load, mag_load, 
        "Regulated & Stable Power Delivery", 
        "Filtered Spectrum (Minimal Harmonics)"
    )

    st.markdown("---")
    st.success(f"🌟 **Engineering Status:** Irradiance set to **{irradiance}**. All three power signals and their respective *Magnitude Spectra* update simultaneously to demonstrate complete system behavior!")

# استدعاء الدالة لتظهر على الشاشة
show_three_powers_analysis()

     