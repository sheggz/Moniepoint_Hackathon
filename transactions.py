from datetime import datetime
from collections import defaultdict
import os
'''
given transaction files, first thing is to read the files and parse them
remember that :

A single line in a transaction file stores information related to 1 transaction in a comma-separated format. The information present is: 
> salesStaffId
> transaction time
> The products sold. (format “[productId1:quantity|productId2:quantity]”)
> sale amount


Example for a line in a transaction file: “4,2025-01-01T16:58:53,[726107:5|553776:5],2114.235”
'''

#say we are given a folder with the text files for all the days in 2024

def process_folder():
    transactions_dir_2024 = input("path to 2024 transactions:")
    for txt_file in os.listdir(transactions_dir_2024):
        if str(txt_file).endswith(".txt"):
            #if str(txt_file) == "cat_input.txt":
            #    continue
            file_path = os.path.join(transactions_dir_2024, txt_file)
            daily_transaction_objs = []
            dailyTransactions = read_transaction_files(file_path)
            for transaction in dailyTransactions:
                daily_transaction_objs.append(process_transaction_line(transaction))
            return daily_transaction_objs

class Transactions:
    def __init__(self, salesStaffId, sale_date, sale_time, productsSold, saleAmount):
        self.salesStaffId = salesStaffId
        self.sale_date = sale_date
        self.sale_time = sale_time
        self.productsSold = productsSold
        self.saleAmount = saleAmount


def read_transaction_files(txtFilePath):
   
    for transaction in txtFilePath:
        with open(txtFilePath, 'r') as file:
            dailyTransactions = file.readlines()
        return dailyTransactions
    
    

#we will process the transactions one by one
def process_transaction_line(transaction):
    transactionParts = transaction.strip().split(',')
    if len(transactionParts) != 4:
        return -1 #incomplete transaction details
    salesStaffId = int(transactionParts[0])
    
    # parse the date and time
    transactionDate_obj = datetime.fromisoformat(transactionParts[1])
    transactionDate = transactionDate_obj.date()
    transactionHour = transactionDate_obj.hour #transactionDate_obj.strftime("%Y-%m")
    
    #parse the products purchased
    products_purchased = {}
    for product in transactionParts[2].strip('[]').split('|'):
        productId, quantity = product.split(':')
        products_purchased[int(productId)] = int(quantity)
    
    saleAmount = float(transactionParts[3])

    return Transactions(salesStaffId, transactionDate,  transactionHour, products_purchased, saleAmount)


'''logic'''
def calculate_metrics(transactions: Transactions):
    daily_sales_volume = defaultdict(int)
    daily_sales_value = defaultdict(float)
    product_sales = defaultdict(int)
    staff_sales = defaultdict(lambda: defaultdict(float))
    hour_sales = defaultdict(lambda: defaultdict(int))
    
    for transaction in transactions:
        
        # Calculate Daily Sales Volume and Value
       
        daily_sales_volume[transaction.sale_date] += sum(transaction.productsSold.values())
        daily_sales_value[transaction.sale_date] += transaction.saleAmount
        
        # Calculate Product Sales by Volume
        for productId, quantity in transaction.productsSold.items():
            product_sales[productId] += quantity
        
        # Calculate Staff Sales (by month)
        #month =    transactionHour.split('T')[0][:7]
        month = transaction.sale_date.month
        #print(month)
        staff_sales[month][transaction.salesStaffId] += transaction.saleAmount
        
        # Calculate Hour Sales Volume
        #hour = transactionHour.split('T')[1][:2]
        hour = transaction.sale_time
        #./print(hour)
        hour_sales[hour]['volume'] += sum(transaction.productsSold.values())
        hour_sales[hour]['transactions'] += 1
    
    return daily_sales_volume, daily_sales_value, product_sales, staff_sales, hour_sales

def report_metrics(daily_sales_volume, daily_sales_value, product_sales, staff_sales, hour_sales):
    # Highest sales volume in a day
    highest_sales_volume_day = max(daily_sales_volume, key=daily_sales_volume.get)
    
    # Highest sales value in a day
    highest_sales_value_day = max(daily_sales_value, key=daily_sales_value.get)
    
    # Most sold product ID by volume
    most_sold_product = max(product_sales, key=product_sales.get)
    
    # Highest sales staff ID for each month
    highest_staff_by_month = {}
    for month, staff_data in staff_sales.items():
        highest_sales_staff = max(staff_data, key=staff_data.get)
        highest_staff_by_month[month] = highest_sales_staff
    
    # Highest hour of the day by average transaction volume
    highest_avg_hour = None
    highest_avg_volume = -1
    for hour, data in hour_sales.items():
        avg_volume = data['volume'] / data['transactions']
        if avg_volume > highest_avg_volume:
            highest_avg_hour = hour
            highest_avg_volume = avg_volume
    
    # Print or return the results
    print(f"Highest sales volume in a day: {highest_sales_volume_day}")
    print(f"Highest sales value in a day: {highest_sales_value_day}")
    print(f"Most sold product ID: {most_sold_product}")
    print(f"Highest sales staff by month: {highest_staff_by_month}")
    print(f"Highest hour of the day by average transaction volume: {highest_avg_hour}")


#def create_transaction_objects():
#    daily_transaction_objs = []
#    dailyTransactions = read_transaction_files(input("Please input the path to the '.txt' file:"))
#    
#    for transaction in dailyTransactions:
#        daily_transaction_objs.append(process_transaction_line(transaction))
#    return daily_transaction_objs

#calculate 



print(report_metrics(*calculate_metrics(process_folder())))

#print(process_folder())
#dailyTransactions = read_transaction_files(input("Please input the path to the '.txt' file:"))
#
#for i in dailyTransactions:
#    print(process_transaction_line(i))
##print(read_transaction_files("./mp-hackathon-sample-data/test-case-1/2025-01-01.txt"))
#"./mp-hackathon-sample-data/test-case-1/2025-01-01.txt"


