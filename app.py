import streamlit as st
import pandas as pd
from datetime import datetime

# 신청자 명단 불러오기
try:
    applied_df = pd.read_csv("applied_list.csv")
except FileNotFoundError:
    st.error("❗ 신청자 명단 파일(applied_list.csv)을 찾을 수 없습니다.")
    st.stop()

st.title("📦 과잠 무인 배부 체크 시스템")

st.write("본인의 **학번**과 **이름**을 입력하고, 아래 버튼을 눌러주세요.")

name = st.text_input("이름")
student_id = st.text_input("학번")

def normalize(text):
    return str(text).strip().lower().replace(" ", "")

if st.button("✅ 수령 완료 체크"):
    if name and student_id:
        # 입력값 전처리 (공백 제거 + 소문자 통일)
        norm_name = normalize(name)
        norm_id = normalize(student_id)

        applied_df["이름_정제"] = applied_df["이름"].apply(normalize)
        applied_df["학번_정제"] = applied_df["학번"].astype(str).apply(normalize)

        matched = applied_df[
            (applied_df["이름_정제"] == norm_name) &
            (applied_df["학번_정제"] == norm_id)
        ]

        if not matched.empty:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_data = pd.DataFrame([[now, student_id.strip(), name.strip()]], columns=["시간", "학번", "이름"])

            try:
                df = pd.read_csv("log.csv")
                df = pd.concat([df, new_data], ignore_index=True)
            except FileNotFoundError:
                df = new_data

            df.to_csv("log.csv", index=False)
            st.success("수령 체크 완료되었습니다. 감사합니다!")
        else:
            st.error("❌ 신청자 명단에 없습니다. 이름/학번을 다시 확인해주세요. 또는 학생회 카카오톡 채널로 문의 부탁드립니다.")
    else:
        st.warning("이름과 학번을 모두 입력해주세요.")

# 관리자용 log.csv 다운로드 (비밀번호 필요)
with st.expander("📁 수령 명단 파일 다운로드 (관리자 전용)"):
    pw = st.text_input("비밀번호를 입력하세요", type="password")
    
    if pw == "0531":
        try:
            log_df = pd.read_csv("log.csv")
            csv = log_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 log.csv 다운로드", csv, "log.csv", "text/csv")
        except FileNotFoundError:
            st.warning("아직 저장된 기록이 없습니다.")
    elif pw != "":
        st.error("비밀번호가 틀렸습니다.")


