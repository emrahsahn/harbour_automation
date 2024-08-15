import chardet
import pandas as pd


class Truck:
    def __init__(self, gelis_zamani, plaka, ulke, ton20, ton30, yuk_miktari, maliyet):
        '''Creates the truck object and stores various properties of the truck'''
        self.arrival_time = gelis_zamani
        self.plaque = plaka
        self.country = ulke
        self.ton20 = ton20
        self.ton30 = ton30
        self.load_quantity = yuk_miktari
        self.cost = maliyet

        # collects the characteristics of the truck in a dictionary
        self.info = {
            "country": self.country,
            "ton20": self.ton20,
            "ton30": self.ton30,
            "load_quantity": self.load_quantity,
            "cost": self.cost,
        }

    def get_info(self):
        return self.info


truck = Truck


class Ship:

    def __init__(self, gelis_zamani, gemi_adi, kapasite, gidilecek_ulke):
        '''Creates the ship object and stores various characteristics of the ship'''
        self.arrival_time = gelis_zamani
        self.name_ship = gemi_adi
        self.capacity = kapasite
        self.destination_country = gidilecek_ulke
        self.load = 0

        # collects the characteristics of the ships in a dictionary
        self.info = {
            "arrival_time": self.arrival_time,
            "name_ship": self.name_ship,
            "capacity": self.capacity,
            "destination_country": self.destination_country,
            "load_list": self.load
        }

    def load_update(self, load):
        '''The ship updates its load, if it exceeds the capacity, the load cannot be added'''
        if self.load + load <= self.capacity:
            self.load += load
            return True
        else:
            return False

    def get_info(self):
        # Returns ship information
        return self.info


def chardet_encoding(file_path):
    '''Detects the character encoding of the file'''
    with open(file_path, "rb") as file:  # rb means that it will read the file in binary mode
        result = chardet.detect(file.read())  # analyzes the file content and detects its encoding
    return result["encoding"]


def time_and_plaque_sort_of_truck(truck):
    '''The function that sorts trucks according to arrival time and license plate number'''
    arrival_time = truck[0]
    plaque = truck[1]
    number_part = plaque.split("_")[-1]
    # the plate was separated and sorted according to the last 4 digits
    return (arrival_time, int(number_part))


greatest_value = 0
'''Global variable: Decrypts the maximum time to be used between functions'''


def read_file_truck():
    '''Reads trucks from the file, sorts them and converts them into Truck objects'''
    global greatest_value
    encodings = chardet_encoding("olaylar.csv")
    data = pd.read_csv("olaylar.csv", encoding=f"{encodings}")
    titles = data.columns
    greatest_value = data[titles[0]].max()

    # aynı zamanda gelen tırları plaka sırasına göre sıralama yaptık
    data[titles[1]] = data[titles[1]]
    data = data.sort_values(by=[titles[0], titles[1]])
    data = sorted(data.values.tolist(), key=time_and_plaque_sort_of_truck)
    return [Truck(*row) for row in data]  # bu satır bir for iteration satırıdır


def read_file_ship():
    '''Reads ships from the file and converts them into Ship objects'''
    encodings = chardet_encoding("gemiler.csv")
    data = pd.read_csv("gemiler.csv", encoding=encodings)
    titles = data.columns

    data = data.to_dict(orient='records')  # bu sayede her satırı temsil eden bir sözlüğün listesini olur
    return [Ship(ship[titles[0]], ship[titles[1]], int(ship[titles[2]]), ship[titles[3]]) for ship in data]


# gemiler_objeleri = [Ship(ship["geliþ_zamaný"], ship["gemi_adý"], int(ship["kapasite"]), ship["gidecek_ülke"])
#                     for ship in load_list]

max_capacity = 750

stack_area_capacity1 = []
stack_area_capacity2 = []
current_load1 = 0
current_load2 = 0


# fonksiyonların içinde kullanılacağı için fonksiyonların dışında tanımlanan değişkenler

def load_download(truck):
    '''Octavo unloads the cargo from the truck and adds it to the stowage area'''
    global current_load1
    # Tır dan yükü indirip istif alanı 1 e yığın olarak ekliyorum.
    if current_load1 + truck.load_quantity <= max_capacity:
        stack_area_capacity1.append(truck.get_info())
        current_load1 += truck.load_quantity
        print(f"İstif alanı 1'e {truck.load_quantity} ton yük {truck.country} ülkesine gidecek şekilde eklendi")
    else:
        # load is placed on only one stack area because the other stack area is the first stack area
        # he provides for her needs.
        print("İstif alanı 1 kapasite dolu, yük eklenemiyor.")


def load_upload(ship):
    '''Allows the ship to pick up cargo from the stowage area'''
    global current_load1, current_load2
    while stack_area_capacity1 and ship.load < ship.capacity:

        # First, we take the element at the top of the cargoes sorted in bulk
        top_load = stack_area_capacity1.pop()
        current_load1 -= top_load["load_quantity"]
        # Then we reduce the current storage area from the total capacity in 1.

        if ship.load_update(top_load["load_quantity"]):
            print(f"Gemi {ship.name_ship} yüklendi: {top_load['load_quantity']} ton ")
            if ship.capacity * 0.95 <= ship.load:
                print(f"Gemi {ship.name_ship} yeterli doluluk düzeyine ulaştı ve gitti.")
            else:
                print(f"Gemi {ship.name_ship} beklemede")
        else:
            # If the ship is full, transfer the cargo to stowage area 2.
            if current_load2 + top_load["load_quantity"] <= max_capacity:
                stack_area_capacity2.append(top_load)
                current_load2 += top_load["load_quantity"]
                print(f"Gemi {ship.name_ship} dolu. Yük istif alanı 2'ye aktarıldı.")
            else:
                print("İstif alanı 2 kapasite dolu, yük eklenemiyor.")


def total_price():
    encodings = chardet_encoding("olaylar.csv")
    data = pd.read_csv("olaylar.csv",encoding=encodings)
    titles = data.columns

    total = data[titles[-1]].sum()
    return f"Şuana kadarki toplam maliyet bu kadar {total}"

total_cost = total_price()

def simulation(trucks, ships):
    global stack_area_capacity1, stack_area_capacity2, current_load1, current_load2
    ships_waiting = {}  # A dictionary that will keep ships waiting by country

    for time in range(greatest_value + 1):
        print(f"Zaman {time}")

        # Find the trucks that arrived at that time
        arriving_trucks = []
        for truck in trucks:
            if truck.arrival_time == time:
                arriving_trucks.append(truck)

        # Don't download loads from trucks arriving at that time
        for truck in arriving_trucks:
            load_download(truck)

        # Find the ships that arrived at the current time and add them to the waiting ships October
        arriving_ships = []
        for ship in ships:
            if ship.arrival_time == time:
                arriving_ships.append(ship)

        # Upload incoming ships to the waiting ships list
        for ship in arriving_ships:
            if ship.destination_country not in ships_waiting:
                ships_waiting[ship.destination_country] = []
            ships_waiting[ship.destination_country].append(ship)

        # Load the cargo in stowage area 1 to the appropriate ships
        for country, waiting_ships in list(ships_waiting.items()):
            for ship in waiting_ships:
                while stack_area_capacity1 and ship.load < ship.capacity:
                    # Check before loading from stowage area 1
                    if not stack_area_capacity1:
                        break  # If stack area 1 is empty, break the loop

                    top_load = stack_area_capacity1[-1]
                    if top_load["country"] == country:
                        # Search according to the desired country Dec
                        if ship.load_update(top_load["load_quantity"]):
                            stack_area_capacity1.pop()  # Take the load off the pile
                            current_load1 -= top_load["load_quantity"]
                            print(f"Gemi {ship.name_ship} yüklendi: {top_load['load_quantity']} ton")

                            if ship.capacity * 0.95 <= ship.load:
                                # If the ship has reached sufficient occupancy level, send it, switch to the new ship and delete the old ship from the list
                                print(f"Gemi {ship.name_ship} yeterli doluluk düzeyine ulaştı ve gitti.")
                                waiting_ships.remove(ship)
                                break  # Get to the other ships
                        else:
                            # If the ship is full or cannot be loaded, break the loop and start the loop again
                            break
                    else:
                        # If it is not the desired load, move the load to the temporary stack
                        stack_area_capacity2.append(stack_area_capacity1.pop())
                        current_load1 -= top_load["load_quantity"]
                        # print(f"İstif alanı 2'ye {top_load['load_quantity']} yük eklendi")

                while stack_area_capacity2:
                    # Restore the temporary stack to stack area 1
                    load = stack_area_capacity2.pop()
                    stack_area_capacity1.append(load)
                    current_load1 += load["load_quantity"]

        # Clear the unloaded ships
        new_ships_waiting = {}
        for country, ship_list in ships_waiting.items():
            if ship_list:
                new_ships_waiting[country] = ship_list

    # Printing the results
    print("İstif alanı 1: ", stack_area_capacity1)
    print("İstif alanı 2: ", stack_area_capacity2)
    for ship in ships:
        print(f"Gemi {ship.name_ship}: {ship.load} ton yüklendi")
    print("Toplam Maliyet: ",total_cost)

trucks = read_file_truck()
ships = read_file_ship()
simulation(trucks, ships)