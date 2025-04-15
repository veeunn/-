import streamlit as st
import pandas as pd
from datetime import datetime

# 신청자 명단 불러오기 (이니셜, 사이즈 포함)
try:
    applied_df = pd.read_csv("applied_list.csv", dtype=str)
except FileNotFoundError:
    st.error("⚠️ 신청자 명단 파일(applied_list.csv)을 찾을 수 없습니다.")
    st.stop()

st.title("📦 과잠 무인 배부 체크 시스템")

st.markdown("""
1️⃣ 본인의 **이름**과 **학번**을 입력하고<br>
2️⃣ 출력되는 이니셜과 사이즈 정보를 확인한 후<br>
3️⃣ **✅ 수령 완료 체크** 버튼을 눌러주세요.
""", unsafe_allow_html=True)

name = st.text_input("이름")
student_id = st.text_input("학번")

def normalize(text):
    return str(text).strip().lower().replace(" ", "")

if name and student_id:
    norm_name = normalize(name)
    norm_id = normalize(student_id)

    applied_df["이름_정제"] = applied_df["이름"].apply(normalize)
    applied_df["학번_정제"] = applied_df["학번"].apply(normalize)

    matched = applied_df[
        (applied_df["이름_정제"] == norm_name) &
        (applied_df["학번_정제"] == norm_id)
    ]

    if not matched.empty:
        row = matched.iloc[0]
        st.success(f"\U0001f4dd [{row['이름']}]님의 과잠 정보")
        st.write(f"- 🪡 **이니셜 각인**: {row['이니셜 각인']}")
        st.write(f"- 📐 **과잠 사이즈**: {row['과잠 사이즈']}")
        st.write("**⬇️ 수령 완료 체크** 버튼 꼭! 눌러주세요.")

        if st.button("✅ 수령 완료 체크"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_data = pd.DataFrame([[now, student_id.strip(), name.strip()]], columns=["시간", "학번", "이름"])

            try:
                df = pd.read_csv("log.csv")
                df = pd.concat([df, new_data], ignore_index=True)
            except FileNotFoundError:
                df = new_data

            df.to_csv("log.csv", index=False)
            st.success("\U0001f389 수령 체크가 완료되었습니다!")
    else:
        st.error("❌ 신청자 명단에 없는 이름/학번입니다. 오탈자 여부를 확인해주세요. 또는 학생회 카카오톡 채널로 문의해주세요.")
else:
    st.info("💬 문의는 카카오톡 채널 <중앙대학교 국제물류학과 학생회>로 연락바랍니다.")

# 관리자용 log 다운로드
with st.expander("📁 수령 명단 파일 다운로드 (관리자 전용)"):
    pw = st.text_input("비밀번호를 입력하세요", type="password")

    if pw == "0531":
        try:
            log_df = pd.read_csv("log.csv")
            csv = log_df.to_csv(index=False).encode("utf-8-sig")
            st.download_button("\U0001f4e5 log.csv 다운로드", csv, "log.csv", "text/csv")
        except FileNotFoundError:
            st.warning("아직 저장된 기록이 없습니다.")
    elif pw != "":
        st.error("비밀번호가 틀렸습니다.")
