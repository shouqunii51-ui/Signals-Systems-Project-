   import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Positive-Only Renewable Energy FFT", layout="wide")

def show_positive_axes_fft():
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

    st.markdown("<div class='main-title'>☀️ Renewable Energy System: Positive Axes Signals & FFT Analysis</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #64748B; margin-bottom: 25px;'>
        Real-world hardware specifications and positive-only domains ($t \ge 0$, $\omega \ge 0$) for <b>Solar Panel (Max 6W)</b>, 
        <b>Battery (Max 3.7W)</b>, and <b>LED Load</b>.
    </div>
    """, unsafe_allow_html=True)

    # سلايدر شدة الإضاءة فقط
    with st.container():
        st.markdown("<div class='box'>", unsafe_allow_html=True)
        st.markdown("### 🎛️ Environmental Control Panel")
        irradiance = st.slider(
            "Solar Irradiance / Light Intensity Level (G):", 
            min_value=0.2, max_value=1.0, value=0.8, step=0.05,
            help="Controls the actual sunlight level hitting the solar panel."
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # النطاق الزمني والترددي للمحاور الموجبة فقط (من 0 فما فوق)
    t = np.linspace(0, 3, 300)       # الزمن يبدأ من 0
    omega = np.linspace(0, 15, 300)  # الترددات الموجبة فقط تبدأ من 0
    omega_val = 4.0                  # تردد النظام الأساسي

    # --- 1. Solar Panel Power (Max = 6W) ---
    p_solar = 6.0 * irradiance * (1.0 + 0.1 * np.cos(omega_val * t))
    mag_solar = np.where(np.abs(omega - omega_val) < 0.6, 6.0 * irradiance, 0.2)

    # --- 2. Battery Storage Power (Max = 3.7W) ---
    p_battery = 3.7 * (1.0 - irradiance) * np.exp(-0.4 * t)
    mag_battery = 3.7 / (1.0 + (omega - omega_val)**2)

    # --- 3. LED Load Power (Small LED - Constant Stable Power ~ 1.5W) ---
    p_load = np.full_like(t, 1.5)
    mag_load = np.where(omega == 0, 2.5, np.abs(np.sin(omega) / (omega + 1e-5)))

    # دالة عرض الأقسام للمحاور الموجبة فقط
    def render_positive_section(title, icon, time_data, mag_data, max_p_text, desc_f):
        st.markdown(f"### {icon} {title}")
        st.markdown("<div class='box'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**📉 Time Domain ($t \ge 0$):** `{max_p_text}`")
            df_t = pd.DataFrame({"Power (W)": time_data}, index=t)
            st.line_chart(df_t, height=200)
            
        with col2:
            st.markdown(f"**📊 Magnitude Spectrum ($\omega \ge 0$):** `{desc_f}`")
            df_f = pd.DataFrame({"Magnitude": mag_data}, index=omega)
            st.line_chart(df_f, height=200)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # عرض المكونات الثلاثة بالمحاور الموجبة
    render_positive_section(
        "1. Solar Panel Power ($P_{solar}$)", 
        "☀️", 
        p_solar, mag_solar, 
        f"Active Power Generation (Peak ~ {6.0*irradiance:.1f}W, Max 6W)", 
        "Positive frequency harmonic peaks"
    )

    render_positive_section(
        "2. Battery Storage Power ($P_{battery}$)", 
        "🔋", 
        p_battery, mag_battery, 
        "Discharge/Buffer Transition (Max 3.7W)", 
        "Positive frequency response curve"
    )

    render_positive_section(
        "3. LED Load Power ($P_{load}$)", 
        "💡", 
        p_load, mag_load, 
        "Stable Constant Power for Small LED (~1.5W)", 
        "DC and low-frequency Sinc spectrum"
    )

    st.markdown("---")
    st.success(f"🌟 **Status:** Irradiance set to **{irradiance*100}%**. All charts now strictly display positive axes ($t \ge 0$ and $\omega \ge 0$) as requested!")

# استدعاء الدالة لتظهر على الشاشة
show_positive_axes_fft()
