# gen_department.py
import random
import numpy as np
import pandas as pd

from generated_data.config import ROW_COUNTS
from generated_data.constants import DEPARTMENT_NAMES
from generated_data.factory import export_csv, inject_null, preview, sequential_ids

N_ROWS = min(ROW_COUNTS["tb_department"], len(DEPARTMENT_NAMES))


def generate_tb_department(ctx):
    department_names = DEPARTMENT_NAMES.copy()
    random.shuffle(department_names)

    tb_department = pd.DataFrame({
        "departmentid": sequential_ids(N_ROWS),
        "departmentname": department_names[:N_ROWS],
        "departmentdisable": np.random.choice(
            [0, 1],
            size=N_ROWS,
            p=[0.95, 0.05]
        )
    })

    tb_department = inject_null(tb_department, "departmentname", 0.02)

    preview(tb_department, "tb_department")
    export_csv(tb_department, "tb_department")

    ctx.add("tb_department", tb_department)
    return tb_department