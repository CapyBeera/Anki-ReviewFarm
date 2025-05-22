
from aqt import (QApplication, QDialog, QDoubleSpinBox, QFont, QFont, QFontMetrics, QFrame, QFrame, QHBoxLayout,
    QLineEdit, QMouseEvent, QPainter, QPainterPath, QRectF, QScrollArea, QTabWidget, QTimer, QWidget,Qt)
from aqt import QVBoxLayout, QLabel, QPushButton
from aqt import mw
from os.path import join, dirname
from aqt import QIcon
from aqt import QPixmap
from aqt.utils import openLink,tooltip
from aqt import QCheckBox
from .config import listOfSupportedPatrons as CreditData
from .config.endroll import EndrollWidget
import random
import os


from .html_media import THEMES, SUNFLOWER

CHARACTER_SELECTION_COLUMN = 10
PLANTS_TEXT = "plantsText"
ICON_PATH = r"media/icons/plantsText.png"
ICON_PATH_02 = r"media/Farm_02_icons/plantsText.png"
backFrame_image = r"Square_button_3.png"
LABELS_SCALED = 75


TOGGLE_PRINT = False
THE_ADDON_NAME = "New Cards Farm by Shige"
BUTTON_WIDTH = 95

SET_LINE_EDID_WIDTH = 400
MAX_LABEL_WIDTH = 100

SET_SCALEDTOWIDTH = 400

def toggle_print(printtext):
    if TOGGLE_PRINT:
        print(">>>>>>>>>>>>>>>>>>",str(printtext))


class SetFontViewer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setFixedHeight(400)
        self.resize(900, self.height())

        config = mw.addonManager.getConfig(__name__)
        self.plant_species = self.theme = config.get("plant_species", "sunflower")
        self.image_size = config.get("image_size", 25)
        self.count_only_graduated_cards = config.get("count_only_graduated_cards", True)
        self.plant_same_crop_all = config.get("plant_same_crop_all", True)
        self.change_crops_randomly = config.get("change_crops_randomly", False)
        self.show_farmer = config.get("show_farmer", True)


        # Set window icon
        addon_path = dirname(__file__)
        self.icon_path = join(addon_path, r"icon.png")
        self.logo_icon = QIcon(self.icon_path)
        self.setWindowIcon(self.logo_icon)


        self.backFrame_image = join(addon_path, backFrame_image)
        self.labels_and_overlays = {}

        if False:
            # Set image on QLabel
            self.patreon_label = QLabel()
            patreon_banner_path = join(addon_path, r"banner.jpg")
            pixmap = QPixmap(patreon_banner_path)
            pixmap = pixmap.scaledToWidth(SET_SCALEDTOWIDTH, Qt.TransformationMode.SmoothTransformation)
            pixmap = self.pixmap_round(pixmap)

            self.patreon_label.setPixmap(pixmap)
            self.patreon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.patreon_label.setFixedSize(pixmap.width(), pixmap.height())
            # Connect mousePressEvent to slot
            self.patreon_label.mousePressEvent = self.open_patreon_Link
            # Set cursor
            self.patreon_label.setCursor(Qt.CursorShape.PointingHandCursor)
            # Connect enterEvent and leaveEvent to slots
            self.patreon_label.enterEvent = self.patreon_label_enterEvent
            self.patreon_label.leaveEvent = self.patreon_label_leaveEvent

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


        if False:
            layout.addWidget(self.patreon_label)

        # -----------------------------------------------------
        the_tab = QTabWidget(self)

        app_style = QApplication.instance().styleSheet()
        if not app_style:
            the_tab.setStyleSheet("background-color: transparent;")

        layout_one = QVBoxLayout()
        tab_one = QWidget()

        layout_one.addWidget(QLabel("<b>Change Crop ： Plant the same crop on all</b>"))

        theme_HBox_layout = QHBoxLayout()
        theme_HBox_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 左寄せに設定



        #== 作物を選択 ===================================================
        themes = THEMES

        count = 0
        row_count = 0
        scroll_area_themes = QScrollArea()
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

            count += 1

            # n個以上で新しい行に移動
            if count >= CHARACTER_SELECTION_COLUMN:
                scroll_layout.addLayout(theme_HBox_layout)
                theme_HBox_layout = QHBoxLayout()  # 新しい行を作成
                theme_HBox_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
                count = 0  # ｶｳﾝﾄをﾘｾｯﾄ
                row_count += 1

        LABELS_HEIGHT = 6
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
        #==========================================================


        layout_one.addStretch(1)
        tab_one.setLayout(layout_one)



        layout_two = QVBoxLayout()
        tab_two = QWidget()



        layout_two.addWidget(self.create_separator()) # ----------------


        self.image_size_label,self.image_size_values_spinbox = self.create_spinbox(
            "[ Size ] 10px ~ 64px  ", 10, 64, self.image_size, 70, 0, 1, "image_size")
        layout_two.addWidget(self.image_size_label)
        layout_two.addWidget(self.image_size_values_spinbox)

        layout_two.addWidget(self.create_separator()) # ----------------


        self.count_only_graduated_cards
        self.count_only_graduated_cards_label = self.create_checkbox("Count only graduated cards","count_only_graduated_cards")
        layout_two.addWidget(self.count_only_graduated_cards_label)

        # plant_same_crop_all

        self.plant_same_crop_all
        self.plant_same_crop_all_label = self.create_checkbox("Plant the same crop on all","plant_same_crop_all")
        layout_two.addWidget(self.plant_same_crop_all_label)

        self.change_crops_randomly
        self.change_crops_randomly_label = self.create_checkbox("Change crops randomly","change_crops_randomly")
        layout_two.addWidget(self.change_crops_randomly_label)
        
        self.show_farmer
        self.show_farmer_label = self.create_checkbox("Show farmer","show_farmer")
        layout_two.addWidget(self.show_farmer_label)
        
        
        

        layout_two.addWidget(self.create_separator()) # ----------------
        layout_two.addWidget(QLabel("Flower : 1 - 20 New Cards"))
        layout_two.addWidget(QLabel("Vegetable : 1 - 30 New Cards"))
        layout_two.addWidget(QLabel("Farmer : Streaks 7+ days Cow costume"))

        layout_two.addStretch(1)
        tab_two.setLayout(layout_two)

        # # ------------------------------------------------------
        # tab_two = QWidget()
        # layout_two = QVBoxLayout()


        # layout_two.addStretch(1)

        # tab_two.setLayout(layout_two)

        # # ------------------------------------------------------
        # tab_three = QWidget()
        # layout_three = QVBoxLayout()



        # layout_three.addStretch(1)
        # tab_three.setLayout(layout_three)

        # # ------------------------------------------------------
        # tab_four = QWidget()
        # layout_four = QVBoxLayout()


        # layout_four.addStretch(1)
        # tab_four.setLayout(layout_four)

        # ------------------------------------------------------

        # tab ｸﾚｼﾞｯﾄ =================================================
        credit_layout = QVBoxLayout()
        credit_data_attributes = [
                                'credits',
                                'caractor',
                                'sound',
                                'addons',
                                'budle',
                                'patreon',
                                'thankYou',
                                ]

        font = QFont("Times New Roman", 15)
        # font.setItalic(True)
        for attribute in credit_data_attributes:
            label = QLabel(f'<style>body, a {{ color: white; }}</style><body>{getattr(CreditData, attribute)}</body>')
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFont(font)
            label.setOpenExternalLinks(True)
            credit_layout.addWidget(label)

        credit_layout.addStretch(1)

        # (Credit)ｽｸﾛｰﾙｴﾘｱを作成 ----------------------
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        tab_Credit = EndrollWidget(self,scroll_area)
        tab_Credit.setLayout(credit_layout)
        scroll_area.setWidget(tab_Credit)

        # ---- ﾀﾌﾞの設定 --------------------------------------
        the_tab.addTab(tab_one,"crops")
        the_tab.addTab(tab_two,"option")
        # the_tab.addTab(tab_three,"sound")
        # the_tab.addTab(tab_four,"custom")
        the_tab.addTab(scroll_area,"credit")
        layout.addWidget(the_tab)
        # --- ﾎﾞﾀﾝの設定 --------------------------------------

        button_layout = QHBoxLayout()
        button_layout.addWidget(button)
        button_layout.addWidget(button2)


        button_layout.addStretch(1)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        music_sound_play(r"open")

    # ------------ patreon label----------------------
    def patreon_label_enterEvent(self, event):
        addon_path = dirname(__file__)
        patreon_banner_hover_path = join(addon_path, r"Patreon_banner.jpg")
        self.pixmap = QPixmap(patreon_banner_hover_path)
        self.pixmap = self.pixmap.scaledToWidth(SET_SCALEDTOWIDTH, Qt.TransformationMode.SmoothTransformation)
        self.pixmap = self.pixmap_round(self.pixmap)
        self.patreon_label.setPixmap(self.pixmap)

    def patreon_label_leaveEvent(self, event):
        addon_path = dirname(__file__)
        patreon_banner_hover_path = join(addon_path, r"banner.jpg")
        self.pixmap = QPixmap(patreon_banner_hover_path)
        self.pixmap = self.pixmap.scaledToWidth(SET_SCALEDTOWIDTH, Qt.TransformationMode.SmoothTransformation)
        self.pixmap = self.pixmap_round(self.pixmap)
        self.patreon_label.setPixmap(self.pixmap)
    # ------------ patreon label----------------------

    def pixmap_round(self,pixmap):
        path = QPainterPath()
        path.addRoundedRect(QRectF(pixmap.rect()), 10, 10)  # 角の丸み
        rounded_pixmap = QPixmap(pixmap.size())
        rounded_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        pixmap = rounded_pixmap
        return pixmap

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

    # ﾃｷｽﾄﾎﾞｯｸｽを作成する関数=========================
    def create_line_edits_and_labels(self, list_attr_name, list_items, b_name, b_index=None):

        main_layout = QVBoxLayout()
        items = list_items if isinstance(list_items, list) else [list_items]
        for i, item in enumerate(items):
            line_edit = QLineEdit(item)
            line_edit.textChanged.connect(lambda text,
                                        i=i,
                                        name=list_attr_name: self.update_list_item(name, i, text))
            line_edit.setMaximumWidth(SET_LINE_EDID_WIDTH)

            if i == 0:
                layout = QHBoxLayout()
                if b_index is not None:
                    b_name_attr = getattr(self, b_name)
                    label_edit = QLineEdit(b_name_attr[b_index])
                    label_edit.textChanged.connect(lambda text,
                                                i=i,
                                                b_name=b_name: self.update_label_item(b_name, b_index, text))
                    label_edit.setFixedWidth(MAX_LABEL_WIDTH)
                    layout.addWidget(label_edit)
                else:
                    label = QLabel(b_name)
                    label.setFixedWidth(MAX_LABEL_WIDTH)
                    layout.addWidget(label)
            else:
                label = QLabel()
                label.setFixedWidth(MAX_LABEL_WIDTH)
                layout = QHBoxLayout()
                layout.addWidget(label)

            line_edit = QLineEdit(item)
            line_edit.textChanged.connect(lambda text,
                                        i=i,
                                        name=list_attr_name: self.update_list_item(name, i, text))
            line_edit.setMaximumWidth(SET_LINE_EDID_WIDTH)
            layout.addWidget(line_edit)
            main_layout.addLayout(layout)
        return main_layout

    def update_label_item(self, b_name, index, text):
        update_label = getattr(self,b_name)
        update_label[index] = text
    def update_list_item(self, list_attr_name, index, text):
        # list_to_update = getattr(self, list_attr_name)
        # list_to_update[index] = text
        list_to_update = getattr(self, list_attr_name)
        if isinstance(list_to_update, list):
            list_to_update[index] = text
        else:
            setattr(self, list_attr_name, text)
    # ===================================================



    # ｽﾋﾟﾝﾎﾞｯｸｽを作成する関数=========================
    def create_spinbox(self, label_text, min_value,
                                max_value, initial_value, width,
                                decimals, step, attribute_name):
        def spinbox_handler(value):
            value = round(value, 1)
            if decimals == 0:
                setattr(self, attribute_name, int(value))
            else:
                setattr(self, attribute_name, value)

        label = QLabel(label_text, self)
        spinbox = QDoubleSpinBox(self)
        spinbox.setMinimum(min_value)
        spinbox.setMaximum(max_value)
        spinbox.setValue(initial_value)
        spinbox.setFixedWidth(width)
        spinbox.setDecimals(decimals)
        spinbox.setSingleStep(step)
        spinbox.valueChanged.connect(spinbox_handler)
        return label, spinbox
    #=================================================







    #-- open patreon link-----
    def open_patreon_Link(self,url):
        music_sound_play(r"openlink")
        openLink("http://patreon.com/Shigeyuki")


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
        mw.moveToState("deckBrowser")

        emoticons = [":-)", ":-D", ";-)"]
        selected_emoticon = random.choice(emoticons)
        tooltip("Changed setting " + selected_emoticon)

    def save_config_fontfamiles(self):
        config = mw.addonManager.getConfig(__name__)

        config["plant_species"] = self.theme
        config["image_size"] = self.image_size
        config["count_only_graduated_cards"] = self.count_only_graduated_cards
        config["plant_same_crop_all"] = self.plant_same_crop_all
        config["change_crops_randomly"] = self.change_crops_randomly
        config["show_farmer"] = self.show_farmer


        mw.addonManager.writeConfig(__name__, config)
        toggle_print(config)




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
        config = mw.addonManager.getConfig(__name__)

        if theme == config.get("plant_species",SUNFLOWER):
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

        label.mousePressEvent = clickAction
        label.setCursor(Qt.CursorShape.PointingHandCursor)  # ｶｰｿﾙを設定
        return label






def get_mediaFile_path(name):
    addon_path =  os.path.dirname(__file__)
    audio_folder = join(addon_path,name)
    return audio_folder

def music_sound_play(folder):
    return


def SetAnkiRestartConfig():
    font_viewer = SetFontViewer()
    try:
        font_viewer.exec()
    except:
        font_viewer.exec_()
