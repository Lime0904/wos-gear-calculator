import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="WOS 영주장비 계산기",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS - 모던 미니멀 디자인
st.markdown("""
<style>
    /* 전체 배경 - 심플한 그레이 */
    .stApp {
        background-color: #f5f7fa;
    }

    /* 메인 컨테이너 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1000px;
    }

    /* 모바일 반응형 */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }

        h1 {
            font-size: 1.5rem !important;
        }

        h2 {
            font-size: 1.2rem !important;
        }

        h3 {
            font-size: 1rem !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.3rem !important;
        }
    }

    /* 헤더 스타일 */
    h1 {
        color: #1a1a1a !important;
        text-align: center;
        font-weight: 600;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }

    h2 {
        color: #2d3748 !important;
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 1.5rem;
        margin-top: 2rem;
    }

    h3 {
        color: #4a5568 !important;
        font-weight: 600;
        font-size: 1.1rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    /* 카드 스타일 - 깔끔한 화이트 */
    .stExpander {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        margin-bottom: 0.75rem;
    }

    .stExpander summary {
        color: #2d3748 !important;
        font-weight: 600;
        font-size: 1rem;
    }

    /* Expander 내부 텍스트 */
    .stExpander div[data-testid="stExpanderDetails"] {
        background-color: white;
    }

    .stExpander div[data-testid="stExpanderDetails"] p,
    .stExpander div[data-testid="stExpanderDetails"] strong {
        color: #2d3748 !important;
    }

    /* 입력 필드 */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid #cbd5e0;
        font-size: 0.95rem;
    }

    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within {
        border-color: #4299e1;
        box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
    }

    .stNumberInput label,
    .stSelectbox label {
        color: #4a5568 !important;
        font-weight: 500;
        font-size: 0.9rem;
    }

    /* Markdown 텍스트 강제 색상 지정 */
    .stMarkdown p, .stMarkdown strong, .stMarkdown b {
        color: #2d3748 !important;
    }

    /* 버튼 - 심플한 블루 */
    .stButton > button {
        background-color: #4299e1;
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 1rem;
        border: none;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        width: 100%;
    }

    .stButton > button:hover {
        background-color: #3182ce;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* 메트릭 카드 */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2d3748;
    }

    [data-testid="stMetricLabel"] {
        font-weight: 500;
        color: #718096 !important;
        font-size: 0.9rem;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.85rem;
    }

    /* 화살표 숨기기 */
    [data-testid="stMetricDelta"] svg {
        display: none;
    }

    /* 데이터프레임 */
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
    }

    /* 결과 영역 배경 */
    .result-section {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin-top: 2rem;
    }

    /* 구분선 */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background-color: #e2e8f0;
    }

    @media (max-width: 768px) {
        hr {
            margin: 1.5rem 0;
        }
    }

    /* 서브타이틀 스타일 */
    .subtitle {
        color: #718096;
        font-size: 0.95rem;
        text-align: center;
        margin-bottom: 0.3rem;
    }

    .version {
        color: #a0aec0;
        font-size: 0.8rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# CSV 데이터 로딩
@st.cache_data
def load_data():
    gear_df = pd.read_csv("data/gear_data.csv")
    # packages_df = pd.read_csv("data/packages.csv")  # 패키지 기능 비활성화
    return gear_df

gear_df = load_data()
gear_levels = gear_df["Level"].tolist()

# 기어 자원 사전 생성
resource_dict = {
    row["Level"]: {
        "Alloy": row["Alloy"],
        "Polish": row["Polish"],
        "Design": row["Design"],
        "Amber": row["Amber"]
    } for _, row in gear_df.iterrows()
}

# 등급 한국어 매핑
level_labels = {
    "Green": "고급", "Green 1*": "고급 1성",
    "Blue": "레어", "Blue 1*": "레어 1성", "Blue 2*": "레어 2성", "Blue 3*": "레어 3성",
    "Purple": "에픽", "Purple 1*": "에픽 1성", "Purple 2*": "에픽 2성", "Purple 3*": "에픽 3성",
    "Purple T1": "에픽 T1", "Purple T1 1*": "에픽 T1 1성", "Purple T1 2*": "에픽 T1 2성", "Purple T1 3*": "에픽 T1 3성",
    "Gold": "레전드", "Gold 1*": "레전드 1성", "Gold 2*": "레전드 2성", "Gold 3*": "레전드 3성",
    "Gold T1": "레전드 T1", "Gold T1 1*": "레전드 T1 1성", "Gold T1 2*": "레전드 T1 2성", "Gold T1 3*": "레전드 T1 3성",
    "Gold T2": "레전드 T2", "Gold T2 1*": "레전드 T2 1성", "Gold T2 2*": "레전드 T2 2성", "Gold T2 3*": "레전드 T2 3성",
    "Legendary": "신화", "Legendary 1*": "신화 1성", "Legendary 2*": "신화 2성", "Legendary 3*": "신화 3성",
    "Legendary T1": "신화 T1", "Legendary T1 1*": "신화 T1 1성", "Legendary T1 2*": "신화 T1 2성", "Legendary T1 3*": "신화 T1 3성",
    "Legendary T2": "신화 T2", "Legendary T2 1*": "신화 T2 1성", "Legendary T2 2*": "신화 T2 2성", "Legendary T2 3*": "신화 T2 3성",
    "Legendary T3": "신화 T3", "Legendary T3 1*": "신화 T3 1성", "Legendary T3 2*": "신화 T3 2성", "Legendary T3 3*": "신화 T3 3성",
    "Legendary T3 3*-1": "신화 T3 3성-1", "Legendary T3 3*-2": "신화 T3 3성-2", "Legendary T3 3*-3": "신화 T3 3성-3", "Legendary T3 3*-4": "신화 T3 3성-4",
    "Legendary T4": "신화 T4", "Legendary T4-1": "신화 T4-1", "Legendary T4-2": "신화 T4-2", "Legendary T4-3": "신화 T4-3", "Legendary T4-4": "신화 T4-4",
    "Legendary T4 1*": "신화 T4 1성", "Legendary T4 1*-1": "신화 T4 1성-1", "Legendary T4 1*-2": "신화 T4 1성-2", "Legendary T4 1*-3": "신화 T4 1성-3", "Legendary T4 1*-4": "신화 T4 1성-4",
    "Legendary T4 2*": "신화 T4 2성", "Legendary T4 2*-1": "신화 T4 2성-1", "Legendary T4 2*-2": "신화 T4 2성-2", "Legendary T4 2*-3": "신화 T4 2성-3", "Legendary T4 2*-4": "신화 T4 2성-4",
    "Legendary T4 3*": "신화 T4 3성",
}

# 병종별 부위 매핑
gear_groups = {
    "방패병": ["Coat", "Pants"],
    "궁병": ["Ring", "Cudgel"],
    "창병": ["Hat", "Watch"]
}

gear_parts_kor = {
    "Hat": "모자",
    "Coat": "상의",
    "Ring": "반지",
    "Watch": "시계",
    "Pants": "하의",
    "Cudgel": "지팡이"
}

st.title("WOS 영주장비 계산기")
st.markdown('<p class="subtitle">영주 장비 업그레이드에 필요한 자원을 계산해보세요</p>', unsafe_allow_html=True)
st.markdown("---")

# 부위 선택 입력
user_inputs = {}

# 기본 선택값 찾기
default_cur = "Legendary T3 3*" if "Legendary T3 3*" in gear_levels else "Gold"
default_tar = "Legendary T4 3*" if "Legendary T4 3*" in gear_levels else "Gold"

# 부위별 병종 매핑
part_unit_type = {
    "Hat": "창병",
    "Watch": "창병",
    "Coat": "방패병",
    "Pants": "방패병",
    "Ring": "궁병",
    "Cudgel": "궁병"
}

# 부위 레이아웃: 2열 x 3행 (창병 -> 방패병 -> 궁병)
gear_layout = [
    ["Hat", "Watch"],      # 1행: 창병
    ["Coat", "Pants"],     # 2행: 방패병
    ["Ring", "Cudgel"]     # 3행: 궁병
]

# 현재 장비 등급
st.subheader("현재 장비 등급")
current_selections = {}
for row in gear_layout:
    cols = st.columns(2)
    for col_idx, part in enumerate(row):
        with cols[col_idx]:
            part_label = gear_parts_kor[part]
            unit_type = part_unit_type[part]
            current_selections[part_label] = st.selectbox(
                f"{part_label} ({unit_type})",
                options=gear_levels,
                index=gear_levels.index(default_cur),
                key=f"{part}_cur",
                format_func=lambda x: level_labels.get(x, x),
                help=f"{part_label}의 현재 등급"
            )

st.markdown("---")

# 목표 장비 등급
st.subheader("목표 장비 등급")
target_selections = {}
for row in gear_layout:
    cols = st.columns(2)
    for col_idx, part in enumerate(row):
        with cols[col_idx]:
            part_label = gear_parts_kor[part]
            unit_type = part_unit_type[part]
            target_selections[part_label] = st.selectbox(
                f"{part_label} ({unit_type})",
                options=gear_levels,
                index=gear_levels.index(default_tar),
                key=f"{part}_tar",
                format_func=lambda x: level_labels.get(x, x),
                help=f"{part_label}의 목표 등급"
            )

# user_inputs 딕셔너리 생성
for part_label in current_selections.keys():
    user_inputs[part_label] = (current_selections[part_label], target_selections[part_label])

st.markdown("---")
st.subheader("보유 자원")

# 2x2 그리드로 재배치
row1 = st.columns(2)
row2 = st.columns(2)

user_owned = {
    "Design": row1[0].number_input(
        "설계도면",
        min_value=0,
        value=0,
        step=100,
        help="보유 중인 설계도면 개수"
    ),
    "Alloy": row1[1].number_input(
        "합금",
        min_value=0,
        value=0,
        step=1000,
        help="보유 중인 합금 개수"
    ),
    "Polish": row2[0].number_input(
        "윤활제",
        min_value=0,
        value=0,
        step=100,
        help="보유 중인 윤활제 개수"
    ),
    "Amber": row2[1].number_input(
        "앰버",
        min_value=0,
        value=0,
        step=10,
        help="보유 중인 앰버 개수"
    ),
}

# 총 보유 자원 계산
total_owned = user_owned.copy()

st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    calculate_btn = st.button(
        "계산하기",
        type="primary",
        use_container_width=True
    )

if calculate_btn:
    total_needed = {k: 0 for k in user_owned}
    upgrade_details = []
    has_upgrade = False

    for part, (cur, tar) in user_inputs.items():
        i1 = gear_levels.index(cur)
        i2 = gear_levels.index(tar)
        if i1 >= i2:
            continue

        has_upgrade = True
        part_resources = {k: 0 for k in user_owned}
        for level in gear_levels[i1+1:i2+1]:
            for k in total_needed:
                amount = resource_dict.get(level, {}).get(k, 0)
                total_needed[k] += amount
                part_resources[k] += amount

        upgrade_details.append({
            "부위": part,
            "현재": level_labels.get(cur, cur),
            "목표": level_labels.get(tar, tar),
            **{f"{k}": part_resources[k] for k in user_owned}
        })

    if not has_upgrade:
        st.warning("⚠️ 업그레이드할 장비가 없습니다. 목표 등급을 현재 등급보다 높게 설정해주세요.")
    else:
        st.subheader("자원 요약")

        # 메트릭 카드로 총합 표시
        st.markdown("### 필요 자원 총량")
        metric_cols = st.columns(4)
        resource_names = {
            "Design": "설계도면",
            "Alloy": "합금",
            "Polish": "윤활제",
            "Amber": "앰버"
        }

        for i, (k, v) in enumerate(user_owned.items()):
            with metric_cols[i]:
                deficit = total_needed[k] - total_owned.get(k, 0)
                if deficit > 0:
                    # 부족 = 빨간색 ↓
                    st.metric(
                        label=resource_names[k],
                        value=f"{total_needed[k]:,}",
                        delta=f"부족 {deficit:,}",
                        delta_color="inverse",
                        help=f"필요: {total_needed[k]:,} | 보유: {total_owned.get(k, 0):,}"
                    )
                elif deficit < 0:
                    # 초과 = 초록색 ↑
                    st.metric(
                        label=resource_names[k],
                        value=f"{total_needed[k]:,}",
                        delta=f"초과 {abs(deficit):,}",
                        delta_color="normal",
                        help=f"필요: {total_needed[k]:,} | 보유: {total_owned.get(k, 0):,}"
                    )
                else:
                    # 충분 = 회색, 화살표 없음
                    st.metric(
                        label=resource_names[k],
                        value=f"{total_needed[k]:,}",
                        delta="충분",
                        delta_color="off",
                        help=f"필요: {total_needed[k]:,} | 보유: {total_owned.get(k, 0):,}"
                    )

        st.markdown("### 상세 내역")

        # 결과 테이블
        result_data = []
        for k in user_owned:
            result_data.append({
                "자원": resource_names[k],
                "필요량": f"{total_needed[k]:,}",
                "보유량": f"{total_owned.get(k, 0):,}",
                "부족량": f"{max(0, total_needed[k] - total_owned.get(k, 0)):,}"
            })

        result_df = pd.DataFrame(result_data)
        st.dataframe(
            result_df,
            use_container_width=True,
            hide_index=True
        )

        # 부위별 업그레이드 상세
        if upgrade_details:
            st.markdown("### 부위별 필요 자원")
            upgrade_df = pd.DataFrame(upgrade_details)
            st.dataframe(
                upgrade_df,
                use_container_width=True,
                hide_index=True
            )

st.markdown("---")
st.markdown("""
<div style='text-align:center; padding: 1.5rem; color: #a0aec0;'>
    <p style='font-size: 0.85rem; margin: 0;'>
        Made by <b>Lime</b>
    </p>
    <p style='font-size: 0.75rem; margin-top: 0.3rem;'>
        v2.0 · T4 신규레벨 반영 · 최종 수정 2025.11.03
    </p>
</div>
""", unsafe_allow_html=True)
