from nicegui import PageArguments, ui

from frontend.ui.components import create_input_field, create_result_area
from frontend.ui.handlers import handle_admin_submit, handle_url_submit
from frontend.shared_state import set_result_area


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
        subtitle = ui.label().classes(
            "text-lg text-gray-600 dark:text-gray-400 text-center max-w-2xl"
        )
        page_switcher = (
            ui.button().classes("absolute top-4 left-4").props("color=primary")
        )
        ui.switch().bind_value(dark).props("flat round color=primary").tooltip(
            "Toggle dark mode"
        ).classes("absolute top-4 right-4")
        ui.sub_pages(
            {"/": main, "/admin": admin},
            data={"title": title, "subtitle": subtitle, "page_switcher": page_switcher},
        ).classes("w-full max-w-[1024px] items-center")


def main(title: ui.label, subtitle: ui.label, page_switcher: ui.button):
    # global elements
    title.text = "🔗 URL Shortener"
    subtitle.text = "Transform long URLs into short, shareable links"
    page_switcher.text = "⚙️ Admin Panel"
    page_switcher.on("click", lambda: ui.navigate.to("/admin"))
    
    create_input_field(
        title="Shorten Your URL",
        input_title="Enter URL",
        input_placeholder="https://example.com/your-long-url",
        input_value="https://bin-nich-kreativ.de",
        button_label="Shorten URL",
        tip="💡 Make sure your URL starts with http:// or https://",
        on_submit=handle_url_submit,
    )
    
    set_result_area(create_result_area())



def admin(
    args: PageArguments, title: ui.label, subtitle: ui.label, page_switcher: ui.button
):
    key = args.query_parameters.get("key", "")
    
    # global elements
    title.text = "⚙️ Admin Dashboard"
    subtitle.text = "Manage and monitor your shortened URLs"
    page_switcher.text = "🏠 Back to Home"
    page_switcher.on("click", lambda: ui.navigate.to("/"))
    
    create_input_field(
        title="Admin Access",
        input_title="Admin Key",
        input_placeholder="Enter your admin key here",
        input_value=key if key else "",
        button_label="Get Analytics",
        tip="🔑 Use the admin key provided when you created your short URL",
        on_submit=handle_admin_submit,
    )

    set_result_area(create_result_area())
    
    if key:
        handle_admin_submit(key, notification=False)


ui.run(favicon="🔗", title="API Shortener")
