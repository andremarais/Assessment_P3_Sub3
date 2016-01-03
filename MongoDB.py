
from pymongo import MongoClient
import pprint

client = MongoClient("localhost", 27017)
coll = client.CT.CT2


def aggregate(db, pipeline):
    return [doc for doc in db.aggregate(pipeline)]


pipeline_postcodes = [{"$match":{"address.postcode":{"$exists":1}}},
                      {"$group": {"_id":"$address.postcode", "count":{"$sum":1}}},
                      {"$sort" : {"count":-1}},
                      {"$limit" : 5}]

print 'Postcodes'
pprint.pprint(aggregate(coll, pipeline_postcodes))
print ''
"""
Postcode range falls into the expected range, with no postcodes in the wrong format
According to https://en.wikipedia.org/wiki/List_of_postal_codes_in_South_Africa, Cape Town and Cape Peninsula postcodes
range between 7100 and 8099
"""

pipeline_cities = [{"$match":{"address.city":{"$exists":1}}},
                   {"$group":{"_id":"$address.city", "count":{"$sum":1}}},
                   {"$sort":{"count":-1}},
                      {"$limit" : 5}]
print 'Cities'
pprint.pprint(aggregate(coll, pipeline_cities))
print ''

"""
Odd that Pinelands is the most frequent city name, but it coincided with the post codes.
I expected more....Cape Towns. Need to see if there is a reason why
"""

pipeline_users = [{"$match":{"address.city":{"$exists":1}}},
                   {"$group":{"_id":"$created.user", "count":{"$sum":1}}},
                   {"$sort":{"count":-1}},
                      {"$limit" : 5}]

print 'Top users'
pprint.pprint(aggregate(coll, pipeline_users))
print ''

"""
Adrian Frith is by far the most active user. After a quick google search, you can see he's big into GIS and data :)
This might also explain why the data is so clean, the 'human' working on this data is someone who works with map data
and a frequent basis.
"""

pipeline_users_per_city = [{"$match":{"address.city":{"$exists":1}}},
                   {"$group": {"_id": {"user" : "$created.user",
                                       "city" : "$address.city"},
                               "count":{"$sum":1}}},
                   {"$sort":{"count":-1}},
                      {"$limit" : 5}]

print 'Top users per city'
pprint.pprint(aggregate(coll, pipeline_users_per_city))
print ''

"""
I have a hunch Adrian either lives in Pinelands, or he loves the area very much. But either way, this might be the
reason we see so Pinelands so much more than Cape Town.
"""

pipeline_street_names = [{"$match":{"address.city":{"$exists":1}}},
                         {"$group":{"_id":"$address.street", "count":{"$sum":1}}},
                         {"$sort":{"count":-1}},
                         {"$limit" : 10}]


print 'Streetnames'
pprint.pprint(aggregate(coll, pipeline_street_names))
print ''

pipeline_street_names_by_city = [{"$match":{"address.city":'Pinelands',}},
                         {"$group":{"_id": {"street name" : "$address.street"}, "count":{"$sum":1}}},
                         {"$sort":{"count":-1}},
                         {"$limit" : 10}]


print 'Streetnames in Pinelands'
pprint.pprint(aggregate(coll, pipeline_street_names_by_city))
print ''

"""
Some nature themed street names in Pinelands, which isn't too surprising. Pine..lands, sunny, ringwood, forest etc
"""

a = 0
pc = aggregate(coll, pipeline_postcodes)
for p in pc:
    a = a + p['count']
print 'Postcode 7405 frequency'
print float(pc[0]['count'])/ a


a = 0
usr = aggregate(coll, pipeline_users)
for p in usr:
    a = a + p['count']
print 'Top user activity'
print float(usr[0]['count'])/ a
print usr
print ''
pipeline_count_types = [{"$group" : {"_id" : "$type",
                                     "count" : {"$sum" : 1}}},
                        {"$sort" : {"count" : -1}}]
pprint.pprint((aggregate(coll, pipeline_count_types)))
print ''


pipeline_amenity = [{"$match":{"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity",
"count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}]

pprint.pprint((aggregate(coll, pipeline_amenity)))


pipeline_restaurants = [{"$match":{"amenity":"fast_food"}},
                        {"$group":{"_id":"$name", "count":{"$sum":1}}},
                        {"$sort":{"count":-1}}]
print ""
pprint.pprint((aggregate(coll, pipeline_restaurants)))

pipeline_restaurants = [{"$match":{"amenity":"restaurant"}},
                        {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},
                        {"$sort":{"count":-1}}]
print ""
pprint.pprint((aggregate(coll, pipeline_restaurants)))

pipeline_worship = [{"$match":{"amenity":"place_of_worship"}},
                        {"$group":{"_id":"$religion", "count":{"$sum":1}}},
                        {"$sort":{"count":-1}}]


print ""
pprint.pprint((aggregate(coll, pipeline_worship)))

# this I got from stackoverflow
# http://stackoverflow.com/questions/11782566/mongodb-select-countdistinct-x-on-an-indexed-column-count-unique-results-for


pipeline_users2 = [{"$match" :{"address.city":{"$exists":1}}},
                   {"$group" :{"_id":"$created.user", "count" : {"$sum": 1}}},
                   {"$match" : {"count" : {"$gt": 5}}},
                   {"$group" : {"_id" : 1, "count" : {"$sum" : 1}}}]

print ""
pprint.pprint((aggregate(coll, pipeline_users2)))