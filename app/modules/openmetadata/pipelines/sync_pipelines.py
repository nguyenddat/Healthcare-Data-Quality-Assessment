from tqdm import tqdm

from metadata.generated.schema.api.services.ingestionPipelines.createIngestionPipeline import CreateIngestionPipelineRequest
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
from metadata.generated.schema.type.entityReference import EntityReference

from ..client import get_metadata_client
from .specs.base import PipelineSpec

def sync_pipelines(
    tables,
    pipeline_specs: list[PipelineSpec],
) -> list[str]:
    client = get_metadata_client()

    tables_by_fqn = {table.fullyQualifiedName.root: table for table in tables}

    synced = []
    for spec in tqdm(pipeline_specs, desc="Syncing test pipelines"):
        table = tables_by_fqn.get(spec.table_fqn)

        if not table:
            continue

        if not table.testSuite:
            continue

        pipeline = client.create_or_update(
            CreateIngestionPipelineRequest(
                name=spec.name,
                pipelineType=PipelineType.TestSuite,
                sourceConfig=SourceConfig(
                    config=TestSuitePipeline(
                        type=TestSuiteConfigType.TestSuite,
                        entityFullyQualifiedName=spec.table_fqn,
                        testCases=spec.test_case_names,
                    )
                ),
                airflowConfig=AirflowConfig(),
                service=EntityReference(
                    id=table.testSuite.id,
                    type="testSuite",
                ),
            )
        )

        client.client.post(f"{client.get_suffix(IngestionPipeline)}/deploy/{str(pipeline.id.root)}")
        synced.append(f"{spec.table_fqn}.{spec.name}")

    return synced


def trigger_pipelines(
    tables,
    test_suite_name: str,
) -> list[str]:
    """Trigger the pipeline for ``test_suite_name`` on each supplied table."""
    client = get_metadata_client()

    triggered = []
    for table in tables:
        if not table.testSuite or not table.testSuite.fullyQualifiedName:
            continue

        pipeline_name = PipelineSpec(
            table_fqn=table.fullyQualifiedName.root,
            table_name=table.name.root,
            test_suite_name=test_suite_name,
        ).name
        pipeline_fqn = f"{table.testSuite.fullyQualifiedName}.{pipeline_name}"
        pipeline = client.get_by_name(entity=IngestionPipeline, fqn=pipeline_fqn)

        if not pipeline:
            continue

        client.client.post(
            f"{client.get_suffix(IngestionPipeline)}/trigger/{pipeline.id.root}"
        )
        triggered.append(f"{table.fullyQualifiedName.root}.{pipeline.name.root}")

    return triggered
