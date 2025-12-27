import streamlit as st
import joblib
import pandas as pd

# =============================
# LOAD MODEL
# =============================
model = joblib.load('stroke_model.pkl')

# =============================
# KONFIGURASI HALAMAN
# =============================
st.set_page_config(
    page_title="Stroke Risk Prediction",
    layout="centered"
)

st.title("🧠 Aplikasi Prediksi Risiko Stroke")
st.write("Masukkan data pasien untuk mengetahui risiko stroke.")

# =============================
# SIDEBAR INPUT
# =============================
st.sidebar.header("Data Pasien")

gender = st.sidebar.radio("Jenis Kelamin", ["Perempuan", "Laki-laki"])
gender = 1 if gender == "Laki-laki" else 0

age = st.sidebar.slider("Usia", 1, 100, 30)

hypertension = st.sidebar.selectbox("Hipertensi", ["Tidak", "Ya"])
hypertension = 1 if hypertension == "Ya" else 0

heart_disease = st.sidebar.selectbox("Penyakit Jantung", ["Tidak", "Ya"])
heart_disease = 1 if heart_disease == "Ya" else 0

ever_married = st.sidebar.selectbox("Pernah Menikah", ["Tidak", "Ya"])
ever_married = 1 if ever_married == "Ya" else 0

work_type = st.sidebar.selectbox(
    "Jenis Pekerjaan",
    ["Pemerintah", "Swasta", "Wiraswasta", "Anak-anak", "Tidak Pernah Bekerja"]
)

work_type_map = {
    "Pemerintah": 0,
    "Tidak Pernah Bekerja": 1,
    "Swasta": 2,
    "Wiraswasta": 3,
    "Anak-anak": 4
}
work_type = work_type_map[work_type]

residence = st.sidebar.selectbox("Tipe Tempat Tinggal", ["Perkotaan", "Pedesaan"])
residence = 0 if residence == "Perkotaan" else 1

avg_glucose = st.sidebar.number_input(
    "Rata-rata Kadar Glukosa", 50.0, 300.0, 100.0
)

bmi = st.sidebar.number_input(
    "BMI (Body Mass Index)", 10.0, 60.0, 22.0
)

smoking = st.sidebar.selectbox(
    "Status Merokok",
    ["Tidak Diketahui", "Tidak Pernah", "Mantan Perokok", "Perokok Aktif"]
)

smoking_map = {
    "Tidak Diketahui": 4,
    "Mantan Perokok": 1,
    "Tidak Pernah": 2,
    "Perokok Aktif": 3
}
smoking = smoking_map[smoking]

# =============================
# DATAFRAME INPUT
# =============================
input_data = pd.DataFrame({
    "gender": [gender],
    "age": [age],
    "hypertension": [hypertension],
    "heart_disease": [heart_disease],
    "ever_married": [ever_married],
    "work_type": [work_type],
    "Residence_type": [residence],
    "avg_glucose_level": [avg_glucose],
    "bmi": [bmi],
    "smoking_status": [smoking]
})
reverse_work_map = {v: k for k, v in work_type_map.items()}
reverse_smoking_map = {v: k for k, v in smoking_map.items()}

st.subheader("Ringkasan Data Pasien")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Jenis Kelamin** : {'Laki-laki' if gender == 1 else 'Perempuan'}")
    st.write(f"**Usia** : {age} tahun")
    st.write(f"**Hipertensi** : {'Ya' if hypertension == 1 else 'Tidak'}")
    st.write(f"**Penyakit Jantung** : {'Ya' if heart_disease == 1 else 'Tidak'}")
    st.write(f"**Pernah Menikah** : {'Ya' if ever_married == 1 else 'Tidak'}")
    

with col2:
    st.write(f"**Jenis Pekerjaan** : {list(work_type_map.keys())[list(work_type_map.values()).index(work_type)]}")
    st.write(f"**Tempat Tinggal** : {'Perkotaan' if residence == 0 else 'Pedesaan'}")
    st.write(f"**Kadar Glukosa** : {avg_glucose}")
    st.write(f"**BMI** : {bmi}")
    st.write(f"**Status Merokok** : {list(smoking_map.keys())[list(smoking_map.values()).index(smoking)]}")

# =============================
# PREDIKSI
# =============================
if st.button("🔍 Prediksi Risiko Stroke"):
    hasil = model.predict(input_data)[0]

    st.subheader("Hasil Prediksi")
    if hasil == 1:
        st.error("⚠️ Pasien **berisiko terkena stroke**")
    else:
        st.success("✅ Pasien **tidak berisiko terkena stroke**")
