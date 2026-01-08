import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import base64

st.set_page_config(layout="wide", page_title="Dashboard Capaian SPM")

# styling
st.markdown("""
<style>
    /* Paksa Background Putih */
    .stweb-triwulan { 
        background-color: #FFFFFF;
    }
    
    [data-testid="stSidebar"] { 
        background-color: #f8f9fa; 
        border-right: 1px solid #e0e0e0; 
    }
    
    /* Judul Indikator */
    .indicator-title {
        font-size: 18px;
        font-weight: 800;
        color: #2c3e50;
        margin-top: 10px;
        margin-bottom: 5px;
        padding-left: 12px;
        border-left: 6px solid #3498db;
    }
    
    /* Sub-judul Total */
    .total-stat {
        font-size: 14px;
        color: #7f8c8d;
        margin-bottom: 15px;
        padding-left: 15px;
        font-weight: 600;
    }
    
    /* Scrollbar Halus */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #f1f1f1; }
    ::-webkit-scrollbar-thumb { background: #c1c1c1; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #a8a8a8; }
</style>
""", unsafe_allow_html=True)

# load data 
def load_data(df_raw):
    try:
        expected_cols = [
            'No', 'Indikator',
            'Sasaran_SMT1', 'Capaian_SMT1',
            'Sasaran_SMT2', 'Capaian_SMT2',
            'Sasaran_SMT3', 'Capaian_SMT3',
            'Sasaran_SMT4', 'Capaian_SMT4'
        ]
        
        num_cols = df_raw.shape[1]
        
        if num_cols < 10:
            df_raw.columns = expected_cols[:num_cols]
            for i in range(num_cols, 10):
                df_raw[expected_cols[i]] = 0
            df = df_raw
        else:
            df = df_raw.iloc[:, :10]
            df.columns = expected_cols

        df = df.dropna(subset=['Indikator'])
        df = df[df['Indikator'].astype(str).str.len() > 3]

        cols_numeric = [c for c in expected_cols if 'Sasaran' in c or 'Capaian' in c]
        for col in cols_numeric:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        return df
        
    except Exception as e:
        st.error(f"Gagal memproses data: {e}")
        return None

# logo
def tampilkan_logo_tengah(file_path, lebar=150):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        html_code = f"""
            <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                <img src="data:image/png;base64,{bin_str}" width="{lebar}px">
            </div>
        """
        st.markdown(html_code, unsafe_allow_html=True)
    except FileNotFoundError:
        pass

# header 
tampilkan_logo_tengah("logo.png", lebar=100) 

st.markdown("""
    <div style='text-align: center;'>
        <h2 style='color: #333333; margin-bottom: 0;'>DINAS KESEHATAN KAB. KLATEN</h2>
        <h4 style='color: #555555;'>Monitoring Capaian SPM</h4>
    </div>
    <hr>
""", unsafe_allow_html=True)

# side bar
with st.sidebar:
    st.header("📂 Upload Data")
    uploaded_file = st.file_uploader("Upload File Excel/CSV", type=["xlsx", "csv"])
    
    df_loaded = None
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.xlsx'):
                xls = pd.ExcelFile(uploaded_file)
                selected_sheet = st.selectbox("Pilih Sheet:", xls.sheet_names)
                df_raw = pd.read_excel(xls, sheet_name=selected_sheet, skiprows=4, header=None)
            else:
                try:
                    df_raw = pd.read_csv(uploaded_file, skiprows=4, header=None, encoding='utf-8')
                except:
                    uploaded_file.seek(0)
                    df_raw = pd.read_csv(uploaded_file, skiprows=4, header=None, encoding='latin1')
            
            df_loaded = load_data(df_raw)
            
        except Exception as e:
            st.error(f"Error file: {e}")

# main
if df_loaded is not None:    
    col_filter1, col_filter2 = st.columns([2,3])
    with col_filter1:
        pilihan_tampilan = st.selectbox(
            "Pilih Data yang Ditampilkan:",
            ["Jumlah Sasaran", "Jumlah Capaian"]
        )
        prefix = "Sasaran" if pilihan_tampilan == "Jumlah Sasaran" else "Capaian"

    st.markdown("<br>", unsafe_allow_html=True)

    # data proses
    data_all_trend = []
    for i in range(1, 5): 
        col_name = f'{prefix}_SMT{i}'
        temp = df_loaded[['Indikator', col_name]].copy()
        temp.columns = ['Indikator', 'Jumlah']
        temp['Semester_Int'] = i 
        temp['Semester_Label'] = f'SMT {i}'
        data_all_trend.append(temp)
    
    df_trend_final = pd.concat(data_all_trend)
    unique_indicators = df_loaded['Indikator'].unique()
    
    # Set Seaborn Style
    sns.set_theme(style="whitegrid") 

    with st.container(height=850, border=True):
        
        for indikator in unique_indicators:
            df_subset = df_trend_final[df_trend_final['Indikator'] == indikator].sort_values('Semester_Int')
            total_val = df_subset['Jumlah'].sum()

            # Header Indikator
            st.markdown(f'<div class="indicator-title">{indikator}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="total-stat">Total 2026: <b>{int(total_val):,}</b></div>', unsafe_allow_html=True)
            
            # Layout Kolom
            col_line, col_donut = st.columns([7, 3])
            
            # line chart
            with col_line:
                fig, ax = plt.subplots(figsize=(8, 4), facecolor='white')
                fig.subplots_adjust(bottom=0.15, top=0.9) 
                
                sns.lineplot(
                    data=df_subset,
                    x='Semester_Label',
                    y='Jumlah',
                    marker='o',
                    markersize=9,
                    linewidth=2.5,
                    color='#2980b9',
                    ax=ax
                )

                y_max = df_subset['Jumlah'].max()
                offset = y_max * 0.08 if y_max > 0 else 1
                
                for x, y in zip(range(len(df_subset)), df_subset['Jumlah']):
                    val_label = int(y)
                    if val_label > 0:
                        ax.text(x, y + offset, f"{val_label:,}", 
                                ha='center', va='bottom', fontsize=10, fontweight='bold', color='#333') 
                ax.set_xlabel("")
                ax.set_ylabel("Jumlah", fontsize=9, color='#555')
                ax.tick_params(axis='x', colors='#333')
                ax.tick_params(axis='y', colors='#333')
                
                if y_max > 0:
                    ax.set_ylim(bottom=0, top=y_max * 1.35) 
                
                sns.despine()
                st.pyplot(fig, use_container_width=True)

            # donut chart 
            with col_donut:
                fig_donut, ax_donut = plt.subplots(figsize=(4, 6), facecolor='white')
                
                fig_donut.subplots_adjust(bottom=0.3, top=0.95)
                
                if total_val > 0:
                    colors = sns.color_palette("pastel")[0:4]
                    
                    def make_autopct(pct):
                        return f'{pct:.0f}%' if pct > 3 else ''

                    wedges, texts, autotexts = ax_donut.pie(
                        df_subset['Jumlah'],
                        labels=None, # Matikan label text di lingkaran (sumber masalah nabrak)
                        autopct=make_autopct,
                        startangle=90,
                        colors=colors,
                        pctdistance=0.8,
                        wedgeprops=dict(width=0.45, edgecolor='white')
                    )
                    
                    plt.setp(autotexts, size=9, weight="bold", color="white")
                    
                    ax_donut.legend(
                        wedges, 
                        df_subset['Semester_Label'], 
                        title="Periode",
                        loc="upper center",      
                        bbox_to_anchor=(0.5, -0.05), 
                        ncol=2,                  
                        frameon=False,
                        fontsize=9
                    )
                    
                    # Teks Tengah
                    ax_donut.text(0, 0, "Proporsi", ha='center', va='center', fontsize=10, color='#95a5a6')
                    
                else:
                    ax_donut.text(0.5, 0.5, "0 Data", ha='center', va='center', color='#999')
                    ax_donut.axis('off')

                st.pyplot(fig_donut, use_container_width=True)
            
            # Garis Pemisah
            st.markdown("<hr style='border-top: 1px dashed #bbb; margin: 10px 0;'>", unsafe_allow_html=True)

else:
    if uploaded_file is None:
        st.info("👋 Silakan upload file Excel di sidebar.")
    else:
        st.warning("Mohon pilih sheet yang benar.")