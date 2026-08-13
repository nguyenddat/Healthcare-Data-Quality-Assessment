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
    CONSTANT_VALUE_DISTINCT_COUNT_THRESHOLD,
    CONSTANT_VALUE_TEST_SUITE_NAME,
    CUSTOM_SQL_TEST_DEFINITION,
)


def _not_constant_test_case(
    client: OpenMetadata, table_fqn: str, qualified_table: str, column_name: str
):
    test_case_name = f"{column_name}_not_constant_check"
    return client.get_or_create_test_case(
        test_case_fqn=f"{table_fqn}.{test_case_name}",
        entity_link=get_entity_link(Table, table_fqn),
        test_definition_fqn=CUSTOM_SQL_TEST_DEFINITION,
        test_case_parameter_values=[
            TestCaseParameterValue(
                name="sqlExpression",
                value=f'SELECT COUNT(DISTINCT "{column_name}") FROM {qualified_table}',
            ),
            TestCaseParameterValue(name="strategy", value="COUNT"),
            TestCaseParameterValue(name="operator", value="!="),
            TestCaseParameterValue(
                name="threshold", value=CONSTANT_VALUE_DISTINCT_COUNT_THRESHOLD
            ),
        ],
    )


def create_constant_value_test_cases() -> None:
    client = get_metadata_client()

    tables = [
        table
        for table in Tables.list_all(filters={"service": config.SERVICE_NAME})
        if table.database.name == config.DATABASE_NAME
    ]

    test_case_ids = []
    for table in tqdm(tables, desc="Constant value test cases:"):
        table_fqn = table.fullyQualifiedName.root
        qualified_table = f'"{table.databaseSchema.name}"."{table.name.root}"'
        for column in table.columns:
            test_case = _not_constant_test_case(
                client, table_fqn, qualified_table, column.name.root
            )
            test_case_ids.append(test_case.id.root)

    if not test_case_ids:
        return

    test_suite = client.get_or_create_test_suite(CONSTANT_VALUE_TEST_SUITE_NAME)
    client.add_logical_test_cases(
        CreateLogicalTestCases(
            testSuiteId=test_suite.id.root,
            testCaseIds=test_case_ids,
        )
    )
