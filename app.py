import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 상수
sigma = 5.67e-8  # 스테판-볼츠만 상수

st.title("🌍 복사 평형과 지표 온도 시뮬레이터")

st.write("""
이 앱은 **복사 평형**을 바탕으로  
알베도, 온실 효과 변화에 따른 **지표 평균 온도**를 보여줍니다.
""")

# -----------------------------
# 입력 슬라이더
# -----------------------------
S = st.slider("태양 상수 S (W/m²)", 1200, 1500, 1361)
base_albedo = st.slider("기본 알베도", 0.1, 0.8, 0.30)
greenhouse = st.slider("온실 효과 계수", 0.0, 0.6, 0.33)

ice_feedback = st.checkbox("❄ 빙하–알베도 양의 피드백 적용")

# -----------------------------
# 피드백 적용 알베도 계산
# -----------------------------
def effective_albedo(T_c, base_albedo):
    if ice_feedback and T_c < 0:
        return min(base_albedo + 0.2, 0.9)
    return base_albedo

# -----------------------------
# 1회 계산
# -----------------------------
absorbed = (1 - base_albedo) * S / 4
effective_energy = absorbed * (1 + greenhouse)
T = (effective_energy / sigma) ** 0.25
T_c = T - 273.15

albedo_used = effective_albedo(T_c, base_albedo)

# 재계산 (피드백 반영)
absorbed_fb = (1 - albedo_used) * S / 4
effective_energy_fb = absorbed_fb * (1 + greenhouse)
T_fb = (effective_energy_fb / sigma) ** 0.25
T_fb_c = T_fb - 273.15

# -----------------------------
# 결과 출력
# -----------------------------
st.subheader("📊 계산 결과")

st.metric("지표 평균 온도 (℃)", round(T_fb_c, 2))
st.write(f"적용된 알베도: **{round(albedo_used, 2)}**")

# -----------------------------
# 그래프 ① 알베도–온도 관계
# -----------------------------
st.subheader("📈 알베도 변화에 따른 지표 온도")

albedo_range = np.linspace(0.1, 0.8, 50)
temps = []

for a in albedo_range:
    absorbed = (1 - a) * S / 4
    energy = absorbed * (1 + greenhouse)
    T_temp = (energy / sigma) ** 0.25 - 273.15
    temps.append(T_temp)

fig, ax = plt.subplots()
ax.plot(albedo_range, temps)
ax.set_xlabel("알베도")
ax.set_ylabel("지표 평균 온도 (℃)")
ax.set_title("알베도 증가 → 지표 온도 감소")

st.pyplot(fig)

# -----------------------------
# 해석 안내
# -----------------------------
st.write("""
### 🔍 해석 포인트
- 알베도가 증가하면 반사 에너지가 증가하여 지표 온도는 감소한다.
- 빙하가 증가하면 알베도가 커져 **추가 냉각**이 발생한다.
- 이는 **양의 피드백(positive feedback)**의 대표적인 예이다.
""")

st.warning("""
⚠️ 본 모델은 개념 이해를 위한 단순화 모델입니다.
실제 지구 시스템은 훨씬 복잡합니다.
""")