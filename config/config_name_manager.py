



# -------------------------

PLANT_BY_DAY = "plant_by_day"
DAY_OF_THE_WEEK = "day_of_the_week"
DAY_OF_THE_WEEK_YEAR = "day_of_the_week_year"
PLANT_BY_WEEK = "plant_by_week"
PLANT_BY_MONTH = "plant_by_month"
PLANT_BY_YEAR = "plant_by_year"
PLANT_SAME_CROP_ALL = "plant_by_same_crop_all"

PLANTING_METHODS_DEFAULT = PLANT_BY_MONTH

PLANTING_METHODS = [
    PLANT_BY_DAY,
    DAY_OF_THE_WEEK,
    DAY_OF_THE_WEEK_YEAR,
    PLANT_BY_WEEK,
    PLANT_BY_MONTH,
    PLANT_BY_YEAR,
    PLANT_SAME_CROP_ALL
]

DELETE_UNUSED_KEYS = [
    PLANT_BY_DAY
]

CROP_RADIO_BUTTON_DICT = {"Plant by day": PLANT_BY_DAY,
                    "Plant by day of the week (month)": DAY_OF_THE_WEEK,
                    "Plant by day of the week (year)": DAY_OF_THE_WEEK_YEAR,
                    "Plant by week (vertical)":PLANT_BY_WEEK,
                    "Plant by month":PLANT_BY_MONTH,
                    "Plant by year": PLANT_BY_YEAR,
                    "Plant by same crop all":PLANT_SAME_CROP_ALL
                    }
