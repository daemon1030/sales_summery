# 📊 매출/지출 상세 분석 시스템

엑셀 파일을 업로드하면 매출과 지출을 자동으로 분석해주는 대시보드입니다.  
월별(8일~익월 7일 기준) 및 연도별 정산을 시각화하여 한눈에 파악할 수 있습니다.

---

## 🖥️ 주요 기능

### 월별 상세 분석
- 수입 대비 **순수익률** 계산 및 시각화
- 카드/현금/재료대/인건비/월세/관리금 **원형 그래프** 비중 분석
- **일별 수입 및 순수익 추이** 막대그래프
- 지출 상세 항목 토글 기능이 있는 **상세 데이터 테이블**

### 연도별 종합 분석
- 연간 총 수입 / 총 순수익 / 평균 순수익률 요약
- **월별 수입 및 순수익 추이** 그래프
- 정산 요약표

---

## 🛠️ 기술 스택

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)

---

## ▶️ 실행 방법

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 앱 실행
streamlit run sales.py
```

실행 후 브라우저에서 `http://localhost:8501` 접속

---

## 📂 엑셀 파일 형식

업로드할 `.xlsx` 파일은 아래 조건을 충족해야 합니다.

- 시트명: `월별`
- 헤더 위치: 3행 (header=2)
- 필수 컬럼: `날짜`, `카드`, `현금`, `월결재`, `토탈수입`, `토탈재료대`, `토탈인건비`, `월세`, `관리금`, `남은돈`

> 테스트용 샘플 파일: [`sample_data.xlsx`](./sample_data.xlsx)

---

## 📅 정산 기준

이 시스템은 일반적인 월 기준(1일~말일)이 아닌 **8일~익월 7일**을 한 달로 계산합니다.

- 날짜가 8일 이상 → 해당 월로 집계
- 날짜가 7일 이하 → 전월로 집계
