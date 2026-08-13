from metadata.generated.schema.api.tests.createLogicalTestCases import (
    CreateLogicalTestCases,
)
from metadata.generated.schema.entity.data.table import Table
from metadata.generated.schema.tests.testCase import TestCaseParameterValue
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.sdk import Tables
from metadata.utils.entity_link import get_entity_link
from tqdm import tqdm

from ....core.settings import config
from ..client import get_metadata_client
from .constants import (
    CUSTOM_SQL_TEST_DEFINITION,
    DATE_DATA_TYPES,
    DIRTY_DATE_VALUES,
    DIRTY_NUMBER_VALUES,
    DIRTY_TEXT_VALUES,
    DIRTY_VALUE_RATIO_THRESHOLD_PERCENT,
    NUMBER_DATA_TYPES,
    TEST_SUITE_NAME,
    TEXT_DATA_TYPES,
)


def _dirty_ratio_test_case(
    client: OpenMetadata,
    table_fqn: str,
    qualified_table: str,
    column_name: str,
    suffix: str,
    dirty_values: list[str],
):
    values = ", ".join(f"'{v}'" for v in dirty_values)
    test_case_name = f"{column_name}_{suffix}"
    sql_expression = (
        f'SELECT COUNT(*) FILTER (WHERE "{column_name}" IN ({values})) * 100 '
        f'/ NULLIF(COUNT(*), 0) FROM {qualified_table}'
    )
    return client.get_or_create_test_case(
        test_case_fqn=f"{table_fqn}.{test_case_name}",
        entity_link=get_entity_link(Table, table_fqn),
        test_definition_fqn=CUSTOM_SQL_TEST_DEFINITION,
        test_case_parameter_values=[
            TestCaseParameterValue(name="sqlExpression", value=sql_expression),
            TestCaseParameterValue(name="strategy", value="COUNT"),
            TestCaseParameterValue(name="operator", value="<="),
            TestCaseParameterValue(
                name="threshold", value=DIRTY_VALUE_RATIO_THRESHOLD_PERCENT
            ),
        ],
    )


def create_dirty_value_test_cases() -> None:
    client = get_metadata_client()

    tables = [
        table
        for table in Tables.list_all(filters={"service": config.SERVICE_NAME})
        if table.database.name == config.DATABASE_NAME
    ]

    test_case_ids = []
    for table in tqdm(tables, desc="Dirty value test cases:"):
        table_fqn = table.fullyQualifiedName.root
        qualified_table = f'"{table.databaseSchema.name}"."{table.name.root}"'
        for column in table.columns:
            column_name = column.name.root
            if column.dataType in TEXT_DATA_TYPES:
                test_case = _dirty_ratio_test_case(
                    client, table_fqn, qualified_table, column_name,
                    "dirty_value_check", DIRTY_TEXT_VALUES,
                )
            elif column.dataType in NUMBER_DATA_TYPES:
                test_case = _dirty_ratio_test_case(
                    client, table_fqn, qualified_table, column_name,
                    "dirty_number_check", DIRTY_NUMBER_VALUES,
                )
            elif column.dataType in DATE_DATA_TYPES:
                test_case = _dirty_ratio_test_case(
                    client, table_fqn, qualified_table, column_name,
                    "dirty_date_check", DIRTY_DATE_VALUES,
                )
            else:
                continue
            test_case_ids.append(test_case.id.root)

    if not test_case_ids:
        return

    test_suite = client.get_or_create_test_suite(TEST_SUITE_NAME)
    client.add_logical_test_cases(
        CreateLogicalTestCases(
            testSuiteId=test_suite.id.root,
            testCaseIds=test_case_ids,
        )
    )
