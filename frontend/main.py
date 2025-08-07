from nicegui import ui
from api import create_url


ui.colors(primary="#7e57c2", secondary="#26c6da", accent="#ff7043")

dark = ui.dark_mode()
old_img_url = ""


def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        ui.dark_mode().enable()
    else:
        ui.dark_mode().disable()


# bg img
ui.element("img").props(
    'src="https://bin-nich-kreativ.de/_astro/background.BPKAcmfN.svg"'
).classes("fixed top-0 left-0 w-screen h-screen object-cover -z-10 blur-[100px]")


# main layout
with ui.column().classes("w-full m-auto items-center gap-8"):
    ui.label("API Shortener").classes(
        "text-4xl font-bold bg-gradient-to-r from-purple-500 to-cyan-400 bg-clip-text text-transparent mt-8"
    )

    ui.switch().bind_value(dark).props("flat round color=primary").tooltip(
        "Toggle dark mode"
    ).classes("absolute top-4 right-4")
    ui.label(create_url("https://example.com")).classes("text-lg")




ui.run(favicon="🔗", title="API Shortener")
