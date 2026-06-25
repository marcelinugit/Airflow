import os

from gustavo_sdk.infrastructure.integration.gcp.gcp import GCP

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    r"C:\Users\Marce\Downloads\ecommercegustavo-data-500420-18c4f67164f6.json"
)

gcp = GCP()

data = [
    {
        "id": 1,
        "nome": "Marce",
        "idade": 20,
    },
    {
        "id": 2,
        "nome": "Pedro",
        "idade": 30,
    },
]

gcp.upload(
    bucket_prefix="ecommercegustavo-data-lake",
    data=data,
    file_name="teste.csv",
)

print("Teste finalizado com sucesso!")