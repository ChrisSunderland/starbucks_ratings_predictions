import pandas as pd
from src.StarbucksProject.entity.config_entity import DataValidationConfig


class DataValidation:

    def __init__(self, config: DataValidationConfig):

        self.config = config

    def load_data(self):

        acs_demo_housing = pd.read_csv(self.config.acs_demo_housing)
        acs_demo_housing = acs_demo_housing.iloc[:, 1:]

        acs_econ = pd.read_csv(self.config.acs_econ)
        acs_econ = acs_econ.iloc[:, 1:]

        acs_housing = pd.read_csv(self.config.acs_housing)
        acs_housing = acs_housing.iloc[:, 1:]

        acs_social = pd.read_csv(self.config.acs_social)
        acs_social = acs_social.iloc[:, 1:]

        yelp = pd.read_csv(self.config.yelp)

        return acs_demo_housing, acs_econ, acs_housing, acs_social, yelp

    def select_fields(self):

        demo_housing, econ, housing, social, yelp = self.load_data()

        demo_housing_cols = ["ZCTA",
                             "Total population",
                             "Total population Sex ratio (males per 100 females)",
                             "Total population Median age (years)"]
        demo_housing = demo_housing[demo_housing_cols]

        econ_cols = ["ZCTA",
                     "Civilian employed population 16 years and over",
                     "Per capita income (dollars)"]
        econ = econ[econ_cols]

        housing_cols = ["ZCTA",
                        "Occupied units paying rent Median (dollars)"]
        housing = housing[housing_cols]

        social_cols = ["ZCTA",
                       "Total households Average household size",
                       "Population 3 years and over enrolled in school College or graduate school",
                       "Population 25 years and over Bachelor's degree",
                       "Population 1 year and over Same house"
                       ]
        social = social[social_cols]

        return demo_housing, econ, housing, social, yelp

    def combine_data(self):

        dh, e, h, s, y = self.select_fields()

        acs_combined = pd.merge(dh, h, on="ZCTA", how="inner")
        acs_combined = pd.merge(acs_combined, e, on="ZCTA", how="inner")
        acs_combined = pd.merge(acs_combined, s, on="ZCTA", how="inner")
        acs_combined.rename(columns={'ZCTA': 'zip'}, inplace=True)

        acs_yelp_combined = pd.merge(acs_combined, y, on="zip", how="inner")

        return acs_yelp_combined

    def clean_data(self, df):

        clean_df = df.copy()

        # rename fields
        new_col_names = {"Total population": "total_pop",
                         "Total population Sex ratio (males per 100 females)": "males_per_100_females",
                         'Total population Median age (years)': 'median_age',
                         'Occupied units paying rent Median (dollars)': 'median_rent',
                         "Civilian employed population 16 years and over": 'total_employed',
                         'Per capita income (dollars)': 'per_capita_income',
                         "Total households Average household size": 'avg_household_size',
                         "Population 3 years and over enrolled in school College or graduate school": "enrolled_in_college",
                         "Population 25 years and over Bachelor's degree": "total_bachelors_degree",
                         "Population 1 year and over Same house": "total_same_residence",
                         'total_stores': 'total_starbucks_locations',
                         'total_reviews': 'total_starbucks_reviews',
                         'review_weighted_avg': 'weighted_avg_starbucks_ratings'}
        clean_df.rename(columns=new_col_names, inplace=True)

        # drop rows
        clean_df = clean_df[clean_df.total_starbucks_locations > 0]

        # handle irregular values
        clean_df = clean_df[clean_df.median_rent != '-']

        # drop fields
        clean_df.drop(["zip", "total_starbucks_locations", "total_starbucks_reviews"], axis=1, inplace=True)

        # convert data types
        comma_cols = ["total_pop", "median_rent", "total_employed", "per_capita_income", "enrolled_in_college",
                      "total_bachelors_degree", "total_same_residence"]
        clean_df[comma_cols] = clean_df[comma_cols].apply(lambda x: x.str.replace(',', ''))
        clean_df[comma_cols] = clean_df[comma_cols].astype(int)

        float_cols = ["males_per_100_females", "median_age", "avg_household_size"]
        clean_df[float_cols] = clean_df[float_cols].astype(float)

        # add the new cleaned CSV to the 'artifacts' folder
        clean_df.to_csv(self.config.acs_yelp_combined, index=False)

    def validate_columns(self):

        data = pd.read_csv(self.config.acs_yelp_combined)

        try:

            validation_status = None

            all_cols = list(data.columns)

            all_schema = self.config.all_schema.keys()

            for col in all_cols:  # check if column is present in the schema defined in YAML file

                if col not in all_schema:
                    validation_status = False
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            raise e