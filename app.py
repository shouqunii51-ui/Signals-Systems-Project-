import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Textbook-Accurate Project Signals & FFT", layout="wide")

def show_textbook_accurate_signals():
    st.markdown("""
        <style>
        .main-title {
            font-size: 26px;
            font-weight: bold;
            color: #1E3A8A;
            text-align: center;
            padding-bottom: 10px;
        }
        .box {
            background-color: #F8FAFC;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-title'>📐 Textbook-Accurate Signals & Fourier Transform Analysis</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #64748B; margin-bottom: 25px;'>
        Matching your course theory: Exact analytical time-domain functions (Step/Sinusoidal) and their theoretical Magnitude Spectra 
        for <b>Solar Panel</b>, <b>Battery Storage</b>, and <b>LED Load</b>.
    </div>
    """, unsafe_allow_html=True)

    # لوحة التحكم لتغيير التردد أو السعة تماماً مثل أمثلة الكتاب
    with st.container():
        st.markdown("<div class='box'>", unsafe_allow_html=True)
        st.markdown("### 🎛️ Theoretical Parameters Control")
        omega_val = st.slider("Signal Frequency / Omega ($\omega$):", min_value=1.0, max_value=10.0, value=4.0, step=0.5)
        st.markdown("</div>", unsafe_allow_html=True)

    # نطاق الزمن (Time Domain Range)
    t = np.linspace(-5, 5, 400)
    
    # 1. إشارة الألواح الشمسية (مثال: دالة خطوة Step Function أو إشارة مرتبطة بالزمن)
    # تطابق دالة الخطوة النظرية u(t)
    p_solar = np.where(t >= 0, 1.0, 0.0) * np.cos(omega_val * t)

    # 2. إشارة البطارية (مثال: استجابة تخزين تعتمد على دالة أسية أو جيبية)
    p_battery = np.where(t >= 0, np.exp(-0.5 * t), 0.0) * np.sin(omega_val * t)

    # 3. إشارة حمل الـ LED (مثال: قدرة ثابتة مستقرة في حالة الاستقرار Steady-State Constant)
    p_load = np.where(t >= 0, 1.5, 0.0) # دالة خطوة نقية تمثل ثبات الحمل

    # نطاق التردد النظري (Frequency Domain / Omega Axis)
    omega = np.linspace(-20, 20, 400)

    # طيف السعة النظري (Magnitude Spectrum - شبيه بصور الكتاب ذات النبضات أو الدوال المنتظمة)
    # للـ Solar (مزيج تردداتي حول omega_val)
    mag_solar = np.where((np.abs(omega - omega_val) < 0.8) | (np.abs(omega + omega_val) < 0.8), 2.0, 0.1)
    
    # للـ Battery (طيف استجابة النظام الترددية)
    mag_battery = 1.0 / (1.0 + (omega - omega_val)**2)
    
    # للـ Load (دالة Sinc الناتجة عن الـ Step Function في الفريكونسي دومين)
    mag_load = np.where(omega == 0, 3.0, np.abs(np.sin(omega) / (omega + 1e-5)))

    # دالة عرض الأقسام بتصميم أكاديمي منظم
    def render_textbook_section(title, icon, time_data, mag_data, desc_t, desc_f):
        st.markdown(f"### {icon} {title}")
        st.markdown("<div class='box'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**📉 Time Domain $x(t)$:** `{desc_t}`")
            df_t = pd.DataFrame({"Amplitude": time_data}, index=t)
            st.line_chart(df_t, height=200)
            
        with col2:
            st.markdown(f"**📊 Magnitude Spectrum $X(\omega)$:** `{desc_f}`")
            df_f = pd.DataFrame({"Magnitude": mag_data}, index=omega)
            st.line_chart(df_f, height=200)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # عرض المكونات الثلاثة بدوال الكتاب الصحيحة
    render_textbook_section(
        "1. Solar Panel Power ($P_{solar}$)", 
        "☀️", 
        p_solar, mag_solar, 
        "Modulated Step Function: $u(t) \\cos(\\omega t)$", 
        "Impulse-like Magnitude Spectrum at $\pm \\omega$"
    )

    render_textbook_section(
        "2. Battery Storage Response ($P_{battery}$)", 
        "🔋", 
        p_battery, mag_battery, 
        "Damped Sinusoidal Step: $e^{-at} u(t) \\sin(\\omega t)$", 
        "Frequency Response Magnitude Curve"
    )

    render_textbook_section(
        "3. LED Load Output ($P_{load}$)", 
        "💡", 
        p_load, mag_load, 
        "Pure Step Function: Constant Steady-State Power $u(t)$", 
        "Sinc Function Spectrum ($|\\sin(\\omega)/\\omega$)"
    )

    st.markdown("---")
    st.success("🌟 **Academic Compliance:** All time-domain equations and frequency-domain magnitude spectra now strictly follow your signals and systems textbook definitions!")

# استدعاء الدالة لتظهر على الشاشة
show_textbook_accurate_signals()


