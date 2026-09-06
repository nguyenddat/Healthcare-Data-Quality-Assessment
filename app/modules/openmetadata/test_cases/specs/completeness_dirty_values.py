from metadata.generated.schema.tests.testCase import TestCaseParameterValue

from .base import TestSpec
from ...utils.identify_text import is_text_datatype
from ...utils.identify_number import is_number_datatype
from ...utils.identify_datetime import is_date_column_name, is_date_datatype

def build_dirty_value_test_specs(tables) -> list[TestSpec]:
    specs = []

    for table in tables:
        table_fqn = table.fullyQualifiedName.root
        qualified_table = f'"{table.databaseSchema.name}"."{table.name.root}"'

        for column in table.columns:
            column_name = column.name.root
            if is_date_datatype(column) or is_date_column_name(column_name):
                prefix = "dirty_date_check"
                dirty_values = ["1900-01-01", "1970-01-01"]

            elif is_text_datatype(column):
                prefix = "dirty_text_check"
                dirty_values = ["", "N/A", ".", "__", "unknown", "x"]

            elif is_number_datatype(column):
                prefix = "dirty_number_check"
                dirty_values = ["0", "-1", "9999"]

            else:
                continue

            test_case_name = f"{prefix}_{column_name}"
            values = ", ".join(f"'{value}'" for value in dirty_values)

            sql_expression = (
                f'SELECT COUNT(*) FILTER '
                f'(WHERE "{column_name}" IN ({values})) '
                f'* 100.0 / NULLIF(COUNT(*), 0) '
                f'FROM {qualified_table}'
            )

            specs.append(
                TestSpec(
                    fqn=f"{table_fqn}.{test_case_name}",
                    table_fqn=table_fqn,
                    test_suite_name="DirtyValueCheck",
                    test_definition_fqn="tableCustomSQLQuery",
                    parameters=[
                        TestCaseParameterValue(
                            name="sqlExpression",
                            value=sql_expression,
                        ),
                        TestCaseParameterValue(
                            name="strategy",
                            value="COUNT",
                        ),
                        TestCaseParameterValue(
                            name="operator",
                            value="<=",
                        ),
                        TestCaseParameterValue(
                            name="threshold",
                            value="50",
                        ),
                    ],
                )
            )

    return specs
