import streamlit as st
import pandas as pd
import numpy as np
import joblib
def prediction():
    st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQUcwUt7Xa8Q9NClbgWyApDRvzvXL_sEEpoLg&usqp=CAU', use_column_width=True)


    st.title('파일을 업로드해서 금일 코스피 가격을 예측합니다!')
    st.markdown("<h3 style='color: red;'>※주의 : 과거 수치를 기반으로 예측한 것이기 때문에 참고만 해주시길 바랍니다.※</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #8C8C8C;'>100대 통계지표를 다운받아 주세요.</h3>", unsafe_allow_html=True)
    st.markdown("[100대 통계지표 사이트](https://ecos.bok.or.kr/#/StatisticsByTheme/KoreanStat100)")
    st.image("통계지표2.png", caption='Optional caption')

    # 첫 번째 파일 업로더
    file1 = st.file_uploader("100대 통계 지표를 업로드하세요..", type=["xlsx"])
    # 두 번째 파일 업로더 
    st.markdown("<h3 style='color: #8C8C8C;'>코스피 데이터를 다운받아 주세요.</h3>", unsafe_allow_html=True)
    st.markdown("[kospi, 통계 사이트](https://ecos.bok.or.kr/#/Short/79bcee)")
    st.image("일일코스피1.png", caption='Optional caption')
    st.image("일일코스피2.png", caption='Optional caption')
    file2 = st.file_uploader("주식시장(일) 파일을 업로드하세요.", type=["csv"])
    p=0

    if file1 is not None and file2 is not None:
        p=p+1
        # 엑셀 파일을 데이터프레임으로 읽기
        df1 = pd.read_excel(file1)
        # CSV 파일을 데이터프레임으로 읽기
        df2 = pd.read_csv(file2)
        # 데이터프레임 인덱스 설정
        df1 = df1.set_index('100대통계명')
        df2 = df2.set_index('계정항목')

        # 첫 번째 데이터프레임에서 필요한 열 선택 및 NaN 값 처리
        x1 = df1.loc[['한국은행 기준금리','금','원/달러 환율(종가)','원/엔(100엔) 환율(매매기준율)','원/유로 환율(매매기준율)','실업률','소비자물가지수'],'ECOS값']
        # 두 번째 데이터프레임에서 필요한 행 선택 및 ',' 제거 및 숫자형 변환
        y = df2.iloc[[2,3,6],-1]
        y = y.str.replace(',', '').astype(float)
        # 모델 입력 데이터 준비
        test = np.concatenate([x1.values, y.values])
        test2 = test.reshape(1,-1)
        # 모델 로드 및 예측
        regressor = joblib.load('regressor2.pkl')
        y_pred = regressor.predict(test2)

        # 결과 출력
        y2=df2.iloc[0,-1]
        y2=np.array(y2)
        y_pred= np.round(y_pred, decimals=2)
        y_pred2 = [f'{num:,.2f}' for num in y_pred]
        y_pred3=y_pred2[0]
        y_pred4=y_pred[0]
        y4=np.vectorize(lambda x: float(x.replace(',', '')))(y2)

        if y_pred4 > y4 :
            st.markdown(f'코스피 예측 가격은 :red[{y_pred3}]원 입니다.')
            st.markdown(f'금일 코스피 가격은 :blue[{y2}]원 입니다.')
            st.info('코스피 가격이 예측 가격보다 낮습니다. :blue[저평가] 되고 있습니다.')
        elif y_pred <y4 :
            st.markdown(f'코스피 예측 가격은 :blue[{y_pred3}]원 입니다.')
            st.markdown(f'금일 코스피 가격은 :red[{y2}]원 입니다.')
            st.error('코스피 가격이 예측 가격보다 높습니다. :red[고평가] 되고 있습니다.')
            

    st.header('지표 수치를 조정하여 가격을 예측합니다.')
    df=pd.read_csv('지표10.csv')
    df.set_index(df.columns[0], inplace=True)
    df.index.name = None
    df=df.drop(columns=['kospi'])
    #st.dataframe(df[::-1].head())
    col=df.columns
    # 사용자 지정 숫자로 모델 예측
    X = []
    if p==0:
        for i in col:
            input_val = st.text_input(i + '의 가격을 입력하세요' )
            if input_val.strip():  # 빈 문자열이 아닌 경우에만 추가
                X.append(float(input_val))  # 입력된 값을 실수로 변환하여 추가
    elif p==1:
        for i,k in zip(col,test):
            input_val = st.text_input(i + '의 수치을 입력하세요' ,help=(f'금일의 {i} 수치는 "{k}" 입니다' ) ,)
            if input_val.strip():  # 빈 문자열이 아닌 경우에만 추가
                X.append(float(input_val))  # 입력된 값을 실수로 변환하여 추가
    
    if st.button('예측하기'):
        regressor=joblib.load('regressor2.pkl')
        X=np.array(X).reshape(1,-1)
        y_pred=regressor.predict(X)
        y_pred=y_pred[0]
        y_pred=round(y_pred)
        y_pred=format(y_pred,',')
        st.success(f'코스피 예측 가격은 :blue[{y_pred}]원 입니다.' )
            





    

