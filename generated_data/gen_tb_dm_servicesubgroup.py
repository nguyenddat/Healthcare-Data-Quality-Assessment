import random
import numpy as np
import pandas as pd

from generated_data.config import ROW_COUNTS
from generated_data.factory import sequential_ids, inject_null, export_csv, preview

N_ROWS = ROW_COUNTS.get("tb_dm_servicesubgroup", random.randint(120, 160))

def generate_tb_dm_servicesubgroup(ctx):
    tb_dm_servicesubgroup = pd.DataFrame({
        "dm_servicesubgroupdbid": sequential_ids(N_ROWS),
        "dm_servicesubgroupid": np.random.choice(
            np.arange(301, 700), size=N_ROWS, replace=False),
        "isthuocungthuphache": np.random.choice(
            [0, 1], size=N_ROWS, p=[0.92, 0.08])})

    tb_dm_servicesubgroup = inject_null(
        tb_dm_servicesubgroup, "dm_servicesubgroupid", 0.01)

    preview(tb_dm_servicesubgroup, "tb_dm_servicesubgroup")
    export_csv(tb_dm_servicesubgroup, "tb_dm_servicesubgroup")

    ctx.add("tb_dm_servicesubgroup", tb_dm_servicesubgroup)

    return tb_dm_servicesubgroup