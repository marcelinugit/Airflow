from gustavo_sdk.infrastructure.common.utils import get_logger

logger = get_logger(__name__)

class GCP:
    def __init__(self) -> None:
        pass

    def upload(
            self,
            bucket_prefix: str,
            data: list[dict],
            file_name: str,
            ) -> None:

                logger.info("GCP upload not implemented yet")