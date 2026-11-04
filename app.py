import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Textbook FFT Analysis", layout="wide")

def show_textbook_fft():
    st.markdown("### 📐 Textbook-Style Fourier Transform (Magnitude Spectrum)")
    st.write("Comparing pure sinusoidal time-domain signals with their theoretical impulse-like Magnitude Spectrum.")

    # سلايدر لتغيير تردد الإشارة (يشبه تغيير الترددات في المحاضرات)
    freq = st.slider("Signal Frequency / Omega ($\omega$):", min_value=1.0, max_value=10.0, value=3.0, step=0.5)

    # 1. التايم دومين: إشارة جيبية نقية (Pure Cosine Wave) تطابق النظريات الأكاديمية
    fs = 200
    t = np.linspace(0, 2, 400)
    x_t = np.cos(2 * np.pi * freq * t) # إشارة جيبية بحتة

    # 2. الفريكونسي دومين: تحويل فورييه لإشارة جيبية يعطي أسهماً عند التردد الموجب والسالب
    # لتمثيل ذلك بأسلوب قريب للكتاب باستخدام الأطر البيانية
    freqs = np.fft.fftfreq(len(t), 1/fs) * 2 * np.pi # بالـ Radian/s أو التردد العادي
    fft_vals = np.abs(np.fft.fft(x_t))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**📉 Time Domain: $x(t) = \cos({freq} \cdot 2\pi t)$**")
        df_time = pd.DataFrame({"Amplitude": x_t}, index=t)
        st.line_chart(df_time, height=250)
        
    with col2:
        st.markdown(f"**📊 Magnitude Spectrum (Impulses at $\pm {freq} \cdot 2\pi$)**")
        df_fft = pd.DataFrame({"Magnitude": fft_vals}, index=freqs)
        st.line_chart(df_fft, height=250)

show_textbook_fft()
