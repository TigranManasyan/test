# Գրել ծրագիր, որը կորոշի դոմենի IP հասցեն և կստուգի թե արդյոք դոմենի port-ը բաց է թե ոչ

# import socket

# domain = input("Մուտքագրեք դոմենը։ ")
# port = int(input("Մուտքագրեք պորտը: "))

# try:
#     ip_address = socket.gethostbyname(domain) #DNS Lookup
#     print(f"{domain} դոմենի IP հասցեն։ {ip_address}")

#     my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     my_socket.settimeout(3)
#     result = my_socket.connect_ex((ip_address, port))

#     if result == 0:
#         print(f"Port {port}-ը {domain} սերվերի վրա բաց է")
#     else:
#         print(f"Port {port}-ը {domain} սերվերի վրա փակ է")

#     my_socket.close()

# except socket.gaierror:
#     print("Չհաջողվեց որոշել IP հասցեն")
# except Exception as error:
#     print("Սխալ։ ", error)


# Գրել ծրագիր, որը ցույց կտա կիրառողի համակարգչի անվանումը (hostname),  local IP հասցեն ցանցում

# import socket


# try: 
#     hostname = socket.gethostname()
#     local_ip = socket.gethostbyname(hostname)
#     print(f"Համակարգչի անունը։ {hostname}")
#     print(f"Local IP հասցեն։ {local_ip}")

# except Exception as error:
#     print("Սխալ տեղի ունեցավ։ ", error)


# import requests

# API_URL = "https://jsonplaceholder.typicode.com/users"

# try:
#     response = requests.get(API_URL, timeout=5)
#     print(f"Կարգավիճակի կոդ։ {response.status_code}")
#     if response.status_code == 200:
#         print(response)
#         data = response.json()
#         print(data[0]['address'])

#     elif response.status_code == 404:
#         print("Էջը գոյություն չունի")
#     else:
#         print("Ձախողված հարցում")
# except requests.exceptions.RequestException as error:
#     print("Ցանցային սխալ։ {error}")


# Գրել ծրագիր, որը համացանցից ըստ մեր տված հղման կբեռնի նկար

# import urllib.request

# file_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4RBEQiYY1Rvjep735ZK5TAG4t20SqXJt7Eki_puREIaUk-ZxxFTva0bcp&s=10"
# local_filename = "car.jpg"

# try:
#     print("Ֆայլի ներբեռնումը սկսվեց ․․․")
#     urllib.request.urlretrieve(file_url, local_filename)
#     print("Ֆայլը հաջողությամբ բեռնվել է")
# except Exception as error:
#     print("Ներբեռնումը ձախողվեց։ ", error)
