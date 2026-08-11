import random
import pandas as pd

from generated_data.config import ROW_COUNTS
from generated_data.constants import ROOM_NAMES
from generated_data.factory import (
    sequential_ids,
    sample_fk,
    inject_null,
    preview,
    export_csv,
)

N_ROWS = ROW_COUNTS["tb_room"]


def generate_room_name():
    return random.choice(ROOM_NAMES)


def generate_tb_room(ctx):
    department_ids = ctx.ids("tb_department", "departmentid")

    tb_room = pd.DataFrame({
        "roomid": sequential_ids(N_ROWS),
        "roomname": [
            generate_room_name()
            for _ in range(N_ROWS)
        ],
        "departmentid": sample_fk(department_ids, size=N_ROWS,),})

    tb_room = inject_null(tb_room, "roomname",0.03,)

    preview(tb_room, "tb_room")
    export_csv(tb_room, "tb_room")

    ctx.add("tb_room", tb_room)

    return tb_room