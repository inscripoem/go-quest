from typing import TYPE_CHECKING

from litestar.plugins import CLIPluginProtocol, InitPluginProtocol


if TYPE_CHECKING:
    from click import Group
    from litestar.config.app import AppConfig


class ApplicationCore(InitPluginProtocol, CLIPluginProtocol):
    """Application core configuration plugin.

    This class is responsible for configuring the main Litestar application with our routes, guards, and various plugins

    """

    __slots__ = ("app_slug",)
    app_slug: str

    def on_cli_init(self, cli: "Group") -> None:
        pass

    def on_app_init(self, app_config: "AppConfig") -> "AppConfig":
        """Configure application for use with SQLAlchemy.

        Args:
            app_config: The :class:`AppConfig <litestar.config.app.AppConfig>` instance.
        """

        from litestar.openapi.config import OpenAPIConfig
        from litestar.openapi.plugins import ScalarRenderPlugin
        from litestar_granian import GranianPlugin

        from go_quest import __version__ as current_version
        from go_quest.config import get_settings
        from go_quest.domain import SystemController

        settings = get_settings()
        self.app_slug = settings.app.slug

        # openapi
        app_config.openapi_config = OpenAPIConfig(
            title=settings.app.NAME,
            version=current_version,
            use_handler_docstrings=True,
            render_plugins=[
                ScalarRenderPlugin(version="latest"),
            ],
            path=settings.server.SCALAR_PATH,
        )

        # plugins
        app_config.plugins.extend(
            [
                GranianPlugin(),
            ]
        )

        # routes
        app_config.route_handlers.extend(
            [
                SystemController,
            ]
        )

        return app_config
