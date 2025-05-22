

from aqt import QMetaObject, QTimer, Qt, mw, gui_hooks

MEDIA_FOLDER_FARM = "media/Farm"
MEDIA_FOLDER_GARDEN = "media/Garden"

MEDIA_FOLDER_FARM_02 = "media/Farm_02"
MEDIA_FOLDER_FARM_02_ICONS = "media/Farm_02_icons"

MEDIA_FOLDER_FARMER = "media/farmer"

TIPPY_FOLDER = "tippy"


# mw.addonManager.setWebExports(
#     __name__, rf"({MEDIA_FOLDER_FARM}|{MEDIA_FOLDER_GARDEN}|{MEDIA_FOLDER_FARM_02})/.*(jpg|webp|png)"
# )


mw.addonManager.setWebExports(
    __name__,
    rf"({MEDIA_FOLDER_FARM}|{MEDIA_FOLDER_GARDEN}|{MEDIA_FOLDER_FARM_02}|{TIPPY_FOLDER}"
    rf"|{MEDIA_FOLDER_FARMER})/.*(jpg|webp|png|js|css)"
)

# mw.addonManager.setWebExports(
#     __name__, rf"({TIPPY_FOLDER})/.*(js|css)"
# )

addon_package = mw.addonManager.addonFromModule(__name__)


mediafolder_farm = f"/_addons/{addon_package}/{MEDIA_FOLDER_FARM}"

mediafolder_garden = f"/_addons/{addon_package}/{MEDIA_FOLDER_GARDEN}"

mediafolder_farm_02 = f"/_addons/{addon_package}/{MEDIA_FOLDER_FARM_02}"

mediafolder_farmer = f"/_addons/{addon_package}/{MEDIA_FOLDER_FARMER}"


FARMER_A = f'{mediafolder_farmer}/Farmer_A.png'
FARMER_B = f'{mediafolder_farmer}/Farmer_B.png'
FARMER_C = f'{mediafolder_farmer}/Farmer_C.png'
FARMER_D = f'{mediafolder_farmer}/Farmer_D.png'

FARMERS = [FARMER_A, FARMER_B, FARMER_C, FARMER_D]


# Farmer_A.png
# Farmer_B.png
# Farmer_C.png
# Farmer_D.png

# plants_image_01 = f'<img src="{mediafolder}/plants free_01.png" style="height: 100px;">'

THEMES = []

SUNFLOWER = "sunflower"
THEMES.append(SUNFLOWER)

ROSE = "rose"
THEMES.append(ROSE)

TULIP = "tulip"
THEMES.append(TULIP)

BIRD_OF_PARADISE = "bird_of_paradise"
THEMES.append(BIRD_OF_PARADISE)

CHAMOMILE = "chamomile"
THEMES.append(CHAMOMILE)

HYACINTH = "hyacinth"
THEMES.append(HYACINTH)

HYDRANGEA = "hydrangea"
THEMES.append(HYDRANGEA)

LOTUS = "lotus"
THEMES.append(LOTUS)

ORCHID = "orchid"
THEMES.append(ORCHID)

CARROT = "carrot"
THEMES.append(CARROT)

POTATO = "potato"
THEMES.append(POTATO)

PUMPKIN = "pumpkin"
THEMES.append(PUMPKIN)

TOMATO = "tomato"
THEMES.append(TOMATO)

CROPS_IMAGES_PATH_DICT = {}




def addButtons(handled, message, context):
    if message == "shige_farm_settings":
        from .new_cards_config import SetAnkiRestartConfig
        # SetAnkiRestartConfig()
        # 直接呼び出すとQDialogの中のQWebEngineがﾌﾘｰｽﾞする
        # QWidgetにするとﾌﾘｰｽﾞしない
        # Qtimerで呼び出すとﾒｲﾝｽﾚｯﾄﾞで安全にGUIを呼び出せるので動作する
        QTimer.singleShot(0, SetAnkiRestartConfig)

        return (True, None)
    elif "shige_newCardsFarm_days" in message:
        parts = message.split(":", 2)
        command, plant_config_date, cards = parts
        try:
            cards = int(cards)
        except ValueError:
            cards = 0
        if cards > 0 :
            from .change_crops import run_change_crops
            QTimer.singleShot(0, lambda: run_change_crops(mw, plant_config_date, cards))
        return (True, None)
    else:
        return handled



gui_hooks.webview_did_receive_js_message.remove(addButtons)
gui_hooks.webview_did_receive_js_message.append(addButtons)





# ==================================================


plants_image_01 = f'{mediafolder_farm}/carrot_01.png'
plants_image_02 = f'{mediafolder_farm}/carrot_02.png'
plants_image_03 = f'{mediafolder_farm}/carrot_03.png'
plants_image_04 = f'{mediafolder_farm}/carrot_04.png'
plants_image_05 = f'{mediafolder_farm}/carrot_05.png'

plants_image_06 = f'{mediafolder_farm}/potato_01.png'
plants_image_07 = f'{mediafolder_farm}/potato_02.png'
plants_image_08 = f'{mediafolder_farm}/potato_03.png'
plants_image_09 = f'{mediafolder_farm}/potato_04.png'
plants_image_10 = f'{mediafolder_farm}/potato_05.png'

plants_image_11 = f'{mediafolder_farm}/pumpkin_01.png'
plants_image_12 = f'{mediafolder_farm}/pumpkin_02.png'
plants_image_13 = f'{mediafolder_farm}/pumpkin_03.png'
plants_image_14 = f'{mediafolder_farm}/pumpkin_04.png'
plants_image_15 = f'{mediafolder_farm}/pumpkin_05.png'

plants_image_16 = f'{mediafolder_farm}/tomato_01.png'
plants_image_17 = f'{mediafolder_farm}/tomato_02.png'
plants_image_18 = f'{mediafolder_farm}/tomato_03.png'
plants_image_19 = f'{mediafolder_farm}/tomato_04.png'
plants_image_20 = f'{mediafolder_farm}/tomato_05.png'


flowers_image_01 = f'{mediafolder_garden}/Rose_01.png'
flowers_image_02 = f'{mediafolder_garden}/Rose_02.png'
flowers_image_03 = f'{mediafolder_garden}/Rose_03.png'

flowers_image_04 = f'{mediafolder_garden}/sunflower_01.png'
flowers_image_05 = f'{mediafolder_garden}/sunflower_02.png'
flowers_image_06 = f'{mediafolder_garden}/sunflower_03.png'

flowers_image_07 = f'{mediafolder_garden}/tulip_01.png'
flowers_image_08 = f'{mediafolder_garden}/tulip_02.png'
flowers_image_09 = f'{mediafolder_garden}/tulip_03.png'

flowers_image_10 = f'{mediafolder_garden}/bird_of_paradise_01.png'
flowers_image_11 = f'{mediafolder_garden}/bird_of_paradise_02.png'
flowers_image_12 = f'{mediafolder_garden}/bird_of_paradise_03.png'

flowers_image_13 = f'{mediafolder_garden}/chamomile_01.png'
flowers_image_14 = f'{mediafolder_garden}/chamomile_02.png'
flowers_image_15 = f'{mediafolder_garden}/chamomile_03.png'

flowers_image_16 = f'{mediafolder_garden}/hyacinth_01.png'
flowers_image_17 = f'{mediafolder_garden}/hyacinth_02.png'
flowers_image_18 = f'{mediafolder_garden}/hyacinth_03.png'

flowers_image_19 = f'{mediafolder_garden}/hydrangea_01.png'
flowers_image_20 = f'{mediafolder_garden}/hydrangea_02.png'
flowers_image_21 = f'{mediafolder_garden}/hydrangea_03.png'

flowers_image_22 = f'{mediafolder_garden}/lotus_01.png'
flowers_image_23 = f'{mediafolder_garden}/lotus_02.png'
flowers_image_24 = f'{mediafolder_garden}/lotus_03.png'

flowers_image_25 = f'{mediafolder_garden}/orchid_01.png'
flowers_image_26 = f'{mediafolder_garden}/orchid_02.png'
flowers_image_27 = f'{mediafolder_garden}/orchid_03.png'



CROPS_IMAGES_PATH_DICT.update({
    SUNFLOWER: [flowers_image_04, flowers_image_05, flowers_image_06],
    ROSE: [flowers_image_01, flowers_image_02, flowers_image_03],
    TULIP: [flowers_image_07, flowers_image_08, flowers_image_09],
    BIRD_OF_PARADISE: [flowers_image_10, flowers_image_11, flowers_image_12],
    CHAMOMILE: [flowers_image_13, flowers_image_14, flowers_image_15],
    HYACINTH: [flowers_image_16, flowers_image_17, flowers_image_18],
    HYDRANGEA: [flowers_image_19, flowers_image_20, flowers_image_21],
    LOTUS: [flowers_image_22, flowers_image_23, flowers_image_24],
    ORCHID: [flowers_image_25, flowers_image_26, flowers_image_27],
    CARROT: [plants_image_01, plants_image_02, plants_image_03, plants_image_04],
    POTATO: [plants_image_06, plants_image_07, plants_image_08, plants_image_09],
    PUMPKIN: [plants_image_11, plants_image_12, plants_image_13, plants_image_14],
    TOMATO: [plants_image_16, plants_image_17, plants_image_18, plants_image_19]
})



# Farm 02

Beets_01 = f"{mediafolder_farm_02}/Beets_01.png"
Beets_02 = f"{mediafolder_farm_02}/Beets_02.png"
Beets_03 = f"{mediafolder_farm_02}/Beets_03.png"
Beets_04 = f"{mediafolder_farm_02}/Beets_04.png"
Beets_05 = f"{mediafolder_farm_02}/Beets_05.png"

Eggplant_01 = f"{mediafolder_farm_02}/Eggplant_01.png"
Eggplant_02 = f"{mediafolder_farm_02}/Eggplant_02.png"
Eggplant_03 = f"{mediafolder_farm_02}/Eggplant_03.png"
Eggplant_04 = f"{mediafolder_farm_02}/Eggplant_04.png"
Eggplant_05 = f"{mediafolder_farm_02}/Eggplant_05.png"

Green_beans_01 = f"{mediafolder_farm_02}/Green beans_01.png"
Green_beans_02 = f"{mediafolder_farm_02}/Green beans_02.png"
Green_beans_03 = f"{mediafolder_farm_02}/Green beans_03.png"
Green_beans_04 = f"{mediafolder_farm_02}/Green beans_04.png"
Green_beans_05 = f"{mediafolder_farm_02}/Green beans_05.png"

Green_bell_pepper_01 = f"{mediafolder_farm_02}/Green bell pepper_01.png"
Green_bell_pepper_02 = f"{mediafolder_farm_02}/Green bell pepper_02.png"
Green_bell_pepper_03 = f"{mediafolder_farm_02}/Green bell pepper_03.png"
Green_bell_pepper_04 = f"{mediafolder_farm_02}/Green bell pepper_04.png"
Green_bell_pepper_05 = f"{mediafolder_farm_02}/Green bell pepper_05.png"

Rhubarb_01 = f"{mediafolder_farm_02}/Rhubarb_01.png"
Rhubarb_02 = f"{mediafolder_farm_02}/Rhubarb_02.png"
Rhubarb_03 = f"{mediafolder_farm_02}/Rhubarb_03.png"
Rhubarb_04 = f"{mediafolder_farm_02}/Rhubarb_04.png"

Acorn_squash_01 = f"{mediafolder_farm_02}/Acorn squash_01.png"
Acorn_squash_02 = f"{mediafolder_farm_02}/Acorn squash_02.png"
Acorn_squash_03 = f"{mediafolder_farm_02}/Acorn squash_03.png"
Acorn_squash_04 = f"{mediafolder_farm_02}/Acorn squash_04.png"
Acorn_squash_05 = f"{mediafolder_farm_02}/Acorn squash_05.png"

Artichoke_01 = f"{mediafolder_farm_02}/Artichoke_01.png"
Artichoke_02 = f"{mediafolder_farm_02}/Artichoke_02.png"
Artichoke_03 = f"{mediafolder_farm_02}/Artichoke_03.png"
Artichoke_04 = f"{mediafolder_farm_02}/Artichoke_04.png"
Artichoke_05 = f"{mediafolder_farm_02}/Artichoke_05.png"

Asparagus_01 = f"{mediafolder_farm_02}/Asparagus_01.png"
Asparagus_02 = f"{mediafolder_farm_02}/Asparagus_02.png"
Asparagus_03 = f"{mediafolder_farm_02}/Asparagus_03.png"
Asparagus_04 = f"{mediafolder_farm_02}/Asparagus_04.png"


BEETS = "beets"
EGGPLANT = "eggplant"
GREEN_BEANS = "green_beans"
GREEN_BELL_PEPPER = "green_bell_pepper"
RHUBARB = "rhubarb"
ACORN_SQUASH = "acorn_squash"
ARTICHOKE = "artichoke"
ASPARAGUS = "asparagus"

# THEMES.extend([BEETS, EGGPLANT, GREEN_BEANS, GREEN_BELL_PEPPER, RHUBARB, ACORN_SQUASH, ARTICHOKE, ASPARAGUS])

CROPS_IMAGES_PATH_DICT.update({
    BEETS: [Beets_01, Beets_02, Beets_03, Beets_04],
    EGGPLANT: [Eggplant_01, Eggplant_02, Eggplant_03, Eggplant_04],
    GREEN_BEANS: [Green_beans_01, Green_beans_02, Green_beans_03, Green_beans_04],
    GREEN_BELL_PEPPER: [Green_bell_pepper_01, Green_bell_pepper_02, Green_bell_pepper_03, Green_bell_pepper_04],
    RHUBARB: [Rhubarb_01, Rhubarb_02, Rhubarb_03, Rhubarb_04],
    ACORN_SQUASH: [Acorn_squash_01, Acorn_squash_02, Acorn_squash_03, Acorn_squash_04],
    ARTICHOKE: [Artichoke_01, Artichoke_02, Artichoke_03, Artichoke_04],
    ASPARAGUS: [Asparagus_01, Asparagus_02, Asparagus_03, Asparagus_04]
})

Blackberries_01 = f"{mediafolder_farm_02}/Blackberries_01.png"
Blackberries_02 = f"{mediafolder_farm_02}/Blackberries_02.png"
Blackberries_03 = f"{mediafolder_farm_02}/Blackberries_03.png"
Blackberries_04 = f"{mediafolder_farm_02}/Blackberries_04.png"
Blackberries_05 = f"{mediafolder_farm_02}/Blackberries_05.png"

Blueberries_01 = f"{mediafolder_farm_02}/Blueberries_01.png"
Blueberries_02 = f"{mediafolder_farm_02}/Blueberries_02.png"
Blueberries_03 = f"{mediafolder_farm_02}/Blueberries_03.png"
Blueberries_04 = f"{mediafolder_farm_02}/Blueberries_04.png"
Blueberries_05 = f"{mediafolder_farm_02}/Blueberries_05.png"

Bok_choy_01 = f"{mediafolder_farm_02}/Bok choy_01.png"
Bok_choy_02 = f"{mediafolder_farm_02}/Bok choy_02.png"
Bok_choy_03 = f"{mediafolder_farm_02}/Bok choy_03.png"
Bok_choy_04 = f"{mediafolder_farm_02}/Bok choy_04.png"
Bok_choy_05 = f"{mediafolder_farm_02}/Bok choy_05.png"

Broccoli_01 = f"{mediafolder_farm_02}/Broccoli_01.png"
Broccoli_02 = f"{mediafolder_farm_02}/Broccoli_02.png"
Broccoli_03 = f"{mediafolder_farm_02}/Broccoli_03.png"
Broccoli_04 = f"{mediafolder_farm_02}/Broccoli_04.png"
Broccoli_05 = f"{mediafolder_farm_02}/Broccoli_05.png"

Brussels_sprouts_01 = f"{mediafolder_farm_02}/Brussels sprouts_01.png"
Brussels_sprouts_02 = f"{mediafolder_farm_02}/Brussels sprouts_02.png"
Brussels_sprouts_03 = f"{mediafolder_farm_02}/Brussels sprouts_03.png"
Brussels_sprouts_04 = f"{mediafolder_farm_02}/Brussels sprouts_04.png"
Brussels_sprouts_05 = f"{mediafolder_farm_02}/Brussels sprouts_05.png"

Butternut_squash_01 = f"{mediafolder_farm_02}/Butternut squash_01.png"
Butternut_squash_02 = f"{mediafolder_farm_02}/Butternut squash_02.png"
Butternut_squash_03 = f"{mediafolder_farm_02}/Butternut squash_03.png"
Butternut_squash_04 = f"{mediafolder_farm_02}/Butternut squash_04.png"
Butternut_squash_05 = f"{mediafolder_farm_02}/Butternut squash_05.png"

Cantaloupe_melon_01 = f"{mediafolder_farm_02}/Cantaloupe melon_01.png"
Cantaloupe_melon_02 = f"{mediafolder_farm_02}/Cantaloupe melon_02.png"
Cantaloupe_melon_03 = f"{mediafolder_farm_02}/Cantaloupe melon_03.png"
Cantaloupe_melon_04 = f"{mediafolder_farm_02}/Cantaloupe melon_04.png"
Cantaloupe_melon_05 = f"{mediafolder_farm_02}/Cantaloupe melon_05.png"

Carrots_01 = f"{mediafolder_farm_02}/Carrots_01.png"
Carrots_02 = f"{mediafolder_farm_02}/Carrots_02.png"
Carrots_03 = f"{mediafolder_farm_02}/Carrots_03.png"
Carrots_04 = f"{mediafolder_farm_02}/Carrots_04.png"
Carrots_05 = f"{mediafolder_farm_02}/Carrots_05.png"

Cassava_01 = f"{mediafolder_farm_02}/Cassava_01.png"
Cassava_02 = f"{mediafolder_farm_02}/Cassava_02.png"
Cassava_03 = f"{mediafolder_farm_02}/Cassava_03.png"
Cassava_04 = f"{mediafolder_farm_02}/Cassava_04.png"
Cassava_05 = f"{mediafolder_farm_02}/Cassava_05.png"


BLACKBERRIES = "blackberries"
BLUEBERRIES = "blueberries"
BOK_CHOY = "bok_choy"
BROCCOLI = "broccoli"
BRUSSELS_SPROUTS = "brussels_sprouts"
BUTTERNUT_SQUASH = "butternut_squash"
CANTALOUPE_MELON = "cantaloupe_melon"
CARROTS = "carrots"
CASSAVA = "cassava"

# THEMES.extend([BLACKBERRIES, BLUEBERRIES, BOK_CHOY, BROCCOLI, BRUSSELS_SPROUTS, BUTTERNUT_SQUASH, CANTALOUPE_MELON, CARROTS, CASSAVA])

CROPS_IMAGES_PATH_DICT.update({
    BLACKBERRIES: [Blackberries_01, Blackberries_02, Blackberries_03, Blackberries_04],
    BLUEBERRIES: [Blueberries_01, Blueberries_02, Blueberries_03, Blueberries_04],
    BOK_CHOY: [Bok_choy_01, Bok_choy_02, Bok_choy_03, Bok_choy_04],
    BROCCOLI: [Broccoli_01, Broccoli_02, Broccoli_03, Broccoli_04],
    BRUSSELS_SPROUTS: [Brussels_sprouts_01, Brussels_sprouts_02, Brussels_sprouts_03, Brussels_sprouts_04],
    BUTTERNUT_SQUASH: [Butternut_squash_01, Butternut_squash_02, Butternut_squash_03, Butternut_squash_04],
    CANTALOUPE_MELON: [Cantaloupe_melon_01, Cantaloupe_melon_02, Cantaloupe_melon_03, Cantaloupe_melon_04],
    CARROTS: [Carrots_01, Carrots_02, Carrots_03, Carrots_04],
    CASSAVA: [Cassava_01, Cassava_02, Cassava_03, Cassava_04]
})


Cauliflower_01 = f"{mediafolder_farm_02}/Cauliflower_01.png"
Cauliflower_02 = f"{mediafolder_farm_02}/Cauliflower_02.png"
Cauliflower_03 = f"{mediafolder_farm_02}/Cauliflower_03.png"
Cauliflower_04 = f"{mediafolder_farm_02}/Cauliflower_04.png"
Cauliflower_05 = f"{mediafolder_farm_02}/Cauliflower_05.png"

Celery_01 = f"{mediafolder_farm_02}/Celery_01.png"
Celery_02 = f"{mediafolder_farm_02}/Celery_02.png"
Celery_03 = f"{mediafolder_farm_02}/Celery_03.png"
Celery_04 = f"{mediafolder_farm_02}/Celery_04.png"
Celery_05 = f"{mediafolder_farm_02}/Celery_05.png"

Cherry_tomatoes_01 = f"{mediafolder_farm_02}/Cherry tomatoes_01.png"
Cherry_tomatoes_02 = f"{mediafolder_farm_02}/Cherry tomatoes_02.png"
Cherry_tomatoes_03 = f"{mediafolder_farm_02}/Cherry tomatoes_03.png"
Cherry_tomatoes_04 = f"{mediafolder_farm_02}/Cherry tomatoes_04.png"
Cherry_tomatoes_05 = f"{mediafolder_farm_02}/Cherry tomatoes_05.png"

Chili_peppers_01 = f"{mediafolder_farm_02}/Chili peppers_01.png"
Chili_peppers_02 = f"{mediafolder_farm_02}/Chili peppers_02.png"
Chili_peppers_03 = f"{mediafolder_farm_02}/Chili peppers_03.png"
Chili_peppers_04 = f"{mediafolder_farm_02}/Chili peppers_04.png"
Chili_peppers_05 = f"{mediafolder_farm_02}/Chili peppers_05.png"

Coffee_01 = f"{mediafolder_farm_02}/Coffee_01.png"
Coffee_02 = f"{mediafolder_farm_02}/Coffee_02.png"
Coffee_03 = f"{mediafolder_farm_02}/Coffee_03.png"
Coffee_04 = f"{mediafolder_farm_02}/Coffee_04.png"
Coffee_05 = f"{mediafolder_farm_02}/Coffee_05.png"

Corn_A_01 = f"{mediafolder_farm_02}/Corn A_01.png"
Corn_A_02 = f"{mediafolder_farm_02}/Corn A_02.png"
Corn_A_03 = f"{mediafolder_farm_02}/Corn A_03.png"
Corn_A_04 = f"{mediafolder_farm_02}/Corn A_04.png"
Corn_A_05 = f"{mediafolder_farm_02}/Corn A_05.png"

Corn_B_01 = f"{mediafolder_farm_02}/Corn B_01.png"
Corn_B_02 = f"{mediafolder_farm_02}/Corn B_02.png"
Corn_B_03 = f"{mediafolder_farm_02}/Corn B_03.png"
Corn_B_04 = f"{mediafolder_farm_02}/Corn B_04.png"
Corn_B_05 = f"{mediafolder_farm_02}/Corn B_05.png"

Crookneck_squash_01 = f"{mediafolder_farm_02}/Crookneck squash_01.png"
Crookneck_squash_02 = f"{mediafolder_farm_02}/Crookneck squash_02.png"
Crookneck_squash_03 = f"{mediafolder_farm_02}/Crookneck squash_03.png"
Crookneck_squash_04 = f"{mediafolder_farm_02}/Crookneck squash_04.png"
Crookneck_squash_05 = f"{mediafolder_farm_02}/Crookneck squash_05.png"

Cucumber_01 = f"{mediafolder_farm_02}/Cucumber_01.png"
Cucumber_02 = f"{mediafolder_farm_02}/Cucumber_02.png"
Cucumber_03 = f"{mediafolder_farm_02}/Cucumber_03.png"
Cucumber_04 = f"{mediafolder_farm_02}/Cucumber_04.png"
Cucumber_05 = f"{mediafolder_farm_02}/Cucumber_05.png"

Daikon_radish_01 = f"{mediafolder_farm_02}/Daikon radish_01.png"
Daikon_radish_02 = f"{mediafolder_farm_02}/Daikon radish_02.png"
Daikon_radish_03 = f"{mediafolder_farm_02}/Daikon radish_03.png"
Daikon_radish_04 = f"{mediafolder_farm_02}/Daikon radish_04.png"
Daikon_radish_05 = f"{mediafolder_farm_02}/Daikon radish_05.png"

Fennel_bulb_01 = f"{mediafolder_farm_02}/Fennel bulb_01.png"
Fennel_bulb_02 = f"{mediafolder_farm_02}/Fennel bulb_02.png"
Fennel_bulb_03 = f"{mediafolder_farm_02}/Fennel bulb_03.png"
Fennel_bulb_04 = f"{mediafolder_farm_02}/Fennel bulb_04.png"
Fennel_bulb_05 = f"{mediafolder_farm_02}/Fennel bulb_05.png"

Garlic_01 = f"{mediafolder_farm_02}/Garlic_01.png"
Garlic_02 = f"{mediafolder_farm_02}/Garlic_02.png"
Garlic_03 = f"{mediafolder_farm_02}/Garlic_03.png"
Garlic_04 = f"{mediafolder_farm_02}/Garlic_04.png"
Garlic_05 = f"{mediafolder_farm_02}/Garlic_05.png"

Gold_potatoes_01 = f"{mediafolder_farm_02}/Gold potatoes_01.png"
Gold_potatoes_02 = f"{mediafolder_farm_02}/Gold potatoes_02.png"
Gold_potatoes_03 = f"{mediafolder_farm_02}/Gold potatoes_03.png"
Gold_potatoes_04 = f"{mediafolder_farm_02}/Gold potatoes_04.png"
Gold_potatoes_05 = f"{mediafolder_farm_02}/Gold potatoes_05.png"

Green_cabbage_01 = f"{mediafolder_farm_02}/Green cabbage_01.png"
Green_cabbage_02 = f"{mediafolder_farm_02}/Green cabbage_02.png"
Green_cabbage_03 = f"{mediafolder_farm_02}/Green cabbage_03.png"
Green_cabbage_04 = f"{mediafolder_farm_02}/Green cabbage_04.png"
Green_cabbage_05 = f"{mediafolder_farm_02}/Green cabbage_05.png"

Green_grapes_01 = f"{mediafolder_farm_02}/Green grapes_01.png"
Green_grapes_02 = f"{mediafolder_farm_02}/Green grapes_02.png"
Green_grapes_03 = f"{mediafolder_farm_02}/Green grapes_03.png"
Green_grapes_04 = f"{mediafolder_farm_02}/Green grapes_04.png"
Green_grapes_05 = f"{mediafolder_farm_02}/Green grapes_05.png"

Honeydew_melon_01 = f"{mediafolder_farm_02}/Honeydew melon_01.png"
Honeydew_melon_02 = f"{mediafolder_farm_02}/Honeydew melon_02.png"
Honeydew_melon_03 = f"{mediafolder_farm_02}/Honeydew melon_03.png"
Honeydew_melon_04 = f"{mediafolder_farm_02}/Honeydew melon_04.png"
Honeydew_melon_05 = f"{mediafolder_farm_02}/Honeydew melon_05.png"

Hops_01 = f"{mediafolder_farm_02}/Hops_01.png"
Hops_02 = f"{mediafolder_farm_02}/Hops_02.png"
Hops_03 = f"{mediafolder_farm_02}/Hops_03.png"
Hops_04 = f"{mediafolder_farm_02}/Hops_04.png"
Hops_05 = f"{mediafolder_farm_02}/Hops_05.png"

Hot_pepper_01 = f"{mediafolder_farm_02}/Hot pepper_01.png"
Hot_pepper_02 = f"{mediafolder_farm_02}/Hot pepper_02.png"
Hot_pepper_03 = f"{mediafolder_farm_02}/Hot pepper_03.png"
Hot_pepper_04 = f"{mediafolder_farm_02}/Hot pepper_04.png"
Hot_pepper_05 = f"{mediafolder_farm_02}/Hot pepper_05.png"

Iceberg_lettuce_01 = f"{mediafolder_farm_02}/Iceberg lettuce_01.png"
Iceberg_lettuce_02 = f"{mediafolder_farm_02}/Iceberg lettuce_02.png"
Iceberg_lettuce_03 = f"{mediafolder_farm_02}/Iceberg lettuce_03.png"
Iceberg_lettuce_04 = f"{mediafolder_farm_02}/Iceberg lettuce_04.png"
Iceberg_lettuce_05 = f"{mediafolder_farm_02}/Iceberg lettuce_05.png"


CAULIFLOWER = "cauliflower"
CELERY = "celery"
CHERRY_TOMATOES = "cherry_tomatoes"
CHILI_PEPPERS = "chili_peppers"
COFFEE = "coffee"
CORN_A = "corn_a"
CORN_B = "corn_b"
CROOKNECK_SQUASH = "crookneck_squash"
CUCUMBER = "cucumber"
DAIKON_RADISH = "daikon_radish"
FENNEL_BULB = "fennel_bulb"
GARLIC = "garlic"
GOLD_POTATOES = "gold_potatoes"
GREEN_CABBAGE = "green_cabbage"
GREEN_GRAPES = "green_grapes"
HONEYDEW_MELON = "honeydew_melon"
HOPS = "hops"
HOT_PEPPER = "hot_pepper"
ICEBERG_LETTUCE = "iceberg_lettuce"

# THEMES.extend([
#     CAULIFLOWER, CELERY, CHERRY_TOMATOES, CHILI_PEPPERS, COFFEE, CORN_A, CORN_B, CROOKNECK_SQUASH, CUCUMBER,
#     DAIKON_RADISH, FENNEL_BULB, GARLIC, GOLD_POTATOES, GREEN_CABBAGE, GREEN_GRAPES, HONEYDEW_MELON, HOPS,
#     HOT_PEPPER, ICEBERG_LETTUCE
# ])

CROPS_IMAGES_PATH_DICT.update({
    CAULIFLOWER: [Cauliflower_01, Cauliflower_02, Cauliflower_03, Cauliflower_04],
    CELERY: [Celery_01, Celery_02, Celery_03, Celery_04],
    CHERRY_TOMATOES: [Cherry_tomatoes_01, Cherry_tomatoes_02, Cherry_tomatoes_03, Cherry_tomatoes_04],
    CHILI_PEPPERS: [Chili_peppers_01, Chili_peppers_02, Chili_peppers_03, Chili_peppers_04],
    COFFEE: [Coffee_01, Coffee_02, Coffee_03, Coffee_04],
    CORN_A: [Corn_A_01, Corn_A_02, Corn_A_03, Corn_A_04],
    CORN_B: [Corn_B_01, Corn_B_02, Corn_B_03, Corn_B_04],
    CROOKNECK_SQUASH: [Crookneck_squash_01, Crookneck_squash_02, Crookneck_squash_03, Crookneck_squash_04],
    CUCUMBER: [Cucumber_01, Cucumber_02, Cucumber_03, Cucumber_04],
    DAIKON_RADISH: [Daikon_radish_01, Daikon_radish_02, Daikon_radish_03, Daikon_radish_04],
    FENNEL_BULB: [Fennel_bulb_01, Fennel_bulb_02, Fennel_bulb_03, Fennel_bulb_04],
    GARLIC: [Garlic_01, Garlic_02, Garlic_03, Garlic_04],
    GOLD_POTATOES: [Gold_potatoes_01, Gold_potatoes_02, Gold_potatoes_03, Gold_potatoes_04],
    GREEN_CABBAGE: [Green_cabbage_01, Green_cabbage_02, Green_cabbage_03, Green_cabbage_04],
    GREEN_GRAPES: [Green_grapes_01, Green_grapes_02, Green_grapes_03, Green_grapes_04],
    HONEYDEW_MELON: [Honeydew_melon_01, Honeydew_melon_02, Honeydew_melon_03, Honeydew_melon_04],
    HOPS: [Hops_01, Hops_02, Hops_03, Hops_04],
    HOT_PEPPER: [Hot_pepper_01, Hot_pepper_02, Hot_pepper_03, Hot_pepper_04],
    ICEBERG_LETTUCE: [Iceberg_lettuce_01, Iceberg_lettuce_02, Iceberg_lettuce_03, Iceberg_lettuce_04]
})



Kale_01 = f"{mediafolder_farm_02}/Kale_01.png"
Kale_02 = f"{mediafolder_farm_02}/Kale_02.png"
Kale_03 = f"{mediafolder_farm_02}/Kale_03.png"
Kale_04 = f"{mediafolder_farm_02}/Kale_04.png"
Kale_05 = f"{mediafolder_farm_02}/Kale_05.png"

Kiwi_01 = f"{mediafolder_farm_02}/Kiwi_01.png"
Kiwi_02 = f"{mediafolder_farm_02}/Kiwi_02.png"
Kiwi_03 = f"{mediafolder_farm_02}/Kiwi_03.png"
Kiwi_04 = f"{mediafolder_farm_02}/Kiwi_04.png"
Kiwi_05 = f"{mediafolder_farm_02}/Kiwi_05.png"

Kohlrabi_01 = f"{mediafolder_farm_02}/Kohlrabi_01.png"
Kohlrabi_02 = f"{mediafolder_farm_02}/Kohlrabi_02.png"
Kohlrabi_03 = f"{mediafolder_farm_02}/Kohlrabi_03.png"
Kohlrabi_04 = f"{mediafolder_farm_02}/Kohlrabi_04.png"
Kohlrabi_05 = f"{mediafolder_farm_02}/Kohlrabi_05.png"

Large_tomatoes_01 = f"{mediafolder_farm_02}/Large tomatoes_01.png"
Large_tomatoes_02 = f"{mediafolder_farm_02}/Large tomatoes_02.png"
Large_tomatoes_03 = f"{mediafolder_farm_02}/Large tomatoes_03.png"
Large_tomatoes_04 = f"{mediafolder_farm_02}/Large tomatoes_04.png"
Large_tomatoes_05 = f"{mediafolder_farm_02}/Large tomatoes_05.png"

Leeks_01 = f"{mediafolder_farm_02}/Leeks_01.png"
Leeks_02 = f"{mediafolder_farm_02}/Leeks_02.png"
Leeks_03 = f"{mediafolder_farm_02}/Leeks_03.png"
Leeks_04 = f"{mediafolder_farm_02}/Leeks_04.png"
Leeks_05 = f"{mediafolder_farm_02}/Leeks_05.png"

Orange_bell_pepper_01 = f"{mediafolder_farm_02}/Orange bell pepper_01.png"
Orange_bell_pepper_02 = f"{mediafolder_farm_02}/Orange bell pepper_02.png"
Orange_bell_pepper_03 = f"{mediafolder_farm_02}/Orange bell pepper_03.png"
Orange_bell_pepper_04 = f"{mediafolder_farm_02}/Orange bell pepper_04.png"
Orange_bell_pepper_05 = f"{mediafolder_farm_02}/Orange bell pepper_05.png"

Parsnips_01 = f"{mediafolder_farm_02}/Parsnips_01.png"
Parsnips_02 = f"{mediafolder_farm_02}/Parsnips_02.png"
Parsnips_03 = f"{mediafolder_farm_02}/Parsnips_03.png"
Parsnips_04 = f"{mediafolder_farm_02}/Parsnips_04.png"
Parsnips_05 = f"{mediafolder_farm_02}/Parsnips_05.png"

Peas_01 = f"{mediafolder_farm_02}/Peas_01.png"
Peas_02 = f"{mediafolder_farm_02}/Peas_02.png"
Peas_03 = f"{mediafolder_farm_02}/Peas_03.png"
Peas_04 = f"{mediafolder_farm_02}/Peas_04.png"
Peas_05 = f"{mediafolder_farm_02}/Peas_05.png"

Pineapple_01 = f"{mediafolder_farm_02}/Pineapple_01.png"
Pineapple_02 = f"{mediafolder_farm_02}/Pineapple_02.png"
Pineapple_03 = f"{mediafolder_farm_02}/Pineapple_03.png"
Pineapple_04 = f"{mediafolder_farm_02}/Pineapple_04.png"
Pineapple_05 = f"{mediafolder_farm_02}/Pineapple_05.png"

Pumpkin_01 = f"{mediafolder_farm_02}/Pumpkin_01.png"
Pumpkin_02 = f"{mediafolder_farm_02}/Pumpkin_02.png"
Pumpkin_03 = f"{mediafolder_farm_02}/Pumpkin_03.png"
Pumpkin_04 = f"{mediafolder_farm_02}/Pumpkin_04.png"
Pumpkin_05 = f"{mediafolder_farm_02}/Pumpkin_05.png"

Purple_cabbage_01 = f"{mediafolder_farm_02}/Purple cabbage_01.png"
Purple_cabbage_02 = f"{mediafolder_farm_02}/Purple cabbage_02.png"
Purple_cabbage_03 = f"{mediafolder_farm_02}/Purple cabbage_03.png"
Purple_cabbage_04 = f"{mediafolder_farm_02}/Purple cabbage_04.png"
Purple_cabbage_05 = f"{mediafolder_farm_02}/Purple cabbage_05.png"

Purple_onion_01 = f"{mediafolder_farm_02}/Purple onion_01.png"
Purple_onion_02 = f"{mediafolder_farm_02}/Purple onion_02.png"
Purple_onion_03 = f"{mediafolder_farm_02}/Purple onion_03.png"
Purple_onion_04 = f"{mediafolder_farm_02}/Purple onion_04.png"
Purple_onion_05 = f"{mediafolder_farm_02}/Purple onion_05.png"

Purple_potatoes_01 = f"{mediafolder_farm_02}/Purple potatoes_01.png"
Purple_potatoes_02 = f"{mediafolder_farm_02}/Purple potatoes_02.png"
Purple_potatoes_03 = f"{mediafolder_farm_02}/Purple potatoes_03.png"
Purple_potatoes_04 = f"{mediafolder_farm_02}/Purple potatoes_04.png"
Purple_potatoes_05 = f"{mediafolder_farm_02}/Purple potatoes_05.png"

Radishes_01 = f"{mediafolder_farm_02}/Radishes_01.png"
Radishes_02 = f"{mediafolder_farm_02}/Radishes_02.png"
Radishes_03 = f"{mediafolder_farm_02}/Radishes_03.png"
Radishes_04 = f"{mediafolder_farm_02}/Radishes_04.png"
Radishes_05 = f"{mediafolder_farm_02}/Radishes_05.png"

Raspberries_01 = f"{mediafolder_farm_02}/Raspberries_01.png"
Raspberries_02 = f"{mediafolder_farm_02}/Raspberries_02.png"
Raspberries_03 = f"{mediafolder_farm_02}/Raspberries_03.png"
Raspberries_04 = f"{mediafolder_farm_02}/Raspberries_04.png"
Raspberries_05 = f"{mediafolder_farm_02}/Raspberries_05.png"

Red_bell_pepper_01 = f"{mediafolder_farm_02}/Red bell pepper_01.png"
Red_bell_pepper_02 = f"{mediafolder_farm_02}/Red bell pepper_02.png"
Red_bell_pepper_03 = f"{mediafolder_farm_02}/Red bell pepper_03.png"
Red_bell_pepper_04 = f"{mediafolder_farm_02}/Red bell pepper_04.png"
Red_bell_pepper_05 = f"{mediafolder_farm_02}/Red bell pepper_05.png"

Red_grapes_01 = f"{mediafolder_farm_02}/Red grapes_01.png"
Red_grapes_02 = f"{mediafolder_farm_02}/Red grapes_02.png"
Red_grapes_03 = f"{mediafolder_farm_02}/Red grapes_03.png"
Red_grapes_04 = f"{mediafolder_farm_02}/Red grapes_04.png"
Red_grapes_05 = f"{mediafolder_farm_02}/Red grapes_05.png"


KALE = "kale"
KIWI = "kiwi"
KOHLRABI = "kohlrabi"
LARGE_TOMATOES = "large_tomatoes"
LEEKS = "leeks"
ORANGE_BELL_PEPPER = "orange_bell_pepper"
PARSNIPS = "parsnips"
PEAS = "peas"
PINEAPPLE = "pineapple"
PUMPKIN_B= "pumpkin_B"
PURPLE_CABBAGE = "purple_cabbage"
PURPLE_ONION = "purple_onion"
PURPLE_POTATOES = "purple_potatoes"
RADISHES = "radishes"
RASPBERRIES = "raspberries"
RED_BELL_PEPPER = "red_bell_pepper"
RED_GRAPES = "red_grapes"

# THEMES.extend([
#     KALE, KIWI, KOHLRABI, LARGE_TOMATOES, LEEKS, ORANGE_BELL_PEPPER, PARSNIPS, PEAS, PINEAPPLE, 
#     PUMPKIN_B, PURPLE_CABBAGE, PURPLE_ONION, PURPLE_POTATOES, RADISHES, RASPBERRIES, RED_BELL_PEPPER, RED_GRAPES
# ])


CROPS_IMAGES_PATH_DICT.update({
    KALE: [Kale_01, Kale_02, Kale_03, Kale_04],
    KIWI: [Kiwi_01, Kiwi_02, Kiwi_03, Kiwi_04],
    KOHLRABI: [Kohlrabi_01, Kohlrabi_02, Kohlrabi_03, Kohlrabi_04],
    LARGE_TOMATOES: [Large_tomatoes_01, Large_tomatoes_02, Large_tomatoes_03, Large_tomatoes_04],
    LEEKS: [Leeks_01, Leeks_02, Leeks_03, Leeks_04],
    ORANGE_BELL_PEPPER: [Orange_bell_pepper_01, Orange_bell_pepper_02, Orange_bell_pepper_03, Orange_bell_pepper_04],
    PARSNIPS: [Parsnips_01, Parsnips_02, Parsnips_03, Parsnips_04],
    PEAS: [Peas_01, Peas_02, Peas_03, Peas_04],
    PINEAPPLE: [Pineapple_01, Pineapple_02, Pineapple_03, Pineapple_04],
    PUMPKIN_B: [Pumpkin_01, Pumpkin_02, Pumpkin_03, Pumpkin_04],
    PURPLE_CABBAGE: [Purple_cabbage_01, Purple_cabbage_02, Purple_cabbage_03, Purple_cabbage_04],
    PURPLE_ONION: [Purple_onion_01, Purple_onion_02, Purple_onion_03, Purple_onion_04],
    PURPLE_POTATOES: [Purple_potatoes_01, Purple_potatoes_02, Purple_potatoes_03, Purple_potatoes_04],
    RADISHES: [Radishes_01, Radishes_02, Radishes_03, Radishes_04],
    RASPBERRIES: [Raspberries_01, Raspberries_02, Raspberries_03, Raspberries_04],
    RED_BELL_PEPPER: [Red_bell_pepper_01, Red_bell_pepper_02, Red_bell_pepper_03, Red_bell_pepper_04],
    RED_GRAPES: [Red_grapes_01, Red_grapes_02, Red_grapes_03, Red_grapes_04]
})



Romaine_lettuce_01 = f"{mediafolder_farm_02}/Romaine lettuce_01.png"
Romaine_lettuce_02 = f"{mediafolder_farm_02}/Romaine lettuce_02.png"
Romaine_lettuce_03 = f"{mediafolder_farm_02}/Romaine lettuce_03.png"
Romaine_lettuce_04 = f"{mediafolder_farm_02}/Romaine lettuce_04.png"
Romaine_lettuce_05 = f"{mediafolder_farm_02}/Romaine lettuce_05.png"

Russet_potatoes_01 = f"{mediafolder_farm_02}/Russet potatoes_01.png"
Russet_potatoes_02 = f"{mediafolder_farm_02}/Russet potatoes_02.png"
Russet_potatoes_03 = f"{mediafolder_farm_02}/Russet potatoes_03.png"
Russet_potatoes_04 = f"{mediafolder_farm_02}/Russet potatoes_04.png"
Russet_potatoes_05 = f"{mediafolder_farm_02}/Russet potatoes_05.png"

Rutabaga_01 = f"{mediafolder_farm_02}/Rutabaga_01.png"
Rutabaga_02 = f"{mediafolder_farm_02}/Rutabaga_02.png"
Rutabaga_03 = f"{mediafolder_farm_02}/Rutabaga_03.png"
Rutabaga_04 = f"{mediafolder_farm_02}/Rutabaga_04.png"
Rutabaga_05 = f"{mediafolder_farm_02}/Rutabaga_05.png"

Scallion_01 = f"{mediafolder_farm_02}/Scallion_01.png"
Scallion_02 = f"{mediafolder_farm_02}/Scallion_02.png"
Scallion_03 = f"{mediafolder_farm_02}/Scallion_03.png"
Scallion_04 = f"{mediafolder_farm_02}/Scallion_04.png"
Scallion_05 = f"{mediafolder_farm_02}/Scallion_05.png"

Sweet_onion_01 = f"{mediafolder_farm_02}/Sweet onion_01.png"
Sweet_onion_02 = f"{mediafolder_farm_02}/Sweet onion_02.png"
Sweet_onion_03 = f"{mediafolder_farm_02}/Sweet onion_03.png"
Sweet_onion_04 = f"{mediafolder_farm_02}/Sweet onion_04.png"
Sweet_onion_05 = f"{mediafolder_farm_02}/Sweet onion_05.png"

Sweet_potatoes_01 = f"{mediafolder_farm_02}/Sweet potatoes_01.png"
Sweet_potatoes_02 = f"{mediafolder_farm_02}/Sweet potatoes_02.png"
Sweet_potatoes_03 = f"{mediafolder_farm_02}/Sweet potatoes_03.png"
Sweet_potatoes_04 = f"{mediafolder_farm_02}/Sweet potatoes_04.png"
Sweet_potatoes_05 = f"{mediafolder_farm_02}/Sweet potatoes_05.png"

Tomatoes_01 = f"{mediafolder_farm_02}/Tomatoes_01.png"
Tomatoes_02 = f"{mediafolder_farm_02}/Tomatoes_02.png"
Tomatoes_03 = f"{mediafolder_farm_02}/Tomatoes_03.png"
Tomatoes_04 = f"{mediafolder_farm_02}/Tomatoes_04.png"
Tomatoes_05 = f"{mediafolder_farm_02}/Tomatoes_05.png"

Turnips_01 = f"{mediafolder_farm_02}/Turnips_01.png"
Turnips_02 = f"{mediafolder_farm_02}/Turnips_02.png"
Turnips_03 = f"{mediafolder_farm_02}/Turnips_03.png"
Turnips_04 = f"{mediafolder_farm_02}/Turnips_04.png"
Turnips_05 = f"{mediafolder_farm_02}/Turnips_05.png"

Watermelon_01 = f"{mediafolder_farm_02}/Watermelon_01.png"
Watermelon_02 = f"{mediafolder_farm_02}/Watermelon_02.png"
Watermelon_03 = f"{mediafolder_farm_02}/Watermelon_03.png"
Watermelon_04 = f"{mediafolder_farm_02}/Watermelon_04.png"
Watermelon_05 = f"{mediafolder_farm_02}/Watermelon_05.png"

White_onion_01 = f"{mediafolder_farm_02}/White onion_01.png"
White_onion_02 = f"{mediafolder_farm_02}/White onion_02.png"
White_onion_03 = f"{mediafolder_farm_02}/White onion_03.png"
White_onion_04 = f"{mediafolder_farm_02}/White onion_04.png"
White_onion_05 = f"{mediafolder_farm_02}/White onion_05.png"

Yellow_bell_pepper_01 = f"{mediafolder_farm_02}/Yellow bell pepper_01.png"
Yellow_bell_pepper_02 = f"{mediafolder_farm_02}/Yellow bell pepper_02.png"
Yellow_bell_pepper_03 = f"{mediafolder_farm_02}/Yellow bell pepper_03.png"
Yellow_bell_pepper_04 = f"{mediafolder_farm_02}/Yellow bell pepper_04.png"
Yellow_bell_pepper_05 = f"{mediafolder_farm_02}/Yellow bell pepper_05.png"

Yellow_squash_01 = f"{mediafolder_farm_02}/Yellow squash_01.png"
Yellow_squash_02 = f"{mediafolder_farm_02}/Yellow squash_02.png"
Yellow_squash_03 = f"{mediafolder_farm_02}/Yellow squash_03.png"
Yellow_squash_04 = f"{mediafolder_farm_02}/Yellow squash_04.png"
Yellow_squash_05 = f"{mediafolder_farm_02}/Yellow squash_05.png"

Zucchini_01 = f"{mediafolder_farm_02}/Zucchini_01.png"
Zucchini_02 = f"{mediafolder_farm_02}/Zucchini_02.png"
Zucchini_03 = f"{mediafolder_farm_02}/Zucchini_03.png"
Zucchini_04 = f"{mediafolder_farm_02}/Zucchini_04.png"
Zucchini_05 = f"{mediafolder_farm_02}/Zucchini_05.png"


ROMAINE_LETTUCE = "romaine_lettuce"
RUSSET_POTATOES = "russet_potatoes"
RUTABAGA = "rutabaga"
SCALLION = "scallion"
SWEET_ONION = "sweet_onion"
SWEET_POTATOES = "sweet_potatoes"
TOMATOES = "tomatoes"
TURNIPS = "turnips"
WATERMELON = "watermelon"
WHITE_ONION = "white_onion"
YELLOW_BELL_PEPPER = "yellow_bell_pepper"
YELLOW_SQUASH = "yellow_squash"
ZUCCHINI = "zucchini"

# THEMES.extend([
#     ROMAINE_LETTUCE, RUSSET_POTATOES, RUTABAGA, SCALLION, SWEET_ONION, SWEET_POTATOES, TOMATOES, TURNIPS, WATERMELON,
#     WHITE_ONION, YELLOW_BELL_PEPPER, YELLOW_SQUASH, ZUCCHINI
# ])


CROPS_IMAGES_PATH_DICT.update({
    ROMAINE_LETTUCE: [Romaine_lettuce_01, Romaine_lettuce_02, Romaine_lettuce_03, Romaine_lettuce_04],
    RUSSET_POTATOES: [Russet_potatoes_01, Russet_potatoes_02, Russet_potatoes_03, Russet_potatoes_04],
    RUTABAGA: [Rutabaga_01, Rutabaga_02, Rutabaga_03, Rutabaga_04],
    SCALLION: [Scallion_01, Scallion_02, Scallion_03, Scallion_04],
    SWEET_ONION: [Sweet_onion_01, Sweet_onion_02, Sweet_onion_03, Sweet_onion_04],
    SWEET_POTATOES: [Sweet_potatoes_01, Sweet_potatoes_02, Sweet_potatoes_03, Sweet_potatoes_04],
    TOMATOES: [Tomatoes_01, Tomatoes_02, Tomatoes_03, Tomatoes_04],
    TURNIPS: [Turnips_01, Turnips_02, Turnips_03, Turnips_04],
    WATERMELON: [Watermelon_01, Watermelon_02, Watermelon_03, Watermelon_04],
    WHITE_ONION: [White_onion_01, White_onion_02, White_onion_03, White_onion_04],
    YELLOW_BELL_PEPPER: [Yellow_bell_pepper_01, Yellow_bell_pepper_02, Yellow_bell_pepper_03, Yellow_bell_pepper_04],
    YELLOW_SQUASH: [Yellow_squash_01, Yellow_squash_02, Yellow_squash_03, Yellow_squash_04],
    ZUCCHINI: [Zucchini_01, Zucchini_02, Zucchini_03, Zucchini_04]
})


# THEMES.extend([BEETS, EGGPLANT, GREEN_BEANS, GREEN_BELL_PEPPER, RHUBARB, ACORN_SQUASH, ARTICHOKE, ASPARAGUS])

# THEMES.extend([BLACKBERRIES, BLUEBERRIES, BOK_CHOY, BROCCOLI, BRUSSELS_SPROUTS, BUTTERNUT_SQUASH, CANTALOUPE_MELON, CARROTS, CASSAVA])

# THEMES.extend([
#     CAULIFLOWER, CELERY, CHERRY_TOMATOES, CHILI_PEPPERS, COFFEE, CORN_A, CORN_B, CROOKNECK_SQUASH, CUCUMBER,
#     DAIKON_RADISH, FENNEL_BULB, GARLIC, GOLD_POTATOES, GREEN_CABBAGE, GREEN_GRAPES, HONEYDEW_MELON, HOPS,
#     HOT_PEPPER, ICEBERG_LETTUCE
# ])

# THEMES.extend([
#     KALE, KIWI, KOHLRABI, LARGE_TOMATOES, LEEKS, ORANGE_BELL_PEPPER, PARSNIPS, PEAS, PINEAPPLE, 
#     PUMPKIN_B, PURPLE_CABBAGE, PURPLE_ONION, PURPLE_POTATOES, RADISHES, RASPBERRIES, RED_BELL_PEPPER, RED_GRAPES
# ])

# THEMES.extend([
#     ROMAINE_LETTUCE, RUSSET_POTATOES, RUTABAGA, SCALLION, SWEET_ONION, SWEET_POTATOES, TOMATOES, TURNIPS, WATERMELON,
#     WHITE_ONION, YELLOW_BELL_PEPPER, YELLOW_SQUASH, ZUCCHINI
# ])

THEMES.extend([
    RUSSET_POTATOES, GOLD_POTATOES, PURPLE_POTATOES, SWEET_POTATOES, CASSAVA, DAIKON_RADISH, CARROTS, PARSNIPS, RADISHES, BEETS, TURNIPS, RUTABAGA,
    GARLIC, SWEET_ONION, PURPLE_ONION, WHITE_ONION, SCALLION, HOT_PEPPER, GREEN_BELL_PEPPER, RED_BELL_PEPPER, ORANGE_BELL_PEPPER, YELLOW_BELL_PEPPER,
    CHILI_PEPPERS, WATERMELON, HONEYDEW_MELON, CANTALOUPE_MELON, ACORN_SQUASH, PUMPKIN_B, CROOKNECK_SQUASH, BUTTERNUT_SQUASH, CORN_A, CORN_B,
    ASPARAGUS, RHUBARB, ROMAINE_LETTUCE, ICEBERG_LETTUCE, KALE, PURPLE_CABBAGE, GREEN_CABBAGE, CELERY, BOK_CHOY, FENNEL_BULB, BRUSSELS_SPROUTS,
    CAULIFLOWER, BROCCOLI, ARTICHOKE, LEEKS, KOHLRABI, EGGPLANT, ZUCCHINI, YELLOW_SQUASH, CUCUMBER, BLACKBERRIES, RASPBERRIES, BLUEBERRIES,
    RED_GRAPES, GREEN_GRAPES, CHERRY_TOMATOES, TOMATOES, LARGE_TOMATOES, PEAS, HOPS, GREEN_BEANS, COFFEE, PINEAPPLE, KIWI
])


def set_image_theme(self, get_image_theme):
    # print(get_image_theme in image_dict)
    if get_image_theme in CROPS_IMAGES_PATH_DICT:
        images = CROPS_IMAGES_PATH_DICT[get_image_theme]
        # print(images)
        for i in range(1, 11):
            # print(images[min(i-1, len(images)-1)])
            setattr(self, f'heatmap_image_{i:02}', images[min(i-1, len(images)-1)])



# ======================================

import random
import time

class PlantSpecies:
    def __init__(self, random_mode=False):
        if random_mode:
            if not random_mode in THEMES:
                random_mode = random.choice(THEMES)
            get_image_theme = random_mode
        else:
            config = mw.addonManager.getConfig(__name__)
            get_image_theme = config.get("plant_species", SUNFLOWER)
        # get_image_theme = random.choice(THEMES)
        set_image_theme(self, get_image_theme)
        # set_image_theme(self, get_image_theme)



# class PlantSpecies:
#     def __init__(self):
#         config = mw.addonManager.getConfig(__name__)
#         get_image_theme = config.get("plant_species", SUNFLOWER)

#         # Garden

#         if get_image_theme == SUNFLOWER:
#             self.heatmap_image_01 = flowers_image_04
#             self.heatmap_image_02 = flowers_image_05
#             self.heatmap_image_03 = flowers_image_06
#             self.heatmap_image_04 = flowers_image_06
#             self.heatmap_image_05 = flowers_image_06
#             self.heatmap_image_06 = flowers_image_06
#             self.heatmap_image_07 = flowers_image_06
#             self.heatmap_image_08 = flowers_image_06
#             self.heatmap_image_09 = flowers_image_06
#             self.heatmap_image_10 = flowers_image_06

#         elif get_image_theme == ROSE:
#             self.heatmap_image_01 = flowers_image_01
#             self.heatmap_image_02 = flowers_image_02
#             self.heatmap_image_03 = flowers_image_03
#             self.heatmap_image_04 = flowers_image_03
#             self.heatmap_image_05 = flowers_image_03
#             self.heatmap_image_06 = flowers_image_03
#             self.heatmap_image_07 = flowers_image_03
#             self.heatmap_image_08 = flowers_image_03
#             self.heatmap_image_09 = flowers_image_03
#             self.heatmap_image_10 = flowers_image_03

#         elif  get_image_theme == TULIP:
#             self.heatmap_image_01 = flowers_image_07
#             self.heatmap_image_02 = flowers_image_08
#             self.heatmap_image_03 = flowers_image_09
#             self.heatmap_image_04 = flowers_image_09
#             self.heatmap_image_05 = flowers_image_09
#             self.heatmap_image_06 = flowers_image_09
#             self.heatmap_image_07 = flowers_image_09
#             self.heatmap_image_08 = flowers_image_09
#             self.heatmap_image_09 = flowers_image_09
#             self.heatmap_image_10 = flowers_image_09

#         elif  get_image_theme == BIRD_OF_PARADISE:
#             self.heatmap_image_01 = flowers_image_10
#             self.heatmap_image_02 = flowers_image_11
#             self.heatmap_image_03 = flowers_image_12
#             self.heatmap_image_04 = flowers_image_12
#             self.heatmap_image_05 = flowers_image_12
#             self.heatmap_image_06 = flowers_image_12
#             self.heatmap_image_07 = flowers_image_12
#             self.heatmap_image_08 = flowers_image_12
#             self.heatmap_image_09 = flowers_image_12
#             self.heatmap_image_10 = flowers_image_12

#         elif  get_image_theme == CHAMOMILE:
#             self.heatmap_image_01 = flowers_image_13
#             self.heatmap_image_02 = flowers_image_14
#             self.heatmap_image_03 = flowers_image_15
#             self.heatmap_image_04 = flowers_image_15
#             self.heatmap_image_05 = flowers_image_15
#             self.heatmap_image_06 = flowers_image_15
#             self.heatmap_image_07 = flowers_image_15
#             self.heatmap_image_08 = flowers_image_15
#             self.heatmap_image_09 = flowers_image_15
#             self.heatmap_image_10 = flowers_image_15

#         elif  get_image_theme == HYACINTH:
#             self.heatmap_image_01 = flowers_image_16
#             self.heatmap_image_02 = flowers_image_17
#             self.heatmap_image_03 = flowers_image_18
#             self.heatmap_image_04 = flowers_image_18
#             self.heatmap_image_05 = flowers_image_18
#             self.heatmap_image_06 = flowers_image_18
#             self.heatmap_image_07 = flowers_image_18
#             self.heatmap_image_08 = flowers_image_18
#             self.heatmap_image_09 = flowers_image_18
#             self.heatmap_image_10 = flowers_image_18

#         elif  get_image_theme == HYDRANGEA:
#             self.heatmap_image_01 = flowers_image_19
#             self.heatmap_image_02 = flowers_image_20
#             self.heatmap_image_03 = flowers_image_21
#             self.heatmap_image_04 = flowers_image_21
#             self.heatmap_image_05 = flowers_image_21
#             self.heatmap_image_06 = flowers_image_21
#             self.heatmap_image_07 = flowers_image_21
#             self.heatmap_image_08 = flowers_image_21
#             self.heatmap_image_09 = flowers_image_21
#             self.heatmap_image_10 = flowers_image_21

#         elif  get_image_theme == LOTUS:
#             self.heatmap_image_01 = flowers_image_22
#             self.heatmap_image_02 = flowers_image_23
#             self.heatmap_image_03 = flowers_image_24
#             self.heatmap_image_04 = flowers_image_24
#             self.heatmap_image_05 = flowers_image_24
#             self.heatmap_image_06 = flowers_image_24
#             self.heatmap_image_07 = flowers_image_24
#             self.heatmap_image_08 = flowers_image_24
#             self.heatmap_image_09 = flowers_image_24
#             self.heatmap_image_10 = flowers_image_24

#         elif  get_image_theme == ORCHID:
#             self.heatmap_image_01 = flowers_image_25
#             self.heatmap_image_02 = flowers_image_26
#             self.heatmap_image_03 = flowers_image_27
#             self.heatmap_image_04 = flowers_image_27
#             self.heatmap_image_05 = flowers_image_27
#             self.heatmap_image_06 = flowers_image_27
#             self.heatmap_image_07 = flowers_image_27
#             self.heatmap_image_08 = flowers_image_27
#             self.heatmap_image_09 = flowers_image_27
#             self.heatmap_image_10 = flowers_image_27

        # # Plants

        # elif  get_image_theme == CARROT:
        #     self.heatmap_image_01 = plants_image_01
        #     self.heatmap_image_02 = plants_image_02
        #     self.heatmap_image_03 = plants_image_03
        #     self.heatmap_image_04 = plants_image_04
        #     self.heatmap_image_05 = plants_image_04
        #     self.heatmap_image_06 = plants_image_04
        #     self.heatmap_image_07 = plants_image_04
        #     self.heatmap_image_08 = plants_image_04
        #     self.heatmap_image_09 = plants_image_04
        #     self.heatmap_image_10 = plants_image_04

        # elif  get_image_theme == POTATO:
        #     self.heatmap_image_01 = plants_image_06
        #     self.heatmap_image_02 = plants_image_07
        #     self.heatmap_image_03 = plants_image_08
        #     self.heatmap_image_04 = plants_image_09
        #     self.heatmap_image_05 = plants_image_09
        #     self.heatmap_image_06 = plants_image_09
        #     self.heatmap_image_07 = plants_image_09
        #     self.heatmap_image_08 = plants_image_09
        #     self.heatmap_image_09 = plants_image_09
        #     self.heatmap_image_10 = plants_image_09

        # elif  get_image_theme == PUMPKIN:
        #     self.heatmap_image_01 = plants_image_11
        #     self.heatmap_image_02 = plants_image_12
        #     self.heatmap_image_03 = plants_image_13
        #     self.heatmap_image_04 = plants_image_14
        #     self.heatmap_image_05 = plants_image_14
        #     self.heatmap_image_06 = plants_image_14
        #     self.heatmap_image_07 = plants_image_14
        #     self.heatmap_image_08 = plants_image_14
        #     self.heatmap_image_09 = plants_image_14
        #     self.heatmap_image_10 = plants_image_14

        # elif  get_image_theme == TOMATO:
        #     self.heatmap_image_01 = plants_image_16
        #     self.heatmap_image_02 = plants_image_17
        #     self.heatmap_image_03 = plants_image_18
        #     self.heatmap_image_04 = plants_image_19
        #     self.heatmap_image_05 = plants_image_19
        #     self.heatmap_image_06 = plants_image_19
        #     self.heatmap_image_07 = plants_image_19
        #     self.heatmap_image_08 = plants_image_19
        #     self.heatmap_image_09 = plants_image_19
        #     self.heatmap_image_10 = plants_image_19

