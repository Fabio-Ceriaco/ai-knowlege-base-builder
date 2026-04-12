### Complete FastAPI streaming example setup

Source: https://fastapi.tiangolo.com/advanced/stream-data

Full example showing imports, FastAPI app initialization, and a multi-line message string used for streaming demonstrations.

```Python
from collections.abc import AsyncIterable, Iterable

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


message = """
Rick: (stumbles in drunkenly, and turns on the lights) Morty! You gotta come on. You got--... you gotta come with me.
Morty: (rubs his eyes) What, Rick? What's going on?
Rick: I got a surprise for you, Morty.
Morty: It's the middle of the night. What are you talking about?
Rick: (spills alcohol on Morty's bed) Come on, I got a surprise for you. (drags Morty by the ankle) Come on, hurry up. (pulls Morty out of his bed and into the hall)
Morty: Ow! Ow! You're tugging me too hard!
Rick: We gotta go, gotta get outta here, come on. Got a surprise for you Morty.
"""
```

---

### Run FastAPI tutorial examples with the CLI

Source: https://fastapi.tiangolo.com/contributing?q=

Execute documentation examples using the development server. This command starts Uvicorn on the default port to verify code functionality.

```bash
fastapi dev tutorial001.py
fast →fastapi dev tutorial001.py
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

restart ↻
```

---

### FastAPI streaming setup with imports

Source: https://fastapi.tiangolo.com/advanced/stream-data?q=

Complete setup showing required imports from collections.abc and fastapi for implementing streaming responses. This is the foundation for all streaming examples.

```python
from collections.abc import AsyncIterable, Iterable

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()
```

---

### Install FastAPI with standard dependencies using pip

Source: https://fastapi.tiangolo.com/virtual-environments?q=

Example of installing a package with extra dependencies, showing how pip downloads and extracts files into the default global environment.

```bash
pip install "fastapi[standard]"
fast →💬 Don't run this now, it's just an example 🤓pip install "fastapi[standard]"
restart ↻
```

---

### Example requirements.txt file

Source: https://fastapi.tiangolo.com/virtual-environments?q=

Sample requirements.txt showing FastAPI and Pydantic with pinned versions. Place this file in your project root and use with pip install -r or uv pip install -r.

```text
fastapi[standard]==0.113.0
pydantic==2.8.0
```

---

### GET /items/ - Basic Example

Source: https://fastapi.tiangolo.com/zh-hant/reference/fastapi

A basic example of a FastAPI GET endpoint that returns a list of items. This demonstrates the simplest usage of the @app.get() decorator with just a path parameter.

```APIDOC
## GET /items/

### Description
Retrieve a list of items from the API.

### Method
GET

### Endpoint
/items/

### Response
#### Success Response (200)
- **name** (string) - The name of the item

#### Response Example
[
  {"name": "Empanada"},
  {"name": "Arepa"}
]
```

---

### Full FastAPI application preview

Source: https://fastapi.tiangolo.com/how-to/separate-openapi-schemas?q=

A complete example showing the Item model used in both POST and GET endpoints.

```Python
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None


app = FastAPI()


@app.post("/items/")
def create_item(item: Item):
    return item


@app.get("/items/")
def read_items() -> list[Item]:
    return [
        Item(
            name="Portal Gun",
            description="Device to travel through the multi-rick-verse",
        ),
        Item(name="Plumbus"),
    ]

```

---

### GET /

Source: https://fastapi.tiangolo.com/tutorial/cors

This endpoint serves as a basic example within a FastAPI application configured with `CORSMiddleware`. It demonstrates a simple GET request that returns a "Hello World" message, subject to the configured CORS policies.

```APIDOC
## GET /

### Description
This is a simple example endpoint demonstrating a basic FastAPI route. When configured with `CORSMiddleware`, this endpoint will respond to GET requests from allowed origins, returning a greeting message.

### Method
GET

### Endpoint
/

### Parameters
#### Path Parameters
(None)

#### Query Parameters
(None)

#### Request Body
(None)

### Request Example
(None)

### Response
#### Success Response (200)
- **message** (string) - A greeting message.

#### Response Example
{
  "message": "Hello World"
}
```

---

### Create a minimal FastAPI application

Source: https://fastapi.tiangolo.com/tutorial/first-steps

Basic FastAPI app with a single GET endpoint. Save this as main.py and run with 'fastapi dev' to start the development server.

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

---

### Install Python Package Dependencies with pip

Source: https://fastapi.tiangolo.com/deployment/docker

Command to install all packages listed in `requirements.txt` using pip, including example output.

```bash
pip install -r requirements.txt
fast →pip install -r requirements.txtSuccessfully installed fastapi pydantic

restart ↻

```

---

### Example URL for multiple query parameters

Source: https://fastapi.tiangolo.com/tutorial/query-params-str-validations

An example URL demonstrating how to pass multiple values for the same query parameter 'q'.

```URL
http://localhost:8000/items/?q=foo&q=bar
```

---

### Install specific package version with pip

Source: https://fastapi.tiangolo.com/virtual-environments

Install a specific version of a package using pip with version pinning syntax. This example shows installing harry version 1, which is needed for the philosophers-stone project.

```bash
pip install "harry==1"
```

---

### Serve documentation with live-reloading

Source: https://fastapi.tiangolo.com/contributing?q=

Builds the site and watches for changes, serving it at http://127.0.0.1:8008. This allows for real-time previewing of documentation edits.

```bash
python ./scripts/docs.py live
fast →python ./scripts/docs.py live
[INFO] Serving on http://127.0.0.1:8008
[INFO] Start watching changes
[INFO] Start detecting changes

restart ↻
```

---

### GET /items/

Source: https://fastapi.tiangolo.com/reference/fastapi

Retrieve a list of items using the FastAPI GET decorator. This example demonstrates a basic path operation returning a list of objects.

```APIDOC
## GET /items/\n\n### Description\nAdd a path operation using an HTTP GET operation to retrieve a list of items.\n\n### Method\nGET\n\n### Endpoint\n/items/\n\n### Parameters\n#### Path Parameters\n- None\n\n### Request Example\nGET /items/\n\n### Response\n#### Success Response (200)\n- **items** (array) - A list of item objects containing names.\n\n#### Response Example\n[\n  {\n    \"name\": \"Empanada\"\n  },\n  {\n    \"name\": \"Arepa\"\n  }\n]
```

---

### Security setup and utility functions

Source: https://fastapi.tiangolo.com/advanced/security/oauth2-scopes?q=

Initialize password hashing, OAuth2 schemes, and core authentication logic.

```python
password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

---

### Install packages from requirements.txt

Source: https://fastapi.tiangolo.com/virtual-environments

Install all project dependencies listed in a requirements.txt file using pip or uv.

```bash
pip install -r requirements.txt
fast →pip install -r requirements.txt
restart ↻
```

```bash
uv pip install -r requirements.txt
fast →uv pip install -r requirements.txt████████████████████████████████████████ 100%
restart ↻
```

---

### Start multiple Uvicorn workers with fastapi command

Source: https://fastapi.tiangolo.com/deployment/server-workers

Use the fastapi run command with --workers flag to start multiple worker processes. This example starts 4 worker processes to handle requests in parallel.

```bash
fastapi run --workers 4 main.py
```

---

### TrustedHostMiddleware **init** Implementation

Source: https://fastapi.tiangolo.com/reference/middleware

Full initialization method that validates host patterns, enforces wildcard constraints, and sets instance attributes. Patterns starting with '_' must be in the form '_.domain' and wildcards are only allowed at the start.

```python
def __init__(
    self,
    app: ASGIApp,
    allowed_hosts: Sequence[str] | None = None,
    www_redirect: bool = True,
) -> None:
    if allowed_hosts is None:
        allowed_hosts = ["*"]

    for pattern in allowed_hosts:
        assert "*" not in pattern[1:], ENFORCE_DOMAIN_WILDCARD
        if pattern.startswith("*") and pattern != "*":
            assert pattern.startswith("*."), ENFORCE_DOMAIN_WILDCARD
    self.app = app
    self.allowed_hosts = list(allowed_hosts)
    self.allow_any = "*" in allowed_hosts
    self.www_redirect = www_redirect
```

---

### Create a Project Directory Structure

Source: https://fastapi.tiangolo.com/virtual-environments

This snippet demonstrates how to set up a basic directory structure for a new Python project using command-line commands.

```bash
cd
mkdir code
cd code
mkdir awesome-project
cd awesome-project
```

---

### Install Uvicorn with standard dependencies

Source: https://fastapi.tiangolo.com/deployment/manually

Use the standard tag to include recommended extras like uvloop for a performance boost.

```bash
pip install "uvicorn[standard]"
fast →pip install "uvicorn[standard]"

restart ↻
```

---

### Install different package version with pip

Source: https://fastapi.tiangolo.com/virtual-environments

Install a different version of the same package to update dependencies. This example shows upgrading harry to version 3 for the prisoner-of-azkaban project.

```bash
pip install "harry==3"
```

---

### GET /items/ - Define a GET Path Operation

Source: https://fastapi.tiangolo.com/zh-hant/reference/fastapi_q=

The GET decorator adds a path operation using an HTTP GET request. It allows you to retrieve data from your API with full control over response models, status codes, and OpenAPI documentation. This example demonstrates a basic GET endpoint that returns a list of items.

````APIDOC
## GET Path Operation

### Description
Add a path operation using an HTTP GET operation to retrieve data from your API.

### Method
GET

### Parameters
#### Configuration Parameters
- **path** (str) - Required - The URL path for this path operation
- **response_model** (type) - Optional - The response model to be used for this path operation
- **status_code** (int) - Optional - The HTTP status code for successful responses
- **tags** (list[str]) - Optional - Tags for grouping operations in OpenAPI documentation
- **dependencies** (list) - Optional - List of dependencies for this path operation
- **summary** (str) - Optional - Summary for this path operation
- **description** (str) - Optional - Description for this path operation
- **response_description** (str) - Optional - Description of the response
- **responses** (dict) - Optional - Additional response documentation
- **deprecated** (bool) - Optional - Mark this operation as deprecated
- **operation_id** (str) - Optional - Custom operation ID for OpenAPI
- **response_model_include** (set) - Optional - Fields to include in response
- **response_model_exclude** (set) - Optional - Fields to exclude from response
- **response_model_by_alias** (bool) - Optional - Use field aliases in response (default: True)
- **response_model_exclude_unset** (bool) - Optional - Exclude unset fields (default: False)
- **response_model_exclude_defaults** (bool) - Optional - Exclude default values (default: False)
- **response_model_exclude_none** (bool) - Optional - Exclude None values (default: False)
- **include_in_schema** (bool) - Optional - Include in OpenAPI schema (default: True)
- **response_class** (type[Response]) - Optional - Custom response class (default: JSONResponse)
- **name** (str) - Optional - Name for this path operation
- **callbacks** (list[BaseRoute]) - Optional - List of OpenAPI callbacks
- **openapi_extra** (dict) - Optional - Extra metadata for OpenAPI schema
- **generate_unique_id_function** (Callable) - Optional - Custom function to generate unique IDs

### Request Example
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
def read_items():
    return [{"name": "Empanada"}, {"name": "Arepa"}]
````

### Response

#### Success Response (200)

- **items** (array) - List of items returned from the endpoint

#### Response Example

```json
[{ "name": "Empanada" }, { "name": "Arepa" }]
```

````

--------------------------------

### Install Development Requirements with uv

Source: https://fastapi.tiangolo.com/contributing

Use `uv sync --extra all` to install all project dependencies and the local FastAPI in editable mode, enabling direct testing of changes.

```bash
uv sync --extra all
````

---

### GET /items/{item_id} Example with Path Validation

Source: https://fastapi.tiangolo.com/reference/parameters?q=

An example of a FastAPI path operation that uses `fastapi.Path` to define and validate an integer path parameter `item_id`, including adding a title for documentation.

````APIDOC
## GET /items/{item_id}

### Description
Retrieves an item by its ID, demonstrating the use of `fastapi.Path` to add metadata to a path parameter.

### Method
GET

### Endpoint
/items/{item_id}

### Parameters
#### Path Parameters
- **item_id** (int) - Required - The ID of the item to get. Defined using `Path(title="The ID of the item to get")`.

### Response
#### Success Response (200)
- **item_id** (int) - The ID of the retrieved item.

#### Response Example
```json
{
  "item_id": 123
}
````

````

--------------------------------

### Run FastAPI development server

Source: https://fastapi.tiangolo.com/tutorial/security/first-steps

Start the application to access the interactive documentation and test the OAuth2 password flow.

```bash
fastapi dev
fast →fastapi dev
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

restart ↻


````

---

### Example URL for query parameters with default values

Source: https://fastapi.tiangolo.com/tutorial/query-params-str-validations

An example URL demonstrating how to access the endpoint without providing 'q' parameters, triggering the default list values.

```URL
http://localhost:8000/items/
```

---

### GET /items/{item_id}

Source: https://fastapi.tiangolo.com/zh-hant/reference/parameters

An example endpoint demonstrating how to use fastapi.Path to validate and document a path parameter.

```APIDOC
## GET /items/{item_id}

### Description
Retrieve an item by its unique ID. This endpoint uses the Path class to provide a human-readable title for the item_id parameter.

### Method
GET

### Endpoint
/items/{item_id}

### Parameters
#### Path Parameters
- **item_id** (int) - Required - The ID of the item to get.

### Request Example
GET /items/5

### Response
#### Success Response (200)
- **item_id** (int) - The ID of the item returned.

#### Response Example
{
  "item_id": 5
}
```

---

### GET /users/me/items/

Source: https://fastapi.tiangolo.com/zh-hant/reference/dependencies?q=

Example endpoint that uses the Security dependency to require specific OAuth2 scopes for access.

```APIDOC
## GET /users/me/items/\n\n### Description\nRetrieve items belonging to the current authenticated user, requiring 'items' scope.\n\n### Method\nGET\n\n### Endpoint\n/users/me/items/\n\n### Parameters\n#### Path Parameters\n- None\n\n#### Query Parameters\n- None\n\n#### Request Body\n- None\n\n### Request Example\nGET /users/me/items/\n\n### Response\n#### Success Response (200)\n- **item_id** (string) - The unique identifier for the item.\n- **owner** (string) - The username of the item owner.\n\n#### Response Example\n[\n  {\n    "item_id": "Foo",\n    "owner": "username"\n  }\n]
```

---

### Install FastAPI with uv

Source: https://fastapi.tiangolo.com/virtual-environments?q=

Install FastAPI with standard extras using uv package manager. Run this once in an activated virtual environment.

```bash
uv pip install "fastapi[standard]"
```

---

### Serve Documentation with Live Reload (Python Script)

Source: https://fastapi.tiangolo.com/contributing

Use the `python ./scripts/docs.py live` command to serve the documentation locally with live-reloading enabled, accessible at `http://127.0.0.1:8008`.

```bash
python ./scripts/docs.py live
```

---

### GET /items/

Source: https://fastapi.tiangolo.com/reference/security

An example endpoint demonstrating the use of APIKeyCookie to extract and validate a session key from request cookies.

```APIDOC
## GET /items/

### Description
Retrieves items while requiring a valid session API key provided via a cookie.

### Method
GET

### Endpoint
/items/

### Parameters
#### Cookie Parameters
- **session** (str) - Required - The API key value passed in the cookie named 'session'.

### Request Example
GET /items/ HTTP/1.1
Cookie: session=secret_session_id

### Response
#### Success Response (200)
- **session** (str) - The value of the session key extracted from the cookie.

#### Response Example
{
  "session": "secret_session_id"
}
```

---

### Example requirements.txt content

Source: https://fastapi.tiangolo.com/virtual-environments

A sample requirements.txt file specifying package versions for FastAPI and Pydantic.

```text
fastapi[standard]==0.113.0
pydantic==2.8.0

```

---

### Password Hashing Setup in Python

Source: https://fastapi.tiangolo.com/advanced/security/oauth2-scopes

Initializes a password hasher using `PasswordHash.recommended()` and generates a dummy hash for comparison with non-existent users to prevent timing attacks.

```python
password_hash = PasswordHash.recommended()
```

```python
DUMMY_HASH = password_hash.hash("dummypassword")
```

---

### GET /heroes/

Source: https://fastapi.tiangolo.com/tutorial/sql-databases?q=

Retrieves a list of all heroes, with optional pagination parameters to control the number of results and starting offset.

```APIDOC
## GET /heroes/

### Description
Retrieves a list of all heroes, with optional pagination parameters to control the number of results and starting offset.

### Method
GET

### Endpoint
/heroes/

### Parameters
#### Query Parameters
- **offset** (integer) - Optional - The number of items to skip before starting to collect the result set. Default is 0.
- **limit** (integer) - Optional - The maximum number of items to return. Default is 100, maximum allowed is 100.

### Request Example
(No request body)

### Response
#### Success Response (200)
- An array of Hero objects.
  - Each Hero object contains:
    - **id** (integer) - The unique identifier of the hero.
    - **name** (string) - The hero's public name.
    - **age** (integer) - The hero's age.
    - **secret_name** (string) - The hero's secret identity name.

#### Response Example
[
  {
    "name": "Deadpond",
    "secret_name": "Dive Wilson",
    "age": 30,
    "id": 1
  },
  {
    "name": "Spider-Boy",
    "secret_name": "Pedro Parqueador",
    "id": 2
  }
]
```

---

### Serve FastAPI Documentation Manually with MkDocs

Source: https://fastapi.tiangolo.com/zh-hant/contributing

Manually serve the documentation using `mkdocs` from within the documentation directory. This command starts a development server on the specified address and port.

```bash
mkdocs serve --dev-addr 127.0.0.1:8008
```

---

### Initial Setup for OAuth2 Scopes in FastAPI

Source: https://fastapi.tiangolo.com/advanced/security/oauth2-scopes?q=

This snippet shows the necessary imports and initial setup for integrating OAuth2 scopes with FastAPI's security features, building upon existing OAuth2 password and JWT token examples.

```python
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel, ValidationError

# to get a string like this run:

```

---

### FastAPI Application Initialization Details

Source: https://fastapi.tiangolo.com/zh-hant/reference/fastapi

Shows internal setup for exception handlers, user middleware, and the ASGI middleware stack during FastAPI application initialization.

```python
self.exception_handlers.setdefault(
        WebSocketRequestValidationError,
        websocket_request_validation_exception_handler,  # type: ignore[arg-type]  # ty: ignore[unused-ignore-comment]
    )  # ty: ignore[no-matching-overload]

    self.user_middleware: list[Middleware] = (
        [] if middleware is None else list(middleware)
    )
    self.middleware_stack: ASGIApp | None = None
    self.setup()
```

---

### GET /items/

Source: https://fastapi.tiangolo.com/zh-hant/reference/status?q=

An example endpoint demonstrating how to return a custom HTTP status code using the FastAPI status module.

```APIDOC
## GET /items/

### Description
An example endpoint that returns a list of items with a specific HTTP 418 (I'm a Teapot) status code.

### Method
GET

### Endpoint
/items/

### Parameters
None

### Request Example
GET /items/

### Response
#### Success Response (418)
- **items** (array) - A list of item objects.

#### Response Example
[
  {
    "name": "Plumbus"
  },
  {
    "name": "Portal Gun"
  }
]
```

---

### GET /items/

Source: https://fastapi.tiangolo.com/reference/dependencies?q=

An example endpoint demonstrating how to use fastapi.Depends to inject common query parameters into a path operation function.

```APIDOC
## GET /items/

### Description
Retrieves a list of items using common query parameters (q, skip, limit) provided by a dependency function.

### Method
GET

### Endpoint
/items/

### Parameters
#### Query Parameters
- **q** (string | null) - Optional - A search query string. Default: null.
- **skip** (integer) - Optional - The number of items to skip. Default: 0.
- **limit** (integer) - Optional - The maximum number of items to return. Default: 100.

### Request Example
GET /items/?q=foo&skip=0&limit=10

### Response
#### Success Response (200)
- **q** (string | null) - The query string provided.
- **skip** (integer) - The skip value used.
- **limit** (integer) - The limit value used.

#### Response Example
{
  "q": "foo",
  "skip": 0,
  "limit": 10
}
```

---

### Serve Documentation Manually with MkDocs

Source: https://fastapi.tiangolo.com/contributing

Serve the documentation locally using `mkdocs serve` on address `127.0.0.1:8008` after navigating to the documentation directory.

```bash
$ mkdocs serve --dev-addr 127.0.0.1:8008
```

---

### Navigate to Documentation Directory

Source: https://fastapi.tiangolo.com/contributing

Change the current directory to the English documentation folder to prepare for manual `mkdocs` commands.

```bash
$ cd docs/en/
```

---

### Run FastAPI Example with Uvicorn Development Server

Source: https://fastapi.tiangolo.com/contributing

Start a FastAPI example application using the development server. Uvicorn runs on port 8000 by default, allowing documentation on port 8008 to run simultaneously without port conflicts.

```bash
fastapi dev tutorial001.py
```

```bash
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

### GET /items/

Source: https://fastapi.tiangolo.com/zh-hant/reference/dependencies?q=

An example endpoint demonstrating how to use the Depends function to inject common query parameters into a path operation function.

```APIDOC
## GET /items/

### Description
Read items using common parameters (q, skip, limit) provided by a dependency function.

### Method
GET

### Endpoint
/items/

### Parameters
#### Query Parameters
- **q** (str | None) - Optional - A search query string.
- **skip** (int) - Optional - The number of items to skip for pagination. Default: 0.
- **limit** (int) - Optional - The maximum number of items to return. Default: 100.

### Request Example
GET /items/?q=example&skip=0&limit=10

### Response
#### Success Response (200)
- **q** (str | None) - The query string provided.
- **skip** (int) - The skip value used.
- **limit** (int) - The limit value used.

### Response Example
{
  "q": "example",
  "skip": 0,
  "limit": 10
}
```

---

### Example PATH Variable on Windows Before Activation

Source: https://fastapi.tiangolo.com/virtual-environments?q=

Shows the default PATH environment variable structure on Windows before virtual environment activation.

```powershell
C:\Windows\System32
```

---

### Initialize GZipMiddleware

Source: https://fastapi.tiangolo.com/reference/middleware

Initializes the GZip middleware with the ASGI application, a minimum size for compression, and the compression level.

```python
GZipMiddleware(app, minimum_size=500, compresslevel=9)
```

```python
def __init__(self, app: ASGIApp, minimum_size: int = 500, compresslevel: int = 9) -> None:
    self.app = app
    self.minimum_size = minimum_size
    self.compresslevel = compresslevel
```

---

### GET /items/

Source: https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration

Retrieves a list of items. This example demonstrates how to add a custom OpenAPI extension (`x-aperture-labs-portal`) to a path operation, which will appear in the generated OpenAPI schema and API documentation.

````APIDOC
## GET /items/

### Description
Retrieves a list of items. This example demonstrates how to add a custom OpenAPI extension (`x-aperture-labs-portal`) to a path operation, which will appear in the generated OpenAPI schema and API documentation.

### Method
GET

### Endpoint
/items/

### Response
#### Success Response (200)
- **item_id** (string) - The ID of the item.

#### Response Example
```json
[
  {
    "item_id": "portal-gun"
  }
]
````

````

--------------------------------

### Install development dependencies with uv

Source: https://fastapi.tiangolo.com/contributing?q=

Creates a virtual environment and installs FastAPI in editable mode with all extras. This ensures local changes are reflected immediately.

```bash
uv sync --extra all
fast →uv sync --extra all
██████████ 25%
````

---

### OPTIONS /items/ - Get Item Options

Source: https://fastapi.tiangolo.com/reference/apirouter?q=

Example endpoint demonstrating the OPTIONS HTTP method using FastAPI's APIRouter. This endpoint returns a list of available additions for items.

````APIDOC
## OPTIONS /items/

### Description
Returns a list of available additions for items using the OPTIONS HTTP method.

### Method
OPTIONS

### Endpoint
/items/

### Response
#### Success Response (200)
- **additions** (list[str]) - List of available item additions

#### Response Example
{
  "additions": ["Aji", "Guacamole"]
}

### Implementation Example
```python
from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()

@router.options("/items/")
def get_item_options():
    return {"additions": ["Aji", "Guacamole"]}

app.include_router(router)
````

````

--------------------------------

### Example PATH Variable on Linux and macOS Before Activation

Source: https://fastapi.tiangolo.com/virtual-environments?q=

Shows the default PATH environment variable structure on Unix-like systems before virtual environment activation.

```bash
/usr/bin:/bin:/usr/sbin:/sbin
````

---

### APIRouter Basic Usage

Source: https://fastapi.tiangolo.com/reference/apirouter?q=

Demonstrates how to create an APIRouter instance, define path operations on it, and include it in a FastAPI application. This example shows a simple GET endpoint that returns a list of users.

````APIDOC
## APIRouter Basic Usage

### Description
Creates an APIRouter instance with a GET endpoint and includes it in the main FastAPI application.

### Example Code
```python
from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

app.include_router(router)
````

### Usage

1. Import APIRouter and FastAPI
2. Create a FastAPI application instance
3. Create an APIRouter instance
4. Define path operations using the router decorator
5. Include the router in the main application using include_router()

````

--------------------------------

### Install FastAPI with standard dependencies

Source: https://fastapi.tiangolo.com/tutorial

Install FastAPI along with recommended optional dependencies like the FastAPI CLI and Uvicorn.

```shell
pip install "fastapi[standard]"
fast →pip install "fastapi[standard]"

restart ↻
````

---

### Test FastAPI WebSockets with TestClient

Source: https://fastapi.tiangolo.com/advanced/testing-websockets

This example defines a FastAPI application with a GET endpoint and a WebSocket endpoint, then shows how to test both using the TestClient, including establishing a WebSocket connection and receiving messages.

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()


def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}

```

---

### Navigate to Project Directory

Source: https://fastapi.tiangolo.com/virtual-environments

Change to the project directory using the cd command. This is the first step before managing virtual environments.

```bash
cd ~/code/prisoner-of-azkaban
```
