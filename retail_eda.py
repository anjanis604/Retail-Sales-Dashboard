import argparse
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def generate_sales_trend(data_path: str, output_path: str):
    """Generate monthly sales trend line chart from retail sales CSV."""
    data_path = Path(data_path)
    output_path = Path(output_path)

    # Ensure paths exist
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    df = pd.read_csv(data_path, parse_dates=["OrderDate"])

    # Validate required columns
    if "Sales" not in df.columns or "OrderDate" not in df.columns:
        raise ValueError("CSV must contain 'OrderDate' and 'Sales' columns")

    monthly = (
        df.groupby(pd.Grouper(key="OrderDate", freq="M"))
        .agg({"Sales": "sum"})
        .reset_index()
    )

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(monthly["OrderDate"], monthly["Sales"], marker="o")
    plt.title("Monthly Sales")
    plt.xlabel("Month")
    plt.ylabel("Total Sales")
    plt.grid(True)
    plt.tight_layout()

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    print(f"Sales trend chart saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retail Sales EDA")
    parser.add_argument(
        "--data", default="../Data/retail_sales.csv", help="Path to input CSV"
    )
    parser.add_argument(
        "--out", default="../Screenshots/retail_sales_trend.png", help="Path to save chart"
    )
    args = parser.parse_args()

    generate_sales_trend(args.data, args.out)
