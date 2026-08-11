import numpy as np
import pandas as pd

from generated_data.config import ROW_COUNTS
from generated_data.factory import sequential_ids, sample_fk, random_datetime, inject_null, preview, export_csv

N_ROWS = ROW_COUNTS["tb_nhanvienactivity"]


def generate_tb_nhanvienactivity(ctx):
    nhanvien_ids = ctx.ids("tb_nhanvien", "nhanvienid")
    treatment_df = ctx.get("tb_treatment")
    treatment_ids = treatment_df["treatmentid"].tolist()
    treatment_begin = dict(zip(treatment_df["treatmentid"], treatment_df["treatmentdate"]))
    servicedata_pttt_ids = ctx.ids("tb_servicedata_pttt", "servicedata_ptttid")

    activitytypeid = np.random.choice([1, 2, 3], size=N_ROWS, p=[0.55, 0.35, 0.10])
    treatmentid = sample_fk(treatment_ids, size=N_ROWS)
    nhanvienid = sample_fk(nhanvien_ids, size=N_ROWS)

    servicedataid = np.random.randint(1000000, 9999999, N_ROWS).astype(float)
    servicedata_ptttid = np.full(N_ROWS, np.nan)

    mask = activitytypeid == 3
    servicedata_ptttid[mask] = sample_fk(servicedata_pttt_ids, size=mask.sum())
    servicedataid[np.random.rand(N_ROWS) < 0.25] = np.nan

    begintime = []
    endtime = []

    for tid in treatmentid:
        begin = random_datetime(treatment_begin[tid], treatment_begin[tid] + pd.Timedelta(days=2))
        end = begin + pd.Timedelta(minutes=np.random.randint(10, 241))
        begintime.append(begin)
        endtime.append(end)

    tb_nhanvienactivity = pd.DataFrame({
        "nhanvienactivityid": sequential_ids(N_ROWS),
        "nhanvienid": nhanvienid,
        "treatmentid": treatmentid,
        "servicedataid": servicedataid,
        "servicedata_ptttid": servicedata_ptttid,
        "begintime": begintime,
        "endtime": endtime,
        "activitytypeid": activitytypeid,
    })

    tb_nhanvienactivity = inject_null(tb_nhanvienactivity, "nhanvienid", 0.01)
    tb_nhanvienactivity = inject_null(tb_nhanvienactivity, "treatmentid", 0.005)

    preview(tb_nhanvienactivity, "tb_nhanvienactivity")
    export_csv(tb_nhanvienactivity, "tb_nhanvienactivity")

    ctx.add("tb_nhanvienactivity", tb_nhanvienactivity)

    return tb_nhanvienactivity