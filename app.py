import streamlit as st
import numpy as np
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="Solar Panel & Signals Project", layout="wide")

def show_solar_intensity_analysis():
    # تصميم مخصص للواجهة
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
    st.markdown("<div class='main-title'>☀️ Solar Panel Power & Magnitude Spectrum Analysis</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #64748B; margin-bottom: 25px;'>
        Analyzing the dynamic response of the <b>Solar Panel</b> when changing <b>Solar Irradiance (Light Intensity)</b> 
        and observing its Fast Fourier Transform (FFT) Magnitude Spectrum.
    </div>
    """, unsafe_allow_html=True)

    # لوحة التحكم بسلايدر واحد فقط لشدة الإضاءة
    with st.container():
        st.markdown("<div class='section-box'>", unsafe_allow_html=True)
        st.markdown("### 🎛️ Control Panel")
        
        # سلايدر شدة الإضاءة فقط
        irradiance = st.slider(
            "Solar Irradiance / Light Intensity (W/m² or Level):", 
            min_value=0.5, max_value=3.0, value=1.5, step=0.1,
            help="Controls the light intensity level hitting the solar panel."
        )
        
        st.markdown("</div>", unsafe_allow_html=True)

    # إعدادات الزمن
    fs = 200  
    T = 2.0   
    t = np.linspace(0, T, int(fs * T), endpoint=False)
    n = len(t)
    fft_freqs = np.fft.fftfreq(n, 1/fs)
    positive_mask = fft_freqs >= 0
    f_axis = fft_freqs[positive_mask]

    # توليد إشارة طاقة الألواح الشمسية بناءً على شدة الإضاءة المحددة
    # انتقال مفاجئ (Step) يتأثر بشدة الإضاءة + قليل من التشويش الواقعي
    solar_transition = np.where(t < 1.0, 1.0 * irradiance, 1.8 * irradiance)
    noise = 0.1 * np.random.normal(0, 1, n)
    p_solar = solar_transition + noise

    # حساب تحويل فورييه (Magnitude Spectrum)
    fft_vals = np.fft.fft(p_solar)
    mag_solar = (2.0 / n) * np.abs(fft_vals[positive_mask])

    # عرض النتائج في صندوق أنيق ومنظم
    st.markdown("### 📊 Solar Panel Output & Spectrum")
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📉 Time Domain:** `Solar Power Generation Over Time`")
        df_time = pd.DataFrame({"Power (W)": p_solar}, index=t)
        st.line_chart(df_time, height=220)
        
    with col2:
        st.markdown("**📊 Magnitude Spectrum:** `Frequency Domain Analysis`")
        df_fft = pd.DataFrame({"Magnitude": mag_solar}, index=f_axis)
        st.line_chart(df_fft, height=220)
        
    st.markdown("</div>", unsafe_allow_html=True)

    st.success(f"🌟 **Status:** Irradiance level set to **{irradiance}**. Notice how changing light intensity scales the power and shifts the spectrum accordingly!")

# استدعاء الدالة لتظهر على الشاشة
show_solar_intensity_analysis()
