def main(results: list):
    # Combine all results
    total_outliers = sum(r["outliers"] for r in results)
    total_records = sum(r["total"] for r in results)

    print("Final Result Summary:")
    print(f"Total Records: {total_records}")
    print(f"Total Outliers: {total_outliers}")

    # TODO: save to blob or POST to webhook
    return {
        "total": total_records,
        "outliers": total_outliers
    }
