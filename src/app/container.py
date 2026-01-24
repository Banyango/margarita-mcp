import wireup

import core
import libs

container = wireup.create_async_container(
    service_modules=[core, libs],
)
