import os.path
import pandas as pd
import warnings
import re

warnings.simplefilter("ignore")


def read_gangneung(filename: str) -> None:
    df = pd.read_excel(filename)
    row = df.index[df[df.columns[0]] == "밀"].tolist()
    row = row[0]

    col = df.columns

    wheat_data = df.iloc[row:row + 3]

    location = filename[21:-5]
    x = "_"
    loc = location.rfind(x)

    years = []
    for i in range(len(col)):
        try:
            year = int(col[i])
            years.append(year)
        except (ValueError, TypeError):
            pass

    items = ["면적", "생산량", "단위생산량"]

    area_row = row
    yield_row = row + 1
    unit_row = row + 2

    area_data = wheat_data.loc[int(area_row)].values[2:]
    yield_data = wheat_data.loc[int(yield_row)].values[2:]
    unit_data = wheat_data.loc[int(unit_row)].values[2:]

    value = [area_data, yield_data, unit_data]

    datasets = []
    for i, item in enumerate(items):
        for k, year in enumerate(years):
            datasets.append(
                {
                    "lo1": location[:loc], "lo2": location[loc + 1:], "lo3": "", "year": year, "item": item,
                    "value": value[i][k]
                }
            )

    return pd.DataFrame(datasets)


def read_donghae(filename: str) -> None:
    df = pd.read_excel(filename)

    remov = [c for c in df.columns if (c[:-2] != "합계") and (c != "합계") and (c[:-3] != "합계")]

    if len(df[remov].columns) == 2:
        row = df.index[df[df.columns[0]] == "밀"].tolist()
        row = row[0]

        wheat_data = df.iloc[row:row + 3]

        location = filename[21:-5]
        x = "_"
        loc = location.rfind(x)

        years = df.loc[0][2:].values

        items = ["면적", "생산량", "단위생산량"]

        area_row = row
        yield_row = row + 1
        unit_row = row + 2

        area_data = wheat_data.loc[area_row].values[2:]
        yield_data = wheat_data.loc[yield_row].values[2:]
        unit_data = wheat_data.loc[unit_row].values[2:]

        value = [area_data, yield_data, unit_data]

        datasets = []
        for i, item in enumerate(items):
            for k, year in enumerate(years):
                datasets.append(
                    {
                        "lo1": location[:loc], "lo2": location[loc + 1:], "lo3": "", "year": year, "item": item,
                        "value": value[i][k]
                    }
                )

    else:
        df = df[remov]

        row = df.index[df[df.columns[0]] == "밀"].tolist()
        row = row[0]

        years = df.loc[0][2:].values
        wheat_data = df.iloc[row:row + 3]

        location = filename[21:-5]
        x = "_"
        xloc = location.rfind(x)

        if len(df.columns) > 2:
            lo3 = df.columns[2:]
            lo3l = []

            for i in lo3:
                i = i.replace(" ", "")
                result = re.compile("[가-힣]+").findall(i)
                result = result[0]
                lo3l.append(result)

        items = ["면적", "생산량", "단위생산량"]

        area_row = row
        yield_row = row + 1
        unit_row = row + 2

        area_data = wheat_data.loc[area_row].values[2:]
        yield_data = wheat_data.loc[yield_row].values[2:]
        unit_data = wheat_data.loc[unit_row].values[2:]

        value = [area_data, yield_data, unit_data]

        datasets = []
        for i, item in enumerate(items):
            for k, year in enumerate(years):
                datasets.append(
                    {
                        "lo1": location[:xloc], "lo2": location[xloc + 1:], "lo3": lo3l[k], "year": year, "item": item,
                        "value": value[i][k]
                    }
                )

    return pd.DataFrame(datasets)


def check_int(value):
    try:
        int(value)

    except ValueError:
        return False

    return True


def read_stat_file(filename: str) -> pd.DataFrame:
    df = pd.read_excel(filename)

    if check_int(df.columns[2]):
        print("강릉타입 처리: ", filename)
        return read_gangneung(filename)
    else:
        print("동해타입 처리: ", filename)
        return read_donghae(filename)


def main():
    output_dir = "../output/kosis/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data_dir = "../input/kosis_wheat/"
    file_list = os.listdir(data_dir)

    for filename in file_list:
        name, extension = os.path.splitext(filename)

        df_stat_wheat = read_stat_file(os.path.join(data_dir, filename))
        df_stat_wheat = df_stat_wheat[df_stat_wheat != "-"]
        df_stat_wheat = df_stat_wheat[df_stat_wheat != "..."]
        df_stat_wheat = df_stat_wheat.dropna()
        df_stat_wheat.to_csv(os.path.join(output_dir, "{}.csv".format(name)), index=False,
                             encoding="utf-8-sig")


if __name__ == "__main__":
    main()
