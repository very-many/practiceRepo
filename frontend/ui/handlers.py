from nicegui import ui
from frontend.services.url_service import URLService
from frontend.shared_state import get_result_area, set_result_area
from frontend.ui.components import create_admin_highlight_card, create_shorten_url_result_card


def handle_url_submit(url: str):
    """Handle URL shortening submission"""
    try:
        result = URLService.shorten_url(url)
        _display_url_success(result)
        ui.notify("URL shortened successfully!", color="positive", position="top")
    except ValueError as e:
        ui.notify(f"⚠️ {str(e)}", color="warning", position="top")
    except Exception as e:
        ui.notify(f"❌ Error: {str(e)}", color="negative", position="top")


def handle_admin_submit(admin_key: str):
    """Handle admin analytics submission"""
    try:
        result = URLService.get_url_analytics(admin_key)
        _display_admin_success(result)
        ui.notify("Admin data loaded successfully!", color="positive", position="top")
    except ValueError as e:
        ui.notify(f"⚠️ {str(e)}", color="warning", position="top")
    except Exception as e:
        ui.notify(f"❌ Error: {str(e)}", color="negative", position="top")


def _display_url_success(result):
    """Display successful URL shortening result"""
    result_area = get_result_area()
    if not result_area:
        print("Result area not set, cannot display result.")
        return
        
    result_area.visible = True
    result_area.clear()

    with result_area:
        # Success header
        with ui.row().classes("w-full items-center gap-3 mb-4"):
            ui.icon("check_circle", color="green").classes("text-2xl")
            ui.label("URL Successfully Shortened!").classes(
                "text-xl font-semibold text-green-600 dark:text-green-400"
            )

        # Result cards
        with ui.column().classes("w-full gap-4"):
            create_shorten_url_result_card(
                title="Shortened URL",
                color="purple",
                result=result.get("url", ""),
                icon="link",
            )

            create_shorten_url_result_card(
                title="Original URL",
                color="blue",
                result=result.get("target_url", ""),
                icon="language",
            )

            create_shorten_url_result_card(
                title="Admin URL",
                color="orange",
                result=result.get("admin_url", "").split("/")[-1],
                icon="admin_panel_settings",
                is_admin=True,
            )


def _display_admin_success(result):
    """Display successful admin analytics result"""
    result_area = get_result_area()
    if not result_area:
        print("Result area not set, cannot display result.")
        return

    result_area.visible = True
    result_area.clear()

    with result_area:
            # Admin header
            with ui.row().classes("w-full items-center gap-3 mb-6"):
                ui.icon("admin_panel_settings", color="primary").classes("text-3xl")
                ui.label("URL Analytics Dashboard").classes(
                    "text-2xl font-bold text-primary"
                )

            # Stats overview
            with ui.row().classes("w-full gap-4 mb-6"):
                # Click counter card
                create_admin_highlight_card(
                    title="Total Clicks",
                    status=str(result.get("clicks", 0)),
                    icon="mouse",
                    color="green"
                )

                # Status card
                status_active = result.get("is_active", False)
                status_color = "green" if status_active else "red"
                status_text = "Active" if status_active else "Inactive"
                status_icon = "check_circle" if status_active else "cancel"

                create_admin_highlight_card(
                    title="URL Status",
                    status=status_text,
                    icon=status_icon,
                    color=status_color
                )

            create_shorten_url_result_card(
                title="Shortened URL",
                color="purple",
                result=result.get("url", ""),
                icon="link",
            )
            create_shorten_url_result_card(
                title="Original URL",
                color="blue",
                result=result.get("target_url", ""),
                icon="language",
            )

            # Admin actions
            with ui.row().classes("w-full justify-center gap-4 mt-6"):
                #ui.button(
                #    "🔄 Refresh Data", on_click=lambda: on_admin_submit(admin_key)
                #).props("color=primary size=md")
                ui.button(
                    "🏠 Back to Home", on_click=lambda: ui.navigate.to("/")
                ).props("color=secondary size=md")


def _create_shorten_url_result_card(
    title: str, color: str, result: str, icon: str, is_admin: bool = False
):
    """Create a result card for shortened URL display"""
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
