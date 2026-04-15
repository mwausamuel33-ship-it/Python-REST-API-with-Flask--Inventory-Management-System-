import requests
base="http://localhost:5000"
def menu():
    print("1. View all\n2. View one\n3. Add\n6. Search API\n7. Exit")
    return input("Choose: ")
while True:
    c=menu()
    if c=="1":
        r=requests.get(f"{base}/inventory")
        print(r.json())
    elif c=="2":
        id=input("ID: ")
        r=requests.get(f"{base}/inventory/{id}")
        print(r.json())
    elif c=="3":
        n=input("Name: ")
        b=input("Brand: ")
        p=float(input("Price: "))
        q=int(input("Qty: "))
        d={"product_name":n,"brands":b,"price":p,"quantity":q}
        r=requests.post(f"{base}/inventory",json=d)
        print(r.json())
    elif c=="6":
        t=input("Search by (b)arcode or (n)ame: ")
        if t=="b":
            bc=input("Barcode: ")
            d={"barcode":bc}
        elif t=="n":
            n=input("Name: ")
            d={"product_name":n}
        r=requests.post(f"{base}/search-external",json=d)
        print(r.json())
    elif c=="7":
        break
    else:
        print("Invalid")
