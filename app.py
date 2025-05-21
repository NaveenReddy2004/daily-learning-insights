import streamlit as st
from generate_insight import create_daily_insight

st.title("📚 Student Learning Insights")

student_id = st.text_input("Enter your Student ID:", "")

if st.button("Get Today's Insight"):
    if not student_id.isdigit():
        st.error("Please enter a valid numeric Student ID.")
    else:
        with st.spinner("Generating your insight..."):
            result = create_daily_insight(int(student_id))
        if result:
            st.markdown(f"### Topic: {result['topic']}")
            st.write(result["insight"])
            st.markdown(f"[Learn More]({result['link']})")
        else:
            st.warning("No interests found for this Student ID.")
