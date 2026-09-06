from dataclasses import dataclass

from metadata.generated.schema.tests.testCase import TestCaseParameterValue

@dataclass
class TestSpec:
    fqn: str
    table_fqn: str
    test_suite_name: str
    test_definition_fqn: str
    parameters: list[TestCaseParameterValue]
