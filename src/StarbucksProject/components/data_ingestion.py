import os
from dotenv import load_dotenv
import urllib.request as request
import zipfile
import pandas as pd
from src.StarbucksProject import logger
from src.StarbucksProject.utils.common import get_size, create_directories
from src.StarbucksProject.entity.config_entity import DataIngestionConfig
from pathlib import Path
import requests
import time


class DataIngestion:

    def __init__(self, config: DataIngestionConfig):  # pass in ConfigurationManager (the entity)
        self.config = config  # accesses relevant section of the YAML file

    def download_file(self):

        if not os.path.exists(self.config.local_zip_file):
            filename, headers = request.urlretrieve(url=self.config.acs_source_url,
                                                    filename=self.config.local_zip_file)
            logger.info(f"{filename} downloaded with following info: \n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_zip_file))}")

    def extract_zip_file(self):

        unzip_path = self.config.root_dir

        with zipfile.ZipFile(self.config.local_zip_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)

    def clean_acs_csv(self, df):

        clean_df = df.copy()
        clean_df.rename(columns={"Label (Grouping)": "ZCTA"}, inplace=True)
        clean_df.dropna(axis=1, how='all', inplace=True)
        cols = clean_df.columns

        clean_df.rename(
            columns=dict(zip(clean_df.columns[1:], [" ".join(col.split("!!")[1:]) for col in list(cols[1:])])),
            inplace=True)

        clean_df = clean_df.loc[:, ~clean_df.columns.duplicated()]
        clean_df.iloc[:, 1:] = clean_df.iloc[:, 1:].shift(periods=-1)
        clean_df["ZCTA"] = clean_df["ZCTA"].str.strip()
        clean_df = clean_df[clean_df["ZCTA"].str.startswith("Z")]
        clean_df["ZCTA"] = clean_df["ZCTA"].apply(lambda x: x.split()[1])
        clean_df.reset_index(drop=True, inplace=True)

        return clean_df

    def clean_all_csvs(self):

        co_social = pd.read_csv('artifacts/data_ingestion/acs_data/co_social.csv')
        co_social_clean = self.clean_acs_csv(co_social)

        co_econ = pd.read_csv('artifacts/data_ingestion/acs_data/co_econ.csv')
        co_econ_clean = self.clean_acs_csv(co_econ)

        co_housing = pd.read_csv('artifacts/data_ingestion/acs_data/co_housing.csv')
        co_housing_clean = self.clean_acs_csv(co_housing)

        co_demo_housing = pd.read_csv('artifacts/data_ingestion/acs_data/co_demo_housing.csv')
        co_demo_housing.drop('Total housing units', axis=1, inplace=True)
        co_demo_housing_clean = self.clean_acs_csv(co_demo_housing)

        create_directories([self.config.acs_data_clean])

        co_social_clean.to_csv(self.config.acs_social_clean)
        co_econ_clean.to_csv(self.config.acs_econ_clean)
        co_housing_clean.to_csv(self.config.acs_housing_clean)
        co_demo_housing_clean.to_csv(self.config.acs_demo_housing_clean)

    def get_yelp_data(self):

        load_dotenv()

        acs_data = pd.read_csv(self.config.acs_demo_housing_clean)
        acs_data = acs_data.iloc[:, 1:3]

        acs_data['Total population'] = acs_data['Total population'].str.replace(',', '')
        acs_data['Total population'] = acs_data['Total population'].astype(int)

        acs_data.sort_values(by='Total population', ascending=False, inplace=True)
        acs_data = acs_data.iloc[:299, :]

        zip_codes = list(acs_data['ZCTA'])
        stores_per_zip = []
        reviews_per_zip = []
        weighted_avg_per_zip = []

        for zip_code in zip_codes:

            off = 0
            term = "starbucks"
            limit = 50
            biz_list = []  # add stores to this list

            while True:

                API_KEY = os.getenv('yelp_api_key')
                ENDPOINT = self.config.yelp_api_endpoint
                HEADERS = {"accept": "application/json",
                           "Authorization": f"Bearer {API_KEY}"}
                PARAMETERS = {'location': zip_code,
                              'term': term,
                              'offset': off,
                              'limit': limit}

                response = requests.get(url=ENDPOINT,
                                        params=PARAMETERS,
                                        headers=HEADERS)
                logger.info("API request made")

                json_response = response.json()
                biz_array = json_response['businesses']
                biz_names = [i['name'] for i in biz_array]
                biz_ratings = [i['rating'] for i in biz_array]
                biz_review_count = [i['review_count'] for i in biz_array]
                biz_zips = [i['location']['zip_code'] for i in biz_array]
                biz_addresses = [",".join(i['location']['display_address']) for i in biz_array]

                biz_data = list(zip(biz_names, biz_ratings, biz_review_count, biz_zips, biz_addresses))
                # filter out the Starbucks stores that aren't in the zip code of interest
                filtered_data = [i for i in biz_data if (term in i[0].lower()) and (i[3] == str(zip_code))]

                if len(filtered_data) == 0:
                    logger.info("Broke out of while loop - last request didn't return any stores in current zip code")
                    break

                for shop in filtered_data:
                    print("store in zip = ", shop)
                    biz_list.append(shop)

                if len([i[3] for i in biz_data[25:] if i[3] == str(zip_code) and term in i[0].lower()]) == 0:
                    print("Broke out of while loop - last 25 results didn't include a store in current zip code")
                    break

                off += limit  # make another HTTP request for the same zip code
                time.sleep(2)

            try:

                # summarize Yelp review history to assess how Starbucks has performed in the zip code
                df = pd.DataFrame(biz_list, columns=['store_name', 'avg_rating', 'reviews', 'zip', 'address'])
                df['store_total_reviews'] = df.groupby('address')['reviews'].cumsum()
                df['store_weight'] = df['avg_rating'] * df['reviews']
                df['store_total_weight'] = df.groupby('address')['store_weight'].cumsum()
                df['avg_rating_weighted'] = round(df['store_total_weight'] / df['store_total_reviews'], 2)
                df = df.drop_duplicates(subset=['address'], keep='last')
                df.drop(['avg_rating', 'reviews', 'address', 'store_weight', 'store_total_weight'], axis=1,
                        inplace=True)
                df['zip_average_contribution'] = round(df['store_total_reviews'] * df['avg_rating_weighted'], 2)

                stores_per_zip.append(df.shape[0])
                reviews_per_zip.append(df['store_total_reviews'].sum())
                weighted_avg_per_zip.append(
                    round(df['zip_average_contribution'].sum() / df['store_total_reviews'].sum(), 3))

            except Exception as e:
                logger.exception(f"{e}")
                logger.info("Current zip code didn't contain any Starbucks locations")
                stores_per_zip.append(0)
                reviews_per_zip.append(0)
                weighted_avg_per_zip.append(0)

            print("\n")

        starbucks_data = list(zip(zip_codes, stores_per_zip, reviews_per_zip, weighted_avg_per_zip))

        starbucks_df = pd.DataFrame(starbucks_data, columns=['zip',
                                                             'total_stores',
                                                             'total_reviews',
                                                             'review_weighted_avg'])

        create_directories([self.config.yelp_data])
        starbucks_df.to_csv(self.config.yelp_csv, index=False)