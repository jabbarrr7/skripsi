import streamlit as st
import numpy as np
import pandas as pd
from genetic_algorithm import GeneticScheduler

st.title("Optimasi Penjadwalan dengan Algoritma Genetika")

# Input jumlah kelas, guru, ruangan, dan slot waktu
num_classes = st.number_input("Jumlah Kelas", min_value=1, value=5)
num_teachers = st.number_input("Jumlah Guru", min_value=1, value=3)
num_rooms = st.number_input("Jumlah Ruangan", min_value=1, value=3)
num_timeslots = st.number_input("Jumlah Slot Waktu", min_value=1, value=5)

# Jalankan Algoritma Genetika
if st.button("Jalankan Optimasi"):
    scheduler = GeneticScheduler(num_classes, num_teachers, num_rooms, num_timeslots)
    best_schedule = scheduler.evolve()

    df_schedule = pd.DataFrame({
        "Kelas": [f"Kelas {i+1}" for i in range(num_classes)],
        "Slot Waktu": best_schedule
    })

    st.write("### Jadwal Optimal:")
    st.dataframe(df_schedule)
