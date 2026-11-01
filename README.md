# Signals-Systems-Project-
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Solar PV-Battery System: Signal Response Simulation")
st.write("هذه المحاكاة التفاعلية توضح استجابة النظام (System Response) لتغيرات الدخل المفاجئة (Step Input) في مشروع إدارة الطاقة.")

step_change = st.slider("مستوى تغير الإضاءة أو الحمل (Step Magnitude)", 0.0, 5.0, 2.0)

t = np.linspace(0, 10, 200)
y = step_change * (1 - np.exp(-t)) 

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(t, y, label='Output Signal y(t)', color='#ff7f0e', linewidth=2.5)
ax.axhline(y=step_change, color='gray', linestyle='--', label='Target Stable Level')
ax.set_title("System Step Response (Time Domain)")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Voltage / Power Amplitude")
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.info("ملاحظة أكاديمية: يوضح هذا المنحنى كيف يتعامل النظام مع التغيرات العابرة (Transient Response) ليصل إلى حالة الاستقرار (Steady-State Stability) بفضل شريحة تنظيم الطاقة BQ25185.")
