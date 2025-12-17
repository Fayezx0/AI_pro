# import sys
# sys.path.append("src")  # إجبار بايثون على رؤية مجلد الكود

# import streamlit as st
# import tempfile
# from pathlib import Path
# import json

# # استيراد أدواتنا القوية
# from csv_profiler.io import read_csv_rows
# from csv_profiler.profiling import profile_rows
# from csv_profiler.render import render_markdown

# # إعداد عنوان الصفحة
# st.set_page_config(page_title="CSV Profiler", page_icon="📊")
# st.title("📊 Fayez's CSV Profiler Dashboard")
# st.write("Upload a CSV file to generate a the report.")

# # 1. زر رفع الملف
# uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# if uploaded_file is not None:
#     try:
#         # Streamlit يعطينا الملف في الذاكرة، لكن دالة القراءة عندنا تتوقع "مسار ملف"
#         # لذلك سنحفظه مؤقتاً في ملف وهمي لنقرأه
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
#             tmp.write(uploaded_file.getvalue())
#             tmp_path = Path(tmp.name)

#         # 2. القراءة والتحليل (باستخدام كودك القديم!)
#         with st.spinner('Analyzing data...'):
#             rows = read_csv_rows(tmp_path)
#             report = profile_rows(rows)
#             markdown_text = render_markdown(report)

#         # 3. عرض النتائج
#         # نستخدم Tabs للترتيب
#         tab1, tab2 = st.tabs(["📄 Report (Markdown)", "⚙️ Raw Data (JSON)"])
        
#         with tab1:
#             st.markdown(markdown_text)
            
#             # زر لتحميل التقرير
#             st.download_button(
#                 label="Download Report as MD",
#                 data=markdown_text,
#                 file_name="report.md",
#                 mime="text/markdown"
#             )

#         with tab2:
#             st.json(report)
            
#         # تنظيف الملف المؤقت
#         tmp_path.unlink()

#     except Exception as e:
#         st.error(f"Error processing file: {e}")


import sys
sys.path.append("src")  # إصلاح مسار الاستيراد

import streamlit as st
import tempfile
import json
from pathlib import Path

# استيراد أدواتنا
from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown

# إعداد الصفحة
st.set_page_config(page_title="CSV Profiler", page_icon="📊", layout="wide")

st.title("📊 CSV Profiler Dashboard")
st.caption("Upload a CSV → Generate Report → Export JSON + Markdown")

# القائمة الجانبية للمدخلات
with st.sidebar:
    st.header("Inputs")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    report_name = st.text_input("Report Name", value="report")

# المنطق الرئيسي
if uploaded_file is not None:
    try:
        # 1. حفظ الملف مؤقتاً وقراءته (عملية سريعة)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = Path(tmp.name)
        
        # قراءة الصفوف فقط
        rows = read_csv_rows(tmp_path)
        
        # عرض معلومات سريعة عن الملف
        st.info(f"File loaded successfully: {len(rows)} rows found.")
        
        # 2. زر التشغيل (هنا وضعت الكود الذي سألت عنه)
        if st.button("Generate Report 🚀"):
            with st.spinner('Analyzing data...'):
                report = profile_rows(rows)
                st.session_state["report"] = report  # حفظ في الذاكرة
                st.success("Analysis Complete!")

        # 3. عرض النتائج (إذا كانت موجودة في الذاكرة)
        if "report" in st.session_state:
            report = st.session_state["report"]
            markdown_text = render_markdown(report)
            json_text = json.dumps(report, indent=2, ensure_ascii=False)

            # تقسيم الشاشة: التقرير + البيانات الخام
            tab1, tab2 = st.tabs(["📄 Report (Markdown)", "⚙️ Raw Data (JSON)"])
            
            with tab1:
                st.markdown(markdown_text)
            
            with tab2:
                st.json(report)

            # 4. خيارات التصدير (مطلوب في Day 4)
            st.divider()
            st.subheader("Export Results")
            
            col1, col2, col3 = st.columns(3)
            
            # زر تحميل Markdown
            col1.download_button(
                "⬇️ Download MD", 
                data=markdown_text, 
                file_name=f"{report_name}.md", 
                mime="text/markdown"
            )
            
            # زر تحميل JSON
            col2.download_button(
                "⬇️ Download JSON", 
                data=json_text, 
                file_name=f"{report_name}.json", 
                mime="application/json"
            )
            
            # زر الحفظ في مجلد المشروع (مطلب أساسي للمحاضر)
            if col3.button("💾 Save to 'outputs/'"):
                out_dir = Path("outputs")
                out_dir.mkdir(parents=True, exist_ok=True)
                (out_dir / f"{report_name}.json").write_text(json_text, encoding="utf-8")
                (out_dir / f"{report_name}.md").write_text(markdown_text, encoding="utf-8")
                st.toast(f"Saved to outputs/{report_name}!", icon="✅")

        # تنظيف الملف المؤقت
        tmp_path.unlink()

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("👈 Please upload a CSV file from the sidebar to start.")