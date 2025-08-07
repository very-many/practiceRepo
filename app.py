from nicegui import ui
from azure_face_api import analyze_image
from utils import get_image_size, create_svg_overlay

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
    ui.label("Azure Face API Demo").classes(
        "text-4xl font-bold bg-gradient-to-r from-purple-500 to-cyan-400 bg-clip-text text-transparent mt-8"
    )

    ui.switch().bind_value(dark).props("flat round color=primary").tooltip(
        "Toggle dark mode"
    ).classes("absolute top-4 right-4")

    with ui.row().classes("w-full justify-center gap-4 items-center"):
        img_url_box = (
            ui.input(
                label="Image URL",
                placeholder="Enter image URL here",
                value="https://microsoftlearning.github.io/AI-900-AIFundamentals/instructions/media/create-face-solutions/store-camera-1.jpg",
            )
            .classes("w-full max-w-2xl")
            .props("clearable")
        )
        analyze_button = (
            ui.button("Analyze", on_click=lambda: on_submit(img_url_box.value))
            .props("color=primary")
            .style
        )

    image_card = ui.card().classes(
        "w-full max-w-[1024px] min-h-[512px] flex items-center justify-center relative shadow-lg rounded-xl "
        "bg-gray-200/60 dark:bg-gray-800/60"
    )
    with image_card:
        result_area = ui.row().classes("inline-block w-full h-full")
        skeleton = ui.skeleton().classes(
            "w-full h-full absolute top-0 left-0 rounded-xl opacity-60"
        )


def on_submit(img_url):
    global old_img_url
    if old_img_url == img_url:
        ui.notify("Image already analyzed", type="info")
        return

    result_area.clear()
    skeleton.visible = True
    try:
        faces = analyze_image(img_url)
        img_width, img_height = get_image_size(img_url)
        with result_area:
            with ui.element("div").classes("relative w-full"):
                ui.image(img_url).classes("w-full block rounded-lg")
                ui.html(create_svg_overlay(faces, img_width, img_height))
        skeleton.visible = False
        ui.notify(f"Success", type="positive")
        old_img_url = img_url
    except Exception as e:
        with result_area:
            skeleton.visible = True
            ui.notify(f"Error: {e}", type="negative")


ui.run(favicon="🤖", title="Azure Face API Demo")
