import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# إعدادات صفحة Streamlit وتصميم الواجهة
st.set_page_config(
    page_title="PV Signal & Fourier Analysis",
    page_icon="☀️",
    layout="centered"
)

# تصميم العنوان الرئيسي بستايل جذاب
st.markdown("<h1 style='text-align: center; color: #ff8c00;'>☀️ Solar PV System: Fourier Analysis & Signal Processing</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>ربط مفاهيم الإشارات والنظم بمشروع الطاقة الشمسية وإدارة البطاريات</h4>", unsafe_allow_html=True)
st.markdown("---")

# مقدمة مبسطة واحترافية
st.markdown("""
### 📌 فكرة الربط بالمادة (Signals & Systems):
عندما يقرأ مستشعر **INA219** الجهد والتيار من اللوح الشمسي (**Solar PV**)، فإن القراءات لا تكون ثابتة تماماً بسبب التشويش البيئي والكهربائي (مثل الإضاءة المتذبذبة أو الظل). 
من خلال **تحويل فورييه (Fourier Transform)**، نستطيع الانتقال من **النطاق الزمني (Time Domain)** إلى **النطاق الترددي (Frequency Domain)** لتحليل طيف الترددات، وكشف مركبات التشويش ومعالجتها قبل إرسالها لشريحة تنظيم الشحن **BQ25185**.
""")

st.markdown("---")

# لوحة التحكم الجانبية (Sliders)
st.sidebar.header("🎛️ تحكم المحاكاة")
noise_level = st.sidebar.slider("شدة التشويش (Noise Intensity)", 0.0, 2.0, 0.6)
freq_signal = st.sidebar.slider("تردد تغير الإضاءة الأساسي", 0.5, 3.0, 1.0)

# توليد البيانات (Time Domain)
t = np.linspace(0, 10, 400)
# إشارة اللوح الشمسي الحقيقية مضاف لها تشويش (Noise)
clean_signal = 3.5 + 1.2 * np.sin(2 * np.pi * freq_signal * t)
np.random.seed(42)
noise = np.random.normal(0, noise_level, len(t))
noisy_signal = clean_signal + noise

# تطبيق تحويل فورييه التقريبي (FFT) لعرض النطاق الترددي
fft_values = np.fft.fft(noisy_signal)
fft_freq = np.fft.fftfreq(len(t), t[1] - t[0])
# نأخذ النصف الموجب فقط من الترددات
positive_freqs = fft_freq[:len(fft_freq)//2]
fft_magnitude = np.abs(fft_values)[:len(fft_values)//2]

# رسم الرسوم البيانية بشكل أنيق
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7))

# 1. Time Domain Plot
ax1.plot(t, noisy_signal, label='Raw Sensor Signal (With Noise)', color='#ff7f0e', alpha=0.7, linewidth=1.5)
ax1.plot(t, clean_signal, label='Ideal PV Signal', color='#2ca02c', linewidth=2.5, linestyle='--')
ax1.set_title("1️⃣ Time Domain: إشارة الجهد الفردية من مستشعر INA219 مع التشويش", fontsize=11, fontweight='bold')
ax1.set_xlabel("Time ($s$)", fontsize=9)
ax1.set_ylabel("Voltage ($V$)", fontsize=9)
ax1.legend(loc='upper right')
ax1.grid(True, linestyle=':', alpha=0.6)

# 2. Frequency Domain Plot (Fourier Transform)
ax2.plot(positive_freqs, fft_magnitude, color='#1f77b4', linewidth=2)
ax2.fill_between(positive_freqs, fft_magnitude, color='#1f77b4', alpha=0.3)
ax2.set_title("2️⃣ Frequency Domain (Fourier Transform): تحليل طيف الترددات وكشف مركبات التشويش", fontsize=11, fontweight='bold')
ax2.set_xlabel("Frequency ($Hz$)", fontsize=9)
ax2.set_ylabel("Magnitude", fontsize=9)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.set_xlim(0, 5)

plt.tight_layout()
st.pyplot(fig)

st.markdown("---")

# تقسيم الشاشة لجزئين لتوضيح الفوائد بشكل منظم
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Time Domain Analysis")
    st.info("يظهر لك كيف تتأثر قراءات اللوح الشمسي بالتغيرات اللحظية، وكيف يمكننا مراقبة الجهد والتيار بشكل مستمر عبر الأردوينو.")

with col2:
    st.markdown("### 🔍 Fourier Spectrum")
    st.info("يظهر لك تحويل فورييه للترددات، وهو المفتاح لمعرفة مصدر أي تذبذب غير مرغوب فيه وتصفية البيانات بذكاء قبل دخولها للبطارية.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>تم تصميم هذه المحاكاة خصيصاً لمشروع تخرج/عرض مادة الإشارات والنظم ⚡</p>", unsafe_layout_html=True)
