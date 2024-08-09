import numpy as np


def medal_tally(df):
    medal_tally = df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
    )

    medal_tally = (
        medal_tally.groupby("region")
        .sum()[["Gold", "Silver", "Bronze"]]
        .sort_values("Gold", ascending=False)
        .reset_index()
    )

    medal_tally["total"] = (
        medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]
    )

    medal_tally["Gold"].astype("int")
    medal_tally["Silver"].astype("int")
    medal_tally["Bronze"].astype("int")
    medal_tally["total"].astype("int")

    return medal_tally


def country_year_list(df):
    years = df["Year"].unique().tolist()
    years.sort()
    years.insert(0, "Overall")

    country = np.unique(df["region"].dropna().values).tolist()
    country.sort()
    country.insert(0, "Overall")

    return years, country


# For plotting a line plot in the app


# def participating_nations_over_time(df):
def data_over_time(df, col):
    nations_over_time = (
        df.drop_duplicates(["Year", col])["Year"]
        .value_counts()
        .reset_index()
        .sort_values("Year")
    )
    nations_over_time.rename(
        columns={"count": col, "Year": "Year/Edition"}, inplace=True
    )
    return nations_over_time


# Table of the most decorated/successful athletes i.e., athletes with most medal wins
def most_successful(df, sport):
    # Done since many values in Medal column are NaN values
    temp_df = df.dropna(subset=["Medal"])
    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]
    # Becomes/converts to a dataframe when reset_index() is used.
    x = (
        temp_df["Name"]
        .value_counts()
        .reset_index()
        .head(15)
        .merge(df, left_on="Name", right_on="Name", how="left")[
            ["Name", "count", "Sport", "region"]
        ]
        .drop_duplicates("Name")
    )
    x.rename(columns={"Name": "Name", "count": "Medals"}, inplace=True)
    return x


# Creating a function having inputs year and country, and will show the output on the app after the
# selected inputs from dropdown box on the app.


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
    )
    # Flag set for showing year-wise medals for a specific country
    flag = 0
    if year == "Overall" and country == "Overall":
        temp_df = medal_df
    if year == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df["region"] == country]
    if year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df["Year"] == int(year)]
    if year != "Overall" and country != "Overall":
        temp_df = medal_df[
            (medal_df["Year"] == int(year)) & (medal_df["region"] == country)
        ]

    if flag == 1:
        x = (
            temp_df.groupby("Year")
            .sum()[["Gold", "Silver", "Bronze"]]
            .sort_values("Year", ascending=True)
            .reset_index()
        )
    else:
        x = (
            temp_df.groupby("region")
            .sum()[["Gold", "Silver", "Bronze"]]
            .sort_values("Gold", ascending=False)
            .reset_index()
        )

    x["total"] = x["Gold"] + x["Silver"] + x["Bronze"]

    x["Gold"].astype("int")
    x["Silver"].astype("int")
    x["Bronze"].astype("int")
    x["total"].astype("int")

    return x


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset="Medal")
    # Solving team sports problem
    temp_df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"],
        inplace=True,
    )

    new_df = temp_df[temp_df["region"] == country]
    final_df = new_df.groupby("Year").count()["Medal"].reset_index()

    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset="Medal")
    # Solving team sports problem
    temp_df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"],
        inplace=True,
    )

    new_df = temp_df[temp_df["region"] == country]

    pt = new_df.pivot_table(
        index="Sport", columns="Year", values="Medal", aggfunc="count"
    ).fillna(0)

    return pt


def most_successful_countrywise(df, country):
    # Done since many values in Medal column are NaN values
    temp_df = df.dropna(subset=["Medal"])

    temp_df = temp_df[temp_df["region"] == country]
    # Becomes/converts to a dataframe when reset_index() is used.
    x = (
        temp_df["Name"]
        .value_counts()
        .reset_index()
        .head(10)
        .merge(df, left_on="Name", right_on="Name", how="left")[
            ["Name", "count", "Sport"]
        ]
        .drop_duplicates("Name")
    )
    x.rename(columns={"Name": "Name", "count": "Medals"}, inplace=True)
    return x


def weight_v_height(df, sport):
    # Creating athlete_df dataframe
    athlete_df = df.drop_duplicates(subset=["Name", "region"])
    # Cleaning sorta the dataframe
    athlete_df.fillna({"Medal": "No Medal"}, inplace=True)

    if sport != "Overall":
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=["Name", "region"])

    # Plot of men vs women participation over the years in the Olympics
    men = (
        athlete_df[athlete_df["Sex"] == "M"]
        .groupby("Year")
        .count()["Name"]
        .reset_index()
    )
    women = (
        athlete_df[athlete_df["Sex"] == "F"]
        .groupby("Year")
        .count()["Name"]
        .reset_index()
    )

    final = men.merge(women, on="Year", how="left")
    final.rename(columns={"Name_x": "Male", "Name_y": "Female"}, inplace=True)

    final.fillna(0, inplace=True)

    return final
