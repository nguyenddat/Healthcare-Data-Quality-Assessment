import numpy as np
import pandas as pd

from generated_data.config import ROW_COUNTS
from generated_data.constants import ICD10_CODES, ICD10_NAMES
from generated_data.factory import sequential_ids, sample_fk, random_datetime, random_datetime_after, inject_null, preview, export_csv

N_ROWS = ROW_COUNTS["tb_medicalrecord"]

def generate_tb_medicalrecord(ctx):
    department_ids = ctx.ids("tb_department", "departmentid")
    staff_ids = ctx.ids("tb_nhanvien", "nhanvienid")
    chamber_ids = ctx.ids("tb_chamber", "chamberid")

    idx = np.random.randint(0, len(ICD10_CODES), N_ROWS)
    date_in = random_datetime("2023-01-01", "2025-12-31", size=N_ROWS)
    los = np.random.randint(1, 31, N_ROWS)
    date_out = random_datetime_after(date_in, days=los)

    tb_medicalrecord = pd.DataFrame({
        "medicalrecordid": sequential_ids(N_ROWS),
        "patientrecordid": np.random.randint(300000, 2000000, N_ROWS),
        "bedid": sample_fk(chamber_ids, size=N_ROWS),
        "departmentid": sample_fk(department_ids, size=N_ROWS),
        "medicalrecorddate_in": date_in,
        "medicalrecorddate_out": date_out,
        "chandoan_in_icd10": np.array(ICD10_CODES)[idx],
        "chandoan_in": np.array(ICD10_NAMES)[idx],
        "userid_dieutri": sample_fk(staff_ids, size=N_ROWS),
        "userid_dieuduong": sample_fk(staff_ids, size=N_ROWS),
        "dm_medicalrecordtypeid": np.random.choice([1, 2, 3, 4], size=N_ROWS, p=[0.55, 0.30, 0.10, 0.05]),
    })

    tb_medicalrecord = inject_null(tb_medicalrecord, "patientrecordid", 0.01)
    tb_medicalrecord = inject_null(tb_medicalrecord, "bedid", 0.02)
    tb_medicalrecord = inject_null(tb_medicalrecord, "departmentid", 0.01)
    tb_medicalrecord = inject_null(tb_medicalrecord, "medicalrecorddate_out", 0.02)
    tb_medicalrecord = inject_null(tb_medicalrecord, "chandoan_in_icd10", 0.03)
    tb_medicalrecord = inject_null(tb_medicalrecord, "chandoan_in", 0.03)
    tb_medicalrecord = inject_null(tb_medicalrecord, "userid_dieutri", 0.01)

    preview(tb_medicalrecord, "tb_medicalrecord")
    export_csv(tb_medicalrecord, "tb_medicalrecord")
    ctx.add("tb_medicalrecord", tb_medicalrecord)

    return tb_medicalrecord