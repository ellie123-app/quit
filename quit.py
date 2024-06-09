import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
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

    
    
    

    #데이터프레임 불러오기
    data = pd.read_csv(url,encoding='utf-8')
    sub_data = pd.read_csv(url0,encoding='utf-8')
 



# -------------------------------------------------------------------
    
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
        period.reset_index(drop=True,inplace=True)
    
    
        # 채널별 탈퇴 사유 비율 계산
        channel_counts = filtered['채널'].value_counts().reset_index()
        channel_counts.columns = ['채널', 'count']
        total_channel_count = channel_counts['count'].sum()
        channel_counts['비율'] = (channel_counts['count'] / total_channel_count) * 100
        channel_counts['비율'] = channel_counts['비율'].round(1)
    
        # 접속 횟수
        bins = [1, 2, 5, 10, 20, float('inf')]
        labels = ["1", "2~5", "5~10", "10~20", "20 이상"]
        data['접속 횟수 구간'] = pd.cut(data['총 접속 수'], bins=bins, labels=labels, right=False)
        period_counts = data.groupby('접속 횟수 구간').size().reset_index(name='count')
        total = period_counts['count'].sum()
        period_counts['비율'] = (period_counts['count'] / total) * 100
        period_counts['접속 횟수 구간'] = pd.Categorical(period_counts['접속 횟수 구간'], categories=labels, ordered=True)
        period_counts = period_counts.sort_values('접속 횟수 구간')
        period_counts.reset_index(drop=True, inplace=True)
    
            
        # 1. 부가세, 종소세 계산 완료 또는 부가세, 종소세, 인건비 결제 완료 한 탈퇴자 비율
        tax_complete = filtered[(filtered['부가세 계산 완료 수'] > 0) | (filtered['종소세 계산 완료 수'] > 0) |
                                (filtered['부가세 결제 수'] > 0) | (filtered['종소세 결제 수'] > 0) | (filtered['인건비 결제 수'] > 0)]
        tax_complete_rate = (tax_complete.shape[0] / filtered.shape[0]) 
    
        # 2. 부가세 계산 진입 > 부가세 계산 완료 또는 종소세 계산 진입 > 종소세 계산 완료인 탈퇴자 비율
        tax_entry_complete = filtered[((filtered['부가세 계산 시작 수'] > filtered['부가세 계산 완료 수'])) |
                                      ((filtered['종소세 계산 시작 수'] > filtered['종소세 계산 완료 수']))]
        tax_entry_complete_rate = (tax_entry_complete.shape[0] / filtered.shape[0]) 

    
        
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
                st.table(period)
            
        with col2:
            st.write("### 접속 횟수별 비율")
            fig4 = px.line(period_counts, x='접속 횟수 구간', y='비율', markers=True)
            fig4.update_traces(line_color='orange')
            fig4.update_layout(width=800, height=400)
            st.plotly_chart(fig4)
            
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

        with col2:
            st.write("### 기타 비율")
            st.text("""
            """)
            st.text("""
            """)
            st.markdown(f"""
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 140px; border: 2px solid gray; border-radius: 10px;">
                    <div style="font-size: 15px; color: gray; margin-top: 8px; margin-bottom: 10px;"> 계산/신고 서비스 사용 비율</div>
                    <div style="font-size: 50px; font-weight: bold;">{tax_complete_rate:.2%}</div>
                </div>
            """, unsafe_allow_html=True)

            st.text("""
            """)
            st.text("""
            """)
            
            st.markdown(f"""
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 140px; border: 2px solid gray; border-radius: 10px;">
                    <div style="font-size: 15px; color: gray; margin-top: 8px; margin-bottom: 10px;"> 계산 서비스 이탈 비율 </div>
                    <div style="font-size: 50px; font-weight: bold;">{tax_entry_complete_rate:.2%}</div>
                </div>
            """, unsafe_allow_html=True)
            
    
    
    
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
        user_dataframe = user_type_counts.copy()
        
        # 각 사용자 유형 비율에 전체 비율을 곱해서 최종 비율 계산
        user_type_counts['개인사업자 비율'] = (user_type_counts['개인사업자 비율'] * user_type_counts['전체 비율'] / 100).round(1)
        user_type_counts['그 외 비율'] = (user_type_counts['그 외 비율'] * user_type_counts['전체 비율'] / 100).round(1)
        user_type_counts['법인 비율'] = (user_type_counts['법인 비율'] * user_type_counts['전체 비율'] / 100).round(1)
        user_type_counts['폐업 비율'] = (user_type_counts['폐업 비율'] * user_type_counts['전체 비율'] / 100).round(1)
    
        # 최종 비율 컬럼 선택
        final_user_type_counts = user_type_counts[['탈퇴사유', '개수', '전체 비율', '개인사업자 비율', '그 외 비율', '법인 비율', '폐업 비율']]
        user_dataframe = user_dataframe[['탈퇴사유', '개수', '전체 비율', '개인사업자 비율', '그 외 비율', '법인 비율', '폐업 비율']]
    
        # 인덱스 재정렬
        final_user_type_counts.reset_index(drop=True, inplace=True)
        user_dataframe.reset_index(drop=True, inplace=True)
    
        # 소숫점 한자리로 표시
        final_user_type_counts = final_user_type_counts.round(1)
        user_dataframe = user_dataframe.round(1)
    
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
        period_dataframe = join_period_counts.copy()
        for label in order:
            join_period_counts[label] = (join_period_counts[label] * join_period_counts['전체 비율'] / 100).round(1)
        
        final_join_period_counts = join_period_counts[['탈퇴사유', 'count', '전체 비율'] + [label for label in order]]
        period_dataframe = period_dataframe[['탈퇴사유', 'count', '전체 비율'] + [label for label in order]]
        
        final_join_period_counts.columns = ['탈퇴사유', '개수', '전체 비율', '0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
        period_dataframe.columns = ['탈퇴사유', '개수', '전체 비율', '0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
        
        final_join_period_counts = final_join_period_counts.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
        period_dataframe = period_dataframe.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
        
    
            
    
    
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
        access_dataframe = access_period_counts.copy()
        
        for label in labels:
            access_period_counts[label] = (access_period_counts[label] * access_period_counts['전체 비율'] / 100).round(1)
        
        final_access_period_counts = access_period_counts[['탈퇴사유', 'count', '전체 비율'] + labels]
        access_dataframe = access_dataframe[['탈퇴사유', 'count', '전체 비율'] + labels]

        final_access_period_counts.columns = ['탈퇴사유', '개수', '전체 비율'] + labels
        access_dataframe.columns = ['탈퇴사유', '개수', '전체 비율'] + labels

        final_access_period_counts = final_access_period_counts.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
        access_dataframe = access_dataframe.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
        
        
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
        channel_dataframe = channel_type_counts.copy()
        
        # 각 채널 비율에 전체 비율을 곱해서 최종 비율 계산
        for col in channel_type_counts.columns[1:-2]:
            channel_type_counts[col] = (channel_type_counts[col] * channel_type_counts['전체 비율'] / 100).round(1)
        
        # 최종 비율 컬럼 선택
        final_channel_type_counts = channel_type_counts[['탈퇴사유', '개수', '전체 비율'] + list(channel_type_counts.columns[1:-2])]
        channel_dataframe = channel_dataframe[['탈퇴사유', '개수', '전체 비율'] + list(channel_dataframe.columns[1:-2])]
    
        
        # 인덱스 재정렬
        final_channel_type_counts.reset_index(drop=True, inplace=True)
        channel_dataframe.reset_index(drop=True, inplace=True)
        
        
        # 소숫점 한자리로 표시
        final_channel_type_counts = final_channel_type_counts.round(1)
        channel_dataframe = channel_dataframe.round(1)
    
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
        final_user_type_counts.sort_values(by='개수', ascending=True, inplace=True)
        final_user_type_counts.reset_index(drop=True, inplace=True)
        user_types = ['개인사업자 비율', '그 외 비율', '법인 비율', '폐업 비율'] 

        # Plotly Express를 사용한 막대 그래프
        fig = px.bar(final_user_type_counts.melt(id_vars='탈퇴사유', value_vars=user_types, var_name='사용자 유형', value_name='비율'),
                     y='탈퇴사유',
                     x='비율',
                     color='사용자 유형',
                     orientation='h',  # 가로 막대 그래프 
                     height=600,
                     hover_data={'비율': ':.2f%'})

        fig.update_layout(barmode='stack',  # 막대를 누적 형태로 표시
                          xaxis_title='비율 (%)',
                          yaxis_title='탈퇴 사유',
                          legend_title='사용자 유형')
        
        # Streamlit에서 그래프 출력
        st.plotly_chart(fig)
            
        for col in user_dataframe.columns:
            if user_dataframe[col].dtype == 'float64':
                user_dataframe[col] = user_dataframe[col].map("{:.1f}".format)
                
        df_display = user_dataframe.sort_values(by='개수', ascending=False)
        df_display.reset_index(drop=True,inplace=True)
    
        # DataFrame 표시
        check0_key = "data_frame_view_0"
        check0 = st.checkbox('데이터프레임 보기', key=check0_key)
        if check0:
            st.table(df_display)


    
    
    
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
        
        for col in period_dataframe.columns:
            if period_dataframe[col].dtype == 'float64':
                period_dataframe[col] = period_dataframe[col].map("{:.1f}".format)
        
        # 데이터프레임 표시
        check1_key = "data_frame_view_1"
        check1 = st.checkbox('데이터프레임 보기', key=check1_key)
        if check1:
            period_dataframe = period_dataframe.round(1)
            st.table(period_dataframe)
    
    
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
        
        for col in access_dataframe.columns:
            if access_dataframe[col].dtype == 'float64':
                access_dataframe[col] = access_dataframe[col].map("{:.1f}".format)
        
        # 데이터프레임 표시
        check2_key = "data_frame_view_2"
        check2 = st.checkbox('데이터프레임 보기', key=check2_key)
        if check2:
            access_dataframe = access_dataframe.round(1)
            st.table(access_dataframe)
        
    
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
        channels = ['KKB', 'SSEM']
        final_channel_type_counts.sort_values(by='개수', ascending=True, inplace=True)
        final_channel_type_counts.reset_index(drop=True, inplace=True)
        
        fig = px.bar(final_channel_type_counts.melt(id_vars='탈퇴사유', value_vars=channels, var_name='채널', value_name='비율'),
                     y='탈퇴사유',
                     x='비율',
                     color='채널',
                     orientation='h',  # 가로 막대 그래프 
                     height=600,
                     hover_data={'비율': ':.2f%'})
        
        fig.update_layout(barmode='stack',  # 막대를 누적 형태로 표시
                          xaxis_title='비율 (%)',
                          yaxis_title='탈퇴 사유',
                          legend_title='채널')
        
        st.plotly_chart(fig)

        for col in channel_dataframe.columns:
            if channel_dataframe[col].dtype == 'float64':
                channel_dataframe[col] = channel_dataframe[col].map("{:.1f}".format)

        dff_display = channel_dataframe.sort_values(by='개수', ascending=False)
        dff_display.reset_index(drop=True, inplace=True)
        
        # DataFrame 표시
        check_channel_key = "data_frame_view_channel"
        check_channel = st.checkbox('데이터프레임 보기', key=check_channel_key)
        if check_channel:
            st.table(dff_display)
    
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    # -------------------------------------------------------------------------------------------------

        def calculate_inquiry_insights(dataframe, inquiry_reason):
            """Calculate insights for a specific inquiry reason from a dataframe."""
            Inquiry_time = dataframe[dataframe['탈퇴사유'].str.contains(inquiry_reason)]
            reason_ratio = (Inquiry_time.shape[0] / dataframe.shape[0]) * 100
            total_access_mean = Inquiry_time['총 접속 수'].mean()
            total_access_0_1_ratio = (Inquiry_time['총 접속 수'] <= 1).mean() * 100
            business_type_ratio = Inquiry_time['사용자 유형'].value_counts(normalize=True) * 100
        
            service_columns = [
                '부가세 결제 수', '부가세 결제 취소 수', '부가세 계산 시작 수', '부가세 계산 완료 수',
                '종소세 결제 수', '종소세 결제 취소 수', '종소세 계산 시작 수', '종소세 계산 완료 수',
                '인건비 결제 수', '인건비 결제 취소 수', '매출알림 서비스 이용 여부', '매출알림 서비스 탈퇴 여부',
                '안심신고 이용 여부', '재가입 여부'
            ]
        
            service_usage_stats = {}
            for column in service_columns:
                if Inquiry_time[column].dtype == 'object':
                    service_usage_stats[f"{column} 비율"] = (Inquiry_time[column] == 'Y').mean() * 100
                else:
                    service_usage_stats[f"{column} 평균"] = Inquiry_time[column].mean()
        
        
            channel_ratio = Inquiry_time['채널'].value_counts(normalize=True) * 100
        
            insights = {
                '개수': Inquiry_time.shape[0],
                '비율': reason_ratio,
                '접속 횟수 평균': total_access_mean,
                '1회이하 접속 비율': total_access_0_1_ratio,
                '가입 기간 평균': Inquiry_time['가입 기간'].mean(),
                '24시간 내 탈퇴 비율': (Inquiry_time['가입 기간'] == 0).mean() * 100,
                **{f'{a} 비율': b for a, b in business_type_ratio.items()},
                **{f'{k} 비율': v for k, v in channel_ratio.items()},
                **service_usage_stats
            }
        
            return pd.DataFrame([insights], index=[inquiry_reason]).round(2)
        
        def generate_all_insights(dataframe):
            unique_reasons = dataframe['탈퇴사유'].str.split(';').explode().unique()
            all_insights = [calculate_inquiry_insights(dataframe, reason) for reason in unique_reasons]
        
            # 마지막 행 임시 저장 및 제거
            last_row = all_insights[-1]
            all_insights = all_insights[:-1]
        
            final_df = pd.concat(all_insights)
        
            # 열 순서 지정
            desired_order = [
                '개수', '비율', '그 외 비율', '개인사업자 비율', 
                '폐업 비율', '법인 비율', '가입 기간 평균', 
                '24시간 내 탈퇴 비율', '접속 횟수 평균', '1회이하 접속 비율', 
                'SSEM 비율', 'KKB 비율'
            ]
            desired_order = desired_order + [col for col in final_df.columns if col not in desired_order]
            final_df = final_df[desired_order]
        
            return final_df

        quit_reason_summary = filtered.copy()
        # 사용 예시
        all_insights_df = generate_all_insights(quit_reason_summary)
        all_insights_df.fillna(0, inplace=True)
        all_insights_df.sort_values('개수', ascending = False, inplace=True)

        st.write("### 탈퇴 사유별 세부 데이터")
        
        if st.checkbox('탈퇴사유별 요약 통계 보기', key='summary_stats'):
            st.dataframe(all_insights_df)
            
    
    # 체크박스 2: 탈퇴사유별 데이터프레임
        # 체크박스 2: 탈퇴사유별 데이터프레임
        if st.checkbox('탈퇴사유별 데이터프레임 보기', key='detailed_data'):
            # 사용자가 탈퇴 사유를 선택할 수 있는 선택 상자 생성
            quit_reason_whole = filtered.copy()
            quit_reason_whole['탈퇴사유'] = quit_reason_whole['탈퇴사유'].str.split(';')
            quit_reason_whole = quit_reason_whole.explode('탈퇴사유')
            reason_options = ['전체'] + sorted(quit_reason_whole['탈퇴사유'].unique())
            selected_reason = st.selectbox('탈퇴 사유 선택:', options=reason_options, index=0)
            # 선택된 사유에 따라 데이터 필터링
            if selected_reason == '전체':
                filtered_view = quit_reason_whole
            else:
                filtered_view = quit_reason_whole[quit_reason_whole['탈퇴사유'] == selected_reason]
            st.dataframe(filtered_view)


    

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

        # 사용자 유형별 탈퇴 사유 비율 계산
        filtered_reason = filtered[['사용자 유형', '탈퇴사유']].copy()
        filtered_reason['탈퇴사유'] = filtered_reason['탈퇴사유'].str.split(';')
        filtered_reason = filtered_reason.explode('탈퇴사유').dropna().reset_index(drop=True)
        
        # 사용자 유형별 총 개수 및 전체 비율 계산
        total_counts_reason = filtered['사용자 유형'].value_counts().reset_index()
        total_counts_reason.columns = ['사용자 유형', 'Total count']
        total_counts_reason['전체 비율'] = (total_counts_reason['Total count'] / total_counts_reason['Total count'].sum() * 100).round(1)
        
        # 사용자 유형별 탈퇴 사유 카운트 및 비율 계산
        reason_counts = filtered_reason.groupby(['사용자 유형', '탈퇴사유']).size().reset_index(name='count')
        
        # 사용자 유형별 총 탈퇴 사유 개수 계산
        total_reason_by_type = filtered_reason.groupby('사용자 유형')['탈퇴사유'].count().reset_index()
        total_reason_by_type.columns = ['사용자 유형', '탈퇴 사유 총합']
        
        # 탈퇴 사유 비율 계산
        reason_counts = reason_counts.merge(total_reason_by_type, on='사용자 유형')
        reason_counts['비율'] = (reason_counts['count'] / reason_counts['탈퇴 사유 총합'] * 100).round(1)
        
        # 사용자 유형별 전체 비율과 탈퇴 사유 비율 병합
        final_counts_reason = reason_counts.pivot_table(index='사용자 유형', columns='탈퇴사유', values='비율', fill_value=0).reset_index()
        final_counts_reason = final_counts_reason.merge(total_counts_reason[['사용자 유형', '전체 비율', 'Total count']], on='사용자 유형')
        
        all_reasons = ['사용할 수 있는 서비스가 없어요.', '개인정보 유출이 걱정돼요.', '타 서비스보다 세금이 더 많이 나와요.', 
                       '자료 수집이 안돼요.', '이용 요금이 비싸요.', '직접 해야 하는 게 많아요.', '문의 답변이 오래 걸려요.', '직접 입력할게요.']

        final_counts_reason_dataframe = final_counts_reason.copy()

        for label in all_reasons:
            final_counts_reason[label] = (final_counts_reason[label] * final_counts_reason['전체 비율'] / 100).round(1)
        
        # 탈퇴 사유 컬럼명 정리
        
        final_counts_reason = final_counts_reason[['사용자 유형', 'Total count', '전체 비율'] + all_reasons]
        final_counts_reason_dataframe = final_counts_reason_dataframe[['사용자 유형', 'Total count', '전체 비율'] + all_reasons]

        final_counts_reason.columns = ['사용자 유형', '개수', '전체 비율'] + all_reasons
        final_counts_reason_dataframe.columns = ['사용자 유형', '개수', '전체 비율'] + all_reasons
        
        # 인덱스 재정렬
        final_counts_reason.reset_index(drop=True, inplace=True)
        final_counts_reason_dataframe.reset_index(drop=True, inplace=True)
        
        # 소숫점 한자리로 표시
        final_counts_reason = final_counts_reason.round(1)
        final_counts_reason_dataframe = final_counts_reason_dataframe.round(1)



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
        join_period_counts_dataframe = join_period_counts.copy()
        for label in order:
            join_period_counts[label] = (join_period_counts[label] * join_period_counts['전체 비율'] / 100).round(1)
        
        final_join_period_counts = join_period_counts[['사용자 유형', 'count', '전체 비율'] + [label for label in order]]
        join_period_counts_dataframe = join_period_counts_dataframe[['사용자 유형', 'count', '전체 비율'] + [label for label in order]]
        
        final_join_period_counts.columns = ['사용자 유형', '개수', '전체 비율', '0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
        join_period_counts_dataframe.columns = ['사용자 유형', '개수', '전체 비율', '0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
        
        final_join_period_counts = final_join_period_counts.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
        join_period_counts_dataframe = join_period_counts_dataframe.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
    
    
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
        access_counts_dataframe = access_counts.copy()
        
        for label in labels:
            access_counts[label] = (access_counts[label] * access_counts['전체 비율'] / 100).round(1)
        
        final_access_counts = access_counts[['사용자 유형', 'count', '전체 비율'] + labels]
        access_counts_dataframe = access_counts_dataframe[['사용자 유형', 'count', '전체 비율'] + labels]
        
        final_access_counts.columns = ['사용자 유형', '개수', '전체 비율'] + labels
        access_counts_dataframe.columns = ['사용자 유형', '개수', '전체 비율'] + labels
        
        final_access_counts = final_access_counts.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
        access_counts_dataframe = access_counts_dataframe.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
        
        # 데이터 유형 확인 및 변환
        for col in final_access_counts.columns[3:]:
            final_access_counts[col] = pd.to_numeric(final_access_counts[col], errors='coerce')

        for col in access_counts_dataframe.columns[3:]:
            access_counts_dataframe[col] = pd.to_numeric(access_counts_dataframe[col], errors='coerce')
    
    
    
                
# ------------------------------------------------------------------------------------------------------ 
      
    
    
        filter3 = filtered[['사용자 유형', '채널']].dropna().reset_index(drop=True)
        
        # 사용자 유형별 채널 카운트 및 비율 계산
        total_counts = filter3['사용자 유형'].value_counts().reset_index()
        total_counts.columns = ['사용자 유형', 'Total count']
        
        channel_counts = filter3.groupby(['사용자 유형', '채널']).size().reset_index(name='count')
        channel_counts = channel_counts.merge(total_counts, on='사용자 유형')
        channel_counts['비율'] = (channel_counts['count'] / channel_counts['Total count'] * 100).round(1)
        
        # 사용자 유형별 전체 비율 계산
        total_counts['전체 비율'] = (total_counts['Total count'] / total_counts['Total count'].sum() * 100).round(1)
        
        # 채널별 비율 계산
        channel_type_counts = channel_counts.pivot_table(index='사용자 유형', columns='채널', values='비율', fill_value=0)
        channel_type_counts = channel_type_counts.reset_index()
        channel_type_counts = channel_type_counts.merge(total_counts[['사용자 유형', '전체 비율']], on='사용자 유형')
        channel_type_counts = channel_type_counts.merge(total_counts[['사용자 유형', 'Total count']], on='사용자 유형')
        channel_type_counts = channel_type_counts.sort_values(by='Total count', ascending=False)
        
        # 채널 컬럼명 변경
        channel_columns = list(channel_type_counts.columns[1:-2])
        channel_type_counts.columns = ['사용자 유형'] + channel_columns + ['전체 비율', '개수']
        channel_dataframe = channel_type_counts.copy()
        
        # 각 채널 비율에 전체 비율을 곱해서 최종 비율 계산
        for col in channel_columns:
            channel_type_counts[col] = (channel_type_counts[col] * channel_type_counts['전체 비율'] / 100).round(1)
        
        # 최종 비율 컬럼 선택
        final_channel_type_counts = channel_type_counts[['사용자 유형', '개수', '전체 비율'] + channel_columns]
        channel_dataframe = channel_dataframe[['사용자 유형', '개수', '전체 비율'] + channel_columns]
        
        # 인덱스 재정렬
        final_channel_type_counts.reset_index(drop=True, inplace=True)
        channel_dataframe.reset_index(drop=True, inplace=True)
        
        # 소숫점 한자리로 표시
        final_channel_type_counts = final_channel_type_counts.round(1)
        channel_dataframe = channel_dataframe.round(1)
    
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

        final_counts_reason.sort_values(by='개수', ascending=True, inplace=True)
        final_counts_reason.reset_index(drop=True, inplace=True)
        
        fig = px.bar(final_counts_reason.melt(id_vars='사용자 유형', value_vars=all_reasons, var_name='탈퇴 사유', value_name='비율'),
                     y='사용자 유형',
                     x='비율',
                     color='탈퇴 사유',
                     orientation='h',
                     height=600,
                     hover_data={'비율': ':.2f%'})
        
        fig.update_layout(barmode='stack',
                          xaxis_title='비율 (%)',
                          yaxis_title='사용자 유형',
                          legend_title='탈퇴 사유')
        
        st.plotly_chart(fig)
        
        # Update the data formatting if needed
        for col in final_counts_reason_dataframe.columns:
            if final_counts_reason_dataframe[col].dtype == 'float64':
                final_counts_reason_dataframe[col] = final_counts_reason_dataframe[col].map("{:.1f}".format)
        
        dfff_display = final_counts_reason_dataframe.sort_values(by='개수', ascending=False)
        dfff_display.reset_index(drop=True, inplace=True)
        
        # Display DataFrame
        check3_key = "data_frame_view_3"
        if st.checkbox('데이터프레임 보기', key=check3_key):
            st.table(dfff_display)
            
    
    
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
        
        for col in join_period_counts_dataframe.columns:
            if join_period_counts_dataframe[col].dtype == 'float64':
                join_period_counts_dataframe[col] = join_period_counts_dataframe[col].map("{:.1f}".format)
        
        check4_key = "data_frame_view_4"
        check4 = st.checkbox('데이터프레임 보기', key=check4_key)
        if check4:
            st.table(join_period_counts_dataframe)
    
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
        
        for col in access_counts_dataframe.columns:
            if access_counts_dataframe[col].dtype == 'float64':
                access_counts_dataframe[col] = access_counts_dataframe[col].map("{:.1f}".format)
        
        check5_key = "data_frame_view_5"
        check5 = st.checkbox('데이터프레임 보기', key=check5_key)
        if check5:
            st.table(access_counts_dataframe)
    
    
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
    
        st.write("### 사용자 유형별 채널 비율")
        channels = ['KKB', 'SSEM']  # Update or confirm these channel labels
        final_channel_type_counts.sort_values(by='개수', ascending=True, inplace=True)
        final_channel_type_counts.reset_index(drop=True, inplace=True)
        
        fig = px.bar(final_channel_type_counts.melt(id_vars='사용자 유형', value_vars=channels, var_name='채널', value_name='비율'),
                     y='사용자 유형',
                     x='비율',
                     color='채널',
                     orientation='h',
                     height=600,
                     hover_data={'비율': ':.2f%'})
        
        fig.update_layout(barmode='stack',
                          xaxis_title='비율 (%)',
                          yaxis_title='사용자 유형',
                          legend_title='채널')
        
        st.plotly_chart(fig)
        
        # Update the data formatting if needed
        for col in channel_dataframe.columns:
            if channel_dataframe[col].dtype == 'float64':
                channel_dataframe[col] = channel_dataframe[col].map("{:.1f}".format)
                
        dffff_display = channel_dataframe.sort_values(by='개수', ascending=False)
        dffff_display.reset_index(drop=True,inplace=True)

        # Display DataFrame
        check6_key = "data_frame_view_6"
        if st.checkbox('데이터프레임 보기', key=check6_key):
            st.table(dffff_display)

        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)

# -----------------------------------------------------------------------------------------------------------------

        def calculate_inquiry_insights(dataframe, business):
            """Calculate insights for a specific business type from a dataframe."""
            business_type = dataframe[dataframe['사용자 유형'].str.contains(business)]
            type_ratio = (business_type.shape[0] / dataframe.shape[0]) * 100
            total_access_mean = business_type['총 접속 수'].mean()
            total_access_0_1_ratio = (business_type['총 접속 수'] <= 1).mean() * 100
        
            service_columns = [
                '부가세 결제 수', '부가세 결제 취소 수', '부가세 계산 시작 수', '부가세 계산 완료 수',
                '종소세 결제 수', '종소세 결제 취소 수', '종소세 계산 시작 수', '종소세 계산 완료 수',
                '인건비 결제 수', '인건비 결제 취소 수', '매출알림 서비스 이용 여부', '매출알림 서비스 탈퇴 여부',
                '안심신고 이용 여부', '재가입 여부'
            ]
        
            service_usage_stats = {}
            for column in service_columns:
                if business_type[column].dtype == 'object':
                    service_usage_stats[f"{column} 비율"] = (business_type[column] == 'Y').mean() * 100
                else:
                    service_usage_stats[f"{column} 평균"] = business_type[column].mean()
                    
            # 탈퇴 사유 비율 계산
            reasons = [
                '사용할 수 있는 서비스가 없어요.', '개인정보 유출이 걱정돼요.', '타 서비스보다 세금이 더 많이 나와요.',
                '자료 수집이 안돼요.', '이용 요금이 비싸요.', '직접 해야 하는 게 많아요.', '문의 답변이 오래 걸려요.', '직접 입력할게요.'
            ]
            reason_counts = business_type['탈퇴사유'].apply(lambda x: [r for r in reasons if r in x])
            reason_flattened = [item for sublist in reason_counts for item in sublist]
            reason_ratio = pd.Series(reason_flattened).value_counts(normalize=True) * 100
            reason_ratio = reason_ratio.to_dict()
        
            channel_ratio = business_type['채널'].value_counts(normalize=True) * 100
        
            insights = {
                '개수': business_type.shape[0],
                '비율': type_ratio,
                '접속 횟수 평균': total_access_mean,
                '1회이하 접속 비율': total_access_0_1_ratio,
                '가입 기간 평균': business_type['가입 기간'].mean(),
                '24시간 내 탈퇴 비율': (business_type['가입 기간'] == 0).mean() * 100,
                **{f'{k} 비율': v for k, v in reason_ratio.items()},
                **{f'{k} 비율': v for k, v in channel_ratio.items()},
                **service_usage_stats
            }
        
            return pd.DataFrame([insights], index=[business]).round(2)
        
        def generate_all_insights(dataframe):
            unique_businesses = dataframe['사용자 유형'].unique()
            all_insights = [calculate_inquiry_insights(dataframe, business) for business in unique_businesses]
        
            final_df = pd.concat(all_insights)
        
            # 열 순서 지정
            reasons = [
                '사용할 수 있는 서비스가 없어요. 비율', '개인정보 유출이 걱정돼요. 비율', '타 서비스보다 세금이 더 많이 나와요. 비율',
                '자료 수집이 안돼요. 비율', '이용 요금이 비싸요. 비율', '직접 해야 하는 게 많아요. 비율', '문의 답변이 오래 걸려요. 비율', '직접 입력할게요. 비율'
            ]
            desired_order = [
                '개수', '비율'] + reasons + ['가입 기간 평균', 
                '24시간 내 탈퇴 비율', '접속 횟수 평균', '1회이하 접속 비율', 
                'SSEM 비율', 'KKB 비율'
            ]
            desired_order = desired_order + [col for col in final_df.columns if col not in desired_order]
            final_df = final_df[desired_order]
        
            return final_df
        
        # 사용 예시
        quit_person_summary = filtered.copy()
        all_insights_df2 = generate_all_insights(quit_person_summary)
        all_insights_df2.fillna(0, inplace=True)
        all_insights_df2.sort_values('개수', ascending = False, inplace=True)

        st.write("### 사용자 유형별 세부 데이터")
        
        if st.checkbox('사용자 유형별 요약 통계 보기', key='summary_stats'):
            st.dataframe(all_insights_df2)
            
    

        if st.checkbox('사용자 유형별 데이터프레임 보기', key='detailed_data'):
            # 사용자가 사용자 유형을 선택할 수 있는 선택 상자 생성
            user_types_whole = filtered.copy()
            user_types_options = ['전체'] + sorted(user_types_whole['사용자 유형'].dropna().unique())
            selected_user_type = st.selectbox('사용자 유형 선택:', options=user_types_options, index=0)
            
            # 선택된 사용자 유형에 따라 데이터 필터링
            if selected_user_type == '전체':
                filtered_view = user_types_whole
            else:
                filtered_view = user_types_whole[user_types_whole['사용자 유형'] == selected_user_type]
            
            st.dataframe(filtered_view)
    
    
    
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
        filtered_reason = filtered[['채널', '탈퇴사유']].copy()
        filtered_reason['탈퇴사유'] = filtered_reason['탈퇴사유'].str.split(';')
        filtered_reason = filtered_reason.explode('탈퇴사유').dropna().reset_index(drop=True)
        
        # 채널별 총 개수 및 전체 비율 계산
        total_counts_reason = filtered['채널'].value_counts().reset_index()
        total_counts_reason.columns = ['채널', 'Total count']
        total_counts_reason['전체 비율'] = (total_counts_reason['Total count'] / total_counts_reason['Total count'].sum() * 100).round(1)
        
        # 채널별 탈퇴 사유 카운트 및 비율 계산
        reason_counts = filtered_reason.groupby(['채널', '탈퇴사유']).size().reset_index(name='count')
        
        # 채널별 총 탈퇴 사유 개수 계산
        total_reason_by_type = filtered_reason.groupby('채널')['탈퇴사유'].count().reset_index()
        total_reason_by_type.columns = ['채널', '탈퇴 사유 총합']
        
        # 탈퇴 사유 비율 계산
        reason_counts = reason_counts.merge(total_reason_by_type, on='채널')
        reason_counts['비율'] = (reason_counts['count'] / reason_counts['탈퇴 사유 총합'] * 100).round(1)
        
        # 채널별 전체 비율과 탈퇴 사유 비율 병합
        final_counts_reason = reason_counts.pivot_table(index='채널', columns='탈퇴사유', values='비율', fill_value=0).reset_index()
        final_counts_reason = final_counts_reason.merge(total_counts_reason[['채널', '전체 비율', 'Total count']], on='채널')
        
        all_reasons = ['사용할 수 있는 서비스가 없어요.', '개인정보 유출이 걱정돼요.', '타 서비스보다 세금이 더 많이 나와요.', 
                       '자료 수집이 안돼요.', '이용 요금이 비싸요.', '직접 해야 하는 게 많아요.', '문의 답변이 오래 걸려요.', '직접 입력할게요.']
        
        final_counts_reason_dataframe = final_counts_reason.copy()
        
        for label in all_reasons:
            final_counts_reason[label] = (final_counts_reason[label] * final_counts_reason['전체 비율'] / 100).round(1)
        
        # 탈퇴 사유 컬럼명 정리
        final_counts_reason = final_counts_reason[['채널', 'Total count', '전체 비율'] + all_reasons]
        final_counts_reason_dataframe = final_counts_reason_dataframe[['채널', 'Total count', '전체 비율'] + all_reasons]
        
        final_counts_reason.columns = ['채널', '개수', '전체 비율'] + all_reasons
        final_counts_reason_dataframe.columns = ['채널', '개수', '전체 비율'] + all_reasons
        
        # 인덱스 재정렬
        final_counts_reason.reset_index(drop=True, inplace=True)
        final_counts_reason_dataframe.reset_index(drop=True, inplace=True)
        
        # 소숫점 한자리로 표시
        final_counts_reason = final_counts_reason.round(1)
        final_counts_reason_dataframe = final_counts_reason_dataframe.round(1)
    
    
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
        channel_user_type_dataframe = channel_user_type_counts.copy()
        
        # 각 사용자 유형 비율에 전체 비율을 곱해서 최종 비율 계산
        for user_type in reason_counts['사용자 유형'].unique():
            channel_user_type_counts[user_type] = (channel_user_type_counts[user_type] * channel_user_type_counts['전체 비율'] / 100).round(1)
        
        
        # 최종 비율 컬럼 선택
        final_channel_user_type_counts = channel_user_type_counts[['채널', '개수', '전체 비율'] + list(reason_counts['사용자 유형'].unique())]
        channel_user_type_dataframe = channel_user_type_dataframe[['채널', '개수', '전체 비율'] + list(reason_counts['사용자 유형'].unique())]
        
        # 인덱스 재정렬
        final_channel_user_type_counts.reset_index(drop=True, inplace=True)
        channel_user_type_dataframe.reset_index(drop=True, inplace=True)
        
        # 소숫점 한자리로 표시
        final_channel_user_type_counts = final_channel_user_type_counts.round(1)
        channel_user_type_dataframe = channel_user_type_dataframe.round(1)
    
    
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
        period_counts_dataframe = period_counts.copy()
        
        for label in order:
            period_counts[label] = (period_counts[label] * period_counts['전체 비율'] / 100).round(1)
        
        # 필요한 열만 선택
        final_period_counts = period_counts[['채널', 'count', '전체 비율'] + [label for label in order]]
        period_counts_dataframe = period_counts_dataframe[['채널', 'count', '전체 비율'] + [label for label in order]]
        
        final_period_counts.columns = ['채널', '개수', '전체 비율', '0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
        period_counts_dataframe.columns = ['채널', '개수', '전체 비율', '0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
        
        final_period_counts = final_period_counts.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
        period_counts_dataframe = period_counts_dataframe.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
    
        # ------------------------------------------------------------------------------------------------------
        
         # 채널별 접속 횟수 비율 전처리
        filter3 = filtered[['채널', '총 접속 수']].copy()
        bins = [1, 2, 5, 10, 20, float('inf')]
        labels = ["1", "2~5", "5~10", "10~20", "20 이상"]
        filter3['접속 횟수 구간'] = pd.cut(filter3['총 접속 수'], bins=bins, labels=labels, right=False)
        filter3 = filter3.dropna(subset=['접속 횟수 구간'])
        filter3 = filter3.reset_index(drop=True)
        
        total_reason_counts = filter3['채널'].value_counts().reset_index()
        total_reason_counts.columns = ['채널', 'Total count']
        
        access_counts = filter3.groupby(['채널', '접속 횟수 구간']).size().unstack(fill_value=0)
        access_counts = access_counts.div(access_counts.sum(axis=1), axis=0) * 100
        access_counts = access_counts.reset_index()
        
        total_counts = filter3['채널'].value_counts().reset_index()
        total_counts.columns = ['채널', 'count']
        total_counts['전체 비율'] = (total_counts['count'] / total_counts['count'].sum() * 100).round(1)
        
        access_counts = access_counts.merge(total_counts[['채널', 'count', '전체 비율']], on='채널')
        access_counts_dataframe = access_counts.copy()
        
        for label in labels:
            access_counts[label] = (access_counts[label] * access_counts['전체 비율'] / 100).round(1)
        
        final_channel_access_counts = access_counts[['채널', 'count', '전체 비율'] + labels]
        access_counts_dataframe = access_counts_dataframe[['채널', 'count', '전체 비율'] + labels]
        
        final_channel_access_counts.columns = ['채널', '개수', '전체 비율'] + labels
        access_counts_dataframe.columns = ['채널', '개수', '전체 비율'] + labels
        
        final_channel_access_counts = final_channel_access_counts.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
        access_counts_dataframe = access_counts_dataframe.sort_values(by='전체 비율', ascending=False).reset_index(drop=True)
        
        # 데이터 유형 확인 및 변환
        for col in final_channel_access_counts.columns[3:]:
            final_channel_access_counts[col] = pd.to_numeric(final_channel_access_counts[col], errors='coerce')

        for col in access_counts_dataframe.columns[3:]:
            access_counts_dataframe[col] = pd.to_numeric(access_counts_dataframe[col], errors='coerce')
    
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
    
        st.write("### 채널별 탈퇴 사유 비율")
        final_counts_reason.sort_values(by='채널', ascending=True, inplace=True)
        final_counts_reason.reset_index(drop=True, inplace=True)
        
        fig = px.bar(final_counts_reason.melt(id_vars='채널', value_vars=all_reasons, var_name='탈퇴 사유', value_name='비율'),
                     y='채널',
                     x='비율',
                     color='탈퇴 사유',
                     orientation='h',
                     height=600,
                     hover_data={'비율': ':.2f%'})
        
        fig.update_layout(barmode='stack',
                          xaxis_title='비율 (%)',
                          yaxis_title='채널',
                          legend_title='탈퇴 사유')
        
        st.plotly_chart(fig)
        
        for col in final_counts_reason_dataframe.columns:
            if final_counts_reason_dataframe[col].dtype == 'float64':
                final_counts_reason_dataframe[col] = final_counts_reason_dataframe[col].map("{:.1f}".format)

        dfffff_display = final_counts_reason_dataframe.sort_values(by='개수', ascending=False)
        dfffff_display.reset_index(drop=True,inplace=True)
        
        
        # DataFrame 표시
        check7_key = "data_frame_view_7"
        check7 = st.checkbox('데이터프레임 보기', key=check7_key)
        if check7:
            st.table(dfffff_display)

    
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
        final_channel_user_type_counts.sort_values(by='채널', ascending=True, inplace=True)
        final_channel_user_type_counts.reset_index(drop=True, inplace=True)
        
        user_types = ['그 외','개인사업자','법인','폐업']

        fig = px.bar(final_channel_user_type_counts.melt(id_vars='채널', value_vars=user_types, var_name='사용자 유형', value_name='비율'),
                     y='채널',
                     x='비율',
                     color='사용자 유형',
                     orientation='h',
                     height=600,
                     hover_data={'비율': ':.2f%'})
        
        fig.update_layout(barmode='stack',
                          xaxis_title='비율 (%)',
                          yaxis_title='채널',
                          legend_title='사용자 유형')
        
        st.plotly_chart(fig)
        
        for col in channel_user_type_dataframe.columns:
            if channel_user_type_dataframe[col].dtype == 'float64':
                channel_user_type_dataframe[col] = channel_user_type_dataframe[col].map("{:.1f}".format)

        dffffff_display = channel_user_type_dataframe.sort_values(by='개수', ascending=False)
        dffffff_display.reset_index(drop=True,inplace=True)
        
        # DataFrame 표시
        check8_key = "data_frame_view_8"
        check8 = st.checkbox('데이터프레임 보기', key=check8_key)
        if check8:
            st.table(dffffff_display)
    
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
        
        for col in period_counts_dataframe.columns:
            if period_counts_dataframe[col].dtype == 'float64':
                period_counts_dataframe[col] = period_counts_dataframe[col].map("{:.1f}".format)
                
        
        check9_key = "data_frame_view_3"
        check9 = st.checkbox('데이터프레임 보기', key=check9_key)
        if check9:
            period_counts_dataframe = period_counts_dataframe.round(1)
            st.table(period_counts_dataframe)
    
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
        
        for channel in final_channel_access_counts['채널'].unique():
            channel_data = final_channel_access_counts[final_channel_access_counts['채널'] == channel]
            
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
        
        for col in access_counts_dataframe.columns:
            if access_counts_dataframe[col].dtype == 'float64':
                access_counts_dataframe[col] = access_counts_dataframe[col].map("{:.1f}".format)
        
        # DataFrame 표시
        check10_key = "data_frame_view_10"
        check10 = st.checkbox('데이터프레임 보기', key=check10_key)
        if check10:
            access_counts_dataframe = access_counts_dataframe.round(1)
            st.table(access_counts_dataframe)


        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)
        st.text("""
        """)

# -----------------------------------------------------------------------------------------------------------------

        def calculate_channel_insights(dataframe, channel):
            """Calculate insights for a specific channel from a dataframe."""
            channel_type = dataframe[dataframe['채널'].str.contains(channel, na=False)]
            type_ratio = (channel_type.shape[0] / dataframe.shape[0]) * 100
            total_access_mean = channel_type['총 접속 수'].mean()
            total_access_0_1_ratio = (channel_type['총 접속 수'] <= 1).mean() * 100
        
            service_columns = [
                '부가세 결제 수', '부가세 결제 취소 수', '부가세 계산 시작 수', '부가세 계산 완료 수',
                '종소세 결제 수', '종소세 결제 취소 수', '종소세 계산 시작 수', '종소세 계산 완료 수',
                '인건비 결제 수', '인건비 결제 취소 수', '매출알림 서비스 이용 여부', '매출알림 서비스 탈퇴 여부',
                '안심신고 이용 여부', '재가입 여부'
            ]
        
            service_usage_stats = {}
            for column in service_columns:
                if channel_type[column].dtype == 'object':
                    service_usage_stats[f"{column} 비율"] = (channel_type[column] == 'Y').mean() * 100
                else:
                    service_usage_stats[f"{column} 평균"] = channel_type[column].mean()
                    
            # 탈퇴 사유 비율 계산
            reasons = [
                '사용할 수 있는 서비스가 없어요.', '개인정보 유출이 걱정돼요.', '타 서비스보다 세금이 더 많이 나와요.',
                '자료 수집이 안돼요.', '이용 요금이 비싸요.', '직접 해야 하는 게 많아요.', '문의 답변이 오래 걸려요.', '직접 입력할게요.'
            ]
            reason_counts = channel_type['탈퇴사유'].dropna().apply(lambda x: [r for r in reasons if r in x])
            reason_flattened = [item for sublist in reason_counts for item in sublist]
            reason_ratio = pd.Series(reason_flattened).value_counts(normalize=True) * 100
            reason_ratio = reason_ratio.to_dict()
             
            business_type_ratio = channel_type['사용자 유형'].value_counts(normalize=True) * 100
        
            insights = {
                '개수': channel_type.shape[0],
                '비율': type_ratio,
                '접속 횟수 평균': total_access_mean,
                '1회이하 접속 비율': total_access_0_1_ratio,
                '가입 기간 평균': channel_type['가입 기간'].mean(),
                '24시간 내 탈퇴 비율': (channel_type['가입 기간'] == 0).mean() * 100,
                **{f'{k} 비율': v for k, v in reason_ratio.items()},
                **{f'{a} 비율': b for a, b in business_type_ratio.items()},
                **service_usage_stats
            }
        
            return pd.DataFrame([insights], index=[channel]).round(2)
        
        def generate_all_insights(dataframe):
            unique_channels = dataframe['채널'].unique()
            all_insights = [calculate_channel_insights(dataframe, channel) for channel in unique_channels]
        
            final_df = pd.concat(all_insights)
        
            # 열 순서 지정
            reasons = [
                '사용할 수 있는 서비스가 없어요. 비율', '개인정보 유출이 걱정돼요. 비율', '타 서비스보다 세금이 더 많이 나와요. 비율',
                '자료 수집이 안돼요. 비율', '이용 요금이 비싸요. 비율', '직접 해야 하는 게 많아요. 비율', '문의 답변이 오래 걸려요. 비율', '직접 입력할게요. 비율'
            ]
            desired_order = [
                '개수', '비율'] + reasons + ['그 외 비율', '개인사업자 비율', 
                '폐업 비율', '법인 비율','가입 기간 평균', 
                '24시간 내 탈퇴 비율', '접속 횟수 평균', '1회이하 접속 비율'
            ]
            desired_order = desired_order + [col for col in final_df.columns if col not in desired_order]
            final_df = final_df[desired_order]
        
            return final_df
        
        # 사용 예시
        quit_channel_summary = filtered.copy()
        all_insights_df3 = generate_all_insights(quit_channel_summary)
        all_insights_df3.fillna(0, inplace=True)
        all_insights_df3.sort_values('개수', ascending = False, inplace=True)
        
        st.write("### 채널별 세부 데이터")
        
        if st.checkbox('채널별 요약 통계 보기', key='summary_stats_channel'):
            st.dataframe(all_insights_df3)
                
        
        if st.checkbox('채널별 데이터프레임 보기', key='detailed_data_channel'):
            # 사용자가 채널을 선택할 수 있는 선택 상자 생성
            channels_whole = filtered.copy()
            channels_options = ['전체'] + sorted(channels_whole['채널'].dropna().unique())
            selected_channel = st.selectbox('채널 선택:', options=channels_options, index=0, key='selectbox_channel')
            
            # 선택된 채널에 따라 데이터 필터링
            if selected_channel == '전체':
                filtered_view = channels_whole
            else:
                filtered_view = channels_whole[channels_whole['채널'] == selected_channel]
            
            st.dataframe(filtered_view)


        
    
#-------------------------------------------------------------------------------------------------
        
    if page == "가입기간별":
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
                
                filtered = filtered.dropna(subset=['탈퇴사유'])
            
            
            else:
                filtered = data
    
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

            # 가입 기간별 탈퇴사유 비율
            filter_join_period = filtered[['가입 구간', '탈퇴사유']].copy()
            filter_join_period['탈퇴사유'] = filter_join_period['탈퇴사유'].str.split(';')
            filter_join_period = filter_join_period.explode('탈퇴사유').dropna().reset_index(drop=True)
            
            # 가입 구간별 총 개수 및 전체 비율 계산
            total_counts = filtered['가입 구간'].value_counts().reset_index()
            total_counts.columns = ['가입 구간', '개수']
            total_counts['전체 비율'] = (total_counts['개수'] / total_counts['개수'].sum() * 100).round(1)
            
            # 가입 구간별 탈퇴 사유 카운트 및 비율 계산
            reason_counts = filter_join_period.groupby(['가입 구간', '탈퇴사유']).size().reset_index(name='count')
            total_reason_counts = reason_counts.groupby('가입 구간')['count'].sum().reset_index()
            reason_counts = reason_counts.merge(total_reason_counts, on='가입 구간', suffixes=('', '_total'))
            reason_counts['비율'] = (reason_counts['count'] / reason_counts['count_total'] * 100).round(1)
            
            # 최종 데이터프레임 생성
            final_counts = reason_counts.pivot_table(index='가입 구간', columns='탈퇴사유', values='비율', fill_value=0).reset_index()
            final_counts = final_counts.merge(total_counts[['가입 구간', '전체 비율', '개수']], on='가입 구간')
            final_counts_dataframe = final_counts.copy()
            
            # 순서 지정
            order = ['0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
            final_counts['가입 구간'] = pd.Categorical(final_counts['가입 구간'], categories=order[::-1], ordered=True)
            final_counts_dataframe['가입 구간'] = pd.Categorical(final_counts_dataframe['가입 구간'], categories=order, ordered=True)
            
            final_counts = final_counts.sort_values('가입 구간').reset_index(drop=True)
            final_counts_dataframe = final_counts_dataframe.sort_values('가입 구간').reset_index(drop=True)
            
            # 전체 비율 곱해서 최종 비율 계산
            for column in final_counts.columns:
                if column not in ['가입 구간', '개수', '전체 비율']:
                    final_counts[column] = (final_counts[column] * final_counts['전체 비율'] / 100).round(1)
    
            reasons = [
                    '사용할 수 있는 서비스가 없어요.', '개인정보 유출이 걱정돼요.', '타 서비스보다 세금이 더 많이 나와요.',
                    '자료 수집이 안돼요.', '이용 요금이 비싸요.', '직접 해야 하는 게 많아요.', '문의 답변이 오래 걸려요.', '직접 입력할게요.'
                ]
            
            # 데이터프레임 순서 지정
            final_counts = final_counts[['가입 구간', '개수', '전체 비율'] + reasons]
            final_counts_dataframe = final_counts_dataframe[['가입 구간', '개수', '전체 비율'] + reasons]
            
            st.write("### 가입기간별 탈퇴 사유 비율")
    
            
            # 그래프 생성
            fig = px.bar(final_counts.melt(id_vars='가입 구간', value_vars=final_counts.columns[3:], var_name='탈퇴 사유', value_name='비율'),
                         y='가입 구간',
                         x='비율',
                         color='탈퇴 사유',
                         orientation='h',
                         height=600,
                         hover_data={'비율': ':.2f%'})
            
            fig.update_layout(barmode='stack',
                              xaxis_title='비율 (%)',
                              yaxis_title='가입 구간',
                              legend_title='탈퇴 사유')
            
            st.plotly_chart(fig)
            
            for col in final_counts_dataframe.columns:
                if final_counts_dataframe[col].dtype == 'float64':
                    final_counts_dataframe[col] = final_counts_dataframe[col].map("{:.1f}".format)
            
            # DataFrame 표시
            check11_key = "data_frame_view_11"
            check11 = st.checkbox('데이터프레임 보기', key=check11_key)
            if check11:
                st.table(final_counts_dataframe)
    
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)
                
    # -------------------------------------------------------------------------------------------------------------
    
            
            # 가입 구간별 사용자 유형 비율
            filter_user_type = filtered[['가입 구간', '사용자 유형']].copy()
            filter_user_type = filter_user_type.dropna().reset_index(drop=True)
            
            # 가입 구간별 총 개수 및 전체 비율 계산
            total_counts_user = filtered['가입 구간'].value_counts().reset_index()
            total_counts_user.columns = ['가입 구간', '개수']
            total_counts_user['전체 비율'] = (total_counts_user['개수'] / total_counts_user['개수'].sum() * 100).round(1)
            
            # 가입 구간별 사용자 유형 카운트 및 비율 계산
            user_type_counts = filter_user_type.groupby(['가입 구간', '사용자 유형']).size().reset_index(name='count')
            total_user_type_counts = user_type_counts.groupby('가입 구간')['count'].sum().reset_index()
            user_type_counts = user_type_counts.merge(total_user_type_counts, on='가입 구간', suffixes=('', '_total'))
            user_type_counts['비율'] = (user_type_counts['count'] / user_type_counts['count_total'] * 100).round(1)
            
            # 최종 데이터프레임 생성
            final_user_type_counts = user_type_counts.pivot_table(index='가입 구간', columns='사용자 유형', values='비율', fill_value=0).reset_index()
            final_user_type_counts = final_user_type_counts.merge(total_counts_user[['가입 구간', '전체 비율', '개수']], on='가입 구간')
            final_user_type_counts_dataframe = final_user_type_counts.copy()
    
            # 각 사용자 유형 비율에 전체 비율 곱하기
            for user_type in final_user_type_counts.columns[1:-2]:
                final_user_type_counts[user_type] = (final_user_type_counts[user_type] * final_user_type_counts['전체 비율'] / 100).round(1)
            
            # 원래 순서대로 가입 구간 정렬
            final_user_type_counts['가입 구간'] = pd.Categorical(final_user_type_counts['가입 구간'], categories=order[::-1], ordered=True)
            final_user_type_counts_dataframe['가입 구간'] = pd.Categorical(final_user_type_counts_dataframe['가입 구간'], categories=order, ordered=True)
    
            final_user_type_counts = final_user_type_counts.sort_values('가입 구간').reset_index(drop=True)
            final_user_type_counts_dataframe = final_user_type_counts_dataframe.sort_values('가입 구간').reset_index(drop=True)
    
            
            # 데이터프레임 순서 지정
            user_types = ['그 외', '개인사업자', '법인', '폐업']
            final_user_type_counts = final_user_type_counts[['가입 구간', '개수', '전체 비율'] + user_types]
            final_user_type_counts_dataframe = final_user_type_counts_dataframe[['가입 구간', '개수', '전체 비율'] + user_types]
    
            
                    
           # 데이터프레임 표시
            st.write("### 가입기간별 사용자 유형 비율")
            
            # 그래프 생성
            fig_user_type = px.bar(final_user_type_counts.melt(id_vars='가입 구간', value_vars=user_types, var_name='사용자 유형', value_name='비율'),
                                   y='가입 구간',
                                   x='비율',
                                   color='사용자 유형',
                                   orientation='h',
                                   height=600,
                                   hover_data={'비율': ':.2f%'})
            
            fig_user_type.update_layout(barmode='stack',
                                        xaxis_title='비율 (%)',
                                        yaxis_title='가입 구간',
                                        legend_title='사용자 유형')
            
            st.plotly_chart(fig_user_type)
            
            for col in final_user_type_counts_dataframe.columns:
                if final_user_type_counts_dataframe[col].dtype == 'float64':
                    final_user_type_counts_dataframe[col] = final_user_type_counts_dataframe[col].map("{:.1f}".format)
            
            # DataFrame 표시
            check12_key = "data_frame_view_12"
            check12 = st.checkbox('데이터프레임 보기', key=check12_key)
            if check12:
                st.table(final_user_type_counts_dataframe)
    
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)       
    
    
    # -------------------------------------------------------------------------------------------------------------
    
    
            # 가입기간별 접속횟수 비율
            filter_join_access = filtered[['가입 구간', '총 접속 수']].copy()
            bins = [1, 2, 5, 10, 20, float('inf')]
            labels = ["1", "2~5", "5~10", "10~20", "20 이상"]
            filter_join_access['접속 횟수 구간'] = pd.cut(filter_join_access['총 접속 수'], bins=bins, labels=labels, right=False)
            filter_join_access = filter_join_access.dropna(subset=['접속 횟수 구간'])
            filter_join_access = filter_join_access.reset_index(drop=True)
            
            total_join_access_counts = filter_join_access['가입 구간'].value_counts().reset_index()
            total_join_access_counts.columns = ['가입 구간', '개수']
            
            join_access_counts = filter_join_access.groupby(['가입 구간', '접속 횟수 구간']).size().unstack(fill_value=0)
            join_access_counts = join_access_counts.div(join_access_counts.sum(axis=1), axis=0) * 100
            join_access_counts = join_access_counts.reset_index()
            
            total_join_access_counts = filter_join_access['가입 구간'].value_counts().reset_index()
            total_join_access_counts.columns = ['가입 구간', '개수']
            total_join_access_counts['전체 비율'] = (total_join_access_counts['개수'] / total_join_access_counts['개수'].sum() * 100).round(1)
            
            join_access_counts = join_access_counts.merge(total_join_access_counts[['가입 구간', '개수', '전체 비율']], on='가입 구간')
            join_access_counts_dataframe = join_access_counts.copy()
            
            for label in labels:
                if label in join_access_counts.columns:
                    join_access_counts[label] = (join_access_counts[label] * join_access_counts['전체 비율'] / 100).round(1)
    
            # 원래 순서대로 가입 구간 정렬
            join_access_counts['가입 구간'] = pd.Categorical(join_access_counts['가입 구간'], categories=order[::-1], ordered=True)
            join_access_counts_dataframe['가입 구간'] = pd.Categorical(join_access_counts_dataframe['가입 구간'], categories=order, ordered=True)
    
            join_access_counts = join_access_counts.sort_values('가입 구간').reset_index(drop=True)
            join_access_counts_dataframe = join_access_counts_dataframe.sort_values('가입 구간').reset_index(drop=True)
    
            
            # 데이터프레임 순서 지정
            join_access_counts = join_access_counts[['가입 구간', '개수', '전체 비율'] + labels]
            join_access_counts_dataframe = join_access_counts_dataframe[['가입 구간', '개수', '전체 비율'] + labels]
    
    
            
            st.write("### 가입기간별 접속횟수 비율")
            fig = go.Figure()
            
            for access_period in join_access_counts['가입 구간'].unique():
                access_data = join_access_counts[join_access_counts['가입 구간'] == access_period]
                fig.add_trace(go.Scatter(
                    x=labels,
                    y=access_data.iloc[0, 3:].values,
                    mode='lines+markers', 
                    name=access_period
                ))
            
            fig.update_layout(
                xaxis_title='접속 횟수 구간',
                yaxis_title='비율 (%)',
                legend_title='가입 구간'
            )
            
            st.plotly_chart(fig)
            
            for col in join_access_counts_dataframe.columns:
                if join_access_counts_dataframe[col].dtype == 'float64':
                    join_access_counts_dataframe[col] = join_access_counts_dataframe[col].map("{:.1f}".format)
            
            check13_key = "data_frame_view_13"
            check13 = st.checkbox('데이터프레임 보기', key=check13_key)
            if check13:
                st.table(join_access_counts_dataframe)
    
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)
    
    
    
    # -------------------------------------------------------------------------------------------------------------
    
    
            
            # 가입기간별 채널 비율
            filter_join_channel = filtered[['가입 구간', '채널']].dropna().reset_index(drop=True)
            
            total_join_channel_counts = filter_join_channel['가입 구간'].value_counts().reset_index()
            total_join_channel_counts.columns = ['가입 구간', '개수']
            
            join_channel_counts = filter_join_channel.groupby(['가입 구간', '채널']).size().unstack(fill_value=0)
            join_channel_counts = join_channel_counts.div(join_channel_counts.sum(axis=1), axis=0) * 100
            join_channel_counts = join_channel_counts.reset_index()
            
            total_join_channel_counts = filter_join_channel['가입 구간'].value_counts().reset_index()
            total_join_channel_counts.columns = ['가입 구간', 'count']
            total_join_channel_counts['전체 비율'] = (total_join_channel_counts['count'] / total_join_channel_counts['count'].sum() * 100).round(1)
            
            join_channel_counts = join_channel_counts.merge(total_join_channel_counts[['가입 구간', 'count', '전체 비율']], on='가입 구간')
            join_channel_counts_dataframe = join_channel_counts.copy()
            
            for label in filter_join_channel['채널'].unique():
                if label in join_channel_counts.columns:
                    join_channel_counts[label] = (join_channel_counts[label] * join_channel_counts['전체 비율'] / 100).round(1)
            
            final_join_channel_counts = join_channel_counts[['가입 구간', 'count', '전체 비율'] + [label for label in filter_join_channel['채널'].unique() if label in join_channel_counts.columns]]
            join_channel_counts_dataframe = join_channel_counts_dataframe[['가입 구간', 'count', '전체 비율'] + [label for label in filter_join_channel['채널'].unique() if label in join_channel_counts.columns]]
            
            final_join_channel_counts.columns = ['가입 구간', '개수', '전체 비율'] + [label for label in filter_join_channel['채널'].unique() if label in join_channel_counts.columns]
            join_channel_counts_dataframe.columns = ['가입 구간', '개수', '전체 비율'] + [label for label in filter_join_channel['채널'].unique() if label in join_channel_counts.columns]
            
            # 원래 순서대로 가입 구간 정렬
            final_join_channel_counts['가입 구간'] = pd.Categorical(final_join_channel_counts['가입 구간'], categories=order[::-1], ordered=True)
            final_join_channel_counts = final_join_channel_counts.sort_values('가입 구간').reset_index(drop=True)
            join_channel_counts_dataframe['가입 구간'] = pd.Categorical(join_channel_counts_dataframe['가입 구간'], categories=order, ordered=True)
            join_channel_counts_dataframe = join_channel_counts_dataframe.sort_values('가입 구간').reset_index(drop=True)
            
            st.write("### 가입기간별 채널 비율")
            
            # 그래프 생성
            fig_channel = px.bar(final_join_channel_counts.melt(id_vars='가입 구간', value_vars=[label for label in filter_join_channel['채널'].unique() if label in join_channel_counts.columns], var_name='채널', value_name='비율'),
                                 y='가입 구간',
                                 x='비율',
                                 color='채널',
                                 orientation='h',
                                 height=600,
                                 hover_data={'비율': ':.2f%'})
            
            fig_channel.update_layout(barmode='stack',
                                      xaxis_title='비율 (%)',
                                      yaxis_title='가입 구간',
                                      legend_title='채널')
            
            st.plotly_chart(fig_channel)
            
            for col in join_channel_counts_dataframe.columns:
                if join_channel_counts_dataframe[col].dtype == 'float64':
                    join_channel_counts_dataframe[col] = join_channel_counts_dataframe[col].map("{:.1f}".format)
            
            check14_key = "data_frame_view_14"
            check14 = st.checkbox('데이터프레임 보기', key=check14_key)
            if check14:
                st.table(join_channel_counts_dataframe)
    
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)
    
    # -------------------------------------------------------------------------------------------------------------
    
            
            
            # 요약 통계 함수 정의
            def calculate_period_insights(dataframe, period):
                """Calculate insights for a specific join period from a dataframe."""
                period_data = dataframe[dataframe['가입 구간'] == period]
                total_count = dataframe.shape[0]
                period_count = period_data.shape[0]
                
                type_ratio = (period_count / total_count) * 100
                total_access_mean = period_data['총 접속 수'].mean()
                total_access_0_1_ratio = (period_data['총 접속 수'] <= 1).mean() * 100
            
                service_columns = [
                    '부가세 결제 수', '부가세 결제 취소 수', '부가세 계산 시작 수', '부가세 계산 완료 수',
                    '종소세 결제 수', '종소세 결제 취소 수', '종소세 계산 시작 수', '종소세 계산 완료 수',
                    '인건비 결제 수', '인건비 결제 취소 수', '매출알림 서비스 이용 여부', '매출알림 서비스 탈퇴 여부',
                    '안심신고 이용 여부', '재가입 여부'
                ]
            
                service_usage_stats = {}
                for column in service_columns:
                    if period_data[column].dtype == 'object':
                        service_usage_stats[f"{column} 비율"] = (period_data[column] == 'Y').mean() * 100
                    else:
                        service_usage_stats[f"{column} 평균"] = period_data[column].mean()
                        
                # 탈퇴 사유 비율 계산
                reasons = [
                    '사용할 수 있는 서비스가 없어요.', '개인정보 유출이 걱정돼요.', '타 서비스보다 세금이 더 많이 나와요.',
                    '자료 수집이 안돼요.', '이용 요금이 비싸요.', '직접 해야 하는 게 많아요.', '문의 답변이 오래 걸려요.', '직접 입력할게요.'
                ]
                reason_counts = period_data['탈퇴사유'].dropna().apply(lambda x: [r for r in reasons if r in x])
                reason_flattened = [item for sublist in reason_counts for item in sublist]
                reason_ratio = pd.Series(reason_flattened).value_counts(normalize=True) * 100
                reason_ratio = reason_ratio.to_dict()
                 
                business_type_ratio = period_data['사용자 유형'].value_counts(normalize=True) * 100
                channel_ratio = period_data['채널'].value_counts(normalize=True) * 100
                
                insights = {
                    '개수': period_count,
                    '비율': type_ratio,
                    '접속 횟수 평균': total_access_mean,
                    '1회이하 접속 비율': total_access_0_1_ratio,
                    '가입 기간 평균': period_data['가입 기간'].mean(),
                    # '24시간 내 탈퇴 비율': (period_data['가입 기간'] == 0).mean() * 100,
                    **{f'{k} 비율': v for k, v in reason_ratio.items()},
                    **{f'{a} 비율': b for a, b in business_type_ratio.items()},
                    **{f'{k} 비율': v for k, v in channel_ratio.items()},
                    **service_usage_stats
                }
            
                return pd.DataFrame([insights], index=[period]).round(2)
            
            def generate_all_insights(dataframe):
                unique_periods = dataframe['가입 구간'].unique()
                all_insights = [calculate_period_insights(dataframe, period) for period in unique_periods]
            
                final_df = pd.concat(all_insights)
            
                # 열 순서 지정
                reasons = [
                    '사용할 수 있는 서비스가 없어요. 비율', '개인정보 유출이 걱정돼요. 비율', '타 서비스보다 세금이 더 많이 나와요. 비율',
                    '자료 수집이 안돼요. 비율', '이용 요금이 비싸요. 비율', '직접 해야 하는 게 많아요. 비율', '문의 답변이 오래 걸려요. 비율', '직접 입력할게요. 비율'
                ]
                desired_order = [
                    '개수', '비율','가입 기간 평균'] + reasons + ['그 외 비율', '개인사업자 비율', 
                    '폐업 비율', '법인 비율', 
                    '접속 횟수 평균', '1회이하 접속 비율', 'SSEM 비율' , 'KKB 비율'
                ]
                desired_order = desired_order + [col for col in final_df.columns if col not in desired_order]
                final_df = final_df[desired_order]
                
                # 가입 구간 순서 지정
                order = ['0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
                final_df = final_df.reindex(order)
    
            
                return final_df
            
            # 사용 예시
            quit_period_summary = filtered.copy()
            all_insights_df3 = generate_all_insights(quit_period_summary)
            all_insights_df3.fillna(0, inplace=True)
    
            
            st.write("### 가입 기간별 세부 데이터")
            
            if st.checkbox('가입 기간별 요약 통계 보기', key='summary_stats_period'):
                st.dataframe(all_insights_df3)
            
            if st.checkbox('가입 기간별 데이터프레임 보기', key='detailed_data_period'):
                # 사용자가 가입 구간을 선택할 수 있는 선택 상자 생성
                periods_whole = filtered.copy()
                periods_options = ['전체'] + order
                selected_period = st.selectbox('가입 구간 선택:', options=periods_options, index=0, key='selectbox_period')
            
                # 선택된 가입 구간에 따라 데이터 필터링
                if selected_period == '전체':
                    filtered_view = periods_whole
                else:
                    filtered_view = periods_whole[periods_whole['가입 구간'] == selected_period]
            
                st.dataframe(filtered_view)     
    
    
#-------------------------------------------------------------------------------------------------
        
    if page == "접속횟수별":
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
                
                filtered = filtered.dropna(subset=['탈퇴사유'])
            
            
            else:
                filtered = data
    
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

            # 접속횟수별 탈퇴사유 비율
            filter_join= filtered[['총 접속 수', '탈퇴사유']].copy()
            bins = [1, 2, 5, 10, 20, float('inf')]
            labels = ["1", "2~5", "5~10", "10~20", "20 이상"]
            filter_join['접속 횟수 구간'] = pd.cut(filter_join['총 접속 수'], bins=bins, labels=labels, right=False)
            filter_join_access = filter_join.dropna(subset=['접속 횟수 구간'])
            filter_join_access['탈퇴사유'] = filter_join_access['탈퇴사유'].str.split(';')
            filter_join_access = filter_join_access.explode('탈퇴사유').dropna().reset_index(drop=True)
        
            total_counts = filter_join['접속 횟수 구간'].value_counts().reset_index()
            total_counts.columns = ['접속 횟수 구간', '개수']
            total_counts['전체 비율'] = (total_counts['개수'] / total_counts['개수'].sum() * 100).round(1)
        
            reason_counts = filter_join_access.groupby(['접속 횟수 구간', '탈퇴사유']).size().reset_index(name='count')
            total_reason_counts = reason_counts.groupby('접속 횟수 구간')['count'].sum().reset_index()
            reason_counts = reason_counts.merge(total_reason_counts, on='접속 횟수 구간', suffixes=('', '_total'))
            reason_counts['비율'] = (reason_counts['count'] / reason_counts['count_total'] * 100).round(1)
        
            final_counts = reason_counts.pivot_table(index='접속 횟수 구간', columns='탈퇴사유', values='비율', fill_value=0).reset_index()
            final_counts = final_counts.merge(total_counts[['접속 횟수 구간', '전체 비율', '개수']], on='접속 횟수 구간')
            final_counts_dataframe = final_counts.copy()
        
            order = ["1", "2~5", "5~10", "10~20", "20 이상"]
            final_counts['접속 횟수 구간'] = pd.Categorical(final_counts['접속 횟수 구간'], categories=order[::-1], ordered=True)
            final_counts_dataframe['접속 횟수 구간'] = pd.Categorical(final_counts_dataframe['접속 횟수 구간'], categories=order, ordered=True)
        
            final_counts = final_counts.sort_values('접속 횟수 구간').reset_index(drop=True)
            final_counts_dataframe = final_counts_dataframe.sort_values('접속 횟수 구간').reset_index(drop=True)
        
            for column in final_counts.columns:
                if column not in ['접속 횟수 구간', '개수', '전체 비율']:
                    final_counts[column] = (final_counts[column] * final_counts['전체 비율'] / 100).round(1)
        
            reasons = [
                '사용할 수 있는 서비스가 없어요.', '개인정보 유출이 걱정돼요.', '타 서비스보다 세금이 더 많이 나와요.',
                '자료 수집이 안돼요.', '이용 요금이 비싸요.', '직접 해야 하는 게 많아요.', '문의 답변이 오래 걸려요.', '직접 입력할게요.'
            ]
        
            final_counts = final_counts[['접속 횟수 구간', '개수', '전체 비율'] + reasons]
            final_counts_dataframe = final_counts_dataframe[['접속 횟수 구간', '개수', '전체 비율'] + reasons]
    
            
            st.write("### 접속횟수별 탈퇴 사유 비율")
        
            
            # 그래프 생성
            fig = px.bar(final_counts.melt(id_vars='접속 횟수 구간', value_vars=final_counts.columns[3:], var_name='탈퇴 사유', value_name='비율'),
                         y='접속 횟수 구간',
                         x='비율',
                         color='탈퇴 사유',
                         orientation='h',
                         height=600,
                         hover_data={'비율': ':.2f%'})
            
            fig.update_layout(barmode='stack',
                              xaxis_title='비율 (%)',
                              yaxis_title='접속 횟수 구간',
                              legend_title='탈퇴 사유')
            
            st.plotly_chart(fig)
            
            for col in final_counts_dataframe.columns:
                if final_counts_dataframe[col].dtype == 'float64':
                    final_counts_dataframe[col] = final_counts_dataframe[col].map("{:.1f}".format)
            
            # DataFrame 표시
            check11_key = "data_frame_view_11"
            check11 = st.checkbox('데이터프레임 보기', key=check11_key)
            if check11:
                st.table(final_counts_dataframe)
        
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)
            
            # -------------------------------------------------------------------------------------------------------------
            
                    
            # 접속 횟수 구간별 사용자 유형 비율
            filter_user = filtered[['총 접속 수', '사용자 유형']].copy()
            filter_user['접속 횟수 구간'] = pd.cut(filter_user['총 접속 수'], bins=bins, labels=labels, right=False)
            filter_user_type = filter_user.dropna(subset=['접속 횟수 구간'])
        
            total_counts_user = filter_user_type['접속 횟수 구간'].value_counts().reset_index()
            total_counts_user.columns = ['접속 횟수 구간', '개수']
            total_counts_user['전체 비율'] = (total_counts_user['개수'] / total_counts_user['개수'].sum() * 100).round(1)
        
            user_type_counts = filter_user_type.groupby(['접속 횟수 구간', '사용자 유형']).size().reset_index(name='count')
            total_user_type_counts = user_type_counts.groupby('접속 횟수 구간')['count'].sum().reset_index()
            user_type_counts = user_type_counts.merge(total_user_type_counts, on='접속 횟수 구간', suffixes=('', '_total'))
            user_type_counts['비율'] = (user_type_counts['count'] / user_type_counts['count_total'] * 100).round(1)
        
            final_user_type_counts = user_type_counts.pivot_table(index='접속 횟수 구간', columns='사용자 유형', values='비율', fill_value=0).reset_index()
            final_user_type_counts = final_user_type_counts.merge(total_counts_user[['접속 횟수 구간', '전체 비율', '개수']], on='접속 횟수 구간')
            final_user_type_counts_dataframe = final_user_type_counts.copy()
        
            for user_type in final_user_type_counts.columns[1:-2]:
                final_user_type_counts[user_type] = (final_user_type_counts[user_type] * final_user_type_counts['전체 비율'] / 100).round(1)
        
            final_user_type_counts['접속 횟수 구간'] = pd.Categorical(final_user_type_counts['접속 횟수 구간'], categories=order[::-1], ordered=True)
            final_user_type_counts_dataframe['접속 횟수 구간'] = pd.Categorical(final_user_type_counts_dataframe['접속 횟수 구간'], categories=order, ordered=True)
        
            final_user_type_counts = final_user_type_counts.sort_values('접속 횟수 구간').reset_index(drop=True)
            final_user_type_counts_dataframe = final_user_type_counts_dataframe.sort_values('접속 횟수 구간').reset_index(drop=True)
        
            user_types = ['그 외', '개인사업자', '법인', '폐업']
            final_user_type_counts = final_user_type_counts[['접속 횟수 구간', '개수', '전체 비율'] + user_types]
            final_user_type_counts_dataframe = final_user_type_counts_dataframe[['접속 횟수 구간', '개수', '전체 비율'] + user_types]
    
        
            
                    
           # 데이터프레임 표시
            st.write("### 접속횟수별 사용자 유형 비율")
            
            # 그래프 생성
            fig_user_type = px.bar(final_user_type_counts.melt(id_vars='접속 횟수 구간', value_vars=user_types, var_name='사용자 유형', value_name='비율'),
                                   y='접속 횟수 구간',
                                   x='비율',
                                   color='사용자 유형',
                                   orientation='h',
                                   height=600,
                                   hover_data={'비율': ':.2f%'})
            
            fig_user_type.update_layout(barmode='stack',
                                        xaxis_title='비율 (%)',
                                        yaxis_title='접속 횟수 구간',
                                        legend_title='사용자 유형')
            
            st.plotly_chart(fig_user_type)
            
            for col in final_user_type_counts_dataframe.columns:
                if final_user_type_counts_dataframe[col].dtype == 'float64':
                    final_user_type_counts_dataframe[col] = final_user_type_counts_dataframe[col].map("{:.1f}".format)
            
            # DataFrame 표시
            check12_key = "data_frame_view_12"
            check12 = st.checkbox('데이터프레임 보기', key=check12_key)
            if check12:
                st.table(final_user_type_counts_dataframe)
        
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)
            
            
            # -------------------------------------------------------------------------------------------------------------
            
            
            # 접속 횟수별 가입 구간 비율
            filter_access = filtered[['총 접속 수', '가입 구간']].copy()
            bins = [1, 2, 5, 10, 20, float('inf')]
            labels = ["1", "2~5", "5~10", "10~20", "20 이상"]
            filter_access['접속 횟수 구간'] = pd.cut(filter_access['총 접속 수'], bins=bins, labels=labels, right=False)
            filter_access_period = filter_access.dropna(subset=['접속 횟수 구간'])
            filter_access_period = filter_access_period.reset_index(drop=True)
            
            total_access_period_counts = filter_access['접속 횟수 구간'].value_counts().reset_index()
            total_access_period_counts.columns = ['접속 횟수 구간', '개수']
            
            access_period_counts = filter_access_period.groupby(['접속 횟수 구간', '가입 구간']).size().unstack(fill_value=0)
            access_period_counts = access_period_counts.div(access_period_counts.sum(axis=1), axis=0) * 100
            access_period_counts = access_period_counts.reset_index()
            
            total_access_period_counts = filter_access_period['접속 횟수 구간'].value_counts().reset_index()
            total_access_period_counts.columns = ['접속 횟수 구간', '개수']
            total_access_period_counts['전체 비율'] = (total_access_period_counts['개수'] / total_access_period_counts['개수'].sum() * 100).round(1)
            
            access_period_counts = access_period_counts.merge(total_access_period_counts[['접속 횟수 구간', '개수', '전체 비율']], on='접속 횟수 구간')
            access_period_counts_dataframe = access_period_counts.copy()
            
            order = ['0일', '30일 이내', '90일 이내', '180일 이내', '365일 이내', '365일 이상']
            
            for label in order:
                if label in access_period_counts.columns:
                    access_period_counts[label] = (access_period_counts[label] * access_period_counts['전체 비율'] / 100).round(1)
            
            # 원래 순서대로 접속 횟수 구간 정렬
            access_period_counts['접속 횟수 구간'] = pd.Categorical(access_period_counts['접속 횟수 구간'], categories=labels, ordered=True)
            access_period_counts_dataframe['접속 횟수 구간'] = pd.Categorical(access_period_counts_dataframe['접속 횟수 구간'], categories=labels, ordered=True)
            
            access_period_counts = access_period_counts.sort_values('접속 횟수 구간').reset_index(drop=True)
            access_period_counts_dataframe = access_period_counts_dataframe.sort_values('접속 횟수 구간').reset_index(drop=True)
            
            # 데이터프레임 순서 지정
            access_period_counts = access_period_counts[['접속 횟수 구간', '개수', '전체 비율'] + order]
            access_period_counts_dataframe = access_period_counts_dataframe[['접속 횟수 구간', '개수', '전체 비율'] + order]
            
            st.write("### 접속횟수별 가입구간 비율")
            fig_access_period = go.Figure()
            
            for period in order:
                if period in access_period_counts.columns:
                    fig_access_period.add_trace(go.Scatter(
                        x=access_period_counts['접속 횟수 구간'],
                        y=access_period_counts[period],
                        mode='lines+markers',
                        name=period
                    ))
            
            fig_access_period.update_layout(
                xaxis_title='접속 횟수 구간',
                yaxis_title='비율 (%)',
                legend_title='가입 구간',
                height=600
            )
            
            st.plotly_chart(fig_access_period)
            
            for col in access_period_counts_dataframe.columns:
                if access_period_counts_dataframe[col].dtype == 'float64':
                    access_period_counts_dataframe[col] = access_period_counts_dataframe[col].map("{:.1f}".format)
    
            
            check13_key = "data_frame_view_13"
            check13 = st.checkbox('데이터프레임 보기', key=check13_key)
            if check13:
                st.table(access_period_counts_dataframe)
    
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)
            
    
    # -------------------------------------------------------------------------------------------------------------
    
            # 접속횟수별 채널 비율
            channel_counts = filtered[['총 접속 수', '채널']].copy()
            channel_counts['접속 횟수 구간'] = pd.cut(channel_counts['총 접속 수'], bins=bins, labels=labels, right=False)
            filter_join_channel = channel_counts.dropna(subset=['접속 횟수 구간'])
            
            # 전체 카운트 및 비율 계산
            total_join_channel_counts = filter_join_channel['접속 횟수 구간'].value_counts().reset_index()
            total_join_channel_counts.columns = ['접속 횟수 구간', '개수']
            total_join_channel_counts['전체 비율'] = (total_join_channel_counts['개수'] / total_join_channel_counts['개수'].sum() * 100).round(1)
            
            # 채널별 비율 계산
            join_channel_counts = filter_join_channel.groupby(['접속 횟수 구간', '채널']).size().unstack(fill_value=0)
            join_channel_counts = join_channel_counts.div(join_channel_counts.sum(axis=1), axis=0) * 100
            join_channel_counts = join_channel_counts.reset_index()
            
            # 전체 비율 적용
            join_channel_counts = join_channel_counts.merge(total_join_channel_counts[['접속 횟수 구간', '개수', '전체 비율']], on='접속 횟수 구간')
            join_channel_counts_dataframe = join_channel_counts.copy()
            
            for label in channel_counts['채널'].unique():
                if label in join_channel_counts.columns:
                    join_channel_counts[label] = (join_channel_counts[label] * join_channel_counts['전체 비율'] / 100).round(1)
            
            final_join_channel_counts = join_channel_counts[['접속 횟수 구간', '개수', '전체 비율'] + [label for label in channel_counts['채널'].unique() if label in join_channel_counts.columns]]
            join_channel_counts_dataframe = join_channel_counts_dataframe[['접속 횟수 구간', '개수', '전체 비율'] + [label for label in channel_counts['채널'].unique() if label in join_channel_counts.columns]]
            
            final_join_channel_counts.columns = ['접속 횟수 구간', '개수', '전체 비율'] + [label for label in channel_counts['채널'].unique() if label in join_channel_counts.columns]
            join_channel_counts_dataframe.columns = ['접속 횟수 구간', '개수', '전체 비율'] + [label for label in channel_counts['채널'].unique() if label in join_channel_counts.columns]
            
            # 원래 순서대로 접속 횟수 구간 정렬
            final_join_channel_counts['접속 횟수 구간'] = pd.Categorical(final_join_channel_counts['접속 횟수 구간'], categories=labels[::-1], ordered=True)
            final_join_channel_counts = final_join_channel_counts.sort_values('접속 횟수 구간').reset_index(drop=True)
            join_channel_counts_dataframe['접속 횟수 구간'] = pd.Categorical(join_channel_counts_dataframe['접속 횟수 구간'], categories=labels, ordered=True)
            join_channel_counts_dataframe = join_channel_counts_dataframe.sort_values('접속 횟수 구간').reset_index(drop=True)
            
            st.write("### 접속횟수별 채널 비율")
            
            # 그래프 생성
            fig_channel = px.bar(final_join_channel_counts.melt(id_vars='접속 횟수 구간', value_vars=[label for label in channel_counts['채널'].unique() if label in join_channel_counts.columns], var_name='채널', value_name='비율'),
                                 y='접속 횟수 구간',
                                 x='비율',
                                 color='채널',
                                 orientation='h',
                                 height=600,
                                 hover_data={'비율': ':.2f%'})
            
            fig_channel.update_layout(barmode='stack',
                                      xaxis_title='비율 (%)',
                                      yaxis_title='접속 횟수 구간',
                                      legend_title='채널')
            
            st.plotly_chart(fig_channel)
            
            for col in join_channel_counts_dataframe.columns:
                if join_channel_counts_dataframe[col].dtype == 'float64':
                    join_channel_counts_dataframe[col] = join_channel_counts_dataframe[col].map("{:.1f}".format)
            
            check14_key = "data_frame_view_14"
            check14 = st.checkbox('데이터프레임 보기', key=check14_key)
            if check14:
                st.table(join_channel_counts_dataframe)
    
        
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)
            st.text("""
            """)
    
    # -------------------------------------------------------------------------------------------------------------
            
            # 접속 횟수 구간 추가
            filtered['접속 횟수 구간'] = pd.cut(filtered['총 접속 수'], bins=[1, 2, 5, 10, 20, float('inf')], labels=["1", "2~5", "5~10", "10~20", "20 이상"], right=False)
            
            # 요약 통계 함수 정의
            def calculate_access_insights(dataframe, access):
                """Calculate insights for a specific access range from a dataframe."""
                access_data = dataframe[dataframe['접속 횟수 구간'] == access]
                total_count = dataframe.shape[0]
                access_count = access_data.shape[0]
                
                type_ratio = (access_count / total_count) * 100
                total_access_mean = access_data['총 접속 수'].mean()
                # total_access_0_1_ratio = (access_data['총 접속 수'] <= 1).mean() * 100
            
                service_columns = [
                    '부가세 결제 수', '부가세 결제 취소 수', '부가세 계산 시작 수', '부가세 계산 완료 수',
                    '종소세 결제 수', '종소세 결제 취소 수', '종소세 계산 시작 수', '종소세 계산 완료 수',
                    '인건비 결제 수', '인건비 결제 취소 수', '매출알림 서비스 이용 여부', '매출알림 서비스 탈퇴 여부',
                    '안심신고 이용 여부', '재가입 여부'
                ]
            
                service_usage_stats = {}
                for column in service_columns:
                    if access_data[column].dtype == 'object':
                        service_usage_stats[f"{column} 비율"] = (access_data[column] == 'Y').mean() * 100
                    else:
                        service_usage_stats[f"{column} 평균"] = access_data[column].mean()
                        
                # 탈퇴 사유 비율 계산
                reasons = [
                    '사용할 수 있는 서비스가 없어요.', '개인정보 유출이 걱정돼요.', '타 서비스보다 세금이 더 많이 나와요.',
                    '자료 수집이 안돼요.', '이용 요금이 비싸요.', '직접 해야 하는 게 많아요.', '문의 답변이 오래 걸려요.', '직접 입력할게요.'
                ]
                reason_counts = access_data['탈퇴사유'].dropna().apply(lambda x: [r for r in reasons if r in x])
                reason_flattened = [item for sublist in reason_counts for item in sublist]
                reason_ratio = pd.Series(reason_flattened).value_counts(normalize=True) * 100
                reason_ratio = reason_ratio.to_dict()
                 
                business_type_ratio = access_data['사용자 유형'].value_counts(normalize=True) * 100
                channel_ratio = access_data['채널'].value_counts(normalize=True) * 100
                
                insights = {
                    '개수': access_count,
                    '비율': type_ratio,
                    '접속 횟수 평균': total_access_mean,
                    # '1회이하 접속 비율': total_access_0_1_ratio,
                    '가입 기간 평균': access_data['가입 기간'].mean(),
                    '24시간 내 탈퇴 비율': (access_data['가입 기간'] == 0).mean() * 100,
                    **{f'{k} 비율': v for k, v in reason_ratio.items()},
                    **{f'{a} 비율': b for a, b in business_type_ratio.items()},
                    **{f'{k} 비율': v for k, v in channel_ratio.items()},
                    **service_usage_stats
                }
            
                return pd.DataFrame([insights], index=[access]).round(2)
            
            def generate_all_insights(dataframe):
                unique_accesses = dataframe['접속 횟수 구간'].unique()
                all_insights = [calculate_access_insights(dataframe, access) for access in unique_accesses]
            
                final_df = pd.concat(all_insights)
            
                # 열 순서 지정
                reasons = [
                    '사용할 수 있는 서비스가 없어요. 비율', '개인정보 유출이 걱정돼요. 비율', '타 서비스보다 세금이 더 많이 나와요. 비율',
                    '자료 수집이 안돼요. 비율', '이용 요금이 비싸요. 비율', '직접 해야 하는 게 많아요. 비율', '문의 답변이 오래 걸려요. 비율', '직접 입력할게요. 비율'
                ]
                desired_order = [
                    '개수', '비율','접속 횟수 평균'] + reasons + ['그 외 비율', '개인사업자 비율', 
                    '폐업 비율', '법인 비율', 
                    '가입 기간 평균', '24시간 내 탈퇴 비율', 'SSEM 비율' , 'KKB 비율'
                ]
                desired_order = desired_order + [col for col in final_df.columns if col not in desired_order]
                final_df = final_df[desired_order]
                
                # 접속 횟수 구간 순서 지정
                labels = ["1", "2~5", "5~10", "10~20", "20 이상"]
                final_df = final_df.reindex(labels)
            
                return final_df
            
            # 사용 예시
            quit_access_summary = filtered.copy()
            all_insights_df3 = generate_all_insights(quit_access_summary)
            all_insights_df3.fillna(0, inplace=True)
            
            st.write("### 접속 횟수별 세부 데이터")
            
            if st.checkbox('접속 횟수별 요약 통계 보기', key='summary_stats_access'):
                st.dataframe(all_insights_df3)
            
            if st.checkbox('접속 횟수별 데이터프레임 보기', key='detailed_data_access'):
                # 사용자가 접속 횟수 구간을 선택할 수 있는 선택 상자 생성
                accesses_whole = filtered.copy()
                accesses_options = ['전체'] + labels
                selected_access = st.selectbox('접속 횟수 구간 선택:', options=accesses_options, index=0, key='selectbox_access')
            
                # 선택된 접속 횟수 구간에 따라 데이터 필터링
                if selected_access == '전체':
                    filtered_view = accesses_whole
                else:
                    filtered_view = accesses_whole[accesses_whole['접속 횟수 구간'] == selected_access]
            
                st.dataframe(filtered_view)
    
    
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
    
