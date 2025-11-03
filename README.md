# WOS 영주장비 계산기

Whiteout Survival 영주 장비 업그레이드에 필요한 자원을 계산하는 웹 애플리케이션입니다.

## 주요 기능

- ✅ 6개 부위별 장비 등급 설정 (창병, 방패병, 궁병)
- ✅ 현재/목표 등급 비교 입력
- ✅ T4 최신 등급 지원
- ✅ 필요 자원 자동 계산 (설계도면, 합금, 윤활제, 앰버)
- ✅ 부위별 상세 자원 내역 제공
- ✅ 모바일 반응형 디자인

## 로컬 실행 방법

```bash
# 필요한 패키지 설치
pip install -r requirements.txt

# 앱 실행
streamlit run gear_calc.py
```

## 배포

이 앱은 [Streamlit Community Cloud](https://streamlit.io/cloud)를 통해 무료로 배포할 수 있습니다.

1. GitHub 저장소에 코드 업로드
2. Streamlit Community Cloud에서 저장소 연결
3. `gear_calc.py`를 메인 파일로 설정
4. Deploy 버튼 클릭

## 데이터 업데이트

`data/gear_data.csv` 파일에서 장비 등급별 필요 자원을 수정할 수 있습니다.

## 버전 정보

- **v2.0** - T4 신규레벨 반영 (2025.11.03)
- 모던 UI 디자인 적용
- 현재/목표 등급 분리 입력

## 제작

Made by **Lime**
