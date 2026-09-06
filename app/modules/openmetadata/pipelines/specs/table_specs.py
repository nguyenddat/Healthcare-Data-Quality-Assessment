from collections import defaultdict

from .base import PipelineSpec
from ...test_cases.specs.base import TestSpec

def build_pipeline_specs(tables, test_specs: list[TestSpec]) -> list[PipelineSpec]:
    test_cases_by_table_and_suite: dict[tuple[str, str], list[str]] = defaultdict(list)

    for spec in test_specs:
        test_case_name = spec.fqn.rsplit(".", 1)[-1]
        test_cases_by_table_and_suite[
            (spec.table_fqn, spec.test_suite_name)
        ].append(test_case_name)

    pipeline_specs = []
    for table in tables:
        table_fqn = table.fullyQualifiedName.root

        for (spec_table_fqn, test_suite_name), test_case_names in (
            test_cases_by_table_and_suite.items()
        ):
            if spec_table_fqn != table_fqn:
                continue

            pipeline_specs.append(
                PipelineSpec(
                    table_fqn=table_fqn,
                    table_name=table.name.root,
                    test_suite_name=test_suite_name,
                    test_case_names=test_case_names,
                )
            )

    return pipeline_specs
