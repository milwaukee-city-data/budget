import csv
import os

from scipy.signal import savgol_filter

from gwpy.time import to_gps
from gwpy.timeseries import TimeSeries

from matplotlib import use
use("Agg")

from matplotlib import font_manager, pyplot, rcParams  # noqa: E402


# set font properties
font_dir = os.path.join(os.environ["HOME"], "Downloads", "vollkorn")
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

# set font family globally
rcParams["font.family"] = "vollkorn"


# -- plotting utilities -----------------------------------------------


def plot_incarcerated_total(data):
    """Parse input and plot trends for the incarcerated population"""
    times = [float(to_gps(t)) for t in data["publication_date"]]
    trends = TimeSeries(data["inmate_total"], times=times) / 1000
    rate = type(trends)(
        savgol_filter(trends.value, 15, 2, deriv=1)
    ) * 1000
    rate.__array_finalize__(trends)
    xticks = [str(n) for n in range(2018, 2022)]

    # stand up axes
    (fig, (tax, rax)) = pyplot.subplots(
        nrows=2,
        sharex=True,
        sharey=False,
        figsize=(12, 6),
    )

    # plot total population
    tax.plot(trends, color="#0d2240", linewidth=2)
    tax.plot(
        [float(to_gps("2019-01-07"))] * 2,
        [19, 24],
        color="#0d2240",
        alpha=0.6,
        linestyle="--",
        linewidth=1,
    )
    tax.plot(
        [float(to_gps("2020-03-25"))] * 2,
        [19, 24],
        color="#0d2240",
        alpha=0.6,
        linestyle="--",
        linewidth=1,
    )
    tax.set_xlim(
        [
            float(to_gps("2018-01-01")),
            float(to_gps("2021-08-06")),
        ]
    )
    tax.set_xticks(
        [float(to_gps(f"{yr}-{mo}-01"))
         for yr in xticks for mo in range(2, 13)
         if to_gps(f"{yr}-{mo}-01") < to_gps("2021-08-06")],
        minor=True,
    )
    tax.set_xticks([float(to_gps(f"{yr}-01-01")) for yr in xticks])
    tax.set_xticklabels(xticks)
    tax.set_ylabel(r"Total population ($\times$ 1000)")
    tax.set_ylim([19, 24])
    tax.text(
        float(to_gps("2019-01-21")),
        21.15,
        "Evers administration\nbegins",
    )
    tax.text(
        float(to_gps("2020-04-08")),
        19.65,
        "COVID-19 lockdown\nbegins",
    )
    tax.grid(color="#0d2240", alpha=0.4, linestyle="dotted")

    # plot rate of change
    rax.plot(rate, color="#00a8e1", linewidth=2)
    rax.plot(
        [float(to_gps("2019-01-07"))] * 2,
        [-160, 60],
        color="#0d2240",
        alpha=0.6,
        linestyle="--",
        linewidth=1,
    )
    rax.plot(
        [float(to_gps("2020-03-25"))] * 2,
        [-160, 60],
        color="#0d2240",
        alpha=0.6,
        linestyle="--",
        linewidth=1,
    )
    rax.set_xlabel("Calendar year")
    rax.set_ylabel("Growth rate (per week)")
    rax.set_ylim([-160, 60])
    rax.grid(color="#0d2240", alpha=0.4, linestyle="dotted")

    # save figure and return
    return fig.savefig("doc-total-percent.png", bbox_inches="tight")


# -- main block -------------------------------------------------------

if __name__ == "__main__":
    # load from CSV
    with open("doc-population-trends.csv", "r") as datafile:
        data = {
            col[0]: [
                float(value)
                if value.isnumeric()
                else value
                for value in col[1:]
            ]
            for col in list(map(list, zip(*csv.reader(datafile))))
        }

    # render population trends as timeseries figures
    plot_incarcerated_total(data)
