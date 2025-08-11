from typing_extensions import Literal
from nicegui import ui
from typing import Callable


def create_admin_highlight_card(title: str, status: str, icon: str, color: str):
    with ui.card().classes(
        f"flex-1 p-6 bg-{color}-100 dark:bg-{color}-800/20 border-none shadow-lg"
    ):
        with ui.row().classes("items-center gap-2"):
            ui.icon(icon).classes(f"text-4xl text-{color}-600 dark:text-{color}-400")
            with ui.column().classes("flex-1 gap-0"):
                ui.label(status).classes(
                    f"text-3xl font-bold text-{color}-600 dark:text-{color}-400"
                )
                ui.label(title).classes(
                    f"text-sm font-medium text-{color}-700 dark:text-{color}-300"
                )


def create_shorten_url_result_card(
    title: str, color: str, result: str, icon: str, is_admin: bool = False
):
    with ui.card().classes(
        f"w-full p-4 bg-{color}-100 dark:bg-{color}-800/20 shadow-lg"
    ):
        with ui.row().classes("items-center gap-3 mb-2"):
            ui.icon(icon).classes(f"text-lg text-{color}-600 dark:text-{color}-400")
            ui.label(title).classes(
                f"font-medium text-{color}-700 dark:text-{color}-300"
            )
        with ui.row().classes("items-center gap-2 w-full"):
            ui.link(
                result,
                result if not is_admin else f"/admin?key={result}",
                new_tab=True if not is_admin else False,
            ).classes(
                f"flex-1 text-{color}-600 dark:text-{color}-400 font-mono text-sm bg-white dark:!bg-gray-800 px-3 py-2 rounded break-all {'no-underline' if is_admin else ''}"
            )
            if is_admin:
                ui.button(
                    "Manage",
                    on_click=lambda: ui.navigate.to(f"/admin?key={result}"),
                ).props("size=sm").classes(f"!bg-{color}-600 dark:!bg-{color}-400")
            ui.button(
                icon="content_copy",
                on_click=lambda: ui.run_javascript(
                    f"navigator.clipboard.writeText('{result}')"
                ),
            ).props(f"flat round size=sm").tooltip("Copy to clipboard").classes(
                f"!text-{color}-600 dark:!text-{color}-400"
            )


def create_input_field(
    title: str,
    input_title: str,
    on_submit: Callable[[str], None],
    input_placeholder: str = "",
    input_value: str = "",
    button_label: str = "Submit",
    tip: str = "",
):
    with ui.card().classes(
        "w-full max-w-4xl p-8 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-0 shadow-xl"
    ):
        ui.label(title).classes("text-xl font-semibold mb-4 text-center")

        with ui.row().classes("w-full gap-4 items-center sm:flex-row flex-col"):
            input = (
                ui.input(
                    label=input_title,
                    placeholder=input_placeholder,
                    value=input_value,
                )
                .classes("sm:flex-1 w-full")
                .props("outlined clearable")
            )
            submit_button = (
                ui.button(button_label, on_click=lambda: on_submit(input.value))
                .props("color=primary size=lg")
                .classes("px-8 w-full sm:w-auto")
            )

        # tip
        if tip:
            ui.label(tip).classes("text-sm text-gray-500 dark:text-gray-400 mt-2")


def create_result_area():
    result_area = ui.card().classes(
        "w-full max-w-4xl p-8 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-0 shadow-xl"
    )
    result_area.visible = False
    return result_area


def create_dialog(
    title: str,
    message: str,
    on_confirm: Callable[[], None],
    gradient: str = "negative",
    button_label: str = "Confirm",
):
    # Confirm button with colorful gradient
    color_gradients = {
        "negative": "from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600",
        "positive": "from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600",
        "primary": "from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600",
        "warning": "from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600",
    }
    gradient = color_gradients.get(gradient, color_gradients["negative"])
    dialog = ui.dialog().classes("w-full")
    with dialog:
        card = (
            ui.card()
            .classes(
                "w-full max-w-md p-8 backdrop-blur-xl border border-white/20 dark:border-white/10 !rounded-2xl shadow-2xl"
            )
            .style(
                "background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%);"
            )
            .props("flat")
        )

        with card:
            # Title with gradient text
            ui.label(title).classes(
                f"text-xl font-bold mb-3 bg-gradient-to-r {gradient} bg-clip-text text-transparent select-none"
            )

            # Message with subtle styling
            ui.label(message).classes(
                "text-gray-700 dark:text-gray-300 mb-8 leading-relaxed"
            )

            with ui.row().classes("w-full justify-end gap-3"):
                # Cancel button with glassmorphism
                ui.button("Cancel", on_click=dialog.close).props("flat").classes(
                    "px-6 py-2 bg-white/20 hover:bg-white/40 dark:bg-white/10 dark:hover:bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl !text-gray-700 dark:!text-gray-300 transition-all duration-200"
                ).style("box-shadow: 0 4px 15px rgba(0,0,0,0.1);")

                ui.button(
                    button_label, on_click=lambda: [dialog.close(), on_confirm()]
                ).props("flat").classes(
                    f"px-6 py-2 bg-gradient-to-r {gradient} text-white rounded-xl font-medium transition-all duration-200 hover:opacity-40"
                ).style(
                    "box-shadow: 0 4px 20px rgba(0,0,0,0.2);"
                )

    dialog.open()

def create_button(label: str, onclick: Callable[[], None], color: str):
    ui.button(
                label, on_click=lambda: onclick()
            ).props("flat size=md").classes(
                f"px-6 py-3 bg-{color}-100 hover:bg-{color}-200 dark:bg-{color}-800/20 hover:dark:bg-{color}-800/30 rounded-xl !text-{color}-700 dark:!text-{color}-400 transition-all duration-200 shadow-lg w-full sm:!w-auto"
            )


