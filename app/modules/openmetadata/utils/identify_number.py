from metadata.generated.schema.entity.data.table import DataType

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

def is_number_datatype(column: any) -> bool:
    if column.dataType in NUMBER_DATA_TYPES:
        return True
    return False
