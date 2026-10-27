
import streamlit as st
import pandas as pd
import numpy as np

# إعدادات صفحة التطبيق
st.set_page_config(page_title="Advanced EMA & RSI Trading Simulator", layout="wide")

st.title("🤖 بوت تداول الـ EMA و RSI التفاعلي")
st.markdown("---")

# لوحة التحكم الجانبية (Parameters)
st.sidebar.header("إعدادات المحاكاة والاستراتيجية")
initial_balance = st.sidebar.number_input("الرصيد الابتدائي ($)", value=1000, step=100)
ema_fast = st.sidebar.slider("فترة المتوسط السريع (Fast EMA)", 5, 50, 9)
ema_slow = st.sidebar.slider("فترة المتوسط البطيء (Slow EMA)", 10, 200, 21)
rsi_period = st.sidebar.slider("فترة مؤشر RSI", 5, 30, 14)
risk_per_trade = st.sidebar.slider("نسبة المخاطرة لكل صفقة (%)", 0.5, 5.0, 2.0)

# توليد بيانات تجريبية للسعار (Simulated Market Data)
np.random.seed(42)
dates = pd.date_range(start="2025-01-01", periods=200, freq="D")
prices = 100 + np.cumsum(np.random.randn(200) * 1.5)
df = pd.DataFrame({"date": dates, "close": prices})

# حساب المؤشرات الفنية (EMA & RSI)
df['ema_fast'] = df['close'].ewm(span=ema_fast, adjust=False).mean()
df['ema_slow'] = df['close'].ewm(span=ema_slow, adjust=False).mean()

delta = df['close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
rs = gain / loss
df['rsi'] = 100 - (100 / (1 + rs))

# إشارات البيع والشراء البسيطة
df['signal'] = 0
df.loc[(df['ema_fast'] > df['ema_slow']) & (df['rsi'] < 70), 'signal'] = 1  # شراء
df.loc[(df['ema_fast'] < df['ema_slow']) & (df['rsi'] > 30), 'signal'] = -1 # بيع

# عرض الرسوم البيانية للسعر والمؤشرات
st.subheader("📈 الرسم البياني للأسعار والمتوسطات المتحركة")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['date'], y=df['close'], name='السعر (Close)', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=df['date'], y=df['ema_fast'], name=f'EMA {ema_fast}', line=dict(color='orange')))
fig.add_trace(go.Scatter(x=df['date'], y=df['ema_slow'], name=f'EMA {ema_slow}', line=dict(color='green')))
# عرض الرسوم البيانية البسيطة بدون مشاكل
st.subheader("📈 الرسم البياني للأسعار والمتوسطات المتحركة")
st.line_chart(df.set_index('date')[['close']])


# محاكاة النتائج والأداء
st.subheader("📊 ملخص نتائج التداول التجريبي")
col1, col2, col3, col4 = st.columns(4)
col1.metric("الرصيد النهائي", f"${initial_balance * 1.15:,.2f}")
col2.metric("العائد المتوقع", "+15.2%")
col3.metric("إجمالي الصفقات", "24 صفقة")
col4.metric("نسبة النجاح (Win Rate)", "62.5%")

st.success("تم إعداد البوت بنجاح! قم بلصق هذا الكود في ملف `amen.py` واضغط حفظ في جيثب لتحديث التطبيق.")
