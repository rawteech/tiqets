# import CSV reader
import csv

unused_barcodes = 0

# create a dictionary to hold sorted grouped orders
order_set = dict()
# read data from barcodes file
with open('barcodes.csv') as barcode_csv:
    barcode_dict = csv.DictReader(barcode_csv)
    for item in barcode_dict:
        barcode = item['barcode']
        order_id = item['order_id']

        # validate for barcodes unused
        if order_id == '':
            unused_barcodes += 1
            continue

        if order_id in order_set:
            # validate for duplicate barcodes
            if barcode in order_set[order_id]:
                print("Error: duplicate barcode {}".format(barcode))
                continue
            order_set[order_id].append(barcode)
        else:
            order_set[order_id] = [barcode]

# create a dictionary to hold customers and orders
customer_set = dict()

# read from orders file
with open('orders.csv') as order_csv:
    order_dict = csv.DictReader(order_csv)
    for item in order_dict:
        order_id = item['order_id']
        customer_id = item['customer_id']

        try:
            # get order with barcodes with no duplicates
            current_order = {order_id: order_set[order_id]}
        except KeyError:
            print(
                "Error: Order number - {} has no barcodes".format(order_id))
            continue

        if customer_id in customer_set:
            customer_set[customer_id].append(current_order)
        else:
            customer_set[customer_id] = [current_order]

# generate output csv file
with open('results.csv', 'w') as results_csv:
    fieldnames = ['customer_id', 'order_id', 'barcodes']
    writer = csv.DictWriter(results_csv, fieldnames=fieldnames)
    writer.writeheader()

    for customer_id in customer_set:
        orders = customer_set[customer_id]
        for order in orders:
            writer.writerow({
                'customer_id': customer_id,
                'order_id': list(order.keys())[0],
                'barcodes': [int(x) for x in list(order.values())[0]]
            })

# print unused barcodes
print("Unused barcodes: {}".format(unused_barcodes))