from dataclasses import dataclass, field


@dataclass
class PipelineSpec:
    table_fqn: str
    table_name: str
    test_suite_name: str
    test_case_names: list[str] = field(default_factory=list)

    @property
    def name(self) -> str:
        return f"{self.table_name}_{self.test_suite_name}_test_pipeline"
