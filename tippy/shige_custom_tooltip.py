

from aqt import mw, gui_hooks

# https://atomiks.github.io/tippyjs/

TIPPY_FOLDER = "tippy"

def get_tooltip():
    # gui_hooks.webview_did_inject_style_into_page
    # mw.addonManager.setWebExports(
    #     __name__, rf"({TIPPY_FOLDER})/.*(js|css)"
    # )
    addon_package = mw.addonManager.addonFromModule(__name__)
    tippy_folder_path = f"/_addons/{addon_package}/{TIPPY_FOLDER}"

    shige_custom_tooltip  = f"""
    <link rel="stylesheet" href="{tippy_folder_path}/tippy.css">
    <link rel="stylesheet" href="{tippy_folder_path}/scale.css">
    <script src="{tippy_folder_path}/popper.min.js"></script>
    <script src="{tippy_folder_path}/tippy.umd.min.js"></script>
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        const selectors = [
            '.shige_day_farm'
        ];
        selectors.forEach(selector => {{
            document.querySelectorAll(selector).forEach(element => {{
                const cardCount = parseInt(element.getAttribute('data-card-count'), 10);
                let backgroundColor;
                    if (cardCount === 0) {{
                        backgroundColor = 'rgba(128, 128, 128, 0.9)';
                }} else if (cardCount > 30) {{
                    const blueValue = Math.min(200, Math.max(0, Math.floor((cardCount / 100) * 200)));
                    backgroundColor = `rgba(${{0 + blueValue}}, 100, 255, 0.9)`;

                }} else {{
                    const blueValue = Math.min(100, Math.max(0, Math.floor((cardCount / 30) * 100)));
                    backgroundColor = `rgba(0, ${{200 - blueValue}}, 255, 0.9)`;
                }}

                tippy(element, {{
                    content: element.getAttribute('data-tippy-content'),
                    allowHTML: true,
                    animation: 'scale',
                    theme: 'custom',
                    onShow(instance) {{
                        const tippyBox = instance.popper.querySelector('.tippy-box');
                        tippyBox.style.backgroundColor = backgroundColor;
                        const tippyArrow = instance.popper.querySelector('.tippy-arrow');
                        tippyArrow.style.color = backgroundColor;
                    }}
                }});
            }});
        }});
    }});
    </script>
    """

    return shige_custom_tooltip

from aqt.webview import WebContent
from aqt.deckbrowser import DeckBrowser

def on_webview_will_set_content(web_content: WebContent, context):

    if not isinstance(context, DeckBrowser):
        # not DeckBrowser, do not modify content
        return

    # DeckBrowser, perform changes to content

    context: DeckBrowser

    addon_package = mw.addonManager.addonFromModule(__name__)
    tippy_folder_path = f"/_addons/{addon_package}/{TIPPY_FOLDER}"

    js_files = [
        "popper.min.js",
        "tippy.umd.min.js",
        "shige_tooltip.js"
    ]

    for js_file in js_files:
        web_content.js.append(f"{tippy_folder_path}/{js_file}")


    css_files = [
        "tippy.css",
        "scale.css"
    ]

    for css_file in css_files:
        web_content.css.append(f"{tippy_folder_path}/{css_file}")


def set_tippy_css_js():
    gui_hooks.webview_will_set_content.append(on_webview_will_set_content)







### simple css ### ﾂｰﾙﾁｯﾌﾟがはみ出たときに表示されない/ｽｸﾛｰﾙﾊﾞｰが表示される/ﾚｲｱｳﾄが崩れる

# def get_tooltip():
#     gui_hooks.webview_did_inject_style_into_page
#     # mw.addonManager.setWebExports(
#     #     __name__, rf"({TIPPY_FOLDER})/.*(js|css)"
#     # )
#     addon_package = mw.addonManager.addonFromModule(__name__)
#     tippy_folder_path = f"/_addons/{addon_package}/{TIPPY_FOLDER}"

#     shige_custom_tooltip  = f"""
#     <link rel="stylesheet" href="{tippy_folder_path}/simple.css">

#     <script>
#     document.addEventListener('DOMContentLoaded', function() {{
#         const selectors = [
#             '.shige_day_farm'
#         ];
#         selectors.forEach(selector => {{
#             document.querySelectorAll(selector).forEach(element => {{
#                 const cardCount = parseInt(element.getAttribute('data-card-count'), 10);
#                 let backgroundColor;
#                     if (cardCount === 0) {{
#                         backgroundColor = 'rgba(128, 128, 128, 0.9)';
#                 }} else if (cardCount > 30) {{
#                     const blueValue = Math.min(200, Math.max(0, Math.floor((cardCount / 100) * 200)));
#                     backgroundColor = `rgba(${{0 + blueValue}}, 100, 255, 0.9)`;

#                 }} else {{
#                     const blueValue = Math.min(100, Math.max(0, Math.floor((cardCount / 30) * 100)));
#                     backgroundColor = `rgba(0, ${{200 - blueValue}}, 255, 0.9)`;
#                 }}

#                 const tooltipText = document.createElement('div');
#                 tooltipText.className = 'custom_shige_tooltiptext';
#                 tooltipText.innerHTML = element.getAttribute('data-tippy-content');
#                 tooltipText.style.backgroundColor = backgroundColor;

#                 const tooltipContainer = document.createElement('div');
#                 tooltipContainer.className = 'custom_shige_tooltip';
#                 tooltipContainer.appendChild(tooltipText);

#                 element.appendChild(tooltipContainer);
#             }});
#         }});
#     }});
#     </script>
#     """

#     return shige_custom_tooltip




# from aqt import mw, gui_hooks

# # https://atomiks.github.io/tippyjs/

# TIPPY_FOLDER = "tippy"

# def get_tooltip():
#     gui_hooks.webview_did_inject_style_into_page
#     # mw.addonManager.setWebExports(
#     #     __name__, rf"({TIPPY_FOLDER})/.*(js|css)"
#     # )
#     addon_package = mw.addonManager.addonFromModule(__name__)
#     tippy_folder_path = f"/_addons/{addon_package}/{TIPPY_FOLDER}"

#     shige_custom_tooltip  = f"""
#     <link rel="stylesheet" href="{tippy_folder_path}/tippy.css">
#     <link rel="stylesheet" href="{tippy_folder_path}/scale.css">
#     <script src="{tippy_folder_path}/popper.min.js"></script>
#     <script src="{tippy_folder_path}/tippy.umd.min.js"></script>
#     <script>
#     document.addEventListener('DOMContentLoaded', function() {{
#         const selectors = [
#             '.shige_day_farm'
#         ];
#         selectors.forEach(selector => {{
#             document.querySelectorAll(selector).forEach(element => {{
#                 const cardCount = parseInt(element.getAttribute('data-card-count'), 10);
#                 const blueValue = Math.min(255, Math.max(0, Math.floor((cardCount / 30) * 100)));
#                 const backgroundColor = `rgb(0, ${{200 - blueValue}}, 255)`;

#                 tippy(element, {{
#                     content: element.getAttribute('data-tippy-content'),
#                     allowHTML: true,
#                     animation: 'scale',
#                     theme: 'custom',
#                     onShow(instance) {{
#                         instance.popper.querySelector('.tippy-box').style.backgroundColor = backgroundColor;
#                         instance.popper.querySelector('.tippy-arrow').style.backgroundColor = backgroundColor;
#                     }}
#                 }});
#             }});
#         }});
#     }});
#     </script>
#     """

#     return shige_custom_tooltip