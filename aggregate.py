from os import listdir, path
from datetime import datetime
from typing import NamedTuple
from dateutil.relativedelta import relativedelta
import pandas as pd


def calc_techblogscore(median_hatebu_count, number_of_articles: int):
    return number_of_articles * (median_hatebu_count + 1)


def main():
    rankings = []
    df_blog_url = pd.read_csv(
        'techbloglist.csv', usecols=[
            'company_name', 'url'])
    dir_csv = 'csv/'
    for filename in listdir(dir_csv):
        company_name = path.splitext(filename)[0]
        df = pd.read_csv(
            dir_csv + filename,
            parse_dates=['published_at'],
            index_col='published_at')
        blog_url = df_blog_url.loc[df_blog_url['company_name']
                                   == company_name].url.item()
        last_year = datetime.today().replace(day=1) - relativedelta(years=1)
        df_thelastyear = df[df.index > last_year]
        thelastyear_hatebu_count_median = df_thelastyear.hatebu_count.median()
        row_count, _ = df_thelastyear.shape
        techblogscore = calc_techblogscore(
            median_hatebu_count=thelastyear_hatebu_count_median,
            number_of_articles=row_count)

        rankings.append([
            company_name,
            row_count,
            thelastyear_hatebu_count_median,
            techblogscore,
            blog_url])

    df = pd.DataFrame(
        rankings,
        columns=[
            'company_name',
            'article_count',
            'hatebu_count',
            'score',
            'url'])
    df.insert(
        0,
        'rank',
        df['score'].rank(
            ascending=False,
            method='min',
            na_option='bottom'))
    df.fillna(0, inplace=True)
    df.sort_values('rank', inplace=True)
    df.to_json('json/rankings.json', orient='records', force_ascii=True)


if __name__ == '__main__':
    main()
