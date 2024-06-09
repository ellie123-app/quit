import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
matplotlib.use('Agg')
import gdown
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(layout="wide")

# 키워드 설정
access_keyword = "nullee_quit"

# 사용자 입력 요청
user_input = st.text_input("접근하려면 키워드를 입력하세요:", "")


# 키워드 검증
if user_input == access_keyword:
    st.success("접근이 허용되었습니다!")
    
    
    
    plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows의 경우
    plt.rcParams['axes.unicode_minus'] = False
    
    # 전체 시트 quit7
    file_id = '176joJvx9vWJ1YeL558YtFaZxlYUQHDdZ'
    url = f'https://drive.google.com/uc?id={file_id}'
    
    # 가입자 대비 탈퇴율 시트 new_quit_final
    file_id0 = '1-9yLe2XkKc1ebj_uS-AOXkgluNPC7QaR'
    url0 = f'https://drive.google.com/uc?id={file_id0}'
    
    data = pd.read_csv(url,encoding='utf-8')
    sub_data = pd.read_csv(url0,encoding='utf-8')
    
    if '탈퇴 일자' in data.columns:
        data['탈퇴 일자'] = pd.to_datetime(data['탈퇴 일자'], errors='coerce')
    
    if '날짜' in sub_data.columns:
        sub_data['날짜'] = pd.to_datetime(sub_data['날짜'], errors='coerce')
        
    st.sidebar.title("페이지 선택")
    page = st.sidebar.selectbox("카테고리별로 볼 수 있어요", ["요약", "탈퇴사유별", "사용자유형별", "채널별", "가입기간별", "접속횟수별", "직접 입력할게요"])
    
    # ------------------------------------------------------------------------------------------------------
     
    
    if page == "요약":
        st.title("탈퇴 대시보드")
        st.text("""탈퇴 통계 어드민 개선 전, 간단하게 탈퇴 통계를 확인하기 위해 제작한 대시보드입니다.
    실시간 연동은 불가하여, 전날까지의 데이터를 업데이트합니다.
        """)
        
        st.text("""
        """)
    
        # 기간 선택 버튼을 가로로 배치
        col1, col2 = st.columns(2)
        
        yesterday = datetime.now() - timedelta(days=1)
        
        with col1:
            start_date = st.date_input("시작 날짜", value=(datetime(2024, 5, 31)).date(), key='start_date')
        
        with col2:
            end_date = st.date_input("종료 날짜", value=yesterday.date(), key='end_date')
    
        st.text("""
        """)
        st.text("""
        """)
        
        # 선택한 날짜 범위에 따라 데이터 필터링
        if '탈퇴 일자' in data.columns:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)  # 종료 날짜를 하루의 끝으로 설정
            filtered = data[(data['탈퇴 일자'] >= start_date) & (data['탈퇴 일자'] <= end_date)]
            
        else:
            filtered = data
    
        # 선택한 날짜 범위에 따라 데이터 필터링
        if '날짜' in sub_data.columns:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)  # 종료 날짜를 하루의 끝으로 설정
            sub_data_filtered = sub_data[(sub_data['날짜'] >= start_date) & (sub_data['날짜'] <= end_date)]
        else:
            sub_data_filtered = sub_data
            
        # ------------------------------------------------------------------------------------------------------
        # filter 전처리
        # 탈퇴 사유별 개수 알기
        
        filter = filtered.copy()
        filter = pd.DataFrame(filter['탈퇴사유'].str.split(';'))
        filter = filter.explode('탈퇴사유')
        filter = filter.dropna(subset=['탈퇴사유'])
        filter = filter.reset_index(drop=True)
        reason_counts = filter['탈퇴사유'].value_counts().reset_index()
        reason_counts.columns = ['탈퇴사유', 'count']
        total_count = reason_counts['count'].sum()
        reason_counts['비율'] = (reason_counts['count'] / total_count) * 100
        reason_counts['비율'] = reason_counts['비율'].round(1)
        
        # 탈퇴 사용자별 알기
        filter0 = filtered.copy()
        user_type_counts = filter0['사용자 유형'].value_counts().reset_index()
        user_type_counts.columns = ['사용자 유형', 'count']
        total_count = user_type_counts['count'].sum()
        user_type_counts['비율'] = (user_type_counts['count'] / total_count) * 100
        user_type_counts['비율'] = user_type_counts['비율'].round(1)
    
        # 가입기간별 알기
        filter1 = filtered.copy()
        period = filter1['가입 구간'].value_counts().reset_index()
        period.columns = ['가입 구간', 'count']
        total_count = period['count'].sum()
        period['비율'] = (period['count'] / total_count) * 100
        period['비율'] = period['비율'].round(1)
    
        
        # 가입 구간을 특정 순서로 정렬
        order = ['0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
        period['가입 구간'] = pd.Categorical(period['가입 구간'], categories=order, ordered=True)
        period = period.sort_values('가입 구간')
    
    
        # 채널별 탈퇴 사유 비율 계산
        channel_counts = filtered['채널'].value_counts().reset_index()
        channel_counts.columns = ['채널', 'count']
        total_channel_count = channel_counts['count'].sum()
        channel_counts['비율'] = (channel_counts['count'] / total_channel_count) * 100
        channel_counts['비율'] = channel_counts['비율'].round(1)
    
        # 접속 횟수를 지정된 구간으로 나누기
        bins = [1, 2, 5, 10, 20, float('inf')]
        labels = ["1", "2~5", "5~10", "10~20", "20 이상"]
        data['접속 횟수 구간'] = pd.cut(data['총 접속 수'], bins=bins, labels=labels, right=False)
        
        # 접속 횟수별 비율 계산
        period_counts = data['접속 횟수 구간'].value_counts(normalize=True).reset_index()
        period_counts.columns = ['접속 횟수 구간', '비율']
        period_counts['비율'] = period_counts['비율'] * 100
    
    
        # 접속 횟수 구간을 특정 순서로 정렬
        period_counts['접속 횟수 구간'] = pd.Categorical(period_counts['접속 횟수 구간'], categories=labels, ordered=True)
        period_counts = period_counts.sort_values('접속 횟수 구간')
    
        # 1. 부가세, 종소세 계산 완료 또는 부가세, 종소세, 인건비 결제 완료 한 탈퇴자 비율
        tax_complete = filtered[(filtered['부가세 계산 완료 수'] > 0) | (filtered['종소세 계산 완료 수'] > 0) |
                                (filtered['부가세 결제 수'] > 0) | (filtered['종소세 결제 수'] > 0) | (filtered['인건비 결제 수'] > 0)]
        tax_complete_rate = (tax_complete.shape[0] / filtered.shape[0]) * 100
    
        # 2. 부가세 계산 진입 > 부가세 계산 완료 또는 종소세 계산 진입 > 종소세 계산 완료인 탈퇴자 비율
        tax_entry_complete = filtered[((filtered['부가세 계산 시작 수'] > 0) & (filtered['부가세 계산 완료 수'] > 0)) |
                                      ((filtered['종소세 계산 시작 수'] > 0) & (filtered['종소세 계산 완료 수'] > 0))]
        tax_entry_complete_rate = (tax_entry_complete.shape[0] / filtered.shape[0]) * 100
    
        # 3. 탈퇴자 SSEM/KKB 비율
        ssem_kkb_counts = filtered['채널'].value_counts(normalize=True).reset_index()
        ssem_kkb_counts.columns = ['채널', '비율']
        ssem_kkb_counts['비율'] = ssem_kkb_counts['비율'] * 100
    
        
        # ------------------------------------------------------------------------------------------------------
    
        col1, col2 = st.columns(2)
        
        with col1:
             # 전체 탈퇴자 수 계산
            total_churners = filtered.shape[0]
            
            st.markdown(f"""
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 140px; border: 2px solid gray; border-radius: 10px;">
                    <div style="font-size: 15px; color: gray; margin-top: 8px; margin-bottom: 10px;">전체 탈퇴자 수</div>
                    <div style="font-size: 50px; font-weight: bold;">{total_churners}명</div>
                </div>
            """, unsafe_allow_html=True)
    
        with col2:
            
            average = sub_data_filtered['탈퇴자 비율'].mean()
            
            st.markdown(f"""
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 140px; border: 2px solid gray; border-radius: 10px;">
                    <div style="font-size: 15px; color: gray; margin-top: 8px; margin-bottom: 10px;"> 가입 대비 탈퇴 비율 평균 </div>
                    <div style="font-size: 50px; font-weight: bold;">{average:.2%}</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 탈퇴 사유별 비율")
            sorted_reason_counts = reason_counts.sort_values(by='비율', ascending=True)
            fig1 = px.bar(sorted_reason_counts, x='비율', y='탈퇴사유', text='비율', orientation='h', color_discrete_sequence=['orange'])
            fig1.update_layout(width=800, height=400)
            st.plotly_chart(fig1)
            st.caption('')
    
            check0_key = "data_frame_view_0"
            check0 = st.checkbox('데이터프레임 보기', key=check0_key)
            if check0:
                reason_counts['비율'] = reason_counts['비율'].map("{:.1f}".format)
                st.table(reason_counts)
        
        with col2:
            st.write("### 사용자 유형별 비율")
            sorted_user_type_counts = user_type_counts.sort_values(by='비율', ascending=True)
            fig2 = px.bar(sorted_user_type_counts, x='비율', y='사용자 유형', text='비율', orientation='h', color_discrete_sequence=['orange'])
            fig2.update_layout(width=800, height=400)
            st.plotly_chart(fig2)
    
            check1_key = "data_frame_view_1"
            check1 = st.checkbox('데이터프레임 보기', key=check1_key)
            if check1:
                user_type_counts['비율'] = user_type_counts['비율'].map("{:.1f}".format)
                st.table(user_type_counts)
    
    
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    
        
        col1, col2 = st.columns(2)
            
        with col1:
    
            # 가입 기간별 비율 선 그래프
            st.write("### 가입 기간별 비율")
            fig3 = px.line(period, x='가입 구간', y='비율', markers=True)
            fig3.update_traces(line_color='orange')
            fig3.update_layout(width=800, height=400)
            st.plotly_chart(fig3)
        
            check2_key = "data_frame_view_2"
            check2 = st.checkbox('데이터프레임 보기', key=check2_key)
            if check2:
                period['비율'] = period['비율'].map("{:.1f}".format)
                st.dataframe(period)
            
        with col2:
            st.write("### 접속 횟수별 비율")
    
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=period_counts['접속 횟수 구간'],
                y=period_counts['비율'],
                mode='lines+markers', 
                name='접속 횟수 구간'
            ))
            fig.update_traces(line_color='orange')
            fig.update_layout(
                xaxis_title='접속 횟수 구간',
                yaxis_title='비율 (%)',
                legend_title='접속 횟수 구간'
            )
            
            st.plotly_chart(fig)
            
            # 데이터프레임 표시
            check3_key = "data_frame_view_3"
            check3 = st.checkbox('데이터프레임 보기', key=check3_key)
            if check3:
                period_counts['비율'] = period_counts['비율'].map("{:.1f}".format)
                st.table(period_counts)
    
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    
        col1, col2 = st.columns(2)
            
        with col1:
            st.write("### 채널별 비율")
            fig_channel = px.bar(channel_counts, x='비율', y='채널', text='비율', orientation='h', color_discrete_sequence=['orange'])
            fig_channel.update_layout(width=800, height=400)
            st.plotly_chart(fig_channel)
            
            check_channel_key = "data_frame_view_channel"
            check_channel = st.checkbox('데이터프레임 보기', key=check_channel_key)
            if check_channel:
                channel_counts['비율'] = channel_counts['비율'].map("{:.1f}".format)
                st.table(channel_counts)
    
    
    
    #---------------------------------------------------------------------------------------------- 
    
    if page == "탈퇴사유별":
        st.title("탈퇴 대시보드")
        st.text("""탈퇴 통계 어드민 개선 전, 간단하게 탈퇴 통계를 확인하기 위해 제작한 대시보드입니다.
    실시간 연동은 불가하여, 전날까지의 데이터를 업데이트합니다.
        """)
        
        st.text("""
        """)
    
        unique_reasons = data['탈퇴사유'].dropna().str.split(';').explode().str.strip().unique().tolist()
        unique_reasons.append('전체')
        
        # 기간 선택 버튼을 가로로 배치
        col1, col2 = st.columns(2)
        
        yesterday = datetime.now() - timedelta(days=1)
        
        with col1:
            start_date = st.date_input("시작 날짜", value=(datetime(2024, 5, 31)).date(), key='start_date')
        
        with col2:
            end_date = st.date_input("종료 날짜", value=yesterday.date(), key='end_date')
    
        
            
    
        st.text("""
        """)
        st.text("""
        """)
        
        # 선택한 날짜 범위에 따라 데이터 필터링
        if '탈퇴 일자' in data.columns:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)  # 종료 날짜를 하루의 끝으로 설정
            filtered = data[(data['탈퇴 일자'] >= start_date) & (data['탈퇴 일자'] <= end_date)]
            
            filtered = filtered.dropna(subset=['탈퇴사유'])
        
        
        else:
            filtered = data
    
            
        # ------------------------------------------------------------------------------------------------------
        # 사용자 유형 filter 전처리
        
        filter = filtered[['탈퇴사유', '사용자 유형']].copy()
        filter['탈퇴사유'] = filter['탈퇴사유'].str.split(';')
        filter = filter.explode('탈퇴사유')
        filter = filter.dropna(subset=['탈퇴사유'])
        filter = filter.reset_index(drop=True)
    
        total_reason_counts = filter['탈퇴사유'].value_counts().reset_index()
        total_reason_counts.columns = ['탈퇴사유', 'Total count']
    
        reason_counts = filter.groupby(['탈퇴사유', '사용자 유형']).size().reset_index(name='count')
        reason_counts = reason_counts.merge(total_reason_counts, on='탈퇴사유')
        reason_counts['비율'] = (reason_counts['count'] / reason_counts['Total count'] * 100).round(1)
    
        # 탈퇴 사유별 전체 비율 계산
        total_counts = filter['탈퇴사유'].value_counts().reset_index()
        total_counts.columns = ['탈퇴사유', 'count']
        total_counts['전체 비율'] = (total_counts['count'] / total_counts['count'].sum() * 100).round(1)
    
        # 사용자 유형별 비율 계산
        user_type_counts = reason_counts.pivot_table(index='탈퇴사유', columns='사용자 유형', values='비율', fill_value=0)
        user_type_counts = user_type_counts.reset_index()
        user_type_counts = user_type_counts.merge(total_counts[['탈퇴사유', '전체 비율']], on='탈퇴사유')
        user_type_counts = user_type_counts.merge(total_reason_counts, on='탈퇴사유')
        user_type_counts = user_type_counts.sort_values(by='전체 비율', ascending=False)
    
        # 사용자 유형 컬럼명 변경
        user_type_counts.columns = ['탈퇴사유', '개인사업자 비율', '그 외 비율', '법인 비율', '폐업 비율', '전체 비율', '개수']
    
        # 각 사용자 유형 비율에 전체 비율을 곱해서 최종 비율 계산
        user_type_counts['개인사업자 비율'] = (user_type_counts['개인사업자 비율'] * user_type_counts['전체 비율'] / 100).round(1)
        user_type_counts['그 외 비율'] = (user_type_counts['그 외 비율'] * user_type_counts['전체 비율'] / 100).round(1)
        user_type_counts['법인 비율'] = (user_type_counts['법인 비율'] * user_type_counts['전체 비율'] / 100).round(1)
        user_type_counts['폐업 비율'] = (user_type_counts['폐업 비율'] * user_type_counts['전체 비율'] / 100).round(1)
    
        # 최종 비율 컬럼 선택
        final_user_type_counts = user_type_counts[['탈퇴사유', '개수', '전체 비율', '개인사업자 비율', '그 외 비율', '법인 비율', '폐업 비율']]
    
        # 인덱스 재정렬
        final_user_type_counts.reset_index(drop=True, inplace=True)
    
        # 소숫점 한자리로 표시
        final_user_type_counts = final_user_type_counts.round(1)
    
    # ------------------------------------------------------------------------------------------------------
    
    
        # 가입 기간별 비율 전처리
        filter_join_period = filtered[['탈퇴사유', '가입 구간']].copy()
        filter_join_period['탈퇴사유'] = filter_join_period['탈퇴사유'].str.split(';')
        filter_join_period = filter_join_period.explode('탈퇴사유')
        filter_join_period = filter_join_period.dropna(subset=['탈퇴사유'])
        filter_join_period = filter_join_period.reset_index(drop=True)
        
        total_join_period_counts = filter_join_period['탈퇴사유'].value_counts().reset_index()
        total_join_period_counts.columns = ['탈퇴사유', 'Total count']
        
        order = ['0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
        filter_join_period['가입 구간'] = pd.Categorical(filter_join_period['가입 구간'], categories=order, ordered=True)
        
        join_period_counts = filter_join_period.groupby(['탈퇴사유', '가입 구간']).size().unstack(fill_value=0)
        join_period_counts = join_period_counts.div(join_period_counts.sum(axis=1), axis=0) * 100
        join_period_counts = join_period_counts.reset_index()
        
        total_join_counts = filter_join_period['탈퇴사유'].value_counts().reset_index()
        total_join_counts.columns = ['탈퇴사유', 'count']
        total_join_counts['전체 비율'] = (total_join_counts['count'] / total_join_counts['count'].sum() * 100).round(1)
        
        join_period_counts = join_period_counts.merge(total_join_counts[['탈퇴사유', 'count', '전체 비율']], on='탈퇴사유')
        for label in order:
            join_period_counts[label] = (join_period_counts[label] * join_period_counts['전체 비율'] / 100).round(1)
        
        final_join_period_counts = join_period_counts[['탈퇴사유', 'count', '전체 비율'] + [label for label in order]]
        final_join_period_counts.columns = ['탈퇴사유', '개수', '전체 비율', '0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
        final_join_period_counts = final_join_period_counts.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
    
            
        
    
    
        # ------------------------------------------------------------------------------------------------------
    
        # 접속 횟수 비율 전처리
        filter_access_count = filtered[['탈퇴사유', '총 접속 수']].copy()
        filter_access_count['탈퇴사유'] = filter_access_count['탈퇴사유'].str.split(';')
        filter_access_count = filter_access_count.explode('탈퇴사유')
        filter_access_count = filter_access_count.dropna(subset=['탈퇴사유'])
        filter_access_count = filter_access_count.reset_index(drop=True)
        
        bins = [1, 2, 5, 10, 20, float('inf')]
        labels = ["1", "2~5", "5~10", "10~20", "20 이상"]
        filter_access_count['접속 횟수 구간'] = pd.cut(filter_access_count['총 접속 수'], bins=bins, labels=labels, right=False)
        
        access_period_counts = filter_access_count.groupby(['탈퇴사유', '접속 횟수 구간']).size().unstack(fill_value=0)
        access_period_counts = access_period_counts.div(access_period_counts.sum(axis=1), axis=0) * 100
        access_period_counts = access_period_counts.reset_index()
        
        total_access_counts = filter_access_count['탈퇴사유'].value_counts().reset_index()
        total_access_counts.columns = ['탈퇴사유', 'count']
        total_access_counts['전체 비율'] = (total_access_counts['count'] / total_access_counts['count'].sum() * 100).round(1)
        
        access_period_counts = access_period_counts.merge(total_access_counts[['탈퇴사유', 'count', '전체 비율']], on='탈퇴사유')
        for label in labels:
            access_period_counts[label] = (access_period_counts[label] * access_period_counts['전체 비율'] / 100).round(1)
        
        final_access_period_counts = access_period_counts[['탈퇴사유', 'count', '전체 비율'] + labels]
        final_access_period_counts.columns = ['탈퇴사유', '개수', '전체 비율'] + labels
        final_access_period_counts = final_access_period_counts.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
        
    # -----------------------------------------------------------------------------------------------------------------
        
        # 탈퇴 사유별 채널 비율 계산
        filter2 = filtered[['탈퇴사유', '채널']].copy()
        filter2['탈퇴사유'] = filter2['탈퇴사유'].str.split(';')
        filter2 = filter2.explode('탈퇴사유')
        filter2 = filter2.dropna(subset=['탈퇴사유'])
        filter2 = filter2.reset_index(drop=True)
        
        total_reason_counts = filter2['탈퇴사유'].value_counts().reset_index()
        total_reason_counts.columns = ['탈퇴사유', 'Total count']
        
        channel_counts = filter2.groupby(['탈퇴사유', '채널']).size().reset_index(name='count')
        channel_counts = channel_counts.merge(total_reason_counts, on='탈퇴사유')
        channel_counts['비율'] = (channel_counts['count'] / channel_counts['Total count'] * 100).round(1)
        
        # 탈퇴 사유별 전체 비율 계산
        total_counts = filter2['탈퇴사유'].value_counts().reset_index()
        total_counts.columns = ['탈퇴사유', 'count']
        total_counts['전체 비율'] = (total_counts['count'] / total_counts['count'].sum() * 100).round(1)
        
        # 채널별 비율 계산
        channel_type_counts = channel_counts.pivot_table(index='탈퇴사유', columns='채널', values='비율', fill_value=0)
        channel_type_counts = channel_type_counts.reset_index()
        channel_type_counts = channel_type_counts.merge(total_counts[['탈퇴사유', '전체 비율']], on='탈퇴사유')
        channel_type_counts = channel_type_counts.merge(total_reason_counts, on='탈퇴사유')
        channel_type_counts = channel_type_counts.sort_values(by='Total count', ascending=False)
        
        # 채널 컬럼명 변경
        channel_type_counts.columns = ['탈퇴사유'] + list(channel_type_counts.columns[1:-2]) + ['전체 비율', '개수']
        
        # 각 채널 비율에 전체 비율을 곱해서 최종 비율 계산
        for col in channel_type_counts.columns[1:-2]:
            channel_type_counts[col] = (channel_type_counts[col] * channel_type_counts['전체 비율'] / 100).round(1)
        
        # 최종 비율 컬럼 선택
        final_channel_type_counts = channel_type_counts[['탈퇴사유', '개수', '전체 비율'] + list(channel_type_counts.columns[1:-2])]
        
        # 인덱스 재정렬
        final_channel_type_counts.reset_index(drop=True, inplace=True)
        
        # 소숫점 한자리로 표시
        final_channel_type_counts = final_channel_type_counts.round(1)
    
    # -----------------------------------------------------------------------------------------------------------------
    
        # 전체 탈퇴자 수 계산
        total_churners = filtered.shape[0]
            
        st.markdown(f"""
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 140px; border: 2px solid gray; border-radius: 10px;">
                    <div style="font-size: 15px; color: gray; margin-top: 8px; margin-bottom: 10px;">전체 탈퇴자 수</div>
                    <div style="font-size: 50px; font-weight: bold;">{total_churners}명</div>
                </div>
            """, unsafe_allow_html=True)
    
    
            
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    
        
     
        st.write("### 탈퇴 사유별 사용자 유형 비율")
    
        fig, ax = plt.subplots(figsize=(12, 6))
    
        user_types = ['개인사업자 비율', '그 외 비율', '법인 비율', '폐업 비율']
        cmap = plt.get_cmap('Set2')
        final_user_type_counts.set_index('탈퇴사유').iloc[:, 2:].plot(kind='barh', stacked=True, ax=ax, colormap=cmap)
        
        ax.set_xlabel('비율 (%)')
        ax.set_ylabel('탈퇴 사유')
        ax.legend(title='사용자 유형')
        plt.gca().invert_yaxis()
        
        st.pyplot(fig)
            
        for col in final_user_type_counts.columns:
            if final_user_type_counts[col].dtype == 'float64':
                final_user_type_counts[col] = final_user_type_counts[col].map("{:.1f}".format)
    
        # DataFrame 표시
        check0_key = "data_frame_view_0"
        check0 = st.checkbox('데이터프레임 보기', key=check0_key)
        if check0:
            st.table(final_user_type_counts)
    
    
    
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    
    
    
        # 가입 기간별 비율 선 그래프
        st.write("### 탈퇴 사유별 가입 기간 비율")
        fig = go.Figure()
        
        for reason in final_join_period_counts['탈퇴사유'].unique():
            reason_data = final_join_period_counts[final_join_period_counts['탈퇴사유'] == reason]
            fig.add_trace(go.Scatter(
                x=['0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상'],
                y=reason_data.iloc[0, 3:].values,
                mode='lines+markers', 
                name=reason))
        
        fig.update_layout(
            xaxis_title='가입 구간',
            yaxis_title='비율 (%)',
            legend_title='탈퇴 사유'
        )
        
        st.plotly_chart(fig)
        
        for col in final_join_period_counts.columns:
            if final_join_period_counts[col].dtype == 'float64':
                final_join_period_counts[col] = final_join_period_counts[col].map("{:.1f}".format)
        
        # 데이터프레임 표시
        check2_key = "data_frame_view_2"
        check2 = st.checkbox('데이터프레임 보기', key=check2_key)
        if check2:
            final_join_period_counts = final_join_period_counts.round(1)
            st.table(final_join_period_counts)
    
    
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    
    
        # 사유별 접속 횟수 비율 선 그래프
        st.write("### 탈퇴 사유별 접속 횟수 비율")
        fig = go.Figure()
        
        for reason in final_access_period_counts['탈퇴사유'].unique():
            reason_data = final_access_period_counts[final_access_period_counts['탈퇴사유'] == reason]
            fig.add_trace(go.Scatter(
                x=labels,
                y=reason_data.iloc[0, 3:].values,
                mode='lines+markers', 
                name=reason))
        
        fig.update_layout(
            xaxis_title='접속 횟수 구간',
            yaxis_title='비율 (%)',
            legend_title='탈퇴 사유'
        )
        
        st.plotly_chart(fig)
        
        for col in final_access_period_counts.columns:
            if final_access_period_counts[col].dtype == 'float64':
                final_access_period_counts[col] = final_access_period_counts[col].map("{:.1f}".format)
        
        # 데이터프레임 표시
        check4_key = "data_frame_view_4"
        check4 = st.checkbox('데이터프레임 보기', key=check4_key)
        if check4:
            final_access_period_counts = final_access_period_counts.round(1)
            st.table(final_access_period_counts)
        
    
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        
    
        # 탈퇴 사유별 채널 비율 시각화
        st.write("### 탈퇴 사유별 채널 비율")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Define the channels for visualization
        channels = ['KKB', 'SSEM']
        cmap = plt.get_cmap('Set2')
        
        # Plot the data
        final_channel_type_counts.set_index('탈퇴사유')[channels].plot(kind='barh', stacked=True, ax=ax, colormap=cmap)
        
        # Set plot labels and legend
        ax.set_xlabel('비율 (%)')
        ax.set_ylabel('탈퇴 사유')
        ax.legend(title='채널')
        plt.gca().invert_yaxis()
        
        # Display the plot
        st.pyplot(fig)
        
        # Format columns for display in the table
        for col in final_channel_type_counts.columns:
            if final_channel_type_counts[col].dtype == 'float64':
                final_channel_type_counts[col] = final_channel_type_counts[col].map("{:.1f}".format)
        
        # DataFrame 표시
        check_channel_key = "data_frame_view_channel"
        check_channel = st.checkbox('데이터프레임 보기', key=check_channel_key)
        if check_channel:
            st.table(final_channel_type_counts)
    
            
    
    
    #---------------------------------------------------------------------------------------------- 
    
    if page == "사용자유형별":
        st.title("탈퇴 대시보드")
        st.text("""탈퇴 통계 어드민 개선 전, 간단하게 탈퇴 통계를 확인하기 위해 제작한 대시보드입니다.
    실시간 연동은 불가하여, 전날까지의 데이터를 업데이트합니다.
        """)
        
        st.text("""
        """)
    
        unique_users = data['사용자 유형'].dropna().unique().tolist()
        unique_users.append('전체')
        
        # 기간 선택 버튼을 가로로 배치
        col1, col2= st.columns(2)
        
        yesterday = datetime.now() - timedelta(days=1)
        
        with col1:
            start_date = st.date_input("시작 날짜", value=(datetime(2024, 5, 31)).date(), key='start_date')
        
        with col2:
            end_date = st.date_input("종료 날짜", value=yesterday.date(), key='end_date')
    
            
    
        st.text("""
        """)
        st.text("""
        """)
        
        # 선택한 날짜 범위에 따라 데이터 필터링
        if '탈퇴 일자' in data.columns:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)  # 종료 날짜를 하루의 끝으로 설정
            filtered = data[(data['탈퇴 일자'] >= start_date) & (data['탈퇴 일자'] <= end_date)]
            
            filtered = filtered.dropna(subset=['탈퇴사유'])
            
        
        else:
            filtered = data
    
    
        # ------------------------------------------------------------------------------------------------------
        # 사용자 유형 filter 전처리
        
        filter = filtered[['사용자 유형', '탈퇴사유']].copy()
        filter['탈퇴사유'] = filter['탈퇴사유'].str.split(';')
        filter = filter.explode('탈퇴사유')
        filter = filter.dropna(subset=['탈퇴사유'])
        filter = filter.reset_index(drop=True)
        
        total_reason_counts = filter['사용자 유형'].value_counts().reset_index()
        total_reason_counts.columns = ['사용자 유형', 'Total count']
        
        reason_counts = filter.groupby(['사용자 유형', '탈퇴사유']).size().reset_index(name='count')
        reason_counts = reason_counts.merge(total_reason_counts, on='사용자 유형')
        reason_counts['비율'] = (reason_counts['count'] / reason_counts['Total count'] * 100).round(1)
        
        # 사용자 유형별 전체 비율 계산
        total_counts = filter['사용자 유형'].value_counts().reset_index()
        total_counts.columns = ['사용자 유형', 'count']
        total_counts['전체 비율'] = (total_counts['count'] / total_counts['count'].sum() * 100).round(1)
        
        # 사용자 유형별 비율 계산
        user_type_counts = reason_counts.pivot_table(index='사용자 유형', columns='탈퇴사유', values='비율', fill_value=0)
        user_type_counts = user_type_counts.reset_index()
        user_type_counts = user_type_counts.merge(total_counts[['사용자 유형', '전체 비율']], on='사용자 유형')
        user_type_counts = user_type_counts.merge(total_reason_counts, on='사용자 유형')
        user_type_counts = user_type_counts.sort_values(by='전체 비율', ascending=False)
        
        # 모든 탈퇴 사유를 포함하도록 설정
        all_reasons = ['사용할 수 있는 서비스가 없어요.', '개인정보 유출이 걱정돼요.', '타 서비스보다 세금이 더 많이 나와요.', '자료 수집이 안돼요.', '이용 요금이 비싸요.','직접 해야 하는 게 많아요.', '문의 답변이 오래 걸려요.','직접 입력할게요.']
        user_type_counts = user_type_counts.reindex(columns=['사용자 유형'] + all_reasons + ['전체 비율', 'Total count'], fill_value=0)
        
        # 각 탈퇴 사유별 최종 비율 계산
        for reason in all_reasons:
            user_type_counts[reason] = (user_type_counts[reason] * user_type_counts['전체 비율'] / 100).round(1)
        
        # 최종 비율 컬럼 선택
        final_user_type_counts = user_type_counts[['사용자 유형', 'Total count', '전체 비율'] + all_reasons]
        
        # 열 이름 설정
        final_user_type_counts.columns = ['사용자 유형', '개수', '전체 비율'] + all_reasons
        
        # 인덱스 재정렬
        final_user_type_counts.reset_index(drop=True, inplace=True)
        
        # 소숫점 첫째 자리까지만 표시
        final_user_type_counts = final_user_type_counts.round(1)
    
    
    
    # ------------------------------------------------------------------------------------------------------
    
    
        # 가입 기간별 비율 전처리
        filter_join_period = filtered[['사용자 유형', '가입 구간']].copy()
        filter_join_period = filter_join_period.dropna(subset=['가입 구간'])
        filter_join_period = filter_join_period.reset_index(drop=True)
        
        total_join_period_counts = filter_join_period['사용자 유형'].value_counts().reset_index()
        total_join_period_counts.columns = ['사용자 유형', 'Total count']
        
        order = ['0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
        filter_join_period['가입 구간'] = pd.Categorical(filter_join_period['가입 구간'], categories=order, ordered=True)
        
        join_period_counts = filter_join_period.groupby(['사용자 유형', '가입 구간']).size().unstack(fill_value=0)
        join_period_counts = join_period_counts.div(join_period_counts.sum(axis=1), axis=0) * 100
        join_period_counts = join_period_counts.reset_index()
        
        total_join_counts = filter_join_period['사용자 유형'].value_counts().reset_index()
        total_join_counts.columns = ['사용자 유형', 'count']
        total_join_counts['전체 비율'] = (total_join_counts['count'] / total_join_counts['count'].sum() * 100).round(1)
        
        join_period_counts = join_period_counts.merge(total_join_counts[['사용자 유형', 'count', '전체 비율']], on='사용자 유형')
        for label in order:
            join_period_counts[label] = (join_period_counts[label] * join_period_counts['전체 비율'] / 100).round(1)
        
        final_join_period_counts = join_period_counts[['사용자 유형', 'count', '전체 비율'] + [label for label in order]]
        final_join_period_counts.columns = ['사용자 유형', '개수', '전체 비율', '0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
        final_join_period_counts = final_join_period_counts.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
    
    
    # ------------------------------------------------------------------------------------------------------ 
        # 사용자 유형별 접속 횟수 비율 전처리
        filter_access = filtered[['사용자 유형', '총 접속 수']].copy()
        bins = [1, 2, 5, 10, 20, float('inf')]
        labels = ["1", "2~5", "5~10", "10~20", "20 이상"]
        filter_access['접속 횟수 구간'] = pd.cut(filter_access['총 접속 수'], bins=bins, labels=labels, right=False)
        filter_access = filter_access.dropna(subset=['접속 횟수 구간'])
        filter_access = filter_access.reset_index(drop=True)
        
        total_access_counts = filter_access['사용자 유형'].value_counts().reset_index()
        total_access_counts.columns = ['사용자 유형', 'Total count']
        
        access_counts = filter_access.groupby(['사용자 유형', '접속 횟수 구간']).size().unstack(fill_value=0)
        access_counts = access_counts.div(access_counts.sum(axis=1), axis=0) * 100
        access_counts = access_counts.reset_index()
        
        total_access_user_counts = filter_access['사용자 유형'].value_counts().reset_index()
        total_access_user_counts.columns = ['사용자 유형', 'count']
        total_access_user_counts['전체 비율'] = (total_access_user_counts['count'] / total_access_user_counts['count'].sum() * 100).round(1)
        
        access_counts = access_counts.merge(total_access_user_counts[['사용자 유형', 'count', '전체 비율']], on='사용자 유형')
        for label in labels:
            access_counts[label] = (access_counts[label] * access_counts['전체 비율'] / 100).round(1)
        
        final_access_counts = access_counts[['사용자 유형', 'count', '전체 비율'] + labels]
        final_access_counts.columns = ['사용자 유형', '개수', '전체 비율'] + labels
        final_access_counts = final_access_counts.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
        
        # 데이터 유형 확인 및 변환
        for col in final_access_counts.columns[3:]:
            final_access_counts[col] = pd.to_numeric(final_access_counts[col], errors='coerce')
    
    
    
                
    # ------------------------------------------------------------------------------------------------------ 
      
    
    
        # 사용자 유형별 채널 비율 전처리
        filter3 = filtered[['사용자 유형', '채널']].copy()
        filter3 = filter3.dropna(subset=['채널'])
        filter3 = filter3.reset_index(drop=True)
    
        total_reason_counts = filter3['사용자 유형'].value_counts().reset_index()
        total_reason_counts.columns = ['사용자 유형', 'Total count']
    
        channel_counts = filter3.groupby(['사용자 유형', '채널']).size().unstack(fill_value=0)
        channel_counts = channel_counts.div(channel_counts.sum(axis=1), axis=0) * 100
        channel_counts = channel_counts.reset_index()
    
        total_counts = filter3['사용자 유형'].value_counts().reset_index()
        total_counts.columns = ['사용자 유형', 'count']
        total_counts['전체 비율'] = (total_counts['count'] / total_counts['count'].sum() * 100).round(1)
    
        channel_counts = channel_counts.merge(total_counts[['사용자 유형', 'count', '전체 비율']], on='사용자 유형')
        for col in channel_counts.columns[1:-2]:
            channel_counts[col] = (channel_counts[col] * channel_counts['전체 비율'] / 100).round(1)
        
        final_channel_counts = channel_counts[['사용자 유형', 'count', '전체 비율'] + list(channel_counts.columns[1:-2])]
        final_channel_counts.columns = ['사용자 유형', '개수', '전체 비율'] + list(channel_counts.columns[1:-2])
        final_channel_counts = final_channel_counts.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
    
    
        # ------------------------------------------------------------------------------------------------------
    
             # 전체 탈퇴자 수 계산
        total_churners = filtered.shape[0]
            
        st.markdown(f"""
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 140px; border: 2px solid gray; border-radius: 10px;">
                    <div style="font-size: 15px; color: gray; margin-top: 8px; margin-bottom: 10px;">전체 탈퇴자 수</div>
                    <div style="font-size: 50px; font-weight: bold;">{total_churners}명</div>
                </div>
            """, unsafe_allow_html=True)
    
    
            
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    
    
        st.write("### 사용자 유형별 탈퇴 사유 비율")
    
        fig, ax = plt.subplots(figsize=(12, 6))
        cmap = plt.get_cmap('Set2')
        final_user_type_counts.set_index('사용자 유형')[all_reasons].plot(kind='barh', stacked=True, ax=ax ,colormap=cmap)
        
        ax.set_xlabel('비율 (%)')
        ax.set_ylabel('사용자 유형')
        ax.legend(title='탈퇴 사유')
        plt.gca().invert_yaxis()
        
        st.pyplot(fig)
            
        for col in final_user_type_counts.columns:
            if final_user_type_counts[col].dtype == 'float64':
                final_user_type_counts[col] = final_user_type_counts[col].map("{:.1f}".format)
    
        # DataFrame 표시
        check0_key = "data_frame_view_0"
        check0 = st.checkbox('데이터프레임 보기', key=check0_key)
        if check0:
            st.table(final_user_type_counts)
    
    
    
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    
    
    
        # 가입 기간별 비율 선 그래프
        st.write("### 사용자 유형별 가입 기간 비율")
        fig = go.Figure()
        
        for user_type in final_join_period_counts['사용자 유형'].unique():
            user_data = final_join_period_counts[final_join_period_counts['사용자 유형'] == user_type]
            fig.add_trace(go.Scatter(
                x=['0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상'],
                y=user_data.iloc[0, 3:].values,
                mode='lines+markers', 
                name=user_type
            ))
        
        fig.update_layout(
            xaxis_title='가입 구간',
            yaxis_title='비율 (%)',
            legend_title='사용자 유형'
        )
        
        st.plotly_chart(fig)
        
        for col in final_join_period_counts.columns:
            if final_join_period_counts[col].dtype == 'float64':
                final_join_period_counts[col] = final_join_period_counts[col].map("{:.1f}".format)
        
        check2_key = "data_frame_view_2"
        check2 = st.checkbox('데이터프레임 보기', key=check2_key)
        if check2:
            st.table(final_join_period_counts)
    
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    
        st.write("### 사용자 유형별 접속 횟수 비율")
    
        fig = go.Figure()
        
        for user_type in final_access_counts['사용자 유형'].unique():
            user_data = final_access_counts[final_access_counts['사용자 유형'] == user_type]
            fig.add_trace(go.Scatter(
                x=labels,
                y=user_data.iloc[0, 3:].values,
                mode='lines+markers', 
                name=user_type
            ))
        
        fig.update_layout(
            xaxis_title='접속 횟수 구간',
            yaxis_title='비율 (%)',
            legend_title='사용자 유형'
        )
        
        st.plotly_chart(fig)
        
        for col in final_access_counts.columns:
            if final_access_counts[col].dtype == 'float64':
                final_access_counts[col] = final_access_counts[col].map("{:.1f}".format)
        
        check3_key = "data_frame_view_3"
        check3 = st.checkbox('데이터프레임 보기', key=check3_key)
        if check3:
            st.table(final_access_counts)
    
    
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    
        st.write("### 사용자 유형별 채널 비율")
        fig, ax = plt.subplots(figsize=(12, 6))
        channels = ['KKB', 'SSEM']
        cmap = plt.get_cmap('Set2')
        final_channel_counts.set_index('사용자 유형')[channels].plot(kind='barh', stacked=True, ax=ax, colormap=cmap)
        ax.set_xlabel('비율 (%)')
        ax.set_ylabel('사용자 유형')
        ax.legend(title='채널')
        plt.gca().invert_yaxis()
        st.pyplot(fig)
            
        for col in final_channel_counts.columns:
            if final_channel_counts[col].dtype == 'float64':
                final_channel_counts[col] = final_channel_counts[col].map("{:.1f}".format)
        
        check5_key = "data_frame_view_5"
        check5 = st.checkbox('데이터프레임 보기', key=check5_key)
        if check5:
            st.table(final_channel_counts)
    
    
    
    
    #---------------------------------------------------------------------------------------------- 
    
    if page == "채널별":
        st.title("탈퇴 대시보드")
        st.text("""탈퇴 통계 어드민 개선 전, 간단하게 탈퇴 통계를 확인하기 위해 제작한 대시보드입니다.
    실시간 연동은 불가하여, 전날까지의 데이터를 업데이트합니다.
        """)
        
        st.text("""
        """)
    
        unique_channels = data['채널'].dropna().unique().tolist()
        unique_channels.append('전체')
        
        # 기간 선택 버튼을 가로로 배치
        col1, col2 = st.columns(2)
        
        yesterday = datetime.now() - timedelta(days=1)
        
        with col1:
            start_date = st.date_input("시작 날짜", value=(datetime(2024, 5, 31)).date(), key='start_date')
        
        with col2:
            end_date = st.date_input("종료 날짜", value=yesterday.date(), key='end_date')
    
    
        
        st.text("""
        """)
        st.text("""
        """)
        
        # 선택한 날짜 범위에 따라 데이터 필터링
        if '탈퇴 일자' in data.columns:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)  # 종료 날짜를 하루의 끝으로 설정
            filtered = data[(data['탈퇴 일자'] >= start_date) & (data['탈퇴 일자'] <= end_date)]
            
            filtered = filtered.dropna(subset=['채널'])
            
        
        else:
            filtered = data
        
        # ------------------------------------------------------------------------------------------------------
    
        # 채널별 탈퇴 사유 비율 계산
        filter = filtered[['채널', '탈퇴사유']].copy()
        filter['탈퇴사유'] = filter['탈퇴사유'].str.split(';')
        filter = filter.explode('탈퇴사유')
        filter = filter.dropna(subset=['탈퇴사유'])
        filter = filter.reset_index(drop=True)
        
        total_reason_counts = filter['채널'].value_counts().reset_index()
        total_reason_counts.columns = ['채널', 'Total count']
        
        reason_counts = filter.groupby(['채널', '탈퇴사유']).size().reset_index(name='count')
        reason_counts = reason_counts.merge(total_reason_counts, on='채널')
        reason_counts['비율'] = (reason_counts['count'] / reason_counts['Total count'] * 100).round(1)
        
        # 채널별 탈퇴 사유별 전체 비율 계산
        total_counts = filter['채널'].value_counts().reset_index()
        total_counts.columns = ['채널', 'Total count']  # 'count'를 'Total count'로 변경
        total_counts['전체 비율'] = (total_counts['Total count'] / total_counts['Total count'].sum() * 100).round(1)
        
        # 탈퇴 사유별 비율 계산
        channel_reason_counts = reason_counts.pivot_table(index='채널', columns='탈퇴사유', values='비율', fill_value=0)
        channel_reason_counts = channel_reason_counts.reset_index()
        channel_reason_counts = channel_reason_counts.merge(total_counts[['채널', '전체 비율']], on='채널')
        channel_reason_counts = channel_reason_counts.merge(total_reason_counts, on='채널')
        channel_reason_counts = channel_reason_counts.sort_values(by='전체 비율', ascending=False)
    
        all_reasons = ['사용할 수 있는 서비스가 없어요.', '개인정보 유출이 걱정돼요.', '타 서비스보다 세금이 더 많이 나와요.', '자료 수집이 안돼요.', '이용 요금이 비싸요.','직접 해야 하는 게 많아요.', '문의 답변이 오래 걸려요.','직접 입력할게요.']
        
        # 모든 탈퇴 사유를 포함하도록 설정
        channel_reason_counts = channel_reason_counts.reindex(columns=['채널'] + all_reasons + ['전체 비율', 'Total count'], fill_value=0)
        
        # 각 탈퇴 사유별 최종 비율 계산
        for reason in all_reasons:
            channel_reason_counts[reason] = (channel_reason_counts[reason] * channel_reason_counts['전체 비율'] / 100).round(1)
        
        # 최종 비율 컬럼 선택
        final_channel_reason_counts = channel_reason_counts[['채널', 'Total count', '전체 비율'] + all_reasons]
        
        # 열 이름 설정
        final_channel_reason_counts.columns = ['채널', '개수', '전체 비율'] + all_reasons
        
        # 인덱스 재정렬
        final_channel_reason_counts.reset_index(drop=True, inplace=True)
        
        # 소숫점 첫째 자리까지만 표시
        final_channel_reason_counts = final_channel_reason_counts.round(1)
    
    
        # ------------------------------------------------------------------------------------------------------
        # 채널별 사용자 유형 전처리
        
        filter = filtered[['채널', '사용자 유형']].copy()
        filter = filter.dropna(subset=['사용자 유형'])
        filter = filter.reset_index(drop=True)
        
        # 전체 채널별 사용자 수
        total_reason_counts = filter['채널'].value_counts().reset_index()
        total_reason_counts.columns = ['채널', 'Total count']
        
        # 사용자 유형별 채널 수
        reason_counts = filter.groupby(['채널', '사용자 유형']).size().reset_index(name='count')
        reason_counts = reason_counts.merge(total_reason_counts, on='채널')
        reason_counts['비율'] = (reason_counts['count'] / reason_counts['Total count'] * 100).round(1)
        
        # 채널별 전체 비율 계산
        total_counts = filter['채널'].value_counts().reset_index()
        total_counts.columns = ['채널', 'count']
        total_counts['전체 비율'] = (total_counts['count'] / total_counts['count'].sum() * 100).round(1)
        
        # 사용자 유형별 비율 계산
        channel_user_type_counts = reason_counts.pivot_table(index='채널', columns='사용자 유형', values='비율', fill_value=0)
        channel_user_type_counts = channel_user_type_counts.reset_index()
        channel_user_type_counts = channel_user_type_counts.merge(total_counts[['채널', '전체 비율']], on='채널')
        channel_user_type_counts = channel_user_type_counts.merge(total_reason_counts, on='채널')
        channel_user_type_counts = channel_user_type_counts.sort_values(by='전체 비율', ascending=False)
        
        # 사용자 유형 컬럼명 변경
        channel_user_type_counts.columns = ['채널'] + list(reason_counts['사용자 유형'].unique()) + ['전체 비율', '개수']
        
        # 각 사용자 유형 비율에 전체 비율을 곱해서 최종 비율 계산
        for user_type in reason_counts['사용자 유형'].unique():
            channel_user_type_counts[user_type] = (channel_user_type_counts[user_type] * channel_user_type_counts['전체 비율'] / 100).round(1)
        
        
        # 최종 비율 컬럼 선택
        final_channel_user_type_counts = channel_user_type_counts[['채널', '개수', '전체 비율'] + list(reason_counts['사용자 유형'].unique())]
        
        # 인덱스 재정렬
        final_channel_user_type_counts.reset_index(drop=True, inplace=True)
        
        # 소숫점 한자리로 표시
        final_channel_user_type_counts = final_channel_user_type_counts.round(1)
    
        # ------------------------------------------------------------------------------------------------------
    
        # 가입기간별 알기
        filter1 = filtered[['채널', '가입 구간']].copy()
        filter1 = filter1.dropna(subset=['가입 구간'])
        filter1 = filter1.reset_index(drop=True)
        
        total_reason_counts = filter1['채널'].value_counts().reset_index()
        total_reason_counts.columns = ['채널', 'Total count']
        
        # 가입 구간을 특정 순서로 정렬
        order = ['0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
        filter1['가입 구간'] = pd.Categorical(filter1['가입 구간'], categories=order, ordered=True)
        
        # 가입 기간별 비율 계산
        period_counts = filter1.groupby(['채널', '가입 구간']).size().unstack(fill_value=0)
        period_counts = period_counts.div(period_counts.sum(axis=1), axis=0) * 100
        period_counts = period_counts.reset_index()
        
        # 전체 비율 계산
        total_counts = filter1['채널'].value_counts().reset_index()
        total_counts.columns = ['채널', 'count']
        total_counts['전체 비율'] = (total_counts['count'] / total_counts['count'].sum() * 100).round(1)
        
        # 최종 비율 계산
        period_counts = period_counts.merge(total_counts[['채널', 'count', '전체 비율']], on='채널')
        for label in order:
            period_counts[label] = (period_counts[label] * period_counts['전체 비율'] / 100).round(1)
        
        # 필요한 열만 선택
        final_period_counts = period_counts[['채널', 'count', '전체 비율'] + [label for label in order]]
        final_period_counts.columns = ['채널', '개수', '전체 비율', '0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
        final_period_counts = final_period_counts.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
    
        
         # 채널별 접속 횟수 비율 전처리
        filter3 = filtered[['채널', '총 접속 수']].copy()
        bins = [1, 2, 5, 10, 20, float('inf')]
        labels = ["1", "2~5", "5~10", "10~20", "20 이상"]
        filter3['접속 횟수 구간'] = pd.cut(filter3['총 접속 수'], bins=bins, labels=labels, right=False)
        filter3 = filter3.dropna(subset=['접속 횟수 구간'])
        filter3 = filter3.reset_index(drop=True)
        
        total_reason_counts = filter3['채널'].value_counts().reset_index()
        total_reason_counts.columns = ['채널', 'Total count']
        
        period_counts = filter3.groupby(['채널', '접속 횟수 구간']).size().unstack(fill_value=0)
        period_counts = period_counts.div(period_counts.sum(axis=1), axis=0) * 100
        period_counts = period_counts.reset_index()
        
        total_counts = filter3['채널'].value_counts().reset_index()
        total_counts.columns = ['채널', 'count']
        total_counts['전체 비율'] = (total_counts['count'] / total_counts['count'].sum() * 100).round(1)
        
        period_counts = period_counts.merge(total_counts[['채널', 'count', '전체 비율']], on='채널')
        for label in labels:
            period_counts[label] = (period_counts[label] * period_counts['전체 비율'] / 100).round(1)
        
        final_channel_period_counts = period_counts[['채널', 'count', '전체 비율'] + labels]
        final_channel_period_counts.columns = ['채널', '개수', '전체 비율'] + labels
        final_channel_period_counts = final_channel_period_counts.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
        
        # 데이터 유형 확인 및 변환
        for col in final_channel_period_counts.columns[3:]:
            final_channel_period_counts[col] = pd.to_numeric(final_channel_period_counts[col], errors='coerce')
    
        # ------------------------------------------------------------------------------------------------------
    
        # 전체 탈퇴자 수 계산
        total_churners = filtered.shape[0]
            
        st.markdown(f"""
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 140px; border: 2px solid gray; border-radius: 10px;">
                    <div style="font-size: 15px; color: gray; margin-top: 8px; margin-bottom: 10px;">전체 탈퇴자 수</div>
                    <div style="font-size: 50px; font-weight: bold;">{total_churners}명</div>
                </div>
            """, unsafe_allow_html=True)
    
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    
        # 채널별 탈퇴 사유 비율
        st.write("### 채널별 탈퇴 사유 비율")
        fig, ax = plt.subplots(figsize=(12, 6))
        cmap = plt.get_cmap('Set2')
        final_channel_reason_counts.set_index('채널')[all_reasons].plot(kind='barh', stacked=True, ax=ax, colormap=cmap)
        ax.set_xlabel('비율 (%)')
        ax.set_ylabel('채널')
        ax.legend(title='탈퇴 사유')
        plt.gca().invert_yaxis()
        st.pyplot(fig)
        
        for col in final_channel_reason_counts.columns:
            if final_channel_reason_counts[col].dtype == 'float64':
                final_channel_reason_counts[col] = final_channel_reason_counts[col].map("{:.1f}".format)
        
        # DataFrame 표시
        check1_key = "data_frame_view_1"
        check1 = st.checkbox('데이터프레임 보기', key=check1_key)
        if check1:
            st.table(final_channel_reason_counts)
    
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    
        # 채널별 사용자 유형 비율
    
        st.write("### 채널별 사용자 유형 비율")
        fig, ax = plt.subplots(figsize=(12, 6))
        user_types = ['개인사업자', '그 외', '법인', '폐업']
        cmap = plt.get_cmap('Set2')
        final_channel_user_type_counts.set_index('채널')[user_types].plot(kind='barh', stacked=True, ax=ax, colormap=cmap)
        ax.set_xlabel('비율 (%)')
        ax.set_ylabel('채널')
        ax.legend(title='사용자 유형')
        plt.gca().invert_yaxis()
        st.pyplot(fig)
        
        for col in final_channel_user_type_counts.columns:
            if final_channel_user_type_counts[col].dtype == 'float64':
                final_channel_user_type_counts[col] = final_channel_user_type_counts[col].map("{:.1f}".format)
        
        # DataFrame 표시
        check2_key = "data_frame_view_2"
        check2 = st.checkbox('데이터프레임 보기', key=check2_key)
        if check2:
            st.table(final_channel_user_type_counts)
    
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    
        # 채널별 가입 구간 비율 선 그래프
        st.write("### 채널별 가입 구간 비율")
        fig = go.Figure()
        
        for channel in final_period_counts['채널'].unique():
            channel_data = final_period_counts[final_period_counts['채널'] == channel]
            fig.add_trace(go.Scatter(
                x=['0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상'],
                y=channel_data.iloc[0, 3:].values,
                mode='lines+markers', 
                name=channel))
        
        fig.update_layout(
            xaxis_title='가입 구간',
            yaxis_title='비율 (%)',
            legend_title='채널'
        )
        
        st.plotly_chart(fig)
        
        for col in final_period_counts.columns:
            if final_period_counts[col].dtype == 'float64':
                final_period_counts[col] = final_period_counts[col].map("{:.1f}".format)
        
        check3_key = "data_frame_view_3"
        check3 = st.checkbox('데이터프레임 보기', key=check3_key)
        if check3:
            final_period_counts = final_period_counts.round(1)
            st.table(final_period_counts)
    
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    
        # 채널별 접속 횟수 비율 선 그래프
        st.write("### 채널별 접속 횟수 비율")
        fig = go.Figure()
        
        for channel in final_channel_period_counts['채널'].unique():
            channel_data = final_channel_period_counts[final_channel_period_counts['채널'] == channel]
            fig.add_trace(go.Scatter(
                x=labels,
                y=channel_data.iloc[0, 3:].values,
                mode='lines+markers', 
                name=channel))
        
        fig.update_layout(
            xaxis_title='접속 횟수 구간',
            yaxis_title='비율 (%)',
            legend_title='채널'
        )
        
        st.plotly_chart(fig)
        
        for col in final_channel_period_counts.columns:
            if final_channel_period_counts[col].dtype == 'float64':
                final_channel_period_counts[col] = final_channel_period_counts[col].map("{:.1f}".format)
        
        # DataFrame 표시
        check4_key = "data_frame_view_4"
        check4 = st.checkbox('데이터프레임 보기', key=check4_key)
        if check4:
            final_channel_period_counts = final_channel_period_counts.round(1)
            st.table(final_channel_period_counts)
    
    #-------------------------------------------------------------------------------------------------
    
    
    
    
    
    
    #-------------------------------------------------------------------------------------------------
    
    if page == "직접 입력할게요":
        st.title("탈퇴 대시보드")
        st.text("""탈퇴 통계 어드민 개선 전, 간단하게 탈퇴 통계를 확인하기 위해 제작한 대시보드입니다.
    실시간 연동은 불가하여, 전날까지의 데이터를 업데이트합니다.
        """)
        st.text("""
        """)
        
        
        # 기간 선택 버튼을 가로로 배치
        col1, col2 = st.columns(2)
        
        yesterday = datetime.now() - timedelta(days=1)
        
        with col1:
            start_date = st.date_input("시작 날짜", value=(datetime(2024, 5, 31)).date(), key='start_date')
        
        with col2:
            end_date = st.date_input("종료 날짜", value=yesterday.date(), key='end_date')
    
        st.text("""
        """)
        st.text("""
        """)
        
        # 선택한 날짜 범위에 따라 데이터 필터링
        if '탈퇴 일자' in data.columns:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)  # 종료 날짜를 하루의 끝으로 설정
            filtered = data[(data['탈퇴 일자'] >= start_date) & (data['탈퇴 일자'] <= end_date)]
            
        else:
            filtered = data
    
        # 선택한 날짜 범위에 따라 데이터 필터링
        if '날짜' in sub_data.columns:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)  # 종료 날짜를 하루의 끝으로 설정
            sub_data_filtered = sub_data[(sub_data['날짜'] >= start_date) & (sub_data['날짜'] <= end_date)]
        else:
            sub_data_filtered = sub_data
    # 직접 입력할게요 raw 데이터!
        filter2 = filtered.copy()
        raw = filter2.loc[filter2['탈퇴사유'] == '직접 입력할게요.', ['Raw','총 접속 수','사용자 유형', '채널','가입 기간','세금 서비스 사용 여부']]
        raw.reset_index(drop=True, inplace=True)
    
        st.write("### 직접 입력할게요")
        st.table(raw)
    
    
        

else:
    st.error("잘못된 키워드입니다. 접근이 거부되었습니다.")
    
# ----------------------------------------------------------------------------------------

