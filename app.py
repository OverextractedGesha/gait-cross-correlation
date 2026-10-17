import os
import streamlit as st
import matplotlib.pyplot as plt

# ==============================================================================
# SECTION 1: CORE ENGINE (PURE PYTHON - TANPA LIBRARY KALKULASI MATEMATIKA)
# ==============================================================================

def load_signal(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [float(line.strip()) for line in f if line.strip()]

def compute_cross_correlation(x, y):
    n = len(x)
    rxy = []
    for l in range(n):
        sigma = sum(a * b for a, b in zip(x[l:], y))
        rxy.append(sigma)
    return rxy

def compute_normalization(rxy, n):
    sample = n - 1
    norm = []
    for l in range(sample):
        denom = sample - l
        norm.append(rxy[l] / denom if denom != 0 else 0.0)
    return norm

def shift_signal(y, lag):
    n = len(y)
    return [0.0 if i < lag else y[i - lag] for i in range(n)]

def find_peaks(data, min_val, min_distance=100):
    peaks = []
    for i in range(1, len(data) - 1):
        if data[i] > data[i - 1] and data[i] > data[i + 1] and data[i] >= min_val:
            if not peaks or (i - peaks[-1][0] >= min_distance):
                peaks.append((i, data[i]))
            elif data[i] > peaks[-1][1]:
                peaks[-1] = (i, data[i])
    peaks.sort(key=lambda item: item[1], reverse=True)
    return peaks

def get_inspection_table(x, y, rxy, center_lag, window=5):
    start = max(0, center_lag - window)
    end = min(len(rxy), center_lag + window + 1)
    rows = []
    for i in range(start, end):
        rows.append({
            "Lag (L)": i,
            "x[L]": round(x[i], 3) if i < len(x) else "-",
            "y[L]": round(y[i], 3) if i < len(y) else "-",
            "rxy[L]": round(rxy[i], 3)
        })
    return rows


# ==============================================================================
# SECTION 2: STREAMLIT GUI & VISUALIZATION
# ==============================================================================

st.set_page_config(
    page_title="Biomodeling - Cross Correlation Gait Analysis",
    page_icon="🚶",
    layout="wide"
)

@st.cache_data
def process_data(heel_path, toe_path):
    x = load_signal(heel_path)
    y = load_signal(toe_path)
    n = len(x)
    rxy = compute_cross_correlation(x, y)
    norm = compute_normalization(rxy, n)
    rxy_peaks = find_peaks(rxy, min_val=1000.0)
    norm_peaks = find_peaks(norm, min_val=0.1)
    return x, y, n, rxy, norm, rxy_peaks, norm_peaks

HEEL_FILE = "Heel123.txt"
TOE_FILE = "Toe123.txt"

if not os.path.exists(HEEL_FILE) or not os.path.exists(TOE_FILE):
    st.error(f"File '{HEEL_FILE}' atau '{TOE_FILE}' tidak ditemukan di direktori saat ini.")
    st.stop()

x, y, n, rxy, norm, rxy_peaks, norm_peaks = process_data(HEEL_FILE, TOE_FILE)

st.title("🚶 Gait Signal Cross-Correlation Analysis")
st.caption("Implementasi Pure Python Berdasarkan Modul Ajar Biomodeling ITS")

# Sidebar
st.sidebar.header("Kontrol Time-Lag")

if "slider_lag" not in st.session_state:
    st.session_state["slider_lag"] = 0

def set_lag(val):
    st.session_state["slider_lag"] = val

b1, b2, b3 = st.sidebar.columns(3)
b1.button("Lag 0", on_click=set_lag, args=(0,))
b2.button("Peak 1 (716)", on_click=set_lag, args=(716,))
b3.button("Peak 2 (1740)", on_click=set_lag, args=(1740,))

lag = st.sidebar.slider(
    "Pilih Time-Lag (L):",
    min_value=0,
    max_value=n - 1,
    step=1,
    key="slider_lag"
)

st.sidebar.markdown("---")
st.sidebar.subheader("Puncak Cross-Korelasi")
for rank, (p_lag, p_val) in enumerate(rxy_peaks[:3], 1):
    st.sidebar.write(f"**Puncak {rank}:** Lag `{p_lag}` | Rxy = `{p_val:.3f}`")

# Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Panjang Sampel (N)", f"{n}")
m2.metric("Lag Aktif (L)", f"{lag}")
m3.metric("Rxy[L]", f"{rxy[lag]:.3f}")
m4.metric("Norm[L]", f"{norm[lag]:.4f}" if lag < len(norm) else "-")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Sinyal Gait (Shifted)",
    "Grafik Cross-Correlation (Rxy)",
    "Grafik Normalisasi (ρxy)",
    "Tabel Inspeksi Data"
])

with tab1:
    st.subheader("Visualisasi Sinyal Gait & Penjajaran Sinyal")
    y_shifted = shift_signal(y, lag)

    fig1, ax1 = plt.subplots(figsize=(12, 4.2))
    ax1.plot(x, color="red", linewidth=1.1, label="Heel (x)")
    ax1.plot(y_shifted, color="green", linewidth=1.1, label=f"Toe (y) [Shifted {lag}]")
    ax1.set_title("Gait Signal", fontsize=12)
    ax1.set_xlabel("Sample Number", fontsize=10)
    ax1.set_ylabel("Amplitudo", fontsize=10)
    ax1.set_xlim(0, n)
    ax1.set_ylim(-0.2, 2.6)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper right")
    st.pyplot(fig1)
    plt.close(fig1)

    if lag in [716, 1740]:
        st.success(f"Kedua sinyal saling berhimpit pada time-lag ke-{lag}.")

with tab2:
    st.subheader("Fungsi Cross-Correlation Rxy(l)")
    fig2, ax2 = plt.subplots(figsize=(12, 4.2))
    ax2.plot(rxy, color="red", linewidth=1.1, label="Rxy")
    ax2.axvline(x=lag, color="blue", linestyle=":", label=f"Lag Dipilih ({lag})")
    for p_lag, p_val in rxy_peaks[:3]:
        ax2.scatter(p_lag, p_val, color="blue", s=25, zorder=5)
        ax2.annotate(f"L={p_lag}\n{p_val:.1f}", (p_lag, p_val), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8)
    ax2.set_title("Cross Correlation", fontsize=12)
    ax2.set_xlabel("Index Time Lag (L)", fontsize=10)
    ax2.set_ylabel("Rxy Value", fontsize=10)
    ax2.set_xlim(0, n)
    ax2.set_ylim(0, 2600)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="upper right")
    st.pyplot(fig2)
    plt.close(fig2)

with tab3:
    st.subheader("Fungsi Normalisasi Cross-Correlation ρxy(l)")
    fig3, ax3 = plt.subplots(figsize=(12, 4.2))
    ax3.plot(norm, color="red", linewidth=1.1, label="Norm")
    ax3.axvline(x=lag, color="blue", linestyle=":", label=f"Lag Dipilih ({lag})")
    ax3.set_title("Normalization", fontsize=12)
    ax3.set_xlabel("Index Time Lag (L)", fontsize=10)
    ax3.set_ylabel("Rxy Normalization", fontsize=10)
    ax3.set_xlim(0, n)
    ax3.set_ylim(0, 0.45)
    ax3.grid(True, linestyle="--", alpha=0.5)
    ax3.legend(loc="upper right")
    st.pyplot(fig3)
    plt.close(fig3)

with tab4:
    st.subheader(f"Inspeksi Nilai di Sekitar Lag {lag}")
    table_rows = get_inspection_table(x, y, rxy, lag, window=5)
    st.dataframe(table_rows, width=1000)
