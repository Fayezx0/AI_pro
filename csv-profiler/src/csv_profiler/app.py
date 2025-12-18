import sys
sys.path.append("src")

import streamlit as st
import tempfile
import json
import httpx           # مكتبة التعامل مع الروابط
import io              # مكتبة لتحويل البيانات إلى ملفات وهمية
from pathlib import Path

# استيراد أدواتنا
from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown

# إعداد الصفحة
st.set_page_config(page_title="CSV Profiler", page_icon="📊", layout="wide")
st.title("📊 CSV Profiler Dashboard")
st.caption("Upload a CSV or Paste a URL → Generate Report → Export Results")

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.header("Data Source")
    
    # خيار التبديل بين الرفع والرابط
    input_method = st.radio("Choose source:", ["Upload File", "From URL"])
    
    uploaded_file = None
    
    if input_method == "Upload File":
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    else: # إذا اختار الرابط
        url = st.text_input("CSV URL", placeholder="https://raw.githubusercontent.com/.../data.csv")
        if url:
            if st.button("Fetch Data 🌐"):
                try:
                    with st.spinner("Downloading..."):
                        # جلب البيانات
                        response = httpx.get(url, timeout=10.0)
                        response.raise_for_status()
                        
                        # التعديل المهم هنا: نستخدم BytesIO و content
                        # لكي يصبح الملف القادم من الرابط مطابقاً للملف المرفوع
                        uploaded_file = io.BytesIO(response.content)
                        st.success("Data fetched successfully!")
                        
                except Exception as e:
                    st.error(f"Failed to load URL: {e}")

# --- المنطق الرئيسي ---
# ملاحظة: uploaded_file الآن قد يأتي من الرفع أو من الرابط، الكود لا يفرق بينهما
if uploaded_file is not None:
    try:
        # 1. حفظ الملف مؤقتاً وقراءته
        # seek(0) مهمة لضمان قراءة الملف من بدايته
        uploaded_file.seek(0)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = Path(tmp.name)
        
        # 2. قراءة الصفوف
        rows = read_csv_rows(tmp_path)
        
        # 3. التحقق من صحة الملف (التحذيرات المطلوبة)
        if not rows:
            st.error("❌ The CSV file is empty!")
            st.stop()
            
        if len(rows) > 0 and len(rows[0]) == 0:
            st.warning("⚠️ CSV file detected, but no columns found (check delimiter)!")

        # 4. معلومات سريعة
        st.info(f"File loaded successfully: {len(rows)} rows found.")
        
        # 5. زر التشغيل
        if st.button("Generate Report 🚀"):
            with st.spinner('Analyzing data...'):
                report = profile_rows(rows)
                st.session_state["report"] = report
                st.toast("Analysis Complete!", icon="✅")

        # 6. عرض النتائج
        if "report" in st.session_state:
            report = st.session_state["report"]
            markdown_text = render_markdown(report)
            json_text = json.dumps(report, indent=2, ensure_ascii=False)

            tab1, tab2 = st.tabs(["📄 Report (Markdown)", "⚙️ Raw Data (JSON)"])
            
            with tab1:
                st.markdown(markdown_text)
            
            with tab2:
                st.json(report)

            # 7. خيارات التصدير
            st.divider()
            st.subheader("Export Results")
            
            # نحدد اسم التقرير الافتراضي
            report_name = st.sidebar.text_input("Report Name for Export", value="report")
            
            col1, col2, col3 = st.columns(3)
            
            col1.download_button(
                "⬇️ Download MD", 
                data=markdown_text, 
                file_name=f"{report_name}.md", 
                mime="text/markdown"
            )
            
            col2.download_button(
                "⬇️ Download JSON", 
                data=json_text, 
                file_name=f"{report_name}.json", 
                mime="application/json"
            )
            
            if col3.button("💾 Save to 'outputs/'"):
                out_dir = Path("outputs")
                out_dir.mkdir(parents=True, exist_ok=True)
                (out_dir / f"{report_name}.json").write_text(json_text, encoding="utf-8")
                (out_dir / f"{report_name}.md").write_text(markdown_text, encoding="utf-8")
                st.toast(f"Saved to outputs/{report_name}!", icon="💾")

        # تنظيف الملف المؤقت
        tmp_path.unlink()

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    # رسالة الترحيب في البداية
    st.info("👈 Please upload a CSV file or paste a URL from the sidebar to start.")