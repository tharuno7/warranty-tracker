# WarrantyWatch

A simple command-line warranty tracker written in Python. Log the gadgets you buy, and WarrantyWatch works out when each warranty ends and warns you before it expires, so you never lose a claim to a missed date.

## Features

- **Add a product**: record the product, shop, price, purchase date and warranty length in months. The expiry date is calculated for you.
- **View all**: list every product, sorted by how soon its warranty ends, with days left or days since expiry.
- **Expiring soon**: show warranties that end within the next 30 days.
- **Search**: find products by product name or shop name.
- **Statistics**: total products, total money spent, how many are under warranty or expired, and which one expires next.
- **Input validation**: rejects empty fields, non-positive prices, future purchase dates and warranty lengths outside 1 to 120 months.
- **Month-end handling**: a purchase on 31 January with a 1-month warranty correctly ends on 28 February (or 29 in a leap year).

## Requirements

- Python 3.7 or newer
- No third-party packages needed. Only the standard library (`csv`, `datetime`) is used.

## How to Run

```bash
python warranty_tracker.py
```

You will see this menu:

```
===== Warranty Tracker =====
1. Add a product     2. View all
3. Expiring soon     4. Search
5. Statistics        0. Exit
```

Type a number and press Enter. Choose `0` to exit.

### Example

```
Choose: 1
Product: Noise Smartwatch
Shop: Croma
Price (Rs): 4999
Purchase date (YYYY-MM-DD, Enter = today): 2026-10-20
Warranty in months: 12
Saved. Warranty for Noise Smartwatch ends on 2027-10-20.
```

## Data Storage

All records are saved to `warranty_tracker.csv` in the folder where you run the program. The file is created automatically on the first save. Each row has these columns:

| Column | Description |
|---|---|
| `id` | Unique number, auto-incremented |
| `product` | Name of the product |
| `shop` | Where it was bought |
| `price` | Price paid in rupees |
| `purchase_date` | Date of purchase (YYYY-MM-DD) |
| `months` | Warranty length in months |
| `expiry_date` | Calculated end of warranty (YYYY-MM-DD) |

## Project Structure

```
.
├── warranty_tracker.py     # the whole application
├── warranty_tracker.csv    # created automatically when you add data
└── README.md
```

## How It Works

- `add_months()` adds calendar months to a date, stepping back day by day when the target month is shorter.
- `days_left()` compares the stored expiry date with today's date.
- `ask()` is a reusable input helper that keeps prompting until the value passes its check.
- Menu choices are mapped to functions in a dictionary, which keeps `main()` short and easy to extend.

## Possible Improvements

- Edit and delete records
- Configurable warning window instead of a fixed 30 days
- Export or import data
- Email or desktop notifications for expiring warranties

## License

Free to use and modify for learning purposes.