import streamlit as st
import numpy as np
import pandas as pd

# إعدادات الصفحة
st.set_page_config(
    page_title="Renewable Energy Interactive Lab",
    page_icon="⚡",
    layout="wide"
)

def show_interactive_lab():
    # تصميم CSS جديد كلياً بألوان عصرية وتفاعلية
    st.markdown("""
        <style>
        .stApp {
            background-color: #F8FAFC;
        }
        .main-header {
            background: linear-gradient(135deg, #3B82F6 0%, #1E3A8A 100%);
            padding: 25px;
            border-radius: 16px;
            color: white;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 10px 20px rgba(59, 130, 246, 0.2);
        }
        .control-box {
            background: #FFFFFF;
            padding: 25px;
            border-radius: 16px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            margin-bottom: 25px;
        }
        .metric-card {
            background: #FFFFFF;
            padding: 20px;
            border-radius: 14px;
            border-left: 5px solid #3B82F6;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
            text-align: center;
        }
        .solar-card { border-left-color: #F59E0B !important; }
        .battery-card { border-left-color: #10B981 !important; }
        .load-card { border-left-color: #6366F1 !important; }
        </style>
    """, unsafe_allow_html=True)

    # العنوان الرئيسي
    st.markdown("""
        <div class='main-header'>
            <h1 style='margin:0; font-size: 28px;'>⚡ Interactive Renewable Energy & FFT Laboratory</h1>
            <p style='margin:5px 0 0 0; color: #E2E8F0; font-size: 15px;'>Signals & Systems Dynamic Analysis Suite</p>
        </div>
    """, unsafe_allow_html=True)

    # لوحة التحكم التفاعلية العلوية
    with st.container():
        st.markdown("<div class='control-box'>", unsafe_allow_html=True)
        st.markdown("### 🎛️ Real-Time Simulation Control")
        
        irradiance_percent = st.slider(
            "Solar Irradiance / Light Intensity Level (G):", 
            min_value=0, max_value=100, value=75, step=1,
            help="Drag to change sunlight intensity from 0% to 100%"
        )
        
        irr_factor = irradiance_percent / 100.0
        st.markdown("</div>", unsafe_allow_html=True)

    # حساب القيم الحية للمقاييس (KPIs)
    current_solar_peak = 6.0 * irr_factor
    current_battery_power = 3.7 * (1.0 - irr_factor)
    current_load_power = 1.5

    # عرض بطاقات المؤشرات الحية (Live Metrics)
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"""
            <div class='metric-card solar-card'>
                <h4 style='color: #D97706; margin:0;'>☀️ Solar Power Peak</h4>
                <h2 style='margin: 5px 0 0 0; color: #1E293B;'>{current_solar_peak:.2f} W</h2>
                <span style='color: #64748B; font-size: 12px;'>Max Limit: 6.0W</span>
            </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
            <div class='metric-card battery-card'>
                <h4 style='color: #059669; margin:0;'>🔋 Battery Buffer</h4>
                <h2 style='margin: 5px 0 0 0; color: #1E293B;'>{current_battery_power:.2f} W</h2>
                <span style='color: #64748B; font-size: 12px;'>Max Limit: 3.7W</span>
            </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
            <div class='metric-card load-card'>
                <h4 style='color: #4F46E5; margin:0;'>💡 LED Load</h4>
                <h2 style='margin: 5px 0 0 0; color: #1E293B;'>{current_load_power} W</h2>
                <span style='color: #64748B; font-size: 12px;'>Constant Regulated</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # إعداد المحاور والبيانات الرياضية
    t = np.linspace(0, 3, 300)
    omega = np.linspace(-15, 15, 300)
    omega_val = 4.0

    p_solar = 6.0 * irr_factor * (1.0 + 0.1 * np.cos(omega_val * t))
    mag_solar = np.where((np.abs(omega - omega_val) < 0.6) | (np.abs(omega + omega_val) < 0.6), 6.0 * irr_factor, 0.2)

    p_battery = 3.7 * (1.0 - irr_factor) * np.exp(-0.4 * t)
    mag_battery = 3.7 / (1.0 + (omega - omega_val)**2)

    p_load = np.full_like(t, 1.5)
    mag_load = np.where((omega == 0), 2.5, np.abs(np.sin(omega) / (omega + 1e-5)) * 1.5)

    # استخدام التبويبات (Tabs) لجعل الواجهة أكثر تفاعلية وتنظيماً
    tab1, tab2, tab3 = st.tabs(["☀️ Solar Panel Analysis", "🔋 Battery Storage Analysis", "💡 LED Load Analysis"])

    with tab1:
        st.markdown("### Solar Generation Performance")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**📉 Time Domain ($t \ge 0$)**")
            st.line_chart(pd.DataFrame({"Power (W)": p_solar}, index=t), height=240)
        with c2:
            st.markdown("**📊 Two-Sided Magnitude Spectrum ($\omega$)**")
            st.line_chart(pd.DataFrame({"Magnitude": mag_solar}, index=omega), height=240)

    with tab2:
        st.markdown("### Battery Buffer & Compensation Response")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**📉 Time Domain ($t \ge 0$)**")
            st.line_chart(pd.DataFrame({"Power (W)": p_battery}, index=t), height=240)
        with c2:
            st.markdown("**📊 Two-Sided Magnitude Spectrum ($\omega$)**")
            st.line_chart(pd.DataFrame({"Magnitude": mag_battery}, index=omega), height=240)

    with tab3:
        st.markdown("### Regulated LED Load Consumption")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**📉 Time Domain ($t \ge 0$)**")
            st.line_chart(pd.DataFrame({"Power (W)": p_load}, index=t), height=240)
        with c2:
            st.markdown("**📊 Two-Sided Magnitude Spectrum ($\omega$)**")
            st.line_chart(pd.DataFrame({"Magnitude": mag_load}, index=omega), height=240)

    st.markdown("---")
    st.success(f"🌟 **Interactive Lab Status:** Irradiance successfully set to **{irradiance_percent}%**. All metrics, time responses, and two-sided spectra are dynamically updated!")

# استدعاء الدالة الرئيسية
show_interactive_lab()
