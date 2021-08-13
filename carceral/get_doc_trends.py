"""Scrape prison population figures from Wisconsin Dept. of Corrections (DOC)

Note: DOC breaks these statistics down in a male/female gender binary,
which is unforutnately reflected below. Percentages calculated here are
relative to the state's reported design capacity in each category.
"""

import json
import os.path
import tabula
import tqdm

from datetime import (datetime, timedelta)

# global data object
POPULATION_DATA = {
    # basic summary
    "publication_date": [],
    "probation_parole_total": [],
    "inmate_total": [],
    "inmate_total_percentage": [],
    "facility_youth_total": [],
    "facility_youth_percentage": [],
    "field_youth_total": [],
    # incarcerated youth
    "copper_lake_count": [],
    "copper_lake_percentage": [],
    "ethan_allen_count": [],
    "ethan_allen_percentage": [],
    "grow_academy_count": [],
    "grow_academy_percentage": [],
    "lincoln_hills_count": [],
    "lincoln_hills_percentage": [],
    "mendota_count": [],
    "mendota_percentage": [],
    "southern_oaks_count": [],
    "southern_oaks_percentage": [],
    # incarcerated adult males
    "male_inmate_count": [],
    "male_inmate_percentage": [],
    "male_maximum_security_count": [],
    "male_maximum_security_percentage": [],
    "male_medium_security_count": [],
    "male_medium_security_percentage": [],
    "male_minimum_security_count": [],
    "male_minimum_security_percentage": [],
    # incarcerated adult females
    "female_inmate_count": [],
    "female_inmate_percentage": [],
    "female_minimum_security_count": [],
    "female_minimum_security_percentage": [],
}
SOURCE_URL = "https://doc.wi.gov/DataResearch/WeeklyPopulationReports"


# -- utilities ----------------------------------------------------------------

def _parse_int(qty):
    if isinstance(qty, str):
        return int(qty.replace(",", ""))
    try:
        return int(qty)
    except ValueError:
        return qty


def _get_filename(date):
    base = (
        date.strftime("%Y.%m.%d")
        if date < datetime(2016, 1, 1)
        else date.strftime("%m%d%Y")
    )
    source = (
        os.path.join(str(date.year), f"{base}.pdf")
        if date < datetime(2021, 1, 1)
        else f"{SOURCE_URL}/{base}.pdf"
    )
    # handle special case for federal holidays
    if not source.startswith(SOURCE_URL) and not os.path.exists(source):
        return _get_filename(date - timedelta(days=1))
    return source


def _get_row_index(frame, search):
    return [
        i for (i, item) in enumerate(frame[frame.keys()[0]])
        if isinstance(item, str) and (search in item)
    ][0]


def _attempt_search_with_fallback(frame, col, search, target=None):
    count = frame.keys()[col]
    cap = frame.keys()[col - 1]
    target = target or search.lower().replace(" ", "_")
    try:
        idx = _get_row_index(frame, search)
        POPULATION_DATA[f"{target}_count"].append(
            _parse_int(frame[count][idx]),
        )
        POPULATION_DATA[f"{target}_percentage"].append(
            100 * _parse_int(frame[count][idx]) / _parse_int(frame[cap][idx]),
        )
    except IndexError:  # entry was not found
        POPULATION_DATA[f"{target}_count"].append(0)
        POPULATION_DATA[f"{target}_percentage"].append(0)


def get_publication_dates(year=2008, month=1, day=4):
    """Construct calendar dates for all publications in a given year"""
    (dates, files) = ([], [])
    dateobj = datetime(year, month, day)
    while dateobj < datetime.now():
        if dateobj == datetime(2013, 1, 4):
            dateobj += timedelta(days=7)  # malformed data file
        dates.append(dateobj.strftime("%m-%d-%Y"))
        files.append(_get_filename(dateobj))
        dateobj += timedelta(days=7)
    return (dates, files)


def parse_totals(data):
    """Parse total population figures from scraped data"""
    # get frame and first data point
    frame = data[0]
    parole = frame.keys()[1]

    # misc. raw total population trends
    POPULATION_DATA["probation_parole_total"].append(
        _parse_int(parole),
    )
    POPULATION_DATA["field_youth_total"].append(
        _parse_int(frame[parole][2]),
    )


def parse_incarcerated_males(data):
    """Parse incarcerated male population figures from scraped data"""
    # get frame and first data point
    frame = [df for df in data if df.columns[0] == "ADULT INSTITUTIONS"][0]

    # total adult population
    POPULATION_DATA["inmate_total"].append(
        _parse_int(frame.keys()[2]),
    )
    POPULATION_DATA["inmate_total_percentage"].append(
        100 * _parse_int(frame.keys()[2]) / _parse_int(frame.keys()[1]),
    )

    # total male population
    _attempt_search_with_fallback(frame, 2, "SUBTOTAL-MALES",
                                  target="male_inmate")

    # maximum security facilities
    _attempt_search_with_fallback(frame, 2, "MAXIMUM SECURITY",
                                  target="male_maximum_security")

    # medium security facilities
    _attempt_search_with_fallback(frame, 2, "MEDIUM SECURITY",
                                  target="male_medium_security")

    # minimum security facilities
    _attempt_search_with_fallback(frame, 2, "MINIMUM SECURITY",
                                  target="male_minimum_security")


def parse_incarcerated_females(data):
    """Parse incarcerated female population figures from scraped data"""
    # get frame and first data point
    frame = [df for df in data if "FEMALES" in df.columns[0]][0]

    # total female population
    POPULATION_DATA["female_inmate_count"].append(
        _parse_int(frame.keys()[2]),
    )
    POPULATION_DATA["female_inmate_percentage"].append(
        100 * _parse_int(frame.keys()[2]) / _parse_int(frame.keys()[1]),
    )

    # minimum security facilities
    _attempt_search_with_fallback(frame, 2, "MINIMUM SECURITY",
                                  target="female_minimum_security")


def parse_facility_youths(data):
    """Parse incarcerated youth population figures from scraped data"""
    # get frame and column names
    frame = [df for df in data if "JUVENILE" in df.columns[0]][0]
    cap = frame.keys()[2]
    count = frame.keys()[3]

    # total facility youth population
    idx = _get_row_index(frame, "Total")
    POPULATION_DATA["facility_youth_total"].append(
        _parse_int(frame[count][idx])
    )
    POPULATION_DATA["facility_youth_percentage"].append(
        100 * _parse_int(frame[count][idx]) / _parse_int(frame[cap][idx]),
    )

    # Copper Lake School
    _attempt_search_with_fallback(frame, 3, "Copper Lake")

    # Ethan Allen
    _attempt_search_with_fallback(frame, 3, "Ethan Allen")

    # Grow Academy
    _attempt_search_with_fallback(frame, 3, "Grow Academy")

    # Lincoln Hills School
    _attempt_search_with_fallback(frame, 3, "Lincoln Hills")

    # Mendota Juvenile Treatment Center
    _attempt_search_with_fallback(frame, 3, "Mendota")

    # Southern Oaks Girls School
    _attempt_search_with_fallback(frame, 3, "Southern Oaks")


def get_trends():
    """Retrieve inmate population figures from state records"""
    # get publication dates
    (dates, files) = get_publication_dates()
    POPULATION_DATA["publication_date"] = dates

    # range over PDF reports and scrape population trends
    for (pubdate, source) in tqdm.tqdm(zip(dates, files), total=len(dates)):
        data = tabula.read_pdf(  # retrieve from Wisconsin DOC
            source,
            pages="all",
        )
        parse_totals(data)  # total inmate population
        parse_incarcerated_males(data)  # incarcerated male poulation
        parse_incarcerated_females(data)  # incarcerated female population
        parse_facility_youths(data)  # facility youth population


# -- main block ---------------------------------------------------------------

if __name__ == "__main__":
    get_trends()

    # write data to file
    with open("doc-population-trends.json", "w") as output:
        output.write(json.dumps(POPULATION_DATA, indent=2))
