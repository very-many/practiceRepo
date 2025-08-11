from nicegui import ui
from frontend.services.url_service import URLService
from frontend.shared_state import get_result_area, set_result_area
from frontend.ui.components import (
    create_admin_highlight_card,
    create_dialog,
    create_shorten_url_result_card,
)


def handle_url_submit(url: str):
    """Handle URL shortening submission"""
    try:
        result = URLService.shorten_url(url)
        ui.notify("URL shortened successfully!", color="positive", position="top")
        _display_url_success(result)
    except ValueError as e:
        ui.notify(f"⚠️ {str(e)}", color="warning", position="top")
    except Exception as e:
        ui.notify(f"❌ Error: {str(e)}", color="negative", position="top")


def handle_admin_submit(secret_key: str, notification: bool = True):
    """Handle admin analytics submission"""
    try:
        result = URLService.get_url_analytics(secret_key)
        if notification:
            ui.notify(
                "Admin data loaded successfully!", color="positive", position="top"
            )
        _display_admin_success(result)
    except ValueError as e:
        ui.notify(f"⚠️ {str(e)}", color="warning", position="top")
    except Exception as e:
        ui.notify(f"❌ Error: {str(e)}", color="negative", position="top")


def handle_toggle_url(secret_key: str, is_active: bool = True):
    """Handle URL deactivation"""
    try:
        URLService.toggle_short_url(secret_key)
        ui.notify(
            f"URL {'reactivated' if is_active else 'deactivated'} successfully!",
            color="positive",
            position="top",
        )
        handle_admin_submit(secret_key, notification=False)
    except ValueError as e:
        ui.notify(f"⚠️ {str(e)}", color="warning", position="top")
    except Exception as e:
        ui.notify(f"❌ Error: {str(e)}", color="negative", position="top")


def handle_delete_url(secret_key: str):
    """Handle URL deletion"""
    try:
        URLService.delete_short_url(secret_key)
        ui.notify("URL deleted successfully!", color="positive", position="top")
        get_result_area().visible = False
        get_result_area().clear()
    except ValueError as e:
        ui.notify(f"⚠️ {str(e)}", color="warning", position="top")
    except Exception as e:
        ui.notify(f"❌ Error: {str(e)}", color="negative", position="top")


def handle_delete_url_confirm(secret_key: str):
    """Handle URL deletion confirmation"""
    create_dialog(
        title="Confirm URL Deletion",
        message="Are you sure you want to delete this URL?",
        button_label="Delete",
        on_confirm=lambda: handle_delete_url(secret_key),
    )


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

    secret_key = result.get("admin_url", "").split("/")[-1]

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
                color="green",
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
                color=status_color,
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
        with ui.row().classes("w-full flex justify-between gap-4 mt-6"):
            ui.button(
                "🔄️ Refresh Data", on_click=lambda: handle_admin_submit(secret_key)
            ).props("flat size=md").classes(
                "px-6 py-3 bg-blue-100 hover:bg-blue-200 dark:bg-blue-800/20 hover:dark:bg-blue-800/30 rounded-xl !text-blue-700 dark:!text-blue-400 transition-all duration-200 shadow-lg"
            )

            ui.button(
                "🧯 Delete URL", on_click=lambda: handle_delete_url_confirm(secret_key)
            ).props("flat size=md").classes(
                "px-6 py-3 bg-red-100 hover:bg-red-200 dark:bg-red-800/20 hover:dark:bg-red-800/30 rounded-xl !text-red-700 dark:!text-red-400 transition-all duration-200 shadow-lg"
            )



            ui.button(
                f"{"🗑️ Deactivate URL" if result.get('is_active', True) else "♻️ Reactivate URL"}",
                on_click=lambda: handle_toggle_url(
                    secret_key, is_active=result.get('is_active', True)
                ),
            ).props("flat size=md").classes(
                f"px-6 py-3 {'bg-yellow-100 hover:bg-yellow-200 dark:bg-yellow-800/20 hover:dark:bg-yellow-800/30 !text-yellow-700 dark:!text-yellow-400' if result.get('is_active', True) else 'bg-green-100 hover:bg-green-200 dark:bg-green-800/20 dark:hover:bg-green-800/30 !text-green-700 dark:!text-green-400'} rounded-xl transition-all duration-200 shadow-lg"
            )
