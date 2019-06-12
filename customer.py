# import CSV reader
import csv

unused_barcodes = 0


def find_key(item_dict, item_val):
    """
    Returns the last key found in a dictionary
    given a some value
    """
    result = None
    for key, val in item_dict.items():
        if val == item_val:
            result = key
    return result


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

# Create top customers dictionary
top_customers = dict()

# generate output csv file
with open('results.csv', 'w') as results_csv:
    fieldnames = ['customer_id', 'order_id', 'barcodes']
    writer = csv.DictWriter(results_csv, fieldnames=fieldnames)
    writer.writeheader()

    for customer_id in customer_set:
        orders = customer_set[customer_id]
        ticket_count = 0

        for order in orders:
            # Get order_ids and barcodes from the order dictionary
            order_id = list(order.keys())[0]
            barcode_list = [int(x) for x in list(order.values())[0]]

            # Write line by line to the CSV file
            writer.writerow({
                'customer_id': customer_id,
                'order_id': order_id,
                'barcodes': barcode_list
            })

            # Increment ticket counter
            ticket_count += len(barcode_list)

        if len(top_customers) >= 5:
            min_tickets = min(top_customers.values())
            if ticket_count > min_tickets:
                to_remove = find_key(top_customers, min_tickets)
                top_customers.pop(to_remove)
                top_customers[customer_id] = ticket_count
        else:
            top_customers[customer_id] = ticket_count

# print top customers
print("\nThe top 5 customers are: ")
for customer_id, tickets in sorted(top_customers.items()):
    print("Customer ID: {} - Tickets bought: {}".format(customer_id, tickets))
print("")  # new line

# print unused barcodes
print("Unused barcodes: {}".format(unused_barcodes))
