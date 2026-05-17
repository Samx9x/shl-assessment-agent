import json

from pathlib import Path


CATALOG_PATH = (
    Path("data")
    / "shl_product_catalog.json"
)


def load_catalog():

    with open(
        CATALOG_PATH,
        "r",
        encoding="utf-8",
    ) as f:

        return json.load(f)


catalog_data = load_catalog()