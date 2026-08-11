# gen_treatment.py

import pandas as pd

from generated_data.config import ROW_COUNTS
from generated_data.factory import (
    sequential_ids,
    sample_fk,
    random_datetime,
    random_datetime_after,
    inject_null,
    preview,
    export_csv,
)

N_ROWS = ROW_COUNTS["tb_treatment"]

def generate_tb_treatment(ctx):
    medicalrecord_ids = ctx.ids("tb_medicalrecord", "medicalrecordid",)

    n_rows = max(len(medicalrecord_ids) * 3, N_ROWS,)

    treatment_ids = sequential_ids(n_rows)

    treatment_date = [random_datetime("2024-01-01", "2025-12-31",)
        for _ in range(n_rows)]

    do_treatment_date = [
        random_datetime_after(dt, 0, 2,)
        for dt in treatment_date
    ]

    end_treatment_date = [
        random_datetime_after(dt, 1, 10,)
        for dt in do_treatment_date
    ]

    tb_treatment = pd.DataFrame({
        "treatmentid": treatment_ids,
        "medicalrecordid": sample_fk(
            medicalrecord_ids,
            size=n_rows,
        ),
        "treatmentcode": [
            f"DT{str(i).zfill(8)}"
            for i in treatment_ids
        ],
        "treatmentdate": treatment_date,
        "do_treatmentdate": do_treatment_date,
        "end_treatmentdate": end_treatment_date,
    })

    tb_treatment = inject_null(tb_treatment, "treatmentcode", 0.01)
    tb_treatment = inject_null(tb_treatment, "end_treatmentdate", 0.03,)

    preview(tb_treatment, "tb_treatment")
    export_csv(tb_treatment, "tb_treatment")

    ctx.add("tb_treatment", tb_treatment)

    return tb_treatment