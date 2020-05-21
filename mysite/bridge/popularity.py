import math
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import get_object_or_404, render
from .models import Bridge
from django.urls import reverse


def top_five_pop_bridges(lat, long):
    """
    this function will find the top 5 most popular bridges out of the closest bridges to the user
    :param lat: user latitude
    :param long: user longitude
    :return: list with top 5 bridges based on traffic
    """
    user_location = [lat, long]
    user_lat = user_location[0]
    user_long = user_location[1]
    # user location information

    with open('whatsthatbridgedata.csv') as f:
        file_reader = csv.reader(f)

        ranking_list = []
        for i in file_reader:
            bridge_latitude = i[0]
            bridge_longitude = i[1]

            R = 6373.0
            # Radius of the Earth
            popularity_num = float(i[2])
            # daily traffic numbers

            bridge_location = [bridge_latitude, bridge_longitude]
            bridge_lat = radians(float(bridge_location[0]))
            bridge_long = radians(float(bridge_location[1]))
            # bridge location

            distance_lat = bridge_lat - user_lat
            distance_long = bridge_long - user_long
            a = sin(distance_lat / 2) ** 2 + cos(user_lat) * cos(bridge_lat) * sin(distance_long / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            # calculates distance of bridges from user

            distance_to_user = float(R * c)
            ranking_info = [i[3], distance_to_user, popularity_num]
            # returns bridge name, distance from user, and daily use number
            ranking_list.append(ranking_info)

    ranking_list.sort(key=lambda ranking_list: ranking_list[1])
    f.close()
    top_five_list = ranking_list[:5]
    top_five_list.sort(key=lambda top_five_list: top_five_list[2], reverse=True)
    htmlfile = open('index.html', w)
    htmlfile.write('<table>' + '<tr>' + '<th>' + 'First' + '</th>' + '<th>' + 'Second' + '</th>' + '<th>' + 'Third' + '</th>'
                   + '<th>' + 'Fourth' + '</th>'
                   + '<th>' + 'Fifth' + '</th>' + '</tr>' + '<tr>')
    for i in top_five_list:
        htmlfile.write('<td>' + top_five_list[i][0] + '</td>')
    htmlfile.write('</tr>' + '</table>')
    return HttpResponseRedirect(reverse('bridge:index'))
