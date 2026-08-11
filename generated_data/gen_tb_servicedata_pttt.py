# gen_servicedata_pttt.py

import numpy as np
import pandas as pd

from generated_data.config import ROW_COUNTS
from generated_data.factory import (
    sequential_ids,
    sample_fk,
    random_datetime,
    export_csv,
    preview,
)

N_ROWS = ROW_COUNTS["tb_servicedata_pttt"]

def generate_tb_servicedata_pttt(ctx):
    medicalrecord_ids = ctx.ids(
        "tb_medicalrecord", "medicalrecordid",
    )

    treatment_ids = ctx.ids("tb_treatment", "treatmentid")

    tb_servicedata_pttt = pd.DataFrame({"servicedata_ptttid": sequential_ids(N_ROWS),
        "medicalrecordid": sample_fk(medicalrecord_ids, size=N_ROWS,),
        "ngaypttt": [
            random_datetime("2024-01-01", "2026-06-30")
            for _ in range(N_ROWS)
        ],
        "do_treatmentid": sample_fk(treatment_ids, size=N_ROWS,),
    })

    preview(tb_servicedata_pttt, "tb_servicedata_pttt")

    export_csv(tb_servicedata_pttt, "tb_servicedata_pttt")

    ctx.add("tb_servicedata_pttt", tb_servicedata_pttt,)

    return tb_servicedata_pttt