
from typing import Dict
from aqt import (QApplication, QDialog,QFontMetrics, QFrame, QFrame, QHBoxLayout,
    QMouseEvent, QPainter, QPoint, QScrollArea, QTabWidget, QTimer, QWidget,Qt)
from aqt import QVBoxLayout, QLabel, QPushButton
from aqt import mw
from os.path import join, dirname
from aqt import QIcon
from aqt import QPixmap
from aqt.utils import tooltip
from aqt import QCheckBox
import random
import os


from .html_media import THEMES
from .config.config_name_manager import PLANTING_METHODS, PLANTING_METHODS_DEFAULT

CHARACTER_SELECTION_COLUMN = 10
LABELS_HEIGHT = 4

PLANTS_TEXT = "plantsText"
ICON_PATH = r"media/icons/plantsText.png"
ICON_PATH_02 = r"media/Farm_02_icons/plantsText.png"
backFrame_image = r"Square_button_3.png"
LABELS_SCALED = 75


THE_ADDON_NAME = "New Cards Farm by Shige"
BUTTON_WIDTH = 95

SET_LINE_EDID_WIDTH = 400
MAX_LABEL_WIDTH = 100

SET_SCALEDTOWIDTH = 400

class ChangeCrops(QDialog):
    def __init__(self, parent=None, plant_config_date="", cards="0"):
        super().__init__(parent)
        # self.setFixedHeight(400)
        self.resize(900, self.height())
        self.plant_config_date = str(plant_config_date)

        config = mw.addonManager.getConfig(__name__)

        self.methods_key = self.crop_planting_methods = config.get("crop_planting_methods", PLANTING_METHODS_DEFAULT)
        if not self.methods_key in PLANTING_METHODS:
            self.methods_key = PLANTING_METHODS_DEFAULT

        # self.crops_dict: Dict  = config.get("crops_dict", {})
        # crop = self.crops_dict.get(str(day), THEMES[0])

        self.crops_dict: Dict  = config.setdefault("farm_crops_dict", {})
        crop = self.crops_dict.setdefault(self.methods_key, {}).get(plant_config_date, THEMES[0])
        if not crop in THEMES:
            crop = THEMES[0]
        self.theme = crop

        # Set window icon
        addon_path = dirname(__file__)
        self.icon_path = join(addon_path, r"icon.png")
        self.logo_icon = QIcon(self.icon_path)
        self.setWindowIcon(self.logo_icon)


        self.backFrame_image = join(addon_path, backFrame_image)
        self.labels_and_overlays = {}

        self.setWindowTitle(THE_ADDON_NAME)

        # QPushButtonを作成して､ﾌｫﾝﾄ名をprintする
        button = QPushButton('OK')
        button.clicked.connect(self.handle_button_clicked)
        button.clicked.connect(self.hide)
        button.setFixedWidth(BUTTON_WIDTH)

        # QPushButtonを作成して､ﾌｫﾝﾄ名をprintする
        button2 = QPushButton('Cancel')
        button2.clicked.connect(self.cancelSelect)
        button2.clicked.connect(self.hide)
        button2.setFixedWidth(BUTTON_WIDTH)


        # ｳｨﾝﾄﾞｳにQFontComboBoxとQLabelとQPushButtonを追加
        layout = QVBoxLayout()


        # -----------------------------------------------------
        the_tab = QTabWidget(self)

        layout_one = QVBoxLayout()
        tab_one = QWidget()


        # from .html_media import CROPS_IMAGES_PATH_DICT

        # if crop in CROPS_IMAGES_PATH_DICT:
        #     image_urls = CROPS_IMAGES_PATH_DICT[crop]

        # addon_package = mw.addonManager.addonFromModule(__name__)
        # mediafolder_farm = f"/_addons/{addon_package}/"

        # crop_pixmaps = []
        # for image_url in image_urls:
        #     if image_url:
        #         image_path = join(addon_path, image_url.replace(mediafolder_farm, ""))
        #         if os.path.exists(image_path):
        #             crop_pixmaps.append(image_path)

        # self.crops_HBox_layout = QHBoxLayout()

        # for crop_pixmap in crop_pixmaps:
        #     crop_label = QLabel()
        #     crop_pixmap = QPixmap(crop_pixmap)
        #     crop_label.setPixmap(crop_pixmap)
        #     self.crops_HBox_layout.addWidget(crop_label)

        # self.crops_HBox_layout.addStretch()

        self.now_crop_label = QLabel(self.theme.replace('_', ' ').upper())
        self.now_crop_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout_one.addWidget(self.now_crop_label)

        crops_HBox_layout = self.generate_crops_sample(self.theme)

        layout_one.addLayout(crops_HBox_layout)

        label = QLabel(f"<b>[ Change crop ]</b> {str(plant_config_date)} : {self.theme} : New Cards {cards}")
        label.setStyleSheet("font-size: 16px;")  # ﾌｫﾝﾄｻｲｽﾞを16pxに設定
        layout_one.addWidget(label)


        theme_HBox_layout = QHBoxLayout()
        theme_HBox_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 左寄せに設定


        #== 作物を選択 ===================================================
        themes = THEMES

        count = 0
        row_count = 0
        scroll_area_themes = QScrollArea()
        target_theme_label = None
        
        # scroll_area_themes.scroll_area.setWidgetResizable(True)
        
        scroll_area_themes.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()


        for theme in themes:
            image_path = get_mediaFile_path(ICON_PATH.replace(PLANTS_TEXT, theme))
            if not os.path.exists(image_path):
                image_path = get_mediaFile_path(ICON_PATH_02.replace(PLANTS_TEXT, theme))
            theme_label = self.create_label_with_image(image_path, theme)

            # theme_HBox_layout.addWidget(theme_label)
            theme_text_label = QLabel(theme)

            # ====  ﾌｫﾝﾄｻｲｽﾞを調整 ========
            metrics = QFontMetrics(theme_text_label.font())
            if metrics.horizontalAdvance(theme_text_label.text()) > LABELS_SCALED:
                while metrics.horizontalAdvance(theme_text_label.text()) > LABELS_SCALED:
                    font = theme_text_label.font()
                    font.setPointSize(font.pointSize() - 1)
                    theme_text_label.setFont(font)
                    metrics = QFontMetrics(font)
            # =============================

            # theme_HBox_layout.addWidget(theme_text_label)

            theme_VBox_layout = QVBoxLayout()
            theme_VBox_layout.addWidget(theme_label)
            theme_VBox_layout.addWidget(theme_text_label)
            theme_HBox_layout.addLayout(theme_VBox_layout)

            if theme == self.theme:
                target_theme_label = theme_label

            count += 1

            # n個以上で新しい行に移動
            if count >= CHARACTER_SELECTION_COLUMN:
                scroll_layout.addLayout(theme_HBox_layout)
                theme_HBox_layout = QHBoxLayout()  # 新しい行を作成
                theme_HBox_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
                count = 0  # ｶｳﾝﾄをﾘｾｯﾄ
                row_count += 1

        # 残りのﾗﾍﾞﾙを追加
        if count > 0:
            scroll_layout.addLayout(theme_HBox_layout)

        if row_count >= LABELS_HEIGHT:
            scroll_widget.setLayout(scroll_layout)
            scroll_area_themes.setWidget(scroll_widget)
            layout_one.addWidget(scroll_area_themes)
            label_height = theme_label.height()
            scroll_area_themes.setFixedHeight(label_height * LABELS_HEIGHT)
        else:
            layout_one.addLayout(scroll_layout)

        if target_theme_label:
            # scroll_area_themes.ensureWidgetVisible(target_theme_label) # 正確でない
            QTimer.singleShot(0, lambda: scroll_area_themes.ensureWidgetVisible(target_theme_label))
            # global_pos = target_theme_label.mapToGlobal(QPoint(0, 0))
            # scroll_pos = scroll_area_themes.viewport().mapFromGlobal(global_pos)
            # scroll_bar = scroll_area_themes.verticalScrollBar()
            # scroll_bar.setValue(scroll_pos.y())

            # scroll_bar = scroll_area_themes.verticalScrollBar()
            # scroll_bar.setValue(target_theme_label.y())


        #==========================================================

        layout_one.addStretch(1)
        tab_one.setLayout(layout_one)

        # ---- ﾀﾌﾞの設定 --------------------------------------
        the_tab.addTab(tab_one,"crops")

        layout.addWidget(the_tab)
        # --- ﾎﾞﾀﾝの設定 --------------------------------------

        button_layout = QHBoxLayout()
        button_layout.addWidget(button)
        button_layout.addWidget(button2)


        button_layout.addStretch(1)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        music_sound_play(r"open")




    def generate_crops_sample(self, crop:str):
        from .html_media import CROPS_IMAGES_PATH_DICT

        if crop in CROPS_IMAGES_PATH_DICT:
            image_urls = CROPS_IMAGES_PATH_DICT[crop]

        addon_path = dirname(__file__)

        addon_package = mw.addonManager.addonFromModule(__name__)
        mediafolder_farm = f"/_addons/{addon_package}/"

        crop_pixmaps = []
        for image_url in image_urls:
            if image_url:
                image_url: str
                image_path = join(addon_path, image_url.replace(mediafolder_farm, ""))
                if os.path.exists(image_path):
                    crop_pixmaps.append(image_path)

        if hasattr(self, 'crops_HBox_layout'):
            while self.crops_HBox_layout.count():
                child = self.crops_HBox_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        else:
            self.crops_HBox_layout = QHBoxLayout()

        self.now_crop_label.setText(crop.replace('_', ' ').upper())

        for crop_pixmap in crop_pixmaps:
            crop_label = QLabel()
            crop_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
            crop_pixmap = QPixmap(crop_pixmap)
            crop_pixmap = crop_pixmap.scaledToWidth(50)
            crop_label.setPixmap(crop_pixmap)
            crop_label.setFixedHeight(100)
            self.crops_HBox_layout.addWidget(crop_label)

        self.crops_HBox_layout.addStretch()
        return self.crops_HBox_layout




    # ｾﾊﾟﾚｰﾀを作成する関数=========================
    def create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("border: 1px solid gray")
        return separator
    # =================================================

    # ﾁｪｯｸﾎﾞｯｸｽを生成する関数=======================
    def create_checkbox(self, label, attribute_name):
        checkbox = QCheckBox(label, self)
        checkbox.setChecked(getattr(self, attribute_name))

        def handler(state):
            if state == 2:
                setattr(self, attribute_name, True)
            else:
                setattr(self, attribute_name, False)
            music_sound_play(r"select")

        checkbox.stateChanged.connect(handler)
        return checkbox
    #=================================================


    # --- cancel -------------
    def cancelSelect(self):
        music_sound_play(r"cancel")
        emoticons = [":-/", ":-O", ":-|"]
        selected_emoticon = random.choice(emoticons)
        tooltip("Canceled " + selected_emoticon)
        self.close()

    #------------checkbox-----------------


    def handle_button_clicked(self):
        music_sound_play(r"OK")
        self.save_config_fontfamiles()

        from .new_cards_heatmap import reset_global_html
        reset_global_html()

        mw.moveToState("deckBrowser")

        emoticons = [":-)", ":-D", ";-)"]
        selected_emoticon = random.choice(emoticons)
        tooltip("Changed setting " + selected_emoticon)

    def save_config_fontfamiles(self):
        config = mw.addonManager.getConfig(__name__)

        self.crops_dict[self.methods_key][self.plant_config_date] = self.theme
        config["farm_crops_dict"] = self.crops_dict

        mw.addonManager.writeConfig(__name__, config)




    # ｷｬﾗｸﾀｰ選択画面
    def create_label_with_image(self, icon_image_path, theme):
        pixmap1 = QPixmap(self.backFrame_image)

        pixmap1 = pixmap1.scaledToWidth(LABELS_SCALED)

        pixmap2 = QPixmap(icon_image_path)
        pixmap2 = pixmap2.scaledToWidth(LABELS_SCALED)

        painter = QPainter(pixmap1)
        painter.drawPixmap(0, 0, pixmap2)
        painter.end()

        label = QLabel()
        label.setPixmap(pixmap1)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFixedSize(LABELS_SCALED, LABELS_SCALED)

        overlay = QLabel(label)  # labelの上に重ねる新たなQLabelを作成
        overlay.setStyleSheet("background-color: rgba(0, 0, 0, 127);")  # 半透明の黒に設定
        overlay.resize(label.size())  # labelと同じｻｲｽﾞに設定
        # config = mw.addonManager.getConfig(__name__)

        if theme == self.theme:
            overlay.hide()

        self.labels_and_overlays[label] = overlay  # 辞書に保存

        def clickAction(event:QMouseEvent):
            if event.button() == Qt.MouseButton.LeftButton:
                self.theme = theme
                overlay.hide()  # ｸﾘｯｸ時にoverlayを非表示に設定

                # 他の全てのQLabelのoverlayを再表示
                for other_label, other_overlay in self.labels_and_overlays.items():
                    if other_label is not label:
                        other_overlay.show()

                self.generate_crops_sample(self.theme)

        label.mousePressEvent = clickAction
        label.setCursor(Qt.CursorShape.PointingHandCursor)  # ｶｰｿﾙを設定
        return label



def get_mediaFile_path(name):
    addon_path =  os.path.dirname(__file__)
    audio_folder = join(addon_path,name)
    return audio_folder

def music_sound_play(folder):
    return


def run_change_crops(parent, plant_config_date, cards):
    change_crops = ChangeCrops(parent, plant_config_date, cards)
    try:
        change_crops.exec()
    except:change_crops.exec_()
