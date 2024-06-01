import csv, folium

def get_state_info(state):
    file = open('starbucks_2018_11_06.csv', 'r', encoding="UTF-8")
    reader = csv.reader(file)
    state_info = []
    for row in reader:
        if row[4] == state:
            state_info.append(row)
    return state_info

def get_lat_long(state_info, m):
    i = 0
    coord_arr = []
    for row in state_info:            
            lat_long = [float(row[15]),float(row[16])]
            coord_arr.append(lat_long)

            # Tag shops on the map
            folium.Marker(location=lat_long, popup="{}. {}".format(i, row[0]), icon=folium.Icon(icon='cloud')).add_to(m)

            i += 1

    return coord_arr