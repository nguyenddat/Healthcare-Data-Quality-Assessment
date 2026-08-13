from metadata.generated.schema.api.classification.createClassification import (
    CreateClassificationRequest,
)
from metadata.generated.schema.api.classification.createTag import CreateTagRequest
from metadata.generated.schema.entity.data.table import Table
from metadata.generated.schema.type.tagLabel import (
    LabelType,
    State,
    TagLabel,
    TagSource,
)
from metadata.ingestion.ometa.mixins.patch_mixin_utils import PatchOperation
from metadata.ingestion.ometa.ometa_api import OpenMetadata

CLASSIFICATION_NAME = "DataCompleteness"

TAGS = {
    "NoData": "Table has zero rows.",
    "SparseData": "Table has very few rows (unused or test data).",
    "FullData": "Table has a substantial, valid amount of data.",
}


def ensure_data_completeness_tags(metadata: OpenMetadata) -> None:
    metadata.create_or_update(
        CreateClassificationRequest(
            name=CLASSIFICATION_NAME,
            description="Classifies tables by how much data they contain.",
            mutuallyExclusive=True,
        )
    )

    for tag_name, description in TAGS.items():
        metadata.create_or_update(
            CreateTagRequest(
                classification=CLASSIFICATION_NAME,
                name=tag_name,
                description=description,
            )
        )


def _tag_label(tag_name: str) -> TagLabel:
    return TagLabel(
        tagFQN=f"{CLASSIFICATION_NAME}.{tag_name}",
        source=TagSource.Classification,
        labelType=LabelType.Manual,
        state=State.Confirmed,
    )


def apply_du_lieu_tag(metadata: OpenMetadata, table: Table, tag_name: str) -> None:
    other_tag_labels = [_tag_label(name) for name in TAGS if name != tag_name]
    metadata.patch_tags(
        entity=Table, source=table, tag_labels=other_tag_labels, operation=PatchOperation.REMOVE
    )
    metadata.patch_tags(entity=Table, source=table, tag_labels=[_tag_label(tag_name)])
