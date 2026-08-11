# gen_hanhvien.py
import pandas as pd
from generated_data.config import ROW_COUNTS
from generated_data.factory import sequential_ids, sample_fk, inject_null, export_csv, preview, random_person_name

N_ROWS = ROW_COUNTS["tb_nhanvien"]

def generate_tb_nhanvien(ctx):
    department_ids = ctx.ids("tb_department", "departmentid")
    tb_nhanvien = pd.DataFrame({
        "nhanvienid": sequential_ids(N_ROWS),
        "departmentid": sample_fk(department_ids, size=N_ROWS),
        "fullname": [random_person_name() for _ in range(N_ROWS)]
    })
    tb_nhanvien = inject_null(tb_nhanvien, "departmentid", 0.01)
    preview(tb_nhanvien, "tb_nhanvien")
    export_csv(tb_nhanvien, "tb_nhanvien")
    ctx.add("tb_nhanvien", tb_nhanvien)
    return tb_nhanvien