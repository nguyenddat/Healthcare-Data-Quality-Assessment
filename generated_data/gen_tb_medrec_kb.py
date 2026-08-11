import pandas as pd

from generated_data.constants import CARE_LEVELS
from generated_data.config import ROW_COUNTS
from generated_data.factory import (
    sequential_ids,
    random_datetime,
    random_choice,
    inject_null,
    preview,
    export_csv,
)

N_ROWS = ROW_COUNTS["tb_medicalrecord_khambenh"]


def generate_tb_medicalrecord_khambenh(ctx):
    medicalrecord_ids = ctx.ids(
        "tb_medicalrecord",
        "medicalrecordid",
    )

    n_rows = min(N_ROWS, len(medicalrecord_ids))

    tb_medicalrecord_khambenh = pd.DataFrame({
        "medicalrecord_khambenhid": sequential_ids(n_rows),
        "medicalrecordid": medicalrecord_ids[:n_rows],
        "chedochamsoc": random_choice(
            CARE_LEVELS,
            n_rows,
        ),
        "ngaynhap": random_datetime(
            "2023-01-01",
            "2025-12-31",
            n_rows,
        ),
    })

    tb_medicalrecord_khambenh = inject_null(
        tb_medicalrecord_khambenh, "chedochamsoc", 0.05,)

    tb_medicalrecord_khambenh = inject_null(tb_medicalrecord_khambenh, "medicalrecordid", 0.01,)

    preview(tb_medicalrecord_khambenh, "tb_medicalrecord_khambenh",)

    export_csv(tb_medicalrecord_khambenh, "tb_medicalrecord_khambenh",)

    ctx.add("tb_medicalrecord_khambenh", tb_medicalrecord_khambenh,)
    return tb_medicalrecord_khambenh