# gen_service.py

import numpy as np
import pandas as pd

from generated_data.config import ROW_COUNTS
from generated_data.constants import SERVICE_NAMES
from generated_data.factory import (
    sequential_ids,
    inject_null,
    export_csv,
    preview,
)

N_ROWS = ROW_COUNTS["tb_service"]


def generate_tb_service(ctx):
    service_names = np.random.choice(
        SERVICE_NAMES,
        size=N_ROWS,
        replace=True,
    )

    gia_bhyt = np.random.choice(
        [310000, 450000, 520000, 680000, 790000, 950000, 1216000],
        size=N_ROWS,
    )

    tb_service = pd.DataFrame({
        "serviceid": sequential_ids(N_ROWS),
        "servicecode": [
            f"DV{str(i).zfill(5)}"
            for i in range(1, N_ROWS + 1)
        ],
        "servicename": service_names,
        "servicenamebhyt": service_names,
        "dm_servicegroupid": np.random.choice(
            [1, 2, 3, 4, 5, 6],
            size=N_ROWS,
            p=[0.15, 0.20, 0.20, 0.15, 0.15, 0.15],
        ),
        "dm_servicesubgroupid": np.random.randint(601, 701, size=N_ROWS,),
        "giabhyt": gia_bhyt,
        "giavienphi": (
            gia_bhyt * np.random.uniform(1.0, 1.3, N_ROWS)
        ).round(-3).astype(int),
        "giadichvu": (
            (
                gia_bhyt * np.random.uniform(1.0, 1.3, N_ROWS)
            ) * np.random.uniform(1.1, 1.5, N_ROWS)
        ).round(-3).astype(int),
        "servicedisable": np.random.choice(
            [0, 1],
            size=N_ROWS,
            p=[0.98, 0.02],
        ),
    })

    tb_service = inject_null(tb_service, "servicenamebhyt", 0.05)

    tb_service = inject_null(tb_service, "dm_servicesubgroupid", 0.02,)

    preview(tb_service, "tb_service")
    export_csv(tb_service, "tb_service")

    ctx.add("tb_service", tb_service)

    return tb_service