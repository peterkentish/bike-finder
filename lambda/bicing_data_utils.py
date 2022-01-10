
def get_station_status_from_id(station_data, id):
    for station in station_data:
            if (station["station_id"]==id):
                return station

def get_num_mechanical_bikes(station_status):
    bikes_by_type =station_status["num_bikes_available_types"]
    mechanical_bikes = int(bikes_by_type["mechanical"])
    return mechanical_bikes

def get_num_electrical_bikes(station_status):
    bikes_by_type =station_status["num_bikes_available_types"]
    e_bikes = int(bikes_by_type["ebike"])
    return e_bikes

def get_speech_output_for_stations(language, station_status, station_id_1, station_id_2, station_id_3):
    first_station_status = get_station_status_from_id(station_status, station_id_1)
    second_station_status = get_station_status_from_id(station_status, station_id_2)
    third_station_status = get_station_status_from_id(station_status, station_id_3)
    

    mechanical_bikes_1 = get_num_mechanical_bikes(first_station_status)
    e_bikes_1 = get_num_electrical_bikes(first_station_status)

    mechanical_bikes_2 = get_num_mechanical_bikes(second_station_status)
    e_bikes_2 = get_num_electrical_bikes(second_station_status)

    mechanical_bikes_3 = get_num_mechanical_bikes(third_station_status)
    e_bikes_3 = get_num_electrical_bikes(third_station_status)

    


    return response_logic(language, mechanical_bikes_1, e_bikes_1, mechanical_bikes_2, e_bikes_2, mechanical_bikes_3, e_bikes_3)



def response_logic(language, mechanical_bikes_1, e_bikes_1, mechanical_bikes_2, e_bikes_2, mechanical_bikes_3, e_bikes_3):
    
    total_bikes = sum([mechanical_bikes_1, e_bikes_1,mechanical_bikes_2, e_bikes_2,mechanical_bikes_3, e_bikes_3])

    #no bikes
    if (total_bikes == 0):
        return language.get_response('main.nobikes')
    #bikes at first station, at multiple elec and multiple mech
    if (mechanical_bikes_1 > 0 and e_bikes_1 > 1):
        return language.get_response('main.closest.both.types').format(mechanical_bikes_1, e_bikes_1)
    #bikes at first station, multiple mech and one elec
    if (mechanical_bikes_1 > 0 and e_bikes_1 == 1):
        return language.get_response('main.closest.both.types.one.electrical').format(mechanical_bikes_1, e_bikes_1)
    # mechanical at closest but no electrical
    output = ""
    if (mechanical_bikes_1 > 0):
        output += language.get_response('main.some.mechanical.no.electrical').format(mechanical_bikes_1)
        output += electrical_bike_finder(e_bikes_2, e_bikes_3, language)
        return output
    # electrical at closest but no mechanical
    if (e_bikes_1 > 0):
        output += language.get_response('main.some.electrical.no.mechanical').format(e_bikes_1)
        output += mechanical_bike_finder(mechanical_bikes_2, mechanical_bikes_3, language)
        return output
    # nothing at closest
    
    output += language.get_response('main.first.station.empty')
    output += electrical_bike_finder(e_bikes_2, e_bikes_3, language)
    output += mechanical_bike_finder(mechanical_bikes_2, mechanical_bikes_3, language)
    return output


    

def electrical_bike_finder(e_bikes_2, e_bikes_3, language):
    output = ""
    if (e_bikes_2 > 0):
        if (e_bikes_2==1):
            output += language.get_response('main.closest.ebike.at.second.solo')
            return output
        else:
            output += language.get_response('main.closest.ebike.at.second.multiple').format(e_bikes_2)
            return output
    elif (e_bikes_3):
        if (e_bikes_3==1):
            output += language.get_response('main.closest.ebike.at.third.solo')
            return output
        else:
            output += language.get_response('main.closest.ebike.at.third.multiple').format(e_bikes_3)
            return output
    output+= language.get_response('main.closest.ebike.not.available')
    return output
    
def mechanical_bike_finder(mechanical_bikes_2, mechanical_bikes_3, language):
    output = ""
    if (mechanical_bikes_2 > 0):
        if (mechanical_bikes_2==1):
            output += language.get_response('main.closest.mbike.at.second.solo')
            return output
        else:
            output += language.get_response('main.closest.mbike.at.second.multiple').format(mechanical_bikes_2)
            return output
    elif (mechanical_bikes_3):
        if (mechanical_bikes_3==1):
            output += language.get_response('main.closest.mbike.at.third.solo')
            return output
        else:
            output += language.get_response('main.closest.mbike.at.third.multiple').format(mechanical_bikes_3)
            return output
    output+= language.get_response('main.closest.mbike.not.available')
    return output
    
    


    

