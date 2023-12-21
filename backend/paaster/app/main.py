from typing import cast

from litestar import Litestar, Request
from litestar.config.cors import CORSConfig
from litestar.datastructures import State
from litestar.openapi import OpenAPIConfig, OpenAPIController
from litestar.openapi.spec import Contact, License, Server
from motor import motor_asyncio
from pydantic import BaseModel

from app.controllers import router
from app.env import SETTINGS


class OpenAPIControllerRouteFix(OpenAPIController):
    def render_stoplight_elements(self, request: Request) -> bytes:
        # Gross hack to overwrite the path for the openapi schema file.
        # due to reverse proxying.
        path_copy = str(self.path)
        self.path = SETTINGS.proxy_urls.backend + self.path

        spotlight_elements = cast(bytes, super().render_stoplight_elements(request))

        self.path = path_copy
        return spotlight_elements

app = Litestar(
    route_handlers=[router],
    state=State(
        {
            "mongo": motor_asyncio.AsyncIOMotorClient(
                SETTINGS.mongo.host, SETTINGS.mongo.port
            )[SETTINGS.mongo.collection],
        }
    ),
    openapi_config=OpenAPIConfig(
        **SETTINGS.open_api.model_dump(),
        root_schema_site="elements",
        openapi_controller=OpenAPIControllerRouteFix,
        enabled_endpoints={"openapi.json", "openapi.yaml", "elements"},
        description="OpenAPI specification for paaster.io, you are expected to read our encryption implementation to implement it yourself.",
        servers=[
            Server(url=SETTINGS.proxy_urls.backend, description="Production server.")
        ],
        terms_of_service="https://paaster.io/terms-of-service",
        license=License(
            name="GNU Affero General Public License v3.0",
            identifier="AGPL-3.0",
            url="https://github.com/WardPearce/paaster/blob/main/LICENSE",
        ),
        contact=Contact(
            name="Paaster API team",
            email="wardpearce@pm.me",
            url="https://github.com/WardPearce/Paaster",
        ),
    ),
    # cors_config=CORSConfig(
    #     allow_origins=[SETTINGS.proxy_urls.backend, SETTINGS.proxy_urls.frontend],
    #     allow_credentials=True,
    # ),
    type_encoders={BaseModel: lambda m: m.model_dump(by_alias=False)},
)
