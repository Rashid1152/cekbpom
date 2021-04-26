import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import csv
import headers_cookies
import mysql.connector


def products_soup():
    '''
    get HTML of product page and make soup of it for parsing data
    '''
    response = requests.get('https://cekbpom.pom.go.id/index.php/home/produk/ducn7gn6h5ihcem28sn1k44550/all/row/1300/page/1/order/4/DESC/search/6/mandiri', headers=headers, cookies=cookies)
    return BeautifulSoup(response.text, 'html.parser')

def detail_soup(id):
    '''
    get HTML of each product and make soup of it for parsing data
    '''

    response = requests.get(f'https://cekbpom.pom.go.id/index.php/home/detil/ducn7gn6h5ihcem28sn1k44550/produk/{id}', headers=headers, cookies=cookies, timeout=5)
    return BeautifulSoup(response.text, 'html.parser')


def get_exact_value(soup, value):
    '''
    we have all table row, we need to find our required field from it, this function
    will help us
    '''

    for tr in soup.select('tr'):
        is_value = tr.select('td')[0].text.strip()
        if is_value == value:
            return tr.select('td')[1].text.strip()
    return ''

def get_location(soup, element):
    '''
    this method will get only address from company name
    '''
    try:
        location = get_exact_value(soup, element).split('-')[1].strip()
    except:
        location = ''
    
    return location


def get_product_details(soup):
    '''
    parsing fields from Beautifulsoup soup and saving into different variables 
    '''
    product_id = get_exact_value(soup, 'Nomor Registrasi')
    product = get_exact_value(soup, 'Produk')
    product_name = get_exact_value(soup, 'Nama Produk')
    brand = get_exact_value(soup, 'Merk')

    registrant = get_exact_value(soup, 'Pendaftar').split('-')[0].strip()
    if not registrant:
        registrant = get_exact_value(soup, 'Pendaftar & Importir').split('-')[0].strip()

    producer = get_exact_value(soup, 'Diproduksi Oleh').split('-')[0].replace('.,','').replace(',','').strip()
    location = get_location(soup, 'Diproduksi Oleh')
    if not producer:
        producer = get_exact_value(soup, 'Pabrik').split('-')[0].strip()
        location = get_location(soup, 'Pabrik')

    issue_date = get_exact_value(soup, 'Tanggal Terbit')
    if not issue_date:
        issue_date = get_exact_value(soup, 'Masa Berlaku s/d')
        

    return product_id, product, product_name, brand, registrant, producer, issue_date, location

def make_mysql_connection():
    '''
    Making connection with mysql database
    '''
    myConnection = mysql.connector.connect(host='rashid786.mysql.pythonanywhere-services.com', 
                                           user='rashid786', 
                                           db='rashid786$cekbpom', 
                                           password='innersql786')
    cur_sor=myConnection.cursor()

    return myConnection, cur_sor

def insert_data(product_id, type, name, brand, registrant, producer, validity, location):
    '''
    create insert a insert query and dump data into product table
    '''
    sql = "INSERT INTO app_product(registration_no,type,name,brand,registrant,producer,validity,location) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (product_id, type, name, brand, registrant, producer, validity, location)
    cur_sor.execute(sql, val)
    myConnection.commit()

def write_file():
    '''
    additional: this method will write data into csv file as well
    '''
    f = open('data.csv', 'w', newline='', encoding='utf-8')
    writer = csv.writer(f)
    writer.writerow(['product_id', 'Product','Product Name', 'Brand', 'Registrant', 'Producer', 'Validity', 'location'])

    return f, writer


# create a object for translating products name into english 
# translator = Translator() 

# make objects of mysql
myConnection, cur_sor = make_mysql_connection()

# get headers and cookies for making get requests
headers, cookies = headers_cookies.get()

# f, writer = write_file()
counter = 1

soup_1 = products_soup()

# get product unique ids and put loop on it
for i in soup_1.select('[urldetil]'):
    id = i.get('urldetil')[1:]

    # make soup of each product
    soup_2 = detail_soup(id)
    
    # get product details from soup2
    product_id, product, product_name, brand, registrant, producer, issue_date, location = get_product_details(soup_2)

    # inserting rows into mysql table
    insert_data(product_id, product, product_name, brand, registrant, producer, issue_date, location)
    
    print(f'{counter} - {id} - dumped..!')
    counter += 1


# writer.writerow([product_id, product, product_name, brand, registrant, producer, issue_date, location])