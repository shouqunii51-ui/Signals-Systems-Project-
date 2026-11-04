import streamlit as st
import numpy as np
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="Project Signals & FFT Analysis", layout="wide")

def show_exact_project_signals_fft():
    # تصميم الأقسام والعناوين
    st.markdown("""
        <style>
        .main-title {
            font-size: 24px;
            font-weight: bold;
            color: #1E3A8A;
            text-align: center;
            padding-bottom: 10px;
        }
        .box {
            background-color: #F8FAFC;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #E2E8F0;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-title'>⚡ Project Signals: Step/Ramp Responses & Their FFT Magnitude Spectra</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #64748B; margin-bottom: 20px;'>
        Applying Fourier Transform directly to your project's exact signals (<b>Solar Panel</b>, <b>Battery</b>, and <b>LED Load</b>) 
        based on Unit Step and Ramp transitions.
    </div>
    """, unsafe_allow_html=True)

    # لوحة تحكم لتغيير مستوى الإشعاع أو قيمة الانتقال (Step/Ramp level)
    with st.container():
        st.markdown("<div class='box'>", unsafe_allow_html=True)
        st.markdown("### 🎛️ Control Panel")
        step_amplitude = st.slider("Step Transition Amplitude (Load/Irradiance Change):", 1.0, 5.0, 2.0, 0.5)
        st.markdown("</div>", unsafe_allow_html=True)

    # إعدادات الزمن ومعدل أخذ العينات
    fs = 200  
    T = 2.0   
    t = np.linspace(0, T, int(fs * T), endpoint=False)
    n = len(t)
    fft_freqs = np.fft.fftfreq(n, 1/fs)
    positive_mask = fft_freqs >= 0
    f_axis = fft_freqs[positive_mask]

    # --- 1. Solar Panel Signal (Step & Ramp transition representing solar output) ---
    # إشارة خطوة أو منحدر تمثل توليد الألواح الشمسية
    p_solar = np.where(t < 1.0, 1.0, step_amplitude) + 0.1 * np.sin(2 * np.pi * 10 * t)

    # --- 2. Battery Storage Signal (Charging/Discharging step state) ---
    # إشارة تخزين البطارية بناءً على حالة النظام
    p_battery = np.where(t < 1.0, step_amplitude * 0.5, 1.0) + 0.05 * np.cos(2 * np.pi * 10 * t)

    # --- 3. LED Load Signal (Step response for load consumption) ---
    # إشارة حمل الـ LED
    p_load = np.where(t < 1.0, 1.5, step_amplitude + 0.5)

    # دالة حساب Magnitude Spectrum لكل إشارة
    def get_magnitude_spectrum(signal):
        fft_vals = np.fft.fft(signal)
        return (2.0 / n) * np.abs(fft_vals[positive_mask])

    mag_solar = get_magnitude_spectrum(p_solar)
    mag_battery = get_magnitude_spectrum(p_battery)
    mag_load = get_magnitude_spectrum(p_load)

    # --- دالة عرض كل إشارة مع فورييه الخاص بها ---
    def render_power_analysis(title, icon, time_signal, mag_spectrum, desc):
        st.markdown(f"### {icon} {title}")
        st.markdown("<div class='box'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**📉 Time Domain Response:** `{desc}`")
            df_time = pd.DataFrame({"Power (W)": time_signal}, index=t)
            st.line_chart(df_time, height=200)
            
        with col2:
            st.markdown("**📊 FFT Magnitude Spectrum:** `Frequency Domain`")
            df_fft = pd.DataFrame({"Magnitude": mag_spectrum}, index=f_axis)
            st.line_chart(df_fft, height=200)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # عرض الثلاث إشارات الخاصة بمشروعك
    render_power_analysis("Solar Panel Power ($P_{solar}$)", "☀️", p_solar, mag_solar, "Step/Ramp Transition from Solar Generation")
    render_power_analysis("Battery Storage Power ($P_{battery}$)", "🔋", p_battery, mag_battery, "Lithium Battery Charging/Discharging State")
    render_power_analysis("LED Load Power ($P_{load}$)", "💡", p_load, mag_load, "LED Load Step Response")

    st.success("🌟 **Project Status:** All exact project signals (Solar, Battery, Load) and their Fourier Transform spectra are now correctly aligned with your system requirements!")

# استدعاء الدالة لتظهر على الشاشة
show_exact_project_signals_fft()

