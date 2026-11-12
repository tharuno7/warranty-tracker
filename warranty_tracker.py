"""Warranty Tracker (csv + datetime): logs gadgets and warns before warranties expire."""
import csv
from datetime import date

FILE = "warranty_tracker.csv"
FIELDS = ["id", "product", "shop", "price", "purchase_date", "months", "expiry_date"]


def add_months(d, months):
    year, month = divmod(d.year * 12 + d.month - 1 + months, 12)
    day = d.day
    while True:
        try:
            return d.replace(year=year, month=month + 1, day=day)
        except ValueError:
            day -= 1  # 31 Jan + 1 month -> 28 Feb


def days_left(r):
    return (date.fromisoformat(r["expiry_date"]) - date.today()).days


def load_rows():
    try:
        with open(FILE, newline="") as f:
            rows = list(csv.DictReader(f))
    except FileNotFoundError:
        return []
    for r in rows:  # csv gives text, so convert numbers back
        r["id"], r["price"], r["months"] = int(r["id"]), float(r["price"]), int(r["months"])
    return rows


def save_rows(rows):
    with open(FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def ask(prompt, kind=str, check=bool, error="Invalid input, try again."):
    while True:
        try:
            value = kind(input(prompt).strip())
            if check(value):
                return value
        except ValueError:
            pass
        print(" ", error)


def show(rows):
    if not rows:
        return print("Nothing found.")
    print(f"\n{'ID':<4}{'Product':<18}{'Shop':<12}{'Price':<9}{'Expiry':<12}Warranty")
    for r in rows:
        d = days_left(r)
        left = f"{d} day(s) left" if d >= 0 else f"Expired {-d} day(s) ago"
        print(f"{r['id']:<4}{r['product'][:17]:<18}{r['shop'][:11]:<12}"
              f"{r['price']:<9.0f}{r['expiry_date']:<12}{left}")


def add_product(rows):
    product = ask("Product: ", error="Cannot be empty.")
    shop = ask("Shop: ", error="Cannot be empty.")
    price = ask("Price (Rs): ", float, lambda v: v > 0, "Enter a number above 0.")
    bought = ask("Purchase date (YYYY-MM-DD, Enter = today): ",
                 lambda s: date.fromisoformat(s) if s else date.today(),
                 lambda d: d <= date.today(), "Use a real date, not in the future.")
    months = ask("Warranty in months: ", int, lambda v: 1 <= v <= 120, "Enter 1 to 120.")
    expiry = add_months(bought, months)
    rows.append({"id": max((r["id"] for r in rows), default=0) + 1, "product": product,
                 "shop": shop, "price": price, "purchase_date": str(bought),
                 "months": months, "expiry_date": str(expiry)})
    save_rows(rows)
    print(f"Saved. Warranty for {product} ends on {expiry}.")


def expiring_soon(rows):
    print("Warranties ending within 30 days:")
    show(sorted([r for r in rows if 0 <= days_left(r) <= 30], key=days_left))


def search(rows):
    word = ask("Search product or shop: ", error="Cannot be empty.").lower()
    show([r for r in rows if word in (r["product"] + r["shop"]).lower()])


def stats(rows):
    if not rows:
        return print("No products yet.")
    active = [r for r in rows if days_left(r) >= 0]
    print(f"\nProducts: {len(rows)}  |  Total spent: Rs {sum(r['price'] for r in rows):.0f}")
    print(f"Under warranty: {len(active)}  |  Expired: {len(rows) - len(active)}")
    if active:
        nxt = min(active, key=days_left)
        print(f"Next to expire: {nxt['product']} in {days_left(nxt)} day(s)")


MENU = """
===== Warranty Tracker =====
1. Add a product     2. View all
3. Expiring soon     4. Search
5. Statistics        0. Exit"""


def main():
    rows = load_rows()
    actions = {"1": add_product, "2": lambda r: show(sorted(r, key=days_left)),
               "3": expiring_soon, "4": search, "5": stats}
    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        if choice == "0":
            return print("Never lose a warranty again!")
        actions.get(choice, lambda r: print("Invalid choice."))(rows)


if __name__ == "__main__":
    main()
