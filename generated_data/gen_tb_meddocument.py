import numpy as np
import pandas as pd

from generated_data.config import ROW_COUNTS
from generated_data.constants import DOCUMENT_TYPES, SIGN_ROLES, SIGN_STATUSES
from generated_data.factory import (
    sequential_ids,
    sample_fk,
    random_datetime,
    random_datetime_after,
    inject_null,
    export_csv,
    preview,
)

N_ROWS = ROW_COUNTS["tb_mediboxdocument"]


def generate_tb_mediboxdocument(ctx):
    patientrecord_ids = ctx.ids("tb_medicalrecord", "patientrecordid")

    tb_mediboxdocument = pd.DataFrame({
        "mediboxdocumentid": sequential_ids(N_ROWS),
        "patientrecordid": sample_fk(
            patientrecord_ids,
            size=N_ROWS,
        ),
        "sochuky_init": np.random.choice([1, 2, 3, 4], size=N_ROWS,
            p=[0.20, 0.40, 0.30, 0.10],),
        "sochuky_daky": 0,
        "mediboxdocumentname": np.random.choice(DOCUMENT_TYPES,size=N_ROWS,),
        "ngaytao": [
            random_datetime(
                "2024-01-01",
                "2025-12-31",
            )
            for _ in range(N_ROWS)
        ],
        "isremove": np.random.choice(
            [0, 1],
            size=N_ROWS,
            p=[0.98, 0.02],
        ),
    })

    tb_mediboxdocument["sochuky_daky"] = [
        np.random.randint(0, x + 1)
        for x in tb_mediboxdocument["sochuky_init"]
    ]

    tb_mediboxdocument = inject_null(
        tb_mediboxdocument,
        "mediboxdocumentname",
        0.01,
    )
    preview(tb_mediboxdocument, "tb_mediboxdocument")
    export_csv(tb_mediboxdocument, "tb_mediboxdocument")
    ctx.add("tb_mediboxdocument", tb_mediboxdocument)
    return tb_mediboxdocument


def generate_tb_mediboxdocument_sign(ctx):
    documents = ctx.get("tb_mediboxdocument")
    nhanvien_ids = ctx.ids("tb_nhanvien", "nhanvienid")

    rows = []
    sign_id = 1

    for r in documents.itertuples(index=False):

        signed_index = (
            set(
                np.random.choice(
                    range(r.sochuky_init),
                    r.sochuky_daky,
                    replace=False,
                )
            )
            if r.sochuky_daky > 0
            else set()
        )

        for i in range(r.sochuky_init):

            signed = i in signed_index

            if signed:
                status = "Đã ký"
                ngayky = random_datetime_after(
                    r.ngaytao,
                    0,
                    5,
                )
                isduocphepky = 0
            else:
                status = np.random.choice(
                    [
                        "Chưa ký",
                        "Từ chối ký",
                        "Đã hủy",
                    ],
                    p=[0.85, 0.10, 0.05],
                )
                ngayky = pd.NaT
                isduocphepky = 1 if status == "Chưa ký" else 0

            rows.append([
                sign_id,
                r.mediboxdocumentid,
                status,
                np.random.choice(SIGN_ROLES),
                np.random.choice(nhanvien_ids),
                ngayky,
                isduocphepky,
            ])

            sign_id += 1

    tb_mediboxdocument_sign = pd.DataFrame(
        rows,
        columns=[
            "mediboxdocument_signid",
            "mediboxdocumentid",
            "dm_mediboxdocument_signstatusid",
            "tenbien",
            "nguoiky",
            "ngayky",
            "isduocphepky",
        ],
    )

    tb_mediboxdocument_sign["dm_mediboxdocument_signstatusid"] = pd.Categorical(
        tb_mediboxdocument_sign["dm_mediboxdocument_signstatusid"],
        categories=SIGN_STATUSES,
        ordered=False,
    )

    tb_mediboxdocument_sign = inject_null(
        tb_mediboxdocument_sign,
        "tenbien",
        0.01,
    )

    preview(tb_mediboxdocument_sign, "tb_mediboxdocument_sign")
    export_csv(tb_mediboxdocument_sign, "tb_mediboxdocument_sign")

    ctx.add(
        "tb_mediboxdocument_sign",
        tb_mediboxdocument_sign,
    )

    return tb_mediboxdocument_sign