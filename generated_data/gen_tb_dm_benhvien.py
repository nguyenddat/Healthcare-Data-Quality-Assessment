import random
import numpy as np
import pandas as pd

from generated_data.config import ROW_COUNTS
from generated_data.constants import HOSPITAL_NAMES
from generated_data.factory import sequential_ids, inject_null, export_csv, preview

N_ROWS = ROW_COUNTS["tb_dm_benhvien"]

hospital_names = random.sample(HOSPITAL_NAMES, min(N_ROWS, len(HOSPITAL_NAMES)))
while len(hospital_names) < N_ROWS:
    hospital_names.append(f"{random.choice(HOSPITAL_NAMES)} Cơ sở {len(hospital_names)-len(HOSPITAL_NAMES)+2}")

hospital_levels = ["Tuyến trung ương", "Tuyến tỉnh", "Tuyến huyện", "Tuyến xã", "Chưa phân tuyến"]
hospital_level_weights = [0.15, 0.35, 0.30, 0.10, 0.10]

def generate_tb_dm_benhvien(ctx):
    hospital_names = random.sample(HOSPITAL_NAMES, min(N_ROWS, len(HOSPITAL_NAMES)))

    while len(hospital_names) < N_ROWS:
        hospital_names.append(
            f"{random.choice(HOSPITAL_NAMES)} Cơ sở {len(hospital_names) - len(HOSPITAL_NAMES) + 2}")

    tb_dm_benhvien = pd.DataFrame({
        "dm_benhviendbid": sequential_ids(N_ROWS),
        "dm_benhvienkcbbd": [
            f"{random.randint(10000, 99999)}"
            for _ in range(N_ROWS)
        ],
        "dm_benhvienname": hospital_names,
        "dm_benhvientuyen": np.random.choice(
            hospital_levels,
            size=N_ROWS,
            p=hospital_level_weights,
        ),
        "dm_benhviendisable": np.random.choice(
            [0, 1],
            size=N_ROWS,
            p=[0.97, 0.03],
        ),
    })
    inject_null(tb_dm_benhvien, "dm_benhvienkcbbd", 0.01)
    inject_null(tb_dm_benhvien, "dm_benhvienname", 0.01)
    inject_null(tb_dm_benhvien, "dm_benhvientuyen", 0.01)

    preview(tb_dm_benhvien, "tb_dm_benhvien")
    export_csv(tb_dm_benhvien, "tb_dm_benhvien.csv")
    return tb_dm_benhvien