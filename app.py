
import streamlit as st

st.set_page_config(
    page_title="Piyasa Mikroyapısı Meydan Okuması",
    page_icon="🏆",
    layout="centered"
)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
defaults = {
    "takim": "",
    "puan": 0,
    "can": 3,
    "seri": 0,
    "q1_done": False,
    "q2_done": False,
    "q3_done": False,
    "q4_done": False,
    "q5_done": False,
    "bonus_done": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def dogru(flag, base_points):
    if not st.session_state[flag]:
        st.session_state.seri += 1
        bonus = 5 if st.session_state.seri >= 2 else 0
        st.session_state.puan += base_points + bonus
        st.session_state[flag] = True
        return bonus
    return 0


def yanlis():
    st.session_state.seri = 0
    if st.session_state.can > 0:
        st.session_state.can -= 1


# -------------------------------------------------
# GİRİŞ
# -------------------------------------------------
st.title("🏆 Piyasa Mikroyapısı Meydan Okuması")
st.write(
    """
Kısa görevleri tamamla, puan topla ve **Piyasa Dedektifi** unvanına ulaş.

Amaç formül ezberlemek değil; piyasada gördüğün işaretleri doğru yorumlamak.
"""
)

if not st.session_state.takim:
    takim = st.text_input("Takım / oyuncu adı", placeholder="Örn. Likidite Avcıları")
    if st.button("Oyuna Başla", type="primary"):
        if takim.strip():
            st.session_state.takim = takim.strip()
            st.rerun()
        else:
            st.warning("Önce bir takım veya oyuncu adı girin.")
    st.stop()

st.write(f"**Oyuncu:** {st.session_state.takim}")

m1, m2, m3 = st.columns(3)
m1.metric("🏅 Puan", st.session_state.puan)
m2.metric("❤️ Can", st.session_state.can)
m3.metric("🔥 Seri", st.session_state.seri)

tamamlanan = sum([
    st.session_state.q1_done,
    st.session_state.q2_done,
    st.session_state.q3_done,
    st.session_state.q4_done,
    st.session_state.q5_done,
])
st.progress(tamamlanan / 5)

st.divider()

# =================================================
# GÖREV 1
# =================================================
st.header("🎯 Seviye 1 — Spread ve Piyasa Derinliği")

with st.expander("📘 Önce kavramları aç", expanded=True):
    st.markdown(
        """
**Spread:** En iyi alış fiyatı ile en iyi satış fiyatı arasındaki farktır.

- **Dar spread:** alış ve satış fiyatları birbirine daha yakındır.
- **Geniş spread:** alış ve satış fiyatları birbirinden daha uzaktır.

**Piyasa derinliği:** Farklı fiyat seviyelerinde ne kadar alış ve satış emri bulunduğunu gösterir.

- **Derin piyasa:** daha fazla alış ve satış emri vardır.
- **Sığ piyasa:** daha az alış ve satış emri vardır.

**İpucu:** Dar spread tek başına yüksek likidite anlamına gelmez.
"""
    )

st.markdown(
    """
### Karşılaştır

**Piyasa A**
- Spread dar
- Piyasa derinliği yüksek

**Piyasa B**
- Spread geniş
- Piyasa derinliği düşük
"""
)

q1 = st.radio(
    "Aynı büyüklükte büyük bir piyasa alış emri hangi piyasada fiyatı daha fazla hareket ettirebilir?",
    ["Piyasa A", "Piyasa B"],
    index=None,
    key="game_q1"
)

if st.button("⚡ Hamleni Yap", key="check1", disabled=st.session_state.q1_done):
    if q1 == "Piyasa B":
        bonus = dogru("q1_done", 20)
        st.success(f"✅ Doğru! +20 puan" + (f" +{bonus} seri bonusu 🔥" if bonus else ""))
        st.markdown(
            """
Sığ piyasada karşı tarafta daha az emir vardır. Büyük bir piyasa emri mevcut emirleri daha hızlı tüketebilir.

**Kazanım:**  
👉 Piyasa derinliği azaldıkça büyük emirlerin fiyat etkisi artabilir.
"""
        )
    elif q1:
        yanlis()
        st.error("❌ Olmadı. 1 can kaybettin.")
        st.info("Derin piyasa, büyük emirleri daha sınırlı fiyat hareketiyle karşılayabilir.")
    else:
        st.info("Önce bir seçenek işaretleyin.")

st.divider()

# =================================================
# GÖREV 2
# =================================================
st.header("💸 Seviye 2 — Spread Avı")

with st.expander("📘 Kavram kartı", expanded=True):
    st.markdown(
        """
**Bid:** piyasadaki en yüksek alış fiyatıdır.  
**Ask:** piyasadaki en düşük satış fiyatıdır.

**Spread = Ask − Bid**

Spread yalnızca iki fiyat arasındaki fark değildir. Aynı zamanda piyasanın:

- işlem maliyeti,
- likiditesi,
- bilgi ve risk düzeyi

hakkında fikir verebilir.
"""
    )

st.markdown(
    """
### Mini hesap

- **Bid = 99,80 TL**
- **Ask = 100,20 TL**
"""
)

q2a = st.radio(
    "Spread kaç TL?",
    ["0,20 TL", "0,40 TL", "1,00 TL"],
    index=None,
    key="game_q2a"
)

q2b = st.radio(
    "Spread genişlediğinde genel olarak hangi yorum daha uygundur?",
    [
        "İşlem maliyeti artabilir ve likidite azalabilir.",
        "Şirketin temel değeri kesin olarak artmıştır.",
        "Piyasa mutlaka daha derindir."
    ],
    index=None,
    key="game_q2b"
)

if st.button("🔍 Sonucu Aç", key="check2", disabled=st.session_state.q2_done):
    if q2a == "0,40 TL" and q2b == "İşlem maliyeti artabilir ve likidite azalabilir.":
        bonus = dogru("q2_done", 20)
        st.success(f"✅ İki adım da doğru! +20 puan" + (f" +{bonus} seri bonusu 🔥" if bonus else ""))
        st.markdown(
            """
**Spread = 100,20 − 99,80 = 0,40 TL**

**Kazanım:**  
👉 Spread, işlem maliyeti ve likidite hakkında bilgi verir.
"""
        )
    else:
        yanlis()
        st.error("❌ En az bir cevap hatalı. 1 can kaybettin.")
        st.info("Önce Ask − Bid hesabını yap; sonra spread'in işlem koşullarıyla ilişkisini düşün.")

st.divider()

# =================================================
# GÖREV 3
# =================================================
st.header("🧠 Seviye 3 — Bilgi mi, Likidite mi?")

with st.expander("📘 Kavram kartı", expanded=True):
    st.markdown(
        """
**Bilgi şoku:** Şirketle ilgili yeni bilgi gelir ve yatırımcıların değerleme beklentisi değişir.

**Likidite şoku:** Şirketle ilgili yeni bilgi olmadan büyük alış veya satış baskısı oluşur.

Örnekler:
- fon çıkışları,
- portföy yeniden dengelemesi,
- teminat ihtiyacı.
"""
    )

st.markdown(
    """
### Vaka

Bir payın fiyatı kısa sürede düşüyor.

Aynı anda:
- spread genişliyor,
- piyasa derinliği azalıyor,
- büyük satışlar fiyatı daha fazla hareket ettiriyor,
- bir süre sonra fiyatın bir kısmı geri geliyor,
- şirket hakkında yeni bir haber bulunmuyor.
"""
)

q3 = st.radio(
    "En uygun ilk yorum hangisidir?",
    [
        "Likidite şoku yaşanmış olabilir.",
        "Şirketin temel değeri kesin olarak düşmüştür.",
        "Fiyat hareketinin tamamı yeni bilgiden kaynaklanmıştır."
    ],
    index=None,
    key="game_q3"
)

if st.button("🕵️ Vakayı Çöz", key="check3", disabled=st.session_state.q3_done):
    if q3 == "Likidite şoku yaşanmış olabilir.":
        bonus = dogru("q3_done", 20)
        st.success(f"✅ Vaka çözüldü! +20 puan" + (f" +{bonus} seri bonusu 🔥" if bonus else ""))
        st.markdown(
            """
Şirket hakkında yeni bilgi olmadan büyük satış baskısı oluşması likidite şokuyla uyumludur.

Fiyatın daha sonra kısmen geri dönmesi, hareketin bir bölümünün geçici likidite etkisi taşıyabileceğini düşündürür.

**Kazanım:**  
👉 Her fiyat hareketi yeni bilgi anlamına gelmez.
"""
        )
    elif q3:
        yanlis()
        st.error("❌ Fazla kesin yorum yaptın. 1 can kaybettin.")
        st.info("Fiyatın düşmesi tek başına bunun nedenini göstermez.")


st.divider()

# =================================================
# GÖREV 4
# =================================================
st.header("⚖️ Seviye 4 — Limit mi, Piyasa mı?")

with st.expander("📘 Kavram kartı", expanded=True):
    st.markdown(
        """
**Limit emir:** Yatırımcı kabul edebileceği fiyat sınırını belirler.

- Fiyat kontrolü daha yüksektir.
- Ancak emir hiç gerçekleşmeyebilir veya kısmen gerçekleşebilir.

**Piyasa emri:** Mevcut karşıt emirlerle mümkün olan fiyatlardan işlem yapmayı amaçlar.

- Gerçekleşme olasılığı daha yüksektir.
- Ancak gerçekleşme fiyatı önceden kesin değildir.

**Temel fark:**  
Limit emir daha fazla **fiyat kontrolü**, piyasa emri daha fazla **gerçekleşme olasılığı** sağlar.
"""
    )

q4 = st.radio(
    "Bir yatırımcı fiyat kontrolüne çok önem veriyor ve emrin hemen gerçekleşmesi şart değil. Hangi emir daha uygundur?",
    [
        "Limit emir",
        "Piyasa emri"
    ],
    index=None,
    key="game_q4"
)

if st.button("🎯 Emir Seçimini Kilitle", key="check4", disabled=st.session_state.q4_done):
    if q4 == "Limit emir":
        bonus = dogru("q4_done", 20)
        st.success(f"✅ Doğru! +20 puan" + (f" +{bonus} seri bonusu 🔥" if bonus else ""))
        st.markdown(
            """
**Neden?**  
Limit emirde yatırımcı kabul edeceği fiyatı belirler.

**Kazanım:**  
👉 Emir seçimi, **fiyat kontrolü ile gerçekleşme olasılığı** arasındaki tercihtir.
"""
        )
    elif q4:
        yanlis()
        st.error("❌ Bu kez olmadı. 1 can kaybettin.")
        st.info("Piyasa emri daha yüksek gerçekleşme olasılığı sağlar; ancak fiyat kontrolü daha düşüktür.")

st.divider()

# =================================================
# GÖREV 5
# =================================================
st.header("🌊 Seviye 5 — Piyasa Toparlanıyor mu?")

with st.expander("📘 Kavram kartı", expanded=True):
    st.markdown(
        """
**Resiliency**, piyasanın bir işlem veya şoktan sonra ne kadar hızlı normale döndüğünü gösterir.

Örneğin büyük bir satış emri:

- alış emirlerini azaltabilir,
- spread'i genişletebilir,
- fiyatı düşürebilir.

Yeni emirler geldikçe piyasa yeniden dengelenir.

**Piyasa hızlı toparlanıyorsa resiliency yüksektir.**
"""
    )

q5 = st.radio(
    "Büyük bir satıştan sonra spread kısa sürede yeniden daralıyor ve alış emirleri geri geliyorsa en uygun yorum hangisidir?",
    [
        "Piyasanın resiliency'si yüksektir.",
        "Piyasa mutlaka sığdır.",
        "Şirketin temel değeri kesin olarak artmıştır."
    ],
    index=None,
    key="game_q5"
)

if st.button("🌊 Toparlanmayı Yorumla", key="check5", disabled=st.session_state.q5_done):
    if q5 == "Piyasanın resiliency'si yüksektir.":
        bonus = dogru("q5_done", 20)
        st.success(f"✅ Doğru! +20 puan" + (f" +{bonus} seri bonusu 🔥" if bonus else ""))
        st.markdown(
            """
Piyasa şoktan sonra hızlı biçimde yeniden dengeleniyor.

**Kazanım:**  
👉 Likidite yalnızca spread ve derinlikten değil, **toparlanma hızından** da oluşur.
"""
        )
    elif q5:
        yanlis()
        st.error("❌ Fazla kesin yorum. 1 can kaybettin.")
        st.info("Burada önemli olan, şoktan sonra piyasanın ne kadar hızlı normale döndüğüdür.")

st.divider()

# =================================================
# BONUS
# =================================================
if tamamlanan == 5:
    st.header("⭐ Bonus Tur — Piyasa Dedektifi")

    st.write(
        """
Bir payda **spread dar**, ancak emir miktarları çok düşük.

Hangisi daha doğru?
"""
    )

    qb = st.radio(
        "Bonus cevabın:",
        [
            "Pay kesinlikle çok likittir.",
            "Dar spread olumlu bir işarettir; ancak düşük derinlik nedeniyle büyük emirler yine fiyatı hareket ettirebilir.",
            "Piyasa derinliği artık önemli değildir."
        ],
        index=None,
        key="bonus_q"
    )

    if st.button("🏆 Bonus Cevabı Kilitle", disabled=st.session_state.bonus_done):
        if qb == "Dar spread olumlu bir işarettir; ancak düşük derinlik nedeniyle büyük emirler yine fiyatı hareket ettirebilir.":
            if not st.session_state.bonus_done:
                st.session_state.bonus_done = True
                st.session_state.puan += 15
            st.success("🌟 Bonus doğru! +15 puan")
            st.write("Dar spread tek başına yüksek likidite anlamına gelmez.")
        elif qb:
            st.warning("Bonus kaçtı. Spread ile derinliği birlikte düşün.")

st.divider()

# =================================================
# SONUÇ / REKABET
# =================================================
st.header("🏁 Skor Kartı")

puan = st.session_state.puan

if puan >= 110:
    unvan = "🏆 Piyasa Dedektifi — Usta Seviye"
elif puan >= 90:
    unvan = "🥇 Piyasa Dedektifi"
elif puan >= 70:
    unvan = "🥈 Likidite Avcısı"
elif puan >= 50:
    unvan = "🥉 Emir İzleyicisi"
else:
    unvan = "📘 Çaylak Trader"

st.subheader(unvan)
st.write(f"**{st.session_state.takim} skoru: {puan} puan**")

if tamamlanan == 5:
    st.success("Beş ana görevin tamamlandı.")
    st.markdown(
        """
### Bugünün 5 ana mesajı
1. **Piyasa derinliği azaldıkça büyük emirlerin fiyat etkisi artabilir.**
2. **Spread, işlem maliyeti ve likidite hakkında bilgi verir.**
3. **Her fiyat hareketi yeni bilgi anlamına gelmez.**
4. **Emir seçimi, fiyat kontrolü ile gerçekleşme olasılığı arasında bir tercihtir.**
5. **Resiliency, piyasanın bir şoktan sonra ne kadar hızlı toparlandığını gösterir.**
"""
    )

st.info(
    "💡 Sınıf rekabeti için herkes ekranındaki son puanı söylesin; en yüksek puanlı takım/oyuncu kazanır."
)

if st.button("🔄 Oyunu Sıfırla"):
    for key in list(defaults.keys()):
        st.session_state[key] = defaults[key]
    st.rerun()
