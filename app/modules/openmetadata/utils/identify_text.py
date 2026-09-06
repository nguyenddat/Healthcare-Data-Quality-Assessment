from metadata.generated.schema.entity.data.table import DataType

TEXT_DATA_TYPES = {DataType.STRING, DataType.TEXT, DataType.VARCHAR, DataType.CHAR, DataType.MEDIUMTEXT}

def is_text_datatype(column: any) -> bool:
    if column.dataType in TEXT_DATA_TYPES:
        return True
    return False
