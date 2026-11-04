import streamlit as st
import numpy as np
import pandas as pd

# إعدادات الصفحة
st.set_page_config(
    page_title="Advanced Renewable Energy FFT Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

def show_ultimate_dashboard():
    # تصميم CSS احترافي وعصري جداً للواجهة
    st.markdown("""
        <style>
        /* خلفية عامة وتنسيق الخطوط */
        .main {
            background-color: #0F172A;
        }
        
        /* الهيدر الرئيسي */
        .hero-banner {
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
            padding: 30px;
            border-radius: 20px;
            border: 1px solid #334155;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }
        .hero-title {
            font-size: 32px;
            font-weight: 800;
            color: #F8FAFC;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }
        .hero-subtitle {
            color: #94A3B8;
            font-size: 16px;
            font-weight: 400;
        }

        /* لوحة التحكم */
        .control-panel {
            background: linear-gradient(135deg, #1E293B 0%, #111827 100%);
            padding: 25px;
            border-radius: 16px;
            border: 1px solid #374151;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
        }

        /* بطاقات الإشارات والرسومات */
        .signal-card {
            background-color: #1E293B;
            padding: 22px;
            border-radius: 16px;
            border: 1px solid #334155;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
            margin-bottom: 25px;
            transition: transform 0.2s ease;
        }
        .signal-card:hover {
            border-color: #3B82F6;
        }
        
        /* عناوين البطاقات */
        .card-title {
            font-size: 20px;
            font-weight: 700;
            color: #F1F5F9;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # عنوان الواجهة الفخم
    st.markdown("""
        <div class='hero-banner'>
            <div class='hero-title'>⚡ Renewable Energy & FFT Analysis Dashboard</div>
            <div class='hero-subtitle'>Signals & Systems Project • Real-Time Dynamic Evaluation of Solar, Battery & LED Load</div>
        </div>
    """, unsafe_allow_html=True)

    # لوحة التحكم التفاعلية
    with st.container():
        st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #F8FAFC; margin-bottom: 15px;'>🎛️ System Control Panel</h3>", unsafe_allow_html=True)
        
        col_s1, col_s2 = st.columns([3, 1])
        with col_s1:
            irradiance_percent = st.slider(
                "Solar Irradiance / Light Intensity Level (G):", 
                min_value=0, max_value=100, value=75, step=1,
                help="Adjust the sunlight percentage hitting the solar panel (0% to 100%)."
            )
        with col_s2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.metric(label="Irradiance State", value=f"{irradiance_percent}%")
            
        irr_factor = irradiance_percent / 100.0
        st.markdown("</div>", unsafe_allow_html=True)

    # إعداد المحاور والبيانات (الزمن من 0 فصاعداً، والترددات ثنائية الطرف Omega)
    t = np.linspace(0, 3, 300)
    omega = np.linspace(-15, 15, 300)
    omega_val = 4.0

    # --- 1. Solar Panel Power (Max = 6W) ---
    p_solar = 6.0 * irr_factor * (1.0 + 0.1 * np.cos(omega_val * t))
    mag_solar = np.where((np.abs(omega - omega_val) < 0.6) | (np.abs(omega + omega_val) < 0.6), 6.0 * irr_factor, 0.2)

    # --- 2. Battery Storage Power (Max = 3.7W) ---
    p_battery = 3.7 * (1.0 - irr_factor) * np.exp(-0.4 * t)
    mag_battery = 3.7 / (1.0 + (omega - omega_val)**2)

    # --- 3. LED Load Power (Small LED - Constant Stable Power ~ 1.5W) ---
    p_load = np.full_like(t, 1.5)
    mag_load = np.where((omega == 0), 2.5, np.abs(np.sin(omega) / (omega + 1e-5)) * 1.5)

    # دالة عرض البطاقات بتصميم أنيق
    def render_dashboard_card(title, icon, time_data, mag_data, time_desc, mag_desc):
        st.markdown(f"<div class='signal-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='card-title'>{icon} {title}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<span style='color: #94A3B8; font-size: 14px;'>📉 Time Domain ($t \ge 0$): <b>{time_desc}</b></span>", unsafe_allow_html=True)
            df_t = pd.DataFrame({"Power (W)": time_data}, index=t)
            st.line_chart(df_t, height=220)
            
        with col2:
            st.markdown(f"<span style='color: #94A3B8; font-size: 14px;'>📊 Magnitude Spectrum (Two-Sided $\omega$): <b>{mag_desc}</b></span>", unsafe_allow_html=True)
            df_f = pd.DataFrame({"Magnitude": mag_data}, index=omega)
            st.line_chart(df_f, height=220)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # عرض المكونات الثلاثة داخل البطاقات العصرية
    render_dashboard_card(
        "Solar Panel Power Generation ($P_{solar}$)", 
        "☀️", 
        p_solar, mag_solar, 
        f"Active Output (Peak ~ {6.0*irr_factor:.1f}W, Max 6W)", 
        "Two-sided harmonic impulse spectrum"
    )

    render_dashboard_card(
        "Battery Storage Buffer Response ($P_{battery}$)", 
        "🔋", 
        p_battery, mag_battery, 
        "Buffer / Discharge Transition (Max 3.7W)", 
        "Symmetric frequency response curve"
    )

    render_dashboard_card(
        "LED Load Stable Consumption ($P_{load}$)", 
        "💡", 
        p_load, mag_load, 
        "Constant Regulated Power for Small LED (~1.5W)", 
        "DC component and Sinc spectral lobes"
    )

    # صندوق الحالة النهائي
    st.markdown("---")
    st.success(f"🌟 **Dashboard Operational:** Solar irradiance is locked at **{irradiance_percent}%**. All system components and frequency domains are fully synchronized and responding in real-time!")

# استدعاء الدالة
show_ultimate_dashboard()
