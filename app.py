import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import pandas as pd

# Fungsi untuk mengevaluasi ekspresi yang dimasukkan oleh pengguna
def evaluate_function(expr, t_val):
    t = sp.symbols('t')
    try:
        return float(expr.subs(t, t_val))
    except Exception as e:
        raise ValueError(f"Error evaluating function at t={t_val}: {e}")

# Fungsi untuk menghitung integral menggunakan aturan trapesium
def trapezoidal_rule(f, a, b, h):
    n = int((b - a) / h)  # Jumlah subinterval
    t_values = np.linspace(a, b, n + 1)  # Titik pembagi
    y_values = [evaluate_function(f, t) for t in t_values]  # Evaluasi fungsi pada titik-titik tersebut

    # Aturan trapesium
    integral_approx = (h / 2) * (y_values[0] + 2 * np.sum(y_values[1:-1]) + y_values[-1])
    return integral_approx, t_values, y_values

# Fungsi untuk menghitung nilai integral analitik berdasarkan ekspresi pengguna
def compute_analytical_integral(expr, a, b):
    t = sp.symbols('t')
    integral_expr = sp.integrate(expr, (t, a, b))
    return float(integral_expr)

# Plotting Function
def plot_trapezoidal(t_vals, y_vals, a, b, h, expr):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t_vals, y_vals, 'b-', label=f'Laju Alir (F(t)) = {sp.pretty(expr)}')

    # Menggambar trapezoid
    for i in range(len(t_vals)-1):
        xs = [t_vals[i], t_vals[i], t_vals[i+1], t_vals[i+1]]
        ys = [0, y_vals[i], y_vals[i+1], 0]
        ax.fill(xs, ys, edgecolor='r', alpha=0.2)

    ax.set_title('Grafik Laju Alir vs Waktu dengan Aturan Trapesium', fontsize=14)
    ax.set_xlabel('Waktu (t) [detik]', fontsize=12)
    ax.set_ylabel('Laju Alir F(t) [m³/detik]', fontsize=12)
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    return fig

# Fungsi untuk mengonversi Matplotlib Figure ke format PNG untuk diunduh
def fig_to_image(fig):
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

# Antarmuka Pengguna dengan Streamlit
def main():
    st.set_page_config(
        page_title="Sistem Bantu Keputusan Pengelolaan Air Irigasi",
        layout="wide",
        page_icon="app_logo.png"  # Mengganti favicon dengan app_logo.png
    )

    # Membuat header dengan dua kolom: logo aplikasi dan logo UIGM
    header_col1, header_col2, header_col3 = st.columns([1, 6, 1])
    with header_col1:
        try:
            st.image("app_logo.png", width=100)
        except Exception:
            st.warning("Logo aplikasi tidak ditemukan. Pastikan file 'app_logo.png' berada di direktori yang sama.")
    with header_col2:
        st.empty()  # Placeholder untuk tengah
    with header_col3:
        try:
            st.image("logo_uigm.png", width=200)  # Memperbesar logo UIGM
        except Exception:
            st.warning("Logo UIGM tidak ditemukan. Pastikan file 'logo_uigm.png' berada di direktori yang sama.")

    st.markdown("---")

    st.title("Sistem Bantu Keputusan Pengelolaan Air Irigasi")
    st.markdown("### Berbasis Metode Trapesium Integral Analisis Numerik")

    st.markdown("---")

    # Menampilkan Nama Tim di bawah header
    st.markdown("### Tim Pengembang")
    st.markdown("""
    - **Agung Pratama**
    - **M.U.Fido Millano**
    - **Yeni**
    - **Ajeng Kusumaning Dewi**
    - **Alfina Elsa Putri**
    """)

    # Menggunakan HTML untuk mengatur ukuran teks "Masukan Data"
    st.markdown("<h4 style='font-size:20px;'>Masukan Data</h4>", unsafe_allow_html=True)

    # Fungsi Input
    func_str = st.text_input(
        "Fungsi Laju Alir Air (F(t))",
        value="2*t**2 + 4*t + 6",
        help="Contoh: 2*t**2 + 4*t + 6"
    )

    # Bounds Input
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Waktu Mulai (a) [detik]", value=0.0, step=0.1)
    with col2:
        b = st.number_input("Waktu Akhir (b) [detik]", value=10.0, step=0.1)

    # Step Size Input
    h = st.number_input("Ukuran Langkah (h) [detik]", value=0.1, step=0.01, min_value=0.01)

    # Kebutuhan Air
    water_need = st.number_input("Kebutuhan Air (m³)", value=500.0, step=10.0, min_value=0.0)

    # Preset Examples
    presets = [
        "Custom",
        "F(t) = 20 (Konstan)",
        "F(t) = 3*t + 2",
        "F(t) = sin(t)",
        "F(t) = exp(t)"
    ]
    preset = st.selectbox("Preset Contoh", presets)

    if preset != "Custom":
        if preset == "F(t) = 20 (Konstan)":
            func_str = "20"
            a = 0.0
            b = 10.0
            h = 0.1
        elif preset == "F(t) = 3*t + 2":
            func_str = "3*t + 2"
            a = 0.0
            b = 10.0
            h = 0.1
        elif preset == "F(t) = sin(t)":
            func_str = "sin(t)"
            a = 0.0
            b = 6.2832  # 2π
            h = 0.1
        elif preset == "F(t) = exp(t)":
            func_str = "exp(t)"
            a = 0.0
            b = 2.0
            h = 0.1

    if st.button("Hitung Volume"):
        try:
            if h <= 0:
                st.error("Ukuran langkah (h) harus positif.")
                return
            if a >= b:
                st.error("Waktu mulai (a) harus kurang dari waktu akhir (b).")
                return
            if water_need < 0:
                st.error("Kebutuhan air tidak boleh bernilai negatif.")
                return

            # Parse fungsi menggunakan SymPy
            t = sp.symbols('t')
            func_expr = sp.sympify(func_str)

            # Validasi apakah fungsi dapat diintegrasikan secara analitik
            try:
                integral_exact = compute_analytical_integral(func_expr, a, b)
            except Exception:
                integral_exact = None

            # Hitung integral dengan metode trapesium
            volume_approx, t_vals, y_vals = trapezoidal_rule(func_expr, a, b, h)

            # Penghitungan error (jika integral analitik tersedia)
            if integral_exact is not None:
                error = abs(volume_approx - integral_exact) / abs(integral_exact) * 100
                error_str = f"{error:.2f}%"
            else:
                error_str = "Tidak dapat dihitung (integral analitik tidak tersedia)"

            # Sistem Bantu Keputusan (Sederhana)
            if volume_approx >= water_need:
                dss_decision = "Kebutuhan air terpenuhi"
                decision_color = "green"
            else:
                dss_decision = "Kebutuhan air belum terpenuhi"
                decision_color = "red"

            # Mengelompokkan hasil perhitungan dalam tabel
            result_data = {
                "Deskripsi": [
                    "Volume Air (Metode Trapesium)",
                    "Integral Analitik",
                    "Error Relatif",
                    "Kebutuhan Air",
                    "Hasil Keputusan"
                ],
                "Nilai": [
                    f"{volume_approx:.4f} m³",
                    f"{integral_exact:.4f} m³" if integral_exact is not None else "Tidak tersedia",
                    error_str,
                    f"{water_need:.2f} m³",
                    dss_decision
                ]
            }

            result_df = pd.DataFrame(result_data)

            # Fungsi untuk mewarnai hasil keputusan
            def color_decision(val):
                color = 'green' if val == "Kebutuhan air terpenuhi" else 'red'
                return f'color: {color}'

            st.markdown("### Hasil Perhitungan")
            st.dataframe(result_df.style.applymap(color_decision, subset=["Nilai"]))

            # Plot grafik
            fig = plot_trapezoidal(t_vals, y_vals, a, b, h, func_expr)
            st.pyplot(fig)

            # Unduh Plot
            st.download_button(
                label="Unduh Plot",
                data=fig_to_image(fig),
                file_name="plot_trapezoidal.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

    st.markdown("---")

    # Formulir Komentar menggunakan FormSubmit
    st.markdown("### Kirim Komentar")
    st.markdown("""
    <form action="https://formsubmit.co/catfunny604@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <div style="margin-bottom: 10px;">
            <label for="name">Nama:</label><br>
            <input type="text" id="name" name="name" required style="width: 100%;">
        </div>
        <div style="margin-bottom: 10px;">
            <label for="email">Email:</label><br>
            <input type="email" id="email" name="email" required style="width: 100%;">
        </div>
        <div style="margin-bottom: 10px;">
            <label for="message">Komentar:</label><br>
            <textarea id="message" name="message" rows="4" required style="width: 100%;"></textarea>
        </div>
        <button type="submit" style="background-color:#4CAF50; color:white; padding:10px 20px; border:none; cursor:pointer;">Kirim</button>
    </form>
    """, unsafe_allow_html=True)

    st.markdown("---")

if __name__ == "__main__":
    main()
