import sys
sys.path.append("src")  # إجبار بايثون على رؤية مجلد الكود

import streamlit as st
import tempfile
from pathlib import Path
import json

# استيراد أدواتنا القوية
from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown

# إعداد عنوان الصفحة
st.set_page_config(page_title="CSV Profiler", page_icon="📊")
st.title("📊 CSV Profiler Dashboard")
st.write("Upload a CSV file to generate a full quality report.")

# 1. زر رفع الملف
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Streamlit يعطينا الملف في الذاكرة، لكن دالة القراءة عندنا تتوقع "مسار ملف"
        # لذلك سنحفظه مؤقتاً في ملف وهمي لنقرأه
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = Path(tmp.name)

        # 2. القراءة والتحليل (باستخدام كودك القديم!)
        with st.spinner('Analyzing data...'):
            rows = read_csv_rows(tmp_path)
            report = profile_rows(rows)
            markdown_text = render_markdown(report)

        # 3. عرض النتائج
        # نستخدم Tabs للترتيب
        tab1, tab2 = st.tabs(["📄 Report (Markdown)", "⚙️ Raw Data (JSON)"])
        
        with tab1:
            st.markdown(markdown_text)
            
            # زر لتحميل التقرير
            st.download_button(
                label="Download Report as MD",
                data=markdown_text,
                file_name="report.md",
                mime="text/markdown"
            )

        with tab2:
            st.json(report)
            
        # تنظيف الملف المؤقت
        tmp_path.unlink()

    except Exception as e:
        st.error(f"Error processing file: {e}")