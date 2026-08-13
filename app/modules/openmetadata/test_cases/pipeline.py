from collections.abc import Generator

from metadata.generated.schema.api.services.ingestionPipelines.createIngestionPipeline import (
    CreateIngestionPipelineRequest,
)
from metadata.generated.schema.entity.services.ingestionPipelines.ingestionPipeline import (
    AirflowConfig,
    IngestionPipeline,
    PipelineType,
)
from metadata.generated.schema.metadataIngestion.testSuitePipeline import (
    TestSuiteConfigType,
    TestSuitePipeline,
)
from metadata.generated.schema.metadataIngestion.workflow import SourceConfig
from metadata.generated.schema.tests.testSuite import TestSuite
from metadata.generated.schema.type.entityReference import EntityReference
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.sdk import Tables

from ....core.settings import config
from ..client import get_metadata_client
from .constants import (
    CONSTANT_VALUE_PIPELINE_NAME,
    CONSTANT_VALUE_TEST_SUFFIX,
    DIRTY_VALUE_PIPELINE_NAME,
    DIRTY_VALUE_TEST_SUFFIXES,
)


def _deploy_pipeline(client: OpenMetadata, pipeline_id: str) -> None:
    client.client.post(f"{client.get_suffix(IngestionPipeline)}/deploy/{pipeline_id}")


def _trigger_pipeline(client: OpenMetadata, pipeline_id: str) -> None:
    client.client.post(f"{client.get_suffix(IngestionPipeline)}/trigger/{pipeline_id}")


def _get_or_create_pipeline(
    client: OpenMetadata,
    test_suite: TestSuite,
    table_fqn: str,
    pipeline_name: str,
    test_case_names: list[str],
) -> IngestionPipeline:
    pipeline_fqn = f"{test_suite.fullyQualifiedName.root}.{pipeline_name}"

    pipeline = client.get_by_name(entity=IngestionPipeline, fqn=pipeline_fqn)
    if pipeline:
        return pipeline

    return client.create_or_update(
        CreateIngestionPipelineRequest(
            name=pipeline_name,
            pipelineType=PipelineType.TestSuite,
            sourceConfig=SourceConfig(
                config=TestSuitePipeline(
                    type=TestSuiteConfigType.TestSuite,
                    entityFullyQualifiedName=table_fqn,
                    testCases=test_case_names,
                )
            ),
            airflowConfig=AirflowConfig(),
            service=EntityReference(id=test_suite.id, type="testSuite"),
        )
    )


def _table_pipelines(
    client: OpenMetadata,
    *,
    include_dirty: bool = True,
    include_constant: bool = True,
) -> Generator[tuple[str, IngestionPipeline], None, None]:
    tables = [
        table
        for table in Tables.list_all(
            filters={"service": config.SERVICE_NAME}, fields=["testSuite"]
        )
        if table.database.name == config.DATABASE_NAME
    ]

    for table in tables:
        if not table.testSuite:
            continue

        table_fqn = table.fullyQualifiedName.root
        test_suite = client.get_by_name(
            entity=TestSuite, fqn=table.testSuite.fullyQualifiedName, fields=["tests"]
        )
        if not test_suite.tests:
            continue

        table_name = table.name.root

        if include_dirty:
            dirty_names = [
                t.name
                for t in test_suite.tests
                if t.name.endswith(DIRTY_VALUE_TEST_SUFFIXES)
            ]
            if dirty_names:
                yield table_fqn, _get_or_create_pipeline(
                    client,
                    test_suite,
                    table_fqn,
                    f"{table_name}_{DIRTY_VALUE_PIPELINE_NAME}",
                    dirty_names,
                )

        if include_constant:
            constant_names = [
                t.name
                for t in test_suite.tests
                if t.name.endswith(CONSTANT_VALUE_TEST_SUFFIX)
            ]
            if constant_names:
                yield table_fqn, _get_or_create_pipeline(
                    client,
                    test_suite,
                    table_fqn,
                    f"{table_name}_{CONSTANT_VALUE_PIPELINE_NAME}",
                    constant_names,
                )


def create_table_test_pipelines() -> list[str]:
    client = get_metadata_client()

    created = []
    for table_fqn, pipeline in _table_pipelines(client):
        _deploy_pipeline(client, str(pipeline.id.root))
        created.append(f"{table_fqn}.{pipeline.name.root}")

    return created


def _run_table_pipelines(*, include_dirty: bool, include_constant: bool) -> list[str]:
    client = get_metadata_client()

    triggered = []
    for table_fqn, pipeline in _table_pipelines(
        client, include_dirty=include_dirty, include_constant=include_constant
    ):
        _trigger_pipeline(client, str(pipeline.id.root))
        triggered.append(f"{table_fqn}.{pipeline.name.root}")

    return triggered


def run_dirty_value_test_pipelines() -> list[str]:
    return _run_table_pipelines(include_dirty=True, include_constant=False)


def run_constant_value_test_pipelines() -> list[str]:
    return _run_table_pipelines(include_dirty=False, include_constant=True)
