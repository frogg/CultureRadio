import os
from .models import Location
import csv



cities = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/cities1000.txt'))


def run(verbose=True):
    with open(cities, newline='', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        csv_reader.__next__()

        for row in csv_reader:
            loc = Location(name=row[1], geom="POINT ({} {})".format(row[4], row[5]), population=row[14])
            loc.save()