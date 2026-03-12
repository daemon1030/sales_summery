import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="new김밥나라 정산 시스템", layout="wide")
st.title("🍱 new김밥나라 매출/지출 상세 분석")

uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요 (.xlsx)", type=["xlsx"])

def get_custom_month(date):
    try:
        if date.day >= 8:
            return date.year, date.month
        else:
            prev_month = date.replace(day=1) - timedelta(days=1)
            return prev_month.year, prev_month.month
    except:
        return None, None

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, sheet_name='월별', header=2)
        df.columns = [str(c).strip() for c in df.columns]
        df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
        df = df.dropna(subset=['날짜'])
        
        # 분석 항목 수치화
        num_cols = ['카드', '현금', '월결재', '토탈수입', '토탈재료대', '토탈인건비', '월세', '관리금', '남은돈']
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        df['정산년월'] = df['날짜'].apply(lambda x: f"{get_custom_month(x)[0]}년 {get_custom_month(x)[1]}월분")
        df['정산연도'] = df['날짜'].apply(lambda x: f"{x.year}년")

        mode = st.sidebar.radio("보고서 선택", ["월별 상세 분석 (8일~7일)", "연도별 총 매출"])

        if mode == "월별 상세 분석 (8일~7일)":
            all_months = sorted(df['정산년월'].unique(), reverse=True)
            selected_month = st.selectbox("정산 월 선택", all_months)
            month_df = df[df['정산년월'] == selected_month].sort_values('날짜')

            # --- 1. 순수익 리포트 (수입 대비 순수익 퍼센트 강조) ---
            total_revenue = month_df['토탈수입'].sum()
            total_profit = month_df['남은돈'].sum()
            profit_rate = (total_profit / total_revenue * 100) if total_revenue > 0 else 0

            st.subheader(f"💰 {selected_month} 수익 성적표")
            col_a, col_b = st.columns([1, 2])
            with col_a:
                st.metric("전체 수입 대비 순수익률", f"{profit_rate:.1f}%")
            with col_b:
                st.write(f"총 수입 {int(total_revenue):,}원 중 **{int(total_profit):,}원** 수익 발생")
                st.progress(min(max(profit_rate/100, 0.0), 1.0))

            # --- 2. 요청하신 6개 항목 원형 그래프 ---
            st.subheader("📊 매출 구성 및 지출 비중 (순수익 제외)")
            # 요청 항목: 카드, 현금, 토탈재료대, 토탈인건비, 월세, 관리금
            pie_data = {
                '항목': ['카드 수입', '현금 수입', '토탈재료대', '토탈인건비', '월세', '관리금'],
                '금액': [
                    month_df['카드'].sum(), 
                    month_df['현금'].sum(),
                    month_df['토탈재료대'].sum(), 
                    month_df['토탈인건비'].sum(),
                    month_df['월세'].sum(), 
                    month_df['관리금'].sum()
                ]
            }
            pie_df = pd.DataFrame(pie_data)
            pie_df = pie_df[pie_df['금액'] > 0] # 0원인 항목은 제외

            fig_pie = px.pie(pie_df, values='금액', names='항목', hole=0.4,
                             color_discrete_sequence=px.colors.qualitative.Set3)
            fig_pie.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

            # --- 3. 일별 매출 흐름 (막대그래프) ---
            st.subheader("📈 일별 수입 및 순수익 추이")
            fig_bar = px.bar(month_df, x='날짜', y=['토탈수입', '남은돈'], barmode='group')
            fig_bar.update_layout(
                yaxis=dict(tickformat=",.0f", range=[-200000, 1500000]),
                legend_title_text='구분'
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            # --- 4. 상세 데이터 (더보기) ---
            st.subheader("📋 상세 데이터")
            show_more = st.checkbox("지출 상세 항목 더보기 (인건비, 월세, 관리금)")
            display_cols = ['날짜', '카드', '현금', '토탈수입', '토탈재료대', '남은돈']
            if show_more:
                display_cols = ['날짜', '카드', '현금', '토탈수입', '토탈재료대', '토탈인건비', '월세', '관리금', '남은돈']
            
            st.dataframe(month_df[display_cols].style.format(precision=0, thousands=","), use_container_width=True)

        else:
            # --- 연도별 총 매출 분석 페이지 ---
            st.header("📈 연도별 종합 성적표")
            all_years = sorted(df['정산연도'].unique(), reverse=True)
            selected_year = st.selectbox("조회할 연도 선택", all_years)
            
            year_df = df[df['정산연도'] == selected_year]
            
            # 연도 전체 합계 계산
            y_total_revenue = year_df['토탈수입'].sum()
            y_total_profit = year_df['남은돈'].sum()
            y_profit_rate = (y_total_profit / y_total_revenue * 100) if y_total_revenue > 0 else 0

            # --- 연도별 요약 인터페이스 추가 ---
            st.markdown(f"### 📊 {selected_year} 전체 요약")
            container = st.container()
            with container:
                col1, col2, col3 = st.columns(3)
                col1.metric(f"{selected_year} 총 수입", f"{int(y_total_revenue):,}원")
                col2.metric(f"{selected_year} 총 순수익", f"{int(y_total_profit):,}원")
                col3.metric("연평균 순수익률", f"{y_profit_rate:.1f}%")
                
                st.write(f"**{selected_year} 수익률 시각화**")
                st.progress(min(max(y_profit_rate/100, 0.0), 1.0))
            
            st.divider()

            # 연도별 월간 추이 그래프
            st.subheader(f"📅 {selected_year} 월별 수입 및 순수익 추이")
            yearly_summary = year_df.groupby('정산년월')[['토탈수입', '남은돈']].sum().reset_index()
            
            fig_year = px.bar(yearly_summary, x='정산년월', y=['토탈수입', '남은돈'], 
                             barmode='group', text_auto=',.0f')
            fig_year.update_layout(
                yaxis=dict(tickformat=",.0f", range=[-1000000, 25000000]),
                legend_title_text='항목'
            )
            st.plotly_chart(fig_year, use_container_width=True)

            # 연도별 상세 데이터 표
            st.subheader(f"📋 {selected_year} 정산 요약표")
            st.table(yearly_summary.style.format({
                '토탈수입': '{:,.0f}원',
                '남은돈': '{:,.0f}원'
            }))

    except Exception as e:
        st.error(f"오류 발생: {e}")