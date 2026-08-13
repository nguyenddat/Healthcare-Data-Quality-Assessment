import dotenv  # noqa: EXE002
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.sdk import configure

dotenv.load_dotenv()


def get_metadata_client() -> OpenMetadata:
    return configure().ometa
