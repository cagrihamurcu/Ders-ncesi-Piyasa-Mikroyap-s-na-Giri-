
import streamlit as st

st.set_page_config(
    page_title="Ders Öncesi Hazırlık",
    page_icon="🎓",
    layout="centered"
)

if "puan" not in st.session_state:
    st.session_state.puan = 0
if "q1_done" not in st.session_state:
    st.session_state.q1_done = False
if "q2_done" not in st.session_state:
    st.session_state.q2_done = False
if "q3_done" not in st.session_state:
    st.session_state.q3_done = False

def add_points(flag, pts):
    if not st.session_state[flag]:
        st.session_state[flag] = True
        st.session_state.puan += pts

st.title("🎓 Ders Öncesi Hazırlık")
st.subheader("Pay Piyasası, Emirler ve Piyasa Mikroyapısı")

st.write(
    """
Bu kısa uygulamanın amacı konuyu öğretmek değil, derse gelmeden önce
bazı temel kavramları **tanımak ve düşünmeye başlamak**.

Yaklaşık süre: **5–7 dakika**
"""
)

done = sum([
    st.session_state.q1_done,
    st.session_state.q2_done,
    st.session_state.q3_done
])
st.progress(done / 3)
st.metric("Hazırlık Puanı", f"{st.session_state.puan}/100")

st.divider()

# -------------------------------------------------
# 1. BID / ASK / SPREAD
# -------------------------------------------------
st.header("1️⃣ Önce Temel Kavramlar")

st.markdown(
    """
**Bid:** piyasadaki en yüksek alış fiyatıdır.  
**Ask:** piyasadaki en düşük satış fiyatıdır.

**Spread**, ask ile bid arasındaki farktır:

**Spread = Ask − Bid**
"""
)

st.markdown(
    """
Örnek:

- Bid = **99,80 TL**
- Ask = **100,20 TL**
"""
)

q1 = st.radio(
    "Spread kaç TL'dir?",
    ["0,20 TL", "0,40 TL", "100,00 TL"],
    index=None,
    key="pre_q1"
)

if st.button("Kontrol et", key="pre_btn1"):
    if q1 == "0,40 TL":
        st.success("✅ Doğru. Spread = 100,20 − 99,80 = 0,40 TL")
        st.write(
            """
**Kısa not:**  
Spread daraldıkça alış ve satış fiyatları birbirine yaklaşır.
Genişledikçe birbirinden uzaklaşır.
"""
        )
        add_points("q1_done", 30)
    elif q1:
        st.warning("Tekrar hesaplayın: Ask − Bid")
    else:
        st.info("Önce bir seçenek işaretleyin.")

st.divider()

# -------------------------------------------------
# 2. PİYASA DERİNLİĞİ
# -------------------------------------------------
st.header("2️⃣ Piyasa Derinliği")

st.markdown(
    """
**Piyasa derinliği**, farklı fiyat seviyelerinde ne kadar alış ve satış emri bulunduğunu gösterir.

- **Derin piyasa:** daha fazla alış ve satış emri vardır.
- **Sığ piyasa:** daha az alış ve satış emri vardır.
"""
)

st.markdown(
    """
Şimdi iki piyasayı düşünün:

**Piyasa A**
- Spread dar
- Emir miktarı yüksek

**Piyasa B**
- Spread geniş
- Emir miktarı düşük
"""
)

q2 = st.radio(
    "Aynı büyüklükte büyük bir piyasa emri hangi piyasada daha az fiyat hareketi yaratabilir?",
    ["Piyasa A", "Piyasa B"],
    index=None,
    key="pre_q2"
)

if st.button("Kontrol et", key="pre_btn2"):
    if q2 == "Piyasa A":
        st.success("✅ Doğru.")
        st.write(
            """
Derin piyasa, büyük emirleri daha fazla karşıt emirle karşılayabilir.

**Kısa not:**  
Dar spread tek başına yeterli değildir; piyasa derinliği de önemlidir.
"""
        )
        add_points("q2_done", 30)
    elif q2:
        st.warning("Bir kez daha düşünün: hangi piyasada daha fazla karşıt emir var?")
    else:
        st.info("Önce bir seçenek işaretleyin.")

st.divider()

# -------------------------------------------------
# 3. BİLGİ Mİ, LİKİDİTE Mİ?
# -------------------------------------------------
st.header("3️⃣ Fiyat Neden Değişmiş Olabilir?")

st.markdown(
    """
Bir payın fiyatı kısa sürede %3 düşüyor.

Bunun nedeni:

- şirketle ilgili olumsuz yeni bilgi olabilir,
- büyük bir yatırımcının satış yapmak zorunda kalması olabilir.

Yani fiyat hareketinin nedeni her zaman tek değildir.
"""
)

q3 = st.radio(
    "Hangisi en doğru yorumdur?",
    [
        "Fiyat düştüyse kesin kötü haber vardır.",
        "Fiyat düşüşü bilgi veya likidite kaynaklı olabilir.",
        "Fiyat düşüşünün nedeni önemli değildir."
    ],
    index=None,
    key="pre_q3"
)

if st.button("Kontrol et", key="pre_btn3"):
    if q3 == "Fiyat düşüşü bilgi veya likidite kaynaklı olabilir.":
        st.success("✅ Doğru.")
        st.markdown(
            """
**Kısa not:**  
Her fiyat hareketi yeni bilgi anlamına gelmez.

Bu ayrımı derste **bilgi şoku** ve **likidite şoku** kavramlarıyla inceleyeceğiz.
"""
        )
        add_points("q3_done", 40)
    elif q3:
        st.warning("Bu yorum fazla kesin.")
    else:
        st.info("Önce bir seçenek işaretleyin.")

st.divider()

# -------------------------------------------------
# MERAK SORUSU
# -------------------------------------------------
st.header("❓ Derse Gelirken Bu Soruyu Düşünün")

st.markdown(
    """
**Aynı şirketin payı, şirket hakkında yeni bilgi gelmeden neden farklı fiyatlardan işlem görebilir?**

Dersin ana konusu bu sorunun cevabıdır.
"""
)

st.divider()

if st.session_state.puan == 100:
    st.balloons()
    st.success("Hazırlık tamamlandı. Derse hazırsınız. 🎉")
    st.markdown(
        """
Derse gelirken şu üç fikri hatırlayın:

1. **Spread**, alış ve satış fiyatları arasındaki farktır.
2. **Piyasa derinliği**, piyasadaki alış ve satış emirlerinin miktarıyla ilgilidir.
3. **Her fiyat hareketi yeni bilgi anlamına gelmez.**
"""
    )
elif st.session_state.puan >= 60:
    st.info("Hazırlık iyi gidiyor. Kalan bölümü de tamamlayın.")
else:
    st.write("Üç kısa bölümü tamamladığınızda hazırlık bitecek.")

st.caption(
    "Ders öncesi hazırlık — Pay Piyasası, Emirler ve Piyasa Mikroyapısı"
)
