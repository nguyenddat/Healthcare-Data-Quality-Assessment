# gen_chamber.py
import random
import numpy as np
import pandas as pd
from generated_data.constants import CHAMBER_NAMES
from generated_data.config import ROW_COUNTS
from generated_data.factory import inject_null, export_csv, preview

N_ROWS = ROW_COUNTS["tb_chamber"]

prefixes = ["Buồng", "Phòng", "Khu", "Hậu phẫu", "Hồi sức", "Cách ly"]
suffixes = ["A", "B", "C", "D", "01", "02", "03", "101", "102", "103", "201", "202", "301", "302", "401", "402", "501", "502"]

def generate_chamber_name():
    if random.random() < 0.7:
        return random.choice(CHAMBER_NAMES)
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

def generate_tb_chamber(ctx):
    tb_chamber = pd.DataFrame({
        "chamberid": np.arange(1, N_ROWS + 1),
        "chambername": [generate_chamber_name() for _ in range(N_ROWS)]
    })
    tb_chamber = inject_null(tb_chamber, "chambername", 0.03)
    preview(tb_chamber, "tb_chamber")
    export_csv(tb_chamber, "tb_chamber")
    ctx.add("tb_chamber", tb_chamber)
    return tb_chamber