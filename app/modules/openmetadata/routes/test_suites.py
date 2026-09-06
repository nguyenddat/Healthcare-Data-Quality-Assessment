from fastapi import APIRouter

from metadata.sdk import Tables

from ....core.settings import config
from ..test_cases.sync_test_cases import sync_test_cases
from ..test_cases.specs.completeness_dirty_values import build_dirty_value_test_specs
from ..test_cases.specs.completeness_constant_values import build_constant_value_test_specs

from ..pipelines.sync_pipelines import sync_pipelines, trigger_pipelines
from ..pipelines.specs.table_specs import build_pipeline_specs

router = APIRouter(prefix="/openmetadata/test-suites")

@router.post("/deploy/dirty-value")
async def deploy_dirty_value_test_suites():
    tables = [table for table in Tables.list_all(filters={"service": config.SERVICE_NAME}) if table.database.name == config.DATABASE_NAME]

    test_specs = build_dirty_value_test_specs(tables)
    created_test_cases = sync_test_cases(test_specs)

    pipeline_specs = build_pipeline_specs(tables, test_specs)
    created_pipelines = sync_pipelines(tables=tables, pipeline_specs=pipeline_specs)

    return {
        "test_cases": {
            "desired": len(test_specs),
            "created": len(created_test_cases),
        },
        "pipelines": {
            "desired": len(pipeline_specs),
            "synced": len(created_pipelines),
        },
    }

@router.post("/deploy/constant-value")
async def deploy_constant_value_test_suites():
    tables = [table for table in Tables.list_all(filters={"service": config.SERVICE_NAME}) if table.database.name == config.DATABASE_NAME]

    test_specs = build_constant_value_test_specs(tables)
    created_test_cases = sync_test_cases(test_specs)

    pipeline_specs = build_pipeline_specs(tables, test_specs)
    created_pipelines = sync_pipelines(tables=tables, pipeline_specs=pipeline_specs)

    return {
        "test_cases": {
            "desired": len(test_specs),
            "created": len(created_test_cases),
        },
        "pipelines": {
            "desired": len(pipeline_specs),
            "synced": len(created_pipelines),
        },
    }

@router.post("/run/dirty-value")
async def run_dirty_value_test_suites():
    tables = [
        table
        for table in Tables.list_all(
            filters={"service": config.SERVICE_NAME}, fields=["testSuite"]
        )
        if table.database.name == config.DATABASE_NAME
    ]
    triggered = trigger_pipelines(tables, test_suite_name="DirtyValueCheck")

    return {
        "test_suite": "DirtyValueCheck",
        "triggered": len(triggered),
        "pipelines": triggered,
    }

@router.post("/run/constant-value")
async def run_constant_value_test_suites():
    tables = [
        table
        for table in Tables.list_all(
            filters={"service": config.SERVICE_NAME}, fields=["testSuite"]
        )
        if table.database.name == config.DATABASE_NAME
    ]
    triggered = trigger_pipelines(tables, test_suite_name="ConstantCheck")

    return {
        "test_suite": "ConstantCheck",
        "triggered": len(triggered),
        "pipelines": triggered,
    }
