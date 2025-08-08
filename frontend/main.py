from unittest import result
from nicegui import PageArguments, ui
from api import create_url, get_admin_info


def on_submit(url: str):
    try:
        result = create_url(url)
        result_area.visible = True
        result_area.clear()
        with result_area:
            with ui.label("Your shortened URL: "):
                ui.link(result.get('url', ''), result.get('url', ''), new_tab=True)
            with ui.label("Your original URL: "):
                ui.link(result.get('target_url', ''), result.get('target_url', ''), new_tab=True)
            with ui.label("Admin Key: "):
                ui.link(result.get('admin_url', '').split("/")[-1], f"/admin?key={result.get('admin_url', '').split('/')[-1]}")
        ui.notify("URL shortened successfully!", color="green")
    except Exception as e:
        ui.notify(f"Error: {str(e)}", color="red")
        
def on_admin_submit(admin_key: str):
    if not admin_key:
        ui.notify("Please enter an admin key.", color="red")
        return
    try:
        result = get_admin_info(admin_key)
        result_area.visible = True
        result_area.clear()
        with result_area:
            with ui.label("Shortened URL: "):
                ui.link(result.get('url', ''), result.get('url', ''), new_tab=True)
            with ui.label("Original URL: "):
                ui.link(result.get('target_url', ''), result.get('target_url', ''), new_tab=True)
            with ui.label("Clicks: "):
                ui.label(str(result.get('clicks', 0)))
            if result.get('is_active', False) == True:
                ui.label("Status: Active")
            else:
                ui.label("Status: Inactive")
        ui.notify("Admin info retrieved successfully!", color="green")
    except Exception as e:
        ui.notify(f"Error: {str(e)}", color="red")


@ui.page("/")
@ui.page("/admin")
def index():
    ui.colors(primary="#7e57c2", secondary="#26c6da", accent="#ff7043")
    dark = ui.dark_mode()
    # bg img
    ui.element("img").props(
        'src="https://bin-nich-kreativ.de/_astro/background.BPKAcmfN.svg"'
    ).classes("fixed top-0 left-0 w-screen h-screen object-cover -z-10 blur-[100px]")

    # main layout
    with ui.column().classes("w-full m-auto items-center gap-8"):
        title = ui.link("URL Shortener", "/").classes(
            "text-4xl font-bold bg-gradient-to-r from-purple-500 to-cyan-400 bg-clip-text text-transparent mt-12 text-center"
        )
        ui.switch().bind_value(dark).props("flat round color=primary").tooltip(
            "Toggle dark mode"
        ).classes("absolute top-4 right-4")
        ui.sub_pages({"/": main, "/admin": admin}, data={"title": title}).classes("w-full max-w-[1024px]")


def main(title: ui.label):
    title.text = "URL Shortener"
    ui.button("Go to Admin page", on_click=lambda: ui.navigate.to("/admin")).classes(
        "absolute top-4 left-4"
    ).props("color=primary")
    with ui.row().classes("w-full justify-center gap-4 items-center"):
        url_to_shorten_box = (
            ui.input(
                label="URL to shorten",
                placeholder="Enter URL here",
                value="https://bin-nich-kreativ.de",
            )
            .classes("w-full max-w-2xl")
            .props("clearable")
        )
        shorten_button = ui.button(
            "Shorten", on_click=lambda: on_submit(url_to_shorten_box.value)
        ).props("color=primary")
        
    global result_area
    result_area = ui.column().classes(
        "w-full max-w-[1024px] flex flow-col justify-center p-8 shadow-lg rounded-xl bg-gray-200/60 dark:bg-gray-800/60"
    )
    result_area.visible = False


def admin(args: PageArguments, title: ui.label):
    key = args.query_parameters.get("key", "")
    title.text = "URL Shortener Admin Page"
    ui.label("Admin page content")
    ui.button("Go to main page", on_click=lambda: ui.navigate.to("/")).classes(
        "absolute top-4 left-4"
    ).props("color=primary")
    with ui.row().classes("w-full justify-center gap-4 items-center"):
        admin_key_box = (
            ui.input(
                label="Admin Key",
                placeholder="Enter Admin Key here",
                value=key if key else "BQEON_XHQGE93U",
            )
            .classes("w-full max-w-2xl")
            .props("clearable")
        )
        admin_button = ui.button(
            "get info", on_click=lambda: on_admin_submit(admin_key_box.value)
        ).props("color=primary")
        
    global result_area
    result_area = ui.column().classes(
        "w-full max-w-[1024px] flex flow-col justify-center p-8 shadow-lg rounded-xl bg-gray-200/60 dark:bg-gray-800/60"
    )
    result_area.visible = False


ui.run(favicon="🔗", title="API Shortener")
