import csv
import json

from gwpy.time import to_gps
from gwpy.timeseries import (TimeSeries, TimeSeriesDict)

from matplotlib import use
use("Agg")


# -- plotting utilities -------------------------------------------------------

def _unpack_data(data, fields):
    times = [float(to_gps(t)) for t in data["publication_date"]]
    return TimeSeriesDict({
        field: TimeSeries(data[field], times=times)
        for field in fields
    })


def plot_incarcerated_youth(data):
    """Parse input and plot trends for incarcerated youths"""
    fields = [
        "facility_youth_total",
        "lincoln_hills_count",
        "ethan_allen_count",
        "copper_lake_count",
        "grow_academy_count",
        "mendota_count",
        "southern_oaks_count",
    ]
    trends = _unpack_data(data, fields)
    idx = data["ethan_allen_count"].index(0)
    xticks = [str(n) for n in range(2008, 2022)]

    # plot raw counts
    plot = trends[fields[0]].plot(
        color="#f7a800",
        label="Total",
        linewidth=2,
        figsize=(12, 6),
    )
    ax = plot.gca()
    ax.plot(
        trends[fields[1]],
        color="#0d2240",
        label="Lincoln Hills",
        linewidth=2,
    )
    ax.plot(
        trends[fields[2]][:idx+1:],
        color="#00a8e1",
        label="Ethan Allen",
        linewidth=2,
    )
    ax.plot(
        trends[fields[3]][idx::],
        color="#0d2240",
        label="Copper Lake",
        alpha=0.25,
        linewidth=1.25,
    )
    ax.plot(
        trends[fields[4]] + trends[fields[5]] + trends[fields[6]],
        color="#0d2240",
        label="Other",
        alpha=0.1,
        linewidth=1.25,
    )
    ax.set_xlabel("Calendar year")
    ax.set_xlim([float(to_gps("2008-01-01")), float(to_gps("2021-08-06"))])
    ax.set_xticks([float(to_gps(f"{yr}-01-01")) for yr in xticks])
    ax.set_xticklabels(xticks)
    ax.tick_params(axis="x", which="minor", bottom=False)
    ax.set_ylabel(r"Population size")
    ax.set_ylim([0, 650])
    ax.grid(color="#0d2240", alpha=0.4, linestyle="dotted")
    ax.legend(loc="upper right")
    plot.savefig("fig/doc-youth-count.pdf", bbox_inches="tight")
    plot.close()


def plot_incarcerated_total(data):
    """Parse input and plot trends for the total number of incarcerated persons
    relative to the design capacity
    """
    fields = [
        "inmate_total_percentage",
        "male_maximum_security_percentage",
        "male_medium_security_percentage",
        "male_minimum_security_percentage",
        "female_minimum_security_percentage",
    ]
    trends = _unpack_data(data, fields)
    xticks = [str(n) for n in range(2018, 2022)]

    # plot percentage relative to design capacity
    plot = trends[fields[0]].plot(
        color="#0d2240",
        label="Total",
        linewidth=2,
        figsize=(12, 6),
    )
    ax = plot.gca()
    ax.plot(
        trends[fields[1]],
        color="#00a8e1",
        label="Max. security",
        linewidth=2,
    )
    ax.plot(
        trends[fields[2]],
        color="#0d2240",
        alpha=0.25,
        label="Med. security",
        linewidth=1.25,
    )
    ax.plot(
        trends[fields[3]],
        color="#0d2240",
        alpha=0.1,
        label="Min. security (male)",
        linewidth=1.25,
    )
    ax.plot(
        trends[fields[4]],
        color="#f7a800",
        label="Min. security (female)",
        linewidth=2,
    )
    ax.plot(
        [float(to_gps("2019-01-07"))] * 2,
        [100, 220],
        color="#0d2240",
        alpha=0.6,
        linestyle="--",
        linewidth=1,
    )
    ax.plot(
        [float(to_gps("2020-03-25"))] * 2,
        [100, 220],
        color="#0d2240",
        alpha=0.6,
        linestyle="--",
        linewidth=1,
    )
    ax.set_xlabel("Calendar year")
    ax.set_xlim([float(to_gps("2018-01-01")), float(to_gps("2021-08-06"))])
    ax.set_xticks(
        [float(to_gps(f"{yr}-{mo}-01"))
         for yr in xticks for mo in range(2, 13)
         if to_gps(f"{yr}-{mo}-01") < to_gps("2021-08-06")],
        minor=True,
    )
    ax.set_xticks([float(to_gps(f"{yr}-01-01")) for yr in xticks])
    ax.set_xticklabels(xticks)
    ax.set_ylabel("Percentage of design capacity")
    ax.set_ylim([100, 220])
    ax.text(
        float(to_gps("2019-01-14")),
        167,
        "Evers administration\nbegins",
    )
    ax.text(
        float(to_gps("2020-03-18")),
        107,
        "COVID-19 lockdown\nbegins",
        ha="right",
    )
    ax.grid(color="#0d2240", alpha=0.4, linestyle="dotted")
    ax.legend(loc="upper right")
    plot.savefig("fig/doc-total-percent.pdf", bbox_inches="tight")
    plot.close()


def plot_incarcerated_adult(data):
    """Parse input and plot trends for incarcerated adults"""
    fields = [
        "probation_parole_total",
        "inmate_total",
        "male_maximum_security_count",
        "male_medium_security_count",
        "male_minimum_security_count",
        "female_minimum_security_count",
    ]
    trends = _unpack_data(data, fields)
    xticks = [str(n) for n in range(2018, 2022)]

    # plot raw counts
    plot = (trends[fields[0]] / 1e3).plot(
        color="#0d2240",
        label="Supervised",
        linewidth=2,
        figsize=(12, 6),
    )
    ax = plot.gca()
    ax.plot(
        trends[fields[1]] / 1e3,
        color="#00a8e1",
        label="Incarcerated",
        linewidth=2,
    )
    ax.plot(
        trends[fields[2]] / 1e3,
        color="#f7a800",
        label="Max. security",
        linestyle="--",
        linewidth=2,
    )
    ax.plot(
        trends[fields[3]] / 1e3,
        color="#f7a800",
        label="Med. security",
        alpha=0.66,
        linestyle="--",
        linewidth=2,
    )
    ax.plot(
        (trends[fields[4]] + trends[fields[5]]) / 1e3,
        color="#f7a800",
        label="Min. security",
        alpha=0.33,
        linestyle="--",
        linewidth=2,
    )
    ax.plot(
        [float(to_gps("2019-01-07"))] * 2,
        [0, 70],
        color="#0d2240",
        alpha=0.6,
        linestyle="--",
        linewidth=1,
    )
    ax.plot(
        [float(to_gps("2020-03-25"))] * 2,
        [0, 70],
        color="#0d2240",
        alpha=0.6,
        linestyle="--",
        linewidth=1,
    )
    ax.set_xlabel("Calendar year")
    ax.set_xlim([float(to_gps("2018-01-01")), float(to_gps("2021-08-06"))])
    ax.set_xticks(
        [float(to_gps(f"{yr}-{mo}-01"))
         for yr in xticks for mo in range(2, 13)
         if to_gps(f"{yr}-{mo}-01") < to_gps("2021-08-06")],
        minor=True,
    )
    ax.set_xticks([float(to_gps(f"{yr}-01-01")) for yr in xticks])
    ax.set_xticklabels(xticks)
    ax.set_ylabel(r"Population size ($\times$ 1000)")
    ax.set_ylim([0, 70])
    ax.text(float(to_gps("2019-01-14")), 43, "Evers administration\nbegins")
    ax.text(float(to_gps("2020-04-01")), 43, "COVID-19 lockdown\nbegins")
    ax.grid(color="#0d2240", alpha=0.4, linestyle="dotted")
    ax.legend(loc="upper left", bbox_to_anchor=(0, 0.79))
    plot.savefig("fig/doc-total-count.pdf", bbox_inches="tight")
    plot.close()


# -- main block ---------------------------------------------------------------

if __name__ == "__main__":
    # load from JSON
    with open("doc-population-trends.json", "r") as datafile:
        trends = json.load(datafile)

    # render population trends as timeseries figures
    plot_incarcerated_youth(trends)
    plot_incarcerated_total(trends)
    plot_incarcerated_adult(trends)

    # write data to CSV spreadsheet
    with open("doc-population-trends.csv", "w") as output:
        writer = csv.writer(output)
        writer.writerow(trends.keys())
        writer.writerows(zip(*[trends[key] for key in trends]))
