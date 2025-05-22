import datetime
import json
import math
import random
from webbrowser import get
# from aqt.qt import *
from aqt import mw, gui_hooks
import time
from collections import OrderedDict
from typing import Dict

from .html_media import THEMES, PlantSpecies, FARMERS
from .tippy.shige_custom_tooltip import get_tooltip


def get_ReviewCard_count(*args,**kwargs):
    if mw.col is None:
        return 0, 0

    config = mw.addonManager.getConfig(__name__)
    count_all_decks = config.get("count_all_decks", True)
    progress_bar_v1 = False

    current_Deck_ID = None

    if mw.state in ["overview", "review"]:
        if not count_all_decks:
            current_Deck_ID = mw.col.decks.current()['id']
    elif mw.state != "deckBrowser":
        return 0, 0

    if (current_Deck_ID and mw.col.decks.is_filtered(current_Deck_ID)) or progress_bar_v1:
        return 0, 0

    if current_Deck_ID:
        def get_child_deck_ids(deck_node):
            child_ids = []
            for child in deck_node.children:
                child_ids.append(child.deck_id)
                child_ids.extend(get_child_deck_ids(child))
            return child_ids

        deck_tree = mw.col.sched.deck_due_tree(current_Deck_ID)

        child_deck_ids = get_child_deck_ids(deck_tree)
        deck_ids = child_deck_ids + [current_Deck_ID]
        deck_ids_tuple = tuple(deck_ids)

        deck_ids_placeholder = 'and cards.did in (' + ', '.join(['?'] * len(deck_ids_tuple)) + ')'
    else:
        deck_ids_placeholder = ""

    # 最初のﾚﾋﾞｭｰ日
    first_review_timestamp = mw.col.db.first("select min(id) from revlog")[0] / 1000
    first_review_day = int(first_review_timestamp / 86400)


    # 現在の日付
    # current_day = int((mw.col.sched.day_cutoff - 86400)/ 86400)
    # current_day = int(mw.col.sched.day_cutoff / 86400) - 1
    current_day = math.ceil(mw.col.sched.day_cutoff / 86400) - 1
    current_day_datetime = datetime.datetime.fromtimestamp(current_day*86400)

    # print(datetime.datetime.fromtimestamp(current_day*86400))


    # https://github.com/ankidroid/Anki-Android/wiki/Database-Structure

    if config.get("count_only_graduated_cards", True):
        # 卒業したｶｰﾄﾞのみｶｳﾝﾄする
        # SELECT MINで重複を削除するとﾏｯﾌﾟに穴が開く
        # query = f"""
        #     SELECT MIN(revlog.id) as earliest_id, revlog.cid
        #     from revlog
        #     join cards on revlog.cid = cards.id
        #     where revlog.type = 0
        #     and revlog.ease in (2, 3, 4)
        #     and cards.left = 0
        #     {deck_ids_placeholder}
        #     GROUP BY revlog.cid
        # """

        # 卒業したｶｰﾄﾞのみｶｳﾝﾄする
        query = f"""
            select revlog.id, revlog.cid
            from revlog
            join cards on revlog.cid = cards.id
            where revlog.type = 0
            and revlog.ease in (2, 3, 4)
            and cards.left = 0
            {deck_ids_placeholder}
        """

    else: # 最初にﾚﾋﾞｭ-した日付でｶｳﾝﾄする
        # query = f"""
        #     SELECT MIN(revlog.id) as earliest_id, revlog.cid
        #     FROM revlog
        #     JOIN cards ON revlog.cid = cards.id
        #     WHERE revlog.type = 0
        #     {deck_ids_placeholder}
        #     GROUP BY revlog.cid
        # """

        # 重複も数えようとすると処理落ちする
        query = f"""
            select revlog.id, revlog.cid
            from revlog
            join cards on revlog.cid = cards.id
            where revlog.type = 0
            {deck_ids_placeholder}
        """

    if current_Deck_ID:
        all_reviews = mw.col.db.all(query, *deck_ids_tuple)
    else:
        all_reviews = mw.col.db.all(query)


    # timestamp = mw.col.sched.day_cutoff
    # local_time = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).astimezone()
    # time_part_seconds = (local_time.hour * 3600) + (local_time.minute * 60) + local_time.second
    rollover_seconds = mw.col.get_config("rollover", 4)* 3600

    epoch = datetime.datetime(1970, 1, 1)
    reviewed_cards_per_day = {}

    for review in all_reviews: # revlog.id, revlog.cid
        # print(f"review : {review}")

        # review_day = int(review[0] / 86400 / 1000)
        epoch_millis = review[0] - rollover_seconds * 1000
        seconds = epoch_millis / 1000
        local_time = datetime.datetime.fromtimestamp(seconds)
        review_day = (local_time - epoch).days

        # print(f"review_day : {review_day}")
        if first_review_day <= review_day <= current_day + 1:
            if review_day in reviewed_cards_per_day:
                reviewed_cards_per_day[review_day].add(review[1])
            else:
                reviewed_cards_per_day[review_day] = {review[1]}
        # print(f"review[1] : {review[1]}")

    # current_year = datetime.datetime.now().year
    current_year = current_day_datetime.year
    next_year_last_day = datetime.datetime(current_year + 1, 12, 31)
    days_until_next_year_last_day = (next_year_last_day - current_day_datetime).days
    # days_until_next_year_last_day = (next_year_last_day - datetime.datetime.now()).days


    # ﾚﾋﾞｭｰ0の日も追加
    # 来年も追加
    # for day in range(first_review_day, current_day + 2):
    for day in range(first_review_day, current_day + days_until_next_year_last_day + 2):
        if day not in reviewed_cards_per_day:
            reviewed_cards_per_day[day] = set()

    reviewed_cards_per_day = OrderedDict(sorted(reviewed_cards_per_day.items()))

    def generate_heatmap(reviewed_cards_per_day):
        # epoch = datetime.datetime(1970, 1, 1)

        # HTMLを生成
        # ｺﾝﾃﾅの問題
        # https://stackoverflow.com/questions/33454533/cant-scroll-to-top-of-flex-item-that-is-overflowing-container
        html = "<div class='shige_new_cards_farm_container'>"
        html += "<div class='shige_heatmap_farm'>"
        prev_year = None
        week_open = False
        first_week_of_year = True

        min_year = float('inf')
        max_year = float('-inf')

        # today = int(mw.col.sched.day_cutoff / 86400)
        # today_date = datetime.datetime.fromtimestamp(current_day*86400)
        # print(today_date)
        # current_year = today_date.year
        current_year = current_day_datetime.year

        # ｽﾄﾘｰｸ-----------------
        max_consecutive_days, current_consecutive_days, learned_today = get_streak(reviewed_cards_per_day)

        crops_dict: Dict  = config.get("crops_dict", {})
        plant_same_crop_all = config.get("plant_same_crop_all", True)
        image_size = config.get("image_size",25)
        change_crops_randomly = config.get("change_crops_randomly", False)
        show_farmer = config.get("show_farmer", True)

        crop_planting_methods =""

        if change_crops_randomly:
            config["plant_species"] = plant_species =  random.choice(THEMES)
            mw.addonManager.writeConfig(__name__, config)
        else:
            plant_species = config.get("plant_species", THEMES[0])


        # config["plant_species"] = random.choice(THEMES)
        # mw.addonManager.writeConfig(__name__, config)
        # plantSpecies = PlantSpecies()

        # image_urls = {
        #     "color-farm-0": "",
        #     "color-farm-1": plantSpecies.heatmap_image_01,
        #     "color-farm-2": plantSpecies.heatmap_image_02,
        #     "color-farm-3": plantSpecies.heatmap_image_03,
        #     "color-farm-4": plantSpecies.heatmap_image_04,
        #     "color-farm-5": plantSpecies.heatmap_image_05,
        #     "color-farm-6": plantSpecies.heatmap_image_06,
        #     "color-farm-7": plantSpecies.heatmap_image_07,
        #     "color-farm-8": plantSpecies.heatmap_image_08,
        #     "color-farm-9": plantSpecies.heatmap_image_09,
        #     "color-farm-10": plantSpecies.heatmap_image_10
        # }

        for index, (day, cards) in enumerate(reviewed_cards_per_day.items()):
            # print( f"{day} , {cards}")
            current_date = epoch + datetime.timedelta(days=day)
            year = current_date.year
            min_year = min(min_year, year)
            max_year = max(max_year, year)
            weekday = current_date.weekday()

            if index == 0 or year != prev_year:
                if week_open:
                    html += "</div>"
                    week_open = False
                if prev_year is not None:
                    html += "</div>"
                # html += f"<div class='shige_heatmap_farm' id='shige_heatmap_farm-{year}' style='display: none;'>"
                html += f"<div id='shige_heatmap_farm-{year}' style='display: none;'>"
                first_week_of_year = True

            prev_year = year
            # 新しい週の開始をﾁｪｯｸ
            if weekday == 0 or week_open == False:
                if first_week_of_year:
                    html += "<div class='shige_week_farm first_week'>"
                    first_week_of_year = False
                else:
                    html += "<div class='shige_week_farm'>"
                week_open = True

            # ﾚﾋﾞｭｰ枚数に基づいて色を選択
            if len(cards) == 0:
                # color = colors[0]
                color_class = "color-farm-0"
            else:
                # color = colors[min(len(cards) // 25 + 1, len(colors) - 1)]
                # color_class = "color-" + str(min(len(cards) // 25 + 1, 4))
                color_class = "color-farm-" + str(min(len(cards) // 10 + 1, 10))


            # delta = datetime.timedelta(days=day)
            # day = (epoch + delta).date()
            day = current_date.date()
            # html += f"<div class='shige_day_farm' style='background-color: {color}' title='Day {day}: {len(cards)} new cards'></div>"
            # html += f"<div class='shige_day_farm {color_class}' title='Day {day}: {len(cards)} new cards'></div>"

            current_year = current_day_datetime.year

            # if day <= current_day_datetime.date():
            #     if len(cards) > 0 :
            #         crop = crops_dict.setdefault(str(day), random.choice(THEMES))
            #     else: # ｶｰﾄﾞが0の場合は作物を削除
            #         crop = crops_dict.get(str(day), random.choice(THEMES))
            #         if str(day) in crops_dict:
            #             del crops_dict[str(day)]
            # else:
            #     crop = random.choice(THEMES)

            # 日ごとに植える
            if not plant_same_crop_all:
                if day <= current_day_datetime.date():
                    crop = crops_dict.get(str(day), random.choice(THEMES))
                    if not crop in THEMES:
                        crop = random.choice(THEMES)
                    if len(cards) > 0 :
                        crops_dict[str(day)] = crop
                    else:
                        if str(day) in crops_dict:
                            del crops_dict[str(day)]
                else:
                    crop = THEMES[0]

            # 曜日ごとに植える
            elif crop_planting_methods == "day_of_the_week":
                crop_day_of_the_week = current_date.strftime('%A')

            # 週ごとに植える
            elif crop_planting_methods == "plant_by_week":
                crop_year, week_number, _ = current_date.isocalendar()
                crop_year_week_str = f"{crop_year}-{week_number}"

                if day <= current_day_datetime.date():
                    crop = crops_dict.get(str(day), random.choice(THEMES))
                    if not crop in THEMES:
                        crop = random.choice(THEMES)
                    if len(cards) > 0 :
                        crops_dict[str(day)] = crop
                    else:
                        if str(day) in crops_dict:
                            del crops_dict[str(day)]

            # 月ごとに植える
            elif crop_planting_methods == "plant_by_month":
                crop_month = current_date.strftime('%B')

            # 年ごとに植える
            elif crop_planting_methods == "plant_by_year":
                crop_year = current_date.year

            # すべて同じ
            else:
                crop = plant_species


            plantSpecies = PlantSpecies(random_mode=crop)

            image_urls = {
                "color-farm-0": "",
                "color-farm-1": plantSpecies.heatmap_image_01,
                "color-farm-2": plantSpecies.heatmap_image_02,
                "color-farm-3": plantSpecies.heatmap_image_03,
                "color-farm-4": plantSpecies.heatmap_image_04,
                "color-farm-5": plantSpecies.heatmap_image_05,
                "color-farm-6": plantSpecies.heatmap_image_06,
                "color-farm-7": plantSpecies.heatmap_image_07,
                "color-farm-8": plantSpecies.heatmap_image_08,
                "color-farm-9": plantSpecies.heatmap_image_09,
                "color-farm-10": plantSpecies.heatmap_image_10
            }

            image_url = image_urls.get(color_class, "")

            # # mw.col.sched.day_cutoffに一致するﾎﾞｯｸｽにのみ黒の枠線を表示
            # if day == current_day_datetime.date():
            #     html += f"<div class='shige_day_farm {color_class} today' title='&nbsp;{len(cards)} new cards :{day}' ></div>"
            # else:
            #     html += f"<div class='shige_day_farm {color_class}' title='&nbsp;{len(cards)} new cards :{day}'></div>"

            # mw.col.sched.day_cutoffに一致するﾎﾞｯｸｽにのみ黒の枠線を表示

            if len(cards) > 0 :
                crop_content = f"{crop}<br>"
            else:
                crop_content = ""

            day_click_action = ""
            if not plant_same_crop_all:
                day_click_action = (
                f" onmousedown=\"handleMouseDown(event)\""
                f" onmouseup=\"handleMouseUp(event, 'shige_newCardsFarm_days:{str(day)}:{len(cards)}')\""
                f" onclick=\"return false;\""
                )

            # 農家を追加
            add_farmer = ""
            if show_farmer:
                if len(cards) > 0:
                    if current_consecutive_days >=7 :
                        farmer_type = FARMERS[0]
                    else:
                        farmer_type = FARMERS[2]
                else:
                    if current_consecutive_days >=7 :
                        farmer_type = FARMERS[1]
                    else:
                        farmer_type = FARMERS[3]

                add_farmer = f"<img src='{farmer_type}'\
                    style='position: absolute;\
                    top: -{image_size}px; right: -{image_size*2}px;\
                    width :{image_size*2}px; \
                    height :'{image_size*2}px; \
                    \'>"


            if day == current_day_datetime.date():
                html += (
                    f"<div id='new_farm_today' class='shige_day_farm {color_class} today' "
                    # f"title='&nbsp;{len(cards)} new cards :{day}'>"
                    f"data-tippy-content='"
                    f"<div style=\"text-align: center;\">"
                    f"<span style=\"font-size: 20px;\">{len(cards)}</span> new cards <br>"
                    f"{day}<br>"
                    f"{crop_content}"
                    f"</div>'"
                    f"data-card-count='{len(cards)}'"
                    f"{day_click_action}"
                    f">"
                )
                if image_url:
                    html += (
                    f"<img src='{image_url}'"
                    f">"
                    # f"<img src='{image_url}' style='position: absolute; top: 0; right: -{image_size}px;'>"
                    )
                html += f"{add_farmer}"
                
                html += "</div>"
            else:
                html += (
                    # f"<div class='shige_day_farm {color_class}' "
                    # f"title='&nbsp;{len(cards)} new cards :{day}'>"
                    f"<div class='shige_day_farm {color_class}' "
                    f"data-tippy-content='"
                    f"<div style=\"text-align: center;\">"
                    f"<span style=\"font-size: 20px;\">{len(cards)}</span> new cards<br>"
                    f"{day}<br>"
                    f"{crop_content}"
                    f"</div>'"
                    f"data-card-count='{len(cards)}'"
                    f"{day_click_action}"
                    f">"
                )
                if image_url:
                    # html += f"<img src='{image_url}'>"
                    html += (
                    f"<img src='{image_url}'"
                    f">"
                    )
                html += "</div>"

                # html += (
                #     # f"<div class='shige_day_farm {color_class}' "
                #     # f"title='&nbsp;{len(cards)} new cards :{day}'>"
                #     f"<div class='shige_day_farm {color_class}' "
                #     f"data-tippy-content='"
                #     f"<div style=\"text-align: center;\">"
                #     f"<span style=\"font-size: 20px;\">{len(cards)}</span> new cards<br>"
                #     f"{day}<br>"
                #     f"{crop_content}"
                #     f"</div>'"
                #     f"data-card-count='{len(cards)}'"
                #     f" onclick=\"pycmd(\'shige_newCardsFarm_days:{str(day)}\')\""
                #     f">"
                # )



            # 週の終わりをﾁｪｯｸ
            # if i % 7 == 6:
            if weekday == 6:
                html += "</div>"
                week_open = False
        html += "</div></div></div>"

        config["crops_dict"] = crops_dict
        mw.addonManager.writeConfig(__name__, config)


        
        # CSSを生成

        # .shige_heatmap_farm {{
        #     display: block;
        #     flex-direction: row;
        #     flex-wrap: nowrap;
        #     margin: 0 auto;
        #     overflow-y: visible;
        #     overflow-x: auto;
        #     padding-top: {image_size}px;
        #     justify-content: center;
        #     width: 80%;
        # }}

        css = """
        <style>
        .shige_new_cards_farm_container {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .shige_heatmap_farm {{
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            margin: 0 auto;
            overflow-y: visible;
            overflow-x: auto;
            padding-top: {image_size}px;

            align-items: center;
        }}
        .shige_week_farm {{
            display: flex;
            flex-direction: column;
            margin-left: auto;
            margin-right: auto;
        }}
        .shige_week_farm.first_week {{
            justify-content: flex-end;
        }}

        """.format(image_size = str(image_size))

        # .shige_heatmap_farm
            # max-width: 80%;

        #

        # css += """
        #         .shige_day_farm {{
        #     width: {image_size}px;
        #     height: {image_size}px;
        #     margin: 1px;
        #     background-size: 100% 100%;
        #     background-repeat: no-repeat;
        #     border-radius: 5%;
        # }}
        # """.format(image_size = str(config.get("image_size",20)))

        # image_size = config.get("image_size",20)
        # css += """
        #         .shige_day_farm {{
        #     width: {image_size_w}px;
        #     height: {image_size_h}px;
        #     margin: 1px;
        #     background-size: 100% auto;
        #     background-repeat: no-repeat;
        #     background-position: bottom;
        #     border-radius: 5%;
        #     image-rendering: pixelated;

        # }}
        # """.format(image_size_w = str(image_size), image_size_h = str(image_size*2))




        css += """
                .shige_day_farm {{
            width: {image_size_w}px;
            height: {image_size_w}px;
            margin: 1px;
            background-size: 100% auto;
            border-radius: 20%;
            image-rendering: pixelated;
            display: flex;
            align-items: flex-end;
            position: relative;
            overflow: visible;

        }}
            .shige_day_farm img {{
        width: {image_size_w}px;
        position: relative;
        z-index: 1;
        pointer-events: none;
        overflow:visible
        }}

        """.format(image_size_w = str(image_size), image_size_h = str(image_size*2))

        # pointer-events: none;

        css += """
        .shige_day_farm.today {
            border: 1px solid #3b82f6;
            box-sizing: border-box;
        }

        .color-farm-0 {
            background-color: #d3d3d3;
        }
        .color-farm-1 {
            background-color: #f5deb3;
        }
        .color-farm-2 {
            background-color: #f5deb3;
        }
        .color-farm-3 {
            background-color: #f5deb3;
        }
        .color-farm-4 {
            background-color: #f5deb3;
        }
        .color-farm-5 {
            background-color: #f5deb3;
        }
        .color-farm-6 {
            background-color: #f5deb3;
        }
        .color-farm-7 {
            background-color: #f5deb3;
        }
        .color-farm-8 {
            background-color: #f5deb3;
        }
        .color-farm-9 {
            background-color: #f5deb3;
        }
        .color-farm-10 {
            background-color: #f5deb3;
        }

        .night_mode .color-farm-0 {
            background-color: #313131;
        }
        .night_mode .color-farm-1 {
            background-color: #3D3D3D;
        }
        .night_mode .color-farm-2 {
            background-color: #3D3D3D;
        }
        .night_mode .color-farm-3 {
            background-color: #3D3D3D;
        }
        .night_mode .color-farm-4 {
            background-color: #3D3D3D;
        }
        .night_mode .color-farm-5 {
            background-color: #3D3D3D;
        }
        .night_mode .color-farm-6 {
            background-color: #3D3D3D;
        }
        .night_mode .color-farm-7 {
            background-color: #3D3D3D;
        }
        .night_mode .color-farm-8 {
            background-color: #3D3D3D;
        }
        .night_mode .color-farm-9 {
            background-color: #3D3D3D;
        }
        .night_mode .color-farm-10 {
            background-color: #3D3D3D;
        }


        """

        # background-color: rgba(255, 193, 102, 0.3) !important;

        #d3d3d3 ｸﾞﾚｰ
        #FFC166 薄茶

        plantSpecies = PlantSpecies()

        map_images = f"""
        .color-farm-0 {{
            background-color: #d3d3d3;
        }}
        .color-farm-1 {{
            background-image: url('{plantSpecies.heatmap_image_01}');
        }}
        .color-farm-2 {{
            background-image: url('{plantSpecies.heatmap_image_02}');
        }}
        .color-farm-3 {{
            background-image: url('{plantSpecies.heatmap_image_03}');
        }}
        .color-farm-4 {{
            background-image: url('{plantSpecies.heatmap_image_04}');
        }}
        .color-farm-5 {{
            background-image: url('{plantSpecies.heatmap_image_05}');
        }}
        .color-farm-6 {{
            background-image: url('{plantSpecies.heatmap_image_06}');
        }}
        .color-farm-7 {{
            background-image: url('{plantSpecies.heatmap_image_07}');
        }}
        .color-farm-8 {{
            background-image: url('{plantSpecies.heatmap_image_08}');
        }}
        .color-farm-9 {{
            background-image: url('{plantSpecies.heatmap_image_09}');
        }}
        .color-farm-10 {{
            background-image: url('{plantSpecies.heatmap_image_10}');
        }}

        .night_mode .color-farm-0 {{
            background-color: #313232;
        }}

        </style>
        """

        map_images = "</style>"

            # border-radius: 50%;
        js = """
        <script>
        var currentYear = {start_year};
        var minYear = {min_year};
        var maxYear = {max_year};
        document.getElementById('shige_heatmap_farm-' + currentYear).style.display = 'flex';

        function switchYear_farm(offset) {{
            document.getElementById('shige_heatmap_farm-' + currentYear).style.display = 'none';
            currentYear += offset;
            currentYear = Math.max(minYear, Math.min(maxYear, currentYear));
            document.getElementById('shige_heatmap_farm-' + currentYear).style.display = 'flex';
            document.getElementById('year_display_farm').innerText = currentYear;
            scrollToToday();
            }}

        function scrollToToday() {{
            var todayElement = document.getElementById("new_farm_today");
            if (todayElement) {{
                var container = todayElement.closest('.shige_heatmap_farm');
                if (container) {{
                    container.scrollLeft = todayElement.offsetLeft - container.offsetLeft - (container.clientWidth / 2) + (todayElement.clientWidth / 2);
                }}
            }}
        }}
        document.addEventListener("DOMContentLoaded", function() {{
        scrollToToday();
        }});

        </script>
        """.format(start_year=current_year,min_year=min_year,max_year=max_year)

        # 長押ししたときのみ実行
        js += """
        <script>
        let isLongPress = false;
        let timer;

        function handleMouseDown(event) {
            isLongPress = false;
            timer = setTimeout(() => {
                isLongPress = true;
            }, 500);
        }

        function handleMouseUp(event, command) {
            clearTimeout(timer);
            if (!isLongPress) {
                pycmd(command);
            }
        }
        </script>
        """


        # function scrollToToday() {{
        #     var todayElement = document.getElementById("new_farm_today");
        #     if (todayElement) {{
        #         var container = todayElement.closest('.shige_heatmap_farm');
        #         if (container) {{
        #             container.scrollLeft = todayElement.offsetLeft - container.offsetLeft - (container.clientWidth / 2) + (todayElement.clientWidth / 2);
        #         }}
        #     }}
        # }}





        # 年を表示
        year_display = "<div id='year_display_farm' class='year_display_farm'>{start_year}</div>".format(start_year=current_year)

        # # ｽﾄﾘｰｸを表示-----------------
        # max_consecutive_days, current_consecutive_days, learned_today = get_streak(reviewed_cards_per_day)

        # shige_streak_farm : javascriptのﾄﾘｶﾞｰに使用

        max_consecutive_days_label = "<div class='shige_streak_farm'>&nbsp; Longest Streak:&nbsp;\
            <strong style='color: #3b82f6;'>{max_consecutive_days} days</strong></div>".format(max_consecutive_days=max_consecutive_days)
        current_consecutive_days_label = "<div class='shige_streak_farm'>&nbsp; Current Streak:&nbsp;\
            <strong style='color: #3b82f6;'>{current_consecutive_days} days</strong></div>".format(current_consecutive_days=current_consecutive_days)

        streak = "<div class='shige_streak_farm_box'>" + max_consecutive_days_label + "&nbsp;&nbsp;&nbsp;&nbsp;" + current_consecutive_days_label + "</div>"
        #------------------------------



        # ﾎﾞﾀﾝを追加 ------------------
        button = """
        <button class="heatmap_shige_button_farm" onclick="switchYear_farm(-1)">◀</button>
        {year_display}
        <button class="heatmap_shige_button_farm" onclick="switchYear_farm(1)">▶</button>
        """.format(year_display=year_display)
        # ------------------------------



        # ｵﾌﾟｼｮﾝ用のﾎﾞﾀﾝを追加 ------------------
        button_2 = """
        <button class="heatmap_shige_button_farm" onclick="pycmd(\'shige_farm_settings\')"> {plant_species} </button>
        """.format( plant_species = plant_species)
        button += button_2
        # ------------------------------


        # 今日の学習枚数
        learned_today_label = "<div class='shige_streak_farm'>&nbsp;\
            <strong style='color: #3b82f6;'>{learned_today} new cards</strong> learned today.</div>\
                ".format(learned_today=learned_today)

        button =  learned_today_label + button

        button_css = """
        <style>

        .shige_streak_farm_container{
        flex-wrap: wrap;
        }


        .heatmap_shige_button_farm {
            padding: 2px 2px;
            text-align: center;
            display: inline-block;
            font-size: 10px;
            margin: 2px 2px;
            cursor: pointer;
            border-radius: 12px;
        }

        .year_display_farm, .heatmap_shige_button_farm {
            display: inline-block;
            font-size: 10px;
            color: gray;
        }

        .shige_streak_farm {
        display: inline-block;
        font-size: 15px;
        }

        .shige_streak_farm_box {
            display: block;
        }


        </style>
        """

        # ﾄﾞﾗｯｸﾞでｽｸﾛｰﾙ
        js += """
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const container = document.querySelector('.shige_heatmap_farm');
            let isDown = false;
            let startX;
            let scrollLeft;

            container.addEventListener('mousedown', (e) => {{
                isDown = true;
                container.classList.add('active');
                startX = e.pageX - container.offsetLeft;
                scrollLeft = container.scrollLeft;
            }});

            container.addEventListener('mouseleave', () => {{
                isDown = false;
                container.classList.remove('active');
            }});

            container.addEventListener('mouseup', () => {{
                isDown = false;
                container.classList.remove('active');
            }});

            container.addEventListener('mousemove', (e) => {{
                if (!isDown) return;
                e.preventDefault();
                const x = e.pageX - container.offsetLeft;
                const walk = (x - startX) * 1;
                container.scrollLeft = scrollLeft - walk;
            }});
        }});
        </script>
        """

        js += get_tooltip()

        js += """
        <script>
        function showContainer() {{
            var container = document.querySelector('.shige_streak_farm_container');
            if (container) {{
                container.style.display = 'block';
            }}
        }}

        </script>

        <script>
        function checkForClass() {{
            const interval = 20;
            const startTime = Date.now();
            const maxTime = 5000;

            const intervalId = setInterval(function() {{
                const currentTime = Date.now();
                const elapsedTime = currentTime - startTime;
                const element = document.querySelector('.shige_streak_farm');
                if (element) {{
                    showContainer()
                    scrollToToday();
                    clearInterval(intervalId);
                }} else if (elapsedTime >= maxTime) {{
                    clearInterval(intervalId);
                    }}
            }}, interval);
        }}

        checkForClass();
        </script>


        """

        html = button + html+ css + map_images + js + button_css + "</div>" + streak


        # document.addEventListener("DOMContentLoaded", function() {{
        #     scrollToToday();
        # }});


        # document.addEventListener("DOMContentLoaded", function() {{
        #     showContainer();
        #     scrollToToday();
        # }});

        html = "<div class='shige_streak_farm_container' style='display: none;'>" + html + "</div>"
        # html = "<div class='shige_streak_farm_container'>" + html + "</div>"

        # config = mw.addonManager.getConfig(__name__)
        # if config.get("border_radius", True):
        #     border_radius = """
        #     <style>
        #         .shige_day_farm {
        #         border-radius: 50%;
        #     }
        #     </style>
        #     """

        #     html = html + border_radius

        return html

    html = generate_heatmap(reviewed_cards_per_day)

    return html

from aqt.deckbrowser import DeckBrowser, DeckBrowserContent

def add_new_count_to_bottom(deck_browser: DeckBrowser, content: DeckBrowserContent):
    add_html = get_ReviewCard_count()
    content.stats += add_html


gui_hooks.deck_browser_will_render_content.append(add_new_count_to_bottom)


# gui_hooks.reviewer_did_show_question.append(get_ReviewCard_count)
# gui_hooks.reviewer_did_answer_card.append(get_ReviewCard_count)
# gui_hooks.main_window_did_init.append(get_ReviewCard_count)
# gui_hooks.state_did_change.append(get_ReviewCard_count)



def get_streak(reviewed_cards_per_day):
    max_consecutive_days = 0
    current_consecutive_days = 0
    previous_day_reviewed = False

    for day, reviews in reviewed_cards_per_day.items():
        if len(reviews) >= 1:
            if previous_day_reviewed:
                current_consecutive_days += 1
            else:
                current_consecutive_days = 1
            previous_day_reviewed = True
        else:
            previous_day_reviewed = False

        max_consecutive_days = max(max_consecutive_days, current_consecutive_days)

    # 現在の連続日数を取得
    # today = int(datetime.datetime.now().timestamp() / 86400)
    # today = int((mw.col.sched.day_cutoff - 86400)/ 86400)
    current_day = math.ceil(mw.col.sched.day_cutoff / 86400) - 1

    yesterday = current_day -1
    if len(reviewed_cards_per_day[yesterday]) < 1:
        current_consecutive_days = 0

    learned_today = len(reviewed_cards_per_day.get(current_day, []))

    return max_consecutive_days, current_consecutive_days, learned_today







# rated:1 今日回答したｶｰﾄﾞ


# 使ってない
# 一日一回だけ有効にする関数
def get_day_cutoff():
    current_time = int(time.time())
    day_cutoff_time = mw.col.sched.day_cutoff
    if current_time >= day_cutoff_time:
        current_day = datetime.datetime.now().strftime('%Y-%m-%d')
        config = mw.addonManager.getConfig(__name__)
        if 'today' not in config or config['today'] != current_day:
            config['today'] = current_day
            mw.addonManager.writeConfig(__name__, config)
            return True
    return False


# """
# def get_revlog_fields():
#     if mw.col is None:
#         return None
#     try:
#         revlog_fields = mw.col.db.all("PRAGMA table_info(revlog)")
#     except:
#         revlog_fields = None

#     return revlog_fields
# def test(*args,**kwargs):
#     revlog_fields = get_revlog_fields()
#     for field in revlog_fields:
#         print(field)
# gui_hooks.main_window_did_init.append(test)
# """



    # # 最初のﾚﾋﾞｭｰ日を取得します｡
    # first_review_timestamp = mw.col.db.first("select min(id) from revlog")[0] / 1000
    # first_review_day = int(first_review_timestamp / 86400)

    
    # epoch = datetime.datetime(1970, 1, 1)
    # delta = datetime.timedelta(days=first_review_day)
    # first_review_date = epoch + delta
    # print(first_review_date)

    # # 現在の日を取得します
    # current_day = int(mw.col.sched.day_cutoff / 86400)
    # print(current_day)

    # # 各日のﾚﾋﾞｭｰ枚数を保存するための辞書を作成します｡
    # reviewed_cards_per_day = {}

    # for day in range(first_review_day, current_day + 2):
    #     # 検索する日の開始時間と終了時間を計算します｡
    #     start_time = (day - 1) * 86400 * 1000
    #     end_time = day * 86400 * 1000

    #     query = f"""
    #         select count(distinct revlog.cid)
    #         from revlog
    #         join cards on revlog.cid = cards.id
    #         where revlog.id > ?
    #         and revlog.id <= ?
    #         and revlog.type = 0
    #         and revlog.ease in (2, 3, 4)
    #         and cards.left = 0
    #         {deck_ids_placeholder}
    #     """

    #     if current_Deck_ID:
    #         reviewed_cards = mw.col.db.first(query, start_time, end_time, *deck_ids_tuple)
    #         # 結果を辞書に保存します｡
    #         reviewed_cards_per_day[day] = reviewed_cards
    #     else:
    #         reviewed_cards = mw.col.db.first(query, start_time, end_time)
    #         reviewed_cards_per_day[day] = reviewed_cards

    #     delta = datetime.timedelta(days=day)
    #     now_day = epoch + delta
    #     print(f"reviewed_cards_per_day[day] : {now_day} : {reviewed_cards}")