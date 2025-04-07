def main(blob_url: str) -> list:
    return [
        f"{blob_url}?chunk=1",
        f"{blob_url}?chunk=2",
        f"{blob_url}?chunk=3"
    ]
