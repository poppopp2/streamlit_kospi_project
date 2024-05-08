import streamlit as st
from corr import corr
from prediction import prediction


def main():
    st.markdown('출처 : https://ecos.bok.or.kr/#/ ')
    choice=st.sidebar.selectbox('옵션', options=['상관계수','코스피 가격 예측'])

    if choice== '상관계수':

        corr()

    if choice=='코스피 가격 예측':
        prediction()

if __name__=='__main__':
    main()