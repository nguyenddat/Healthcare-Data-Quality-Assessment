# gen_dm_icd10.py
import random
import pandas as pd

from generated_data.config import ROW_COUNTS
from generated_data.constants import ICD10_CODES
from generated_data.factory import sequential_ids, export_csv, preview

N_ROWS = min(
    ROW_COUNTS.get("tb_dm_icd10", len(ICD10_CODES)),
    len(ICD10_CODES)
)


def generate_tb_dm_icd10(ctx):
    codes = ICD10_CODES.copy()
    random.shuffle(codes)

    tb_dm_icd10 = pd.DataFrame({
        "dm_icd10dbid": sequential_ids(N_ROWS),
        "icd10code": codes[:N_ROWS]
    })

    preview(tb_dm_icd10, "tb_dm_icd10")
    export_csv(tb_dm_icd10, "tb_dm_icd10")

    ctx.add("tb_dm_icd10", tb_dm_icd10)
    return tb_dm_icd10