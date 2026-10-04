import re
import json
with open("practice5/receipt.txt", "r", encoding="utf-8") as file:
    text=file.read()
print(text)
#all prices
prices=re.findall(r'\d+[.,]\d{2}', text)
print(prices)
#find all product names
products=re.findall(r'\d+\\\.\s*\n?(.*?)(?=\n\d+[.,]?\d*\s*x)',text)
print(products)
#total
items = re.findall(r'(\d+,\d+)\s*x\s*([\d\s]+,\d{2})', text)

total = 0

for quantity, price in items:
    quantity = float(quantity.replace(',', '.'))
    price = float(price.replace(' ', '').replace(',', '.'))
    total += quantity * price

print(total)

#date time
date_time=re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})', text)
if date_time:
    print(date_time.group(1))

#payment method
payment = re.search(r'(Банковская карта)', text)

if payment:
    print(payment.group(1))

#json
receipt = {
    "products": products,
    "prices": prices,
    "total": total,
    "date": date_time.group(1),
    "time": date_time.group(2),
    "payment_method": payment.group(1)
}

print(json.dumps(receipt, ensure_ascii=False, indent=4))