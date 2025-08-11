from nicegui import ui
from frontend.services.url_service import URLService
from frontend.shared_state import get_result_area, set_result_area
from frontend.ui.components import (
    create_admin_highlight_card,
    create_button,
    create_dialog,
    create_shorten_url_result_card,
)


def handle_url_submit(url: str):
    """Handle URL shortening submission"""
    try:
        result = URLService.shorten_url(url)
        ui.notify("URL shortened successfully!", color="positive")
        _display_url_success(result)
    except ValueError as e:
        ui.notify(f"⚠️ {str(e)}", color="warning")
    except Exception as e:
        ui.notify(f"❌ Error: {str(e)}", color="negative")


def handle_admin_submit(secret_key: str, notification: bool = True):
    """Handle admin analytics submission"""
    try:
        result = URLService.get_url_analytics(secret_key)
        if notification:
            ui.notify(
                "Admin data loaded successfully!", color="positive"
            )
        _display_admin_success(result)
    except ValueError as e:
        ui.notify(f"⚠️ {str(e)}", color="warning")
    except Exception as e:
        ui.notify(f"❌ Error: {str(e)}", color="negative")


def handle_toggle_url(secret_key: str, is_active: bool = True):
    """Handle URL deactivation"""
    try:
        URLService.toggle_short_url(secret_key)
        ui.notify(
            f"URL {'reactivated' if is_active else 'deactivated'} successfully!",
            color="positive"
        )
        handle_admin_submit(secret_key, notification=False)
    except ValueError as e:
        ui.notify(f"⚠️ {str(e)}", color="warning")
    except Exception as e:
        ui.notify(f"❌ Error: {str(e)}", color="negative")


def handle_delete_url(secret_key: str):
    """Handle URL deletion"""
    try:
        URLService.delete_short_url(secret_key)
        ui.notify("URL deleted successfully!", color="positive")
        get_result_area().visible = False
        get_result_area().clear()
    except ValueError as e:
        ui.notify(f"⚠️ {str(e)}", color="warning")
    except Exception as e:
        ui.notify(f"❌ Error: {str(e)}", color="negative")


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
        with ui.row().classes(
            "w-full flex sm:flex-row flex-col justify-between gap-4 mt-6"
        ):
            create_button(
                label="🔄️ Refresh Data",
                onclick=lambda: handle_admin_submit(secret_key),
                color="blue",
            )
            create_button(
                label="🧯 Delete URL",
                onclick=lambda: handle_delete_url_confirm(secret_key),
                color="red",
            )
            create_button(
                label=f"{'🗑️ Deactivate URL' if status_active else '♻️ Reactivate URL'}",
                onclick=lambda: handle_toggle_url(secret_key, is_active=status_active),
                color="yellow" if status_active else "green",
            )
