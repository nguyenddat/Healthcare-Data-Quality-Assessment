from metadata.generated.schema.tests.testCase import TestCaseParameterValue

from .base import TestSpec
from ...utils.identify_text import is_text_datatype
from ...utils.identify_number import is_number_datatype
from ...utils.identify_datetime import is_date_column_name, is_date_datatype

def build_constant_value_test_specs(tables) -> list[TestSpec]:
    specs = []
    for table in tables:
        table_fqn = table.fullyQualifiedName.root
        qualified_table = f'"{table.databaseSchema.name}"."{table.name.root}"'

        for column in table.columns:
            column_name = column.name.root
            test_case_name = f"not_constant_check_{column_name}"

            sql_expression = (
                f'SELECT COUNT(DISTINCT "{column_name}") '
                f'FROM {qualified_table}'
            )

            specs.append(
                TestSpec(
                    fqn=f"{table_fqn}.{test_case_name}",
                    table_fqn=table_fqn,
                    test_suite_name="ConstantCheck",
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
                            value="!=",
                        ),
                        TestCaseParameterValue(
                            name="threshold",
                            value="1",
                        ),
                    ],
                )
            )

    return specs
