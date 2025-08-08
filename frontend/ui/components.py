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