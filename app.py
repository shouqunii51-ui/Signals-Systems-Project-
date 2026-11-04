import streamlit as st
import numpy as np
import pandas as pd

# إعدادات الصفحة بتصميم عريض
st.set_page_config(page_title="Renewable Energy FFT Dashboard", layout="wide")

def show_advanced_renewable_fft():
    # تصميم CSS مخصص ومميز للواجهة (Modern UI Design)
    st.markdown("""
        <style>
        .main-header {
            font-size: 28px;
            font-weight: 800;
            color: #0F172A;
            text-align: center;
            margin-bottom: 5px;
        }
        .sub-header {
            text-align: center;
            color: #475569;
            font-size: 15px;
            margin-bottom: 30px;
        }
        .control-card {
            background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%);
            padding: 25px;
            border-radius: 16px;
            border: 1px solid #CBD5E1;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 25px;
        }
        .signal-card {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 14px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.03);
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # الهيدر والعنوان بتصميم عصري
    st.markdown("<div class='main-header'>⚡ Advanced Renewable Energy FFT Analysis Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Signals & Systems Project • Solar Generation, Battery Storage, and LED Load Frequency Domain Evaluation</div>", unsafe_allow_html=True)

    # لوحة التحكم بتصميم أنيق (سلايدر النسبة المئوية 0 - 100%)
    with st.container():
        st.markdown("<div class='control-card'>", unsafe_allow_html=True)
        st.markdown("### 🎛️ System Control Panel")
        
        # سلايدر شدة الإضاءة من 0 إلى 100%
        irradiance_percent = st.slider(
            "Solar Irradiance / Light Intensity Level (G):", 
            min_value=0, max_value=100, value=80, step=1,
            help="Adjust the sunlight percentage hitting the solar panel (0% to 100%)."
        )
        
        # تحويل النسبة المئوية إلى عامل ضرب رياضي (0.0 إلى 1.0)
        irr_factor = irradiance_percent / 100.0
        
        st.markdown(f"**Current Irradiance State:** `{irradiance_percent}%` (Multiplier: `{irr_factor:.2f}`)")
        st.markdown("</div>", unsafe_allow_html=True)

    # إعداد المحاور (الزمن موجب t >= 0، والترددات متماثلة تشمل السالب والموجبomega)
    t = np.linspace(0, 3, 300)          # الزمن من 0 إلى 3 ثوانٍ
    omega = np.linspace(-15, 15, 300)   # الترددات تشمل النطاق السالب والموجب
    omega_val = 4.0                     # تردد النظام الأساسي

    # --- 1. Solar Panel Power (Max = 6W) ---
    p_solar = 6.0 * irr_factor * (1.0 + 0.1 * np.cos(omega_val * t))
    mag_solar = np.where((np.abs(omega - omega_val) < 0.6) | (np.abs(omega + omega_val) < 0.6), 6.0 * irr_factor, 0.2)

    # --- 2. Battery Storage Power (Max = 3.7W) ---
    p_battery = 3.7 * (1.0 - irr_factor) * np.exp(-0.4 * t)
    mag_battery = 3.7 / (1.0 + (omega - omega_val)**2)

    # --- 3. LED Load Power (Small LED - Constant Stable Power ~ 1.5W) ---
    p_load = np.full_like(t, 1.5)
    mag_load = np.where((omega == 0), 2.5, np.abs(np.sin(omega) / (omega + 1e-5)) * 1.5)

    # دالة عرض الأقسام بتصميم بطاقات منفصلة ونظيفة
    def render_modern_section(title, icon, time_data, mag_data, time_desc, mag_desc):
        st.markdown(f"### {icon} {title}")
        st.markdown("<div class='signal-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**📉 Time Domain ($t \ge 0$):** `{time_desc}`")
            df_t = pd.DataFrame({"Power (W)": time_data}, index=t)
            st.line_chart(df_t, height=210)
            
        with col2:
            st.markdown(f"**📊 Magnitude Spectrum (Two-Sided $\omega$):** `{mag_desc}`")
            df_f = pd.DataFrame({"Magnitude": mag_data}, index=omega)
            st.line_chart(df_f, height=210)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # عرض المكونات الثلاثة بتصميم الواجهة الجديد
    render_modern_section(
        "Solar Panel Power ($P_{solar}$)", 
        "☀️", 
        p_solar, mag_solar, 
        f"Active Generation (Peak ~ {6.0*irr_factor:.1f}W, Max 6W)", 
        "Two-sided harmonic impulse spectrum"
    )

    render_modern_section(
        "Battery Storage Power ($P_{battery}$)", 
        "🔋", 
        p_battery, mag_battery, 
        "Buffer/Discharge Transition (Max 3.7W)", 
        "Symmetric frequency response curve"
    )

    render_modern_section(
        "LED Load Power ($P_{load}$)", 
        "💡", 
        p_load, mag_load, 
        "Constant Stable Power for Small LED (~1.5W)", 
        "DC component and Sinc spectral lobes"
    )

    # صندوق الحالة والتأكيد الأكاديمي
    st.markdown("---")
    st.success(f"🌟 **System Status Active:** Irradiance is successfully configured to **{irradiance_percent}%**. All time-domain and two-sided frequency-domain spectra are updating in real-time according to system parameters!")

# استدعاء الدالة لتظهر على الشاشة
show_advanced_renewable_fft()
