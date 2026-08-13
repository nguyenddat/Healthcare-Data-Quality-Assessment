from metadata.generated.schema.entity.data.table import DataType

DIRTY_TEXT_VALUES = ["", "N/A", ".", "__", "unknown", "x"]
DIRTY_NUMBER_VALUES = ["0", "-1", "9999"]
DIRTY_DATE_VALUES = ["1900-01-01", "1970-01-01"]

TEXT_DATA_TYPES = {
    DataType.STRING,
    DataType.TEXT,
    DataType.VARCHAR,
    DataType.CHAR,
    DataType.MEDIUMTEXT,
}

NUMBER_DATA_TYPES = {
    DataType.NUMBER,
    DataType.INT,
    DataType.FLOAT,
    DataType.DOUBLE,
    DataType.DECIMAL,
    DataType.TINYINT,
    DataType.SMALLINT,
    DataType.BIGINT,
    DataType.BYTEINT,
}

DATE_DATA_TYPES = {
    DataType.DATE,
    DataType.DATETIME,
    DataType.TIMESTAMP,
}

CUSTOM_SQL_TEST_DEFINITION = "tableCustomSQLQuery"
TEST_SUITE_NAME = "DirtyValueDetection"

DIRTY_VALUE_RATIO_THRESHOLD_PERCENT = "50"

CONSTANT_VALUE_DISTINCT_COUNT_THRESHOLD = "1"
CONSTANT_VALUE_TEST_SUITE_NAME = "ConstantValueDetection"

DIRTY_VALUE_TEST_SUFFIXES = (
    "dirty_value_check",
    "dirty_number_check",
    "dirty_date_check",
)
CONSTANT_VALUE_TEST_SUFFIX = "not_constant_check"

DIRTY_VALUE_PIPELINE_NAME = "dirty_value_pipeline"
CONSTANT_VALUE_PIPELINE_NAME = "constant_value_pipeline"
