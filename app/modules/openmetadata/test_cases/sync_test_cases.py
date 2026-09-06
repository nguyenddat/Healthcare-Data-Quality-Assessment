from tqdm import tqdm

from metadata.generated.schema.entity.data.table import Table
from metadata.generated.schema.tests.testCase import TestCase
from metadata.generated.schema.api.tests.createLogicalTestCases import CreateLogicalTestCases

from metadata.utils.entity_link import get_entity_link

from ..client import get_metadata_client
from .specs.completeness_dirty_values import build_dirty_value_test_specs
from .specs.completeness_constant_values import build_constant_value_test_specs

spec_builders = [
    build_dirty_value_test_specs,
    build_constant_value_test_specs
]

def sync_test_cases(tables) -> list[str]:
    client = get_metadata_client()

    specs = []
    for builder in spec_builders:
        specs.extend(builder(tables))

    existing_test_cases = client.list_all_entities(entity=TestCase, limit=1000)
    existing_fqns = {test_case.fullyQualifiedName.root for test_case in existing_test_cases}

    missing_specs = [spec for spec in specs if spec.fqn not in existing_fqns]

    suite_test_case_ids: dict[str, list[str]] = defaultdict(list)
    for spec in tqdm(missing_specs, desc="Creating missing test cases"):
        test_case = client.get_or_create_test_case(
            test_case_fqn=spec.fqn,
            entity_link=get_entity_link(
                Table,
                spec.table_fqn,
            ),
            test_definition_fqn=spec.test_definition_fqn,
            test_case_parameter_values=spec.parameters,
        )
        suite_test_case_ids[spec.test_suite_name].append(test_case.id.root)

    for suite_name, test_case_ids in suite_test_case_ids.items():
        if not test_case_ids:
            continue

        test_suite = client.get_or_create_test_suite(suite_name)

        client.add_logical_test_cases(
            CreateLogicalTestCases(
                testSuiteId=test_suite.id.root,
                testCaseIds=test_case_ids,
            )
        )

    return [spec.fqn for spec in missing_specs]
