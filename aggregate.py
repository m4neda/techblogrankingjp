
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd


def get_csv() -> pd.DataFrame:
    pass


def calc_techblogscore(median_hatebu_count, number_of_articles: int):
    return number_of_articles * (median_hatebu_count + 1)


def main():
    df = pd.read_csv(
        'csv/xxx.csv',
        parse_dates=['published_at'],
        index_col='published_at')

    last_year = datetime.today().replace(day=1) - relativedelta(years=1)
    df_thelastyear = df[df.index > last_year]
    thelastyear_hatebu_count_median = df_thelastyear.hatebu_count.median()
    row_count, _ = df_thelastyear.shape
    techblogscore = calc_techblogscore(
        median_hatebu_count=thelastyear_hatebu_count_median,
        number_of_articles=row_count)
    print(techblogscore)

if __name__ == '__main__':
    main()
