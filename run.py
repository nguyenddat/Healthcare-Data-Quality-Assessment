import os  # noqa: EXE002
import time

from sqlalchemy import create_engine

from generated_data.context import DataContext
from generated_data.gen_chamber import generate_tb_chamber
from generated_data.gen_nhanvien import generate_tb_nhanvien
from generated_data.gen_tb_department import generate_tb_department
from generated_data.gen_tb_dm_benhvien import generate_tb_dm_benhvien
from generated_data.gen_tb_dm_icd10 import generate_tb_dm_icd10
from generated_data.gen_tb_dm_servicesubgroup import generate_tb_dm_servicesubgroup
from generated_data.gen_tb_meddocument import generate_tb_mediboxdocument
from generated_data.gen_tb_medicalrecord import generate_tb_medicalrecord
from generated_data.gen_tb_medrec_kb import generate_tb_medicalrecord_khambenh
from generated_data.gen_tb_nhanvienactivity import generate_tb_nhanvienactivity
from generated_data.gen_tb_room import generate_tb_room
from generated_data.gen_tb_service import generate_tb_service
from generated_data.gen_tb_servicedata_pttt import generate_tb_servicedata_pttt
from generated_data.gen_tb_treatment import generate_tb_treatment

# ---- DB CONFIG (edit to match your Postgres) ----
DB_URL = os.environ.get(
    "DB_URL",
    "postgresql://postgres:postgres@localhost:5432/healthcare_sim"
)

# Generate HIS Synthetic Data
ctx = DataContext()
print("=" * 80)
print("START GENERATING SYNTHETIC HIS DATA")
print("=" * 80)
generate_tb_dm_benhvien(ctx)
generate_tb_department(ctx)
generate_tb_room(ctx)
generate_tb_chamber(ctx)
generate_tb_nhanvien(ctx)
generate_tb_dm_icd10(ctx)
generate_tb_dm_servicesubgroup(ctx)
generate_tb_service(ctx)
generate_tb_medicalrecord(ctx)
generate_tb_treatment(ctx)
generate_tb_medicalrecord_khambenh(ctx)
generate_tb_servicedata_pttt(ctx)
generate_tb_mediboxdocument(ctx)
generate_tb_nhanvienactivity(ctx)

# Summary after generate
print()
print("=" * 80)
print("GENERATED TABLE SUMMARY")
print("=" * 80)
for name, df in ctx.tables.items():
    print(f"{name:<40} rows={len(df):<10} columns={len(df.columns)}")


def create_engine_with_retry():
    while True:
        try:
            engine = create_engine(DB_URL)
            conn = engine.connect()
            conn.close()
            print("Postgres connected")
            return engine
        except Exception as e:
            print("Waiting Postgres...", e)
            time.sleep(5)


engine = create_engine_with_retry()

# Load Data Into Postgres (for OpenMetadata ingestion + DQ tests)
print()
print("=" * 80)
print("START LOADING TABLES INTO POSTGRES")
print("=" * 80)
for table_name, df in ctx.tables.items():
    print(f"\nLoading table: {table_name}")
    print("Schema:", list(df.columns))
    print("Rows:", len(df))
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=1000,
    )
    print(f"LOADED {table_name}")

print()
print("=" * 80)
print("ALL DATA LOADED TO POSTGRES")
print("=" * 80)