# Practical Task 2: Technical Research Report

This document presents independent research findings covering core web services concepts: the Python `requests` HTTP library, the comparison between JSON and XML data exchange formats, and the architectural principles governing RESTful APIs.

---

## 1. Python `requests` Module

### 1.1 What is the `requests` Library?
The `requests` module is an open-source, third-party HTTP client library for Python created by Kenneth Reitz, designed under the philosophy of "HTTP for Humans." It abstracts the cumbersome low-level network mechanics of sending HTTP/1.1 requests across the internet, providing a clean, elegant, and Pythonic API for consuming external web APIs, querying websites, and transmitting payload data.

### 1.2 Why `requests` is Favored Over Built-in Standard Libraries (e.g., `urllib`)
Python ships with built-in networking modules such as `urllib.request` and `urllib.parse`. While these standard library modules require no external installation, developers almost universally favor `requests` for the following reasons:
1. **Simplified API Syntax**: With `urllib`, making an authenticated POST request with URL-encoded query parameters and custom headers often requires ten or more lines of boilerplate, manually constructing request objects, opening URL openers, and managing byte conversions. With `requests`, the identical operation is achieved in a single readable line (`requests.post(url, json=data, headers=headers)`).
2. **Automatic Decoding and JSON Parsing**: `urllib` returns raw bytes that require manual character decoding (such as `.decode('utf-8')`) before parsing. `requests` automatically detects character encoding and exposes a built-in `.json()` helper method that deserializes responses directly into native Python dictionaries and lists.
3. **Session Persistence and Connection Pooling**: The `requests.Session` class automatically handles connection reuse via `urllib3`, keeps TCP connections alive, and preserves cookies across successive requests—features that require significant custom coding in standard `urllib`.
4. **Intuitive Form and Query Parameter Handling**: In `urllib`, developers must manually import `urllib.parse.urlencode()` and convert query parameters into ASCII strings. `requests` accepts native Python dictionaries passed to the `params` (for URL query strings) or `data`/`json` (for request bodies) arguments.

### 1.3 Primary HTTP Methods in `requests`
The `requests` module provides direct helper functions mapped to standard HTTP verbs:
- **`GET` (`requests.get(url, params=...)`)**: Used to read or retrieve data from a resource without modifying server state.
- **`POST` (`requests.post(url, json=...)`)**: Used to submit new data payloads to the server, commonly used to create new database records or submit form data.
- **`PUT` (`requests.put(url, json=...)`)**: Used to replace or update an existing resource in its entirety with a newly supplied representation.
- **`DELETE` (`requests.delete(url)`)**: Used to instruct the server to remove an identified resource.

### 1.4 Code Example: Performing a GET Request and Parsing JSON Response
The following snippet demonstrates querying a public API endpoint, checking for HTTP errors, and extracting data from the returned JSON payload:

```python
import requests

def fetch_sample_post():
    # Target REST API endpoint
    url = "https://jsonplaceholder.typicode.com/posts/1"

    try:
        # Perform HTTP GET request with a 5-second timeout
        response = requests.get(url, timeout=5)

        # Raise an HTTPError if the response status code was 4xx or 5xx
        response.raise_for_status()

        # Parse response body as JSON directly into a Python dictionary
        post_data = response.json()

        # Display extracted fields
        print(f"Status Code : {response.status_code}")
        print(f"Post Title  : {post_data.get('title')}")
        print(f"User ID     : {post_data.get('userId')}")
        print(f"Body Text   : {post_data.get('body')}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected networking error occurred: {err}")

if __name__ == "__main__":
    fetch_sample_post()
```

---

## 2. JSON and XML Data Formats

### 2.1 Definitions and Primary Use Cases

#### JavaScript Object Notation (JSON)
JSON is a lightweight, text-based data interchange format derived from the object literal syntax of JavaScript. Despite its origins, JSON is language-agnostic and relies on two universal data structures: collections of name/value pairs (analogous to Python dictionaries, hash tables, or structs) and ordered lists of values (analogous to arrays or lists).
- **Primary Use Cases**: Web service communication, client-server data transfer in Single Page Applications (SPAs) and mobile apps, configuration files (e.g., `package.json`, `tsconfig.json`), and document-oriented NoSQL databases (e.g., MongoDB, CouchDB).

#### Extensible Markup Language (XML)
XML is a standardized, text-based markup language developed by the World Wide Web Consortium (W3C). It uses customizable start and end tags enclosed in angle brackets (`<tag>value</tag>`) alongside element attributes to define hierarchical data structures.
- **Primary Use Cases**: Enterprise legacy software integration, SOAP-based web services, document formatting standards (such as Microsoft Office `.docx` and `.xlsx` schemas), RSS/Atom feeds, Android layout definitions, and complex transactional systems requiring rigorous mathematical schema validation (XSD).

---

### 2.2 JSON: Advantages and Disadvantages

#### Advantages of JSON:
1. **Lightweight and Bandwidth-Efficient**: JSON syntax lacks redundant closing tags (relying instead on concise braces `{}` and brackets `[]`), leading to significantly smaller payload sizes and lower network transmission latency.
2. **Native Parsing in Web Browsers**: Because JSON is syntactically a subset of JavaScript, web browsers can parse and serialize it natively at high hardware speeds via `JSON.parse()` and `JSON.stringify()`.
3. **Natural Mapping to Modern Data Structures**: JSON data translates directly into native objects, lists, strings, booleans, and numbers across virtually all programming languages (e.g., Python `dict` and `list`), eliminating the need for complex object-relational mapping logic.
4. **High Human Readability**: Clean formatting and clear key-value relationships make JSON documents simple for engineers and API consumers to read, debug, and construct manually.

#### Disadvantages of JSON:
1. **Lack of Native Comments**: The official JSON standard deliberately forbids comments, making it less than ideal for heavily documented configuration files where developers need to annotate options.
2. **Limited Primitive Data Types**: JSON supports only strings, numbers, booleans, null, arrays, and objects. It does not provide built-in native support for dates, timestamps, binary data, or complex geometric types, requiring workarounds like ISO-8601 strings.
3. **No Native Schema Validation**: Unlike XML which natively pairs with XSD schemas, JSON relies on third-party frameworks (such as JSON Schema) for structural validation, which are less universally integrated into older enterprise tooling.
4. **No Support for Attributes or Mixed Content**: JSON properties must map to strict keys and values, making it unsuited for formatting human-written markup documents containing mixed inline tags (such as rich text paragraphs with embedded links or italic words).

---

### 2.3 XML: Advantages and Disadvantages

#### Advantages of XML:
1. **Rigorous Structural Validation (XSD / DTD)**: XML can be strictly verified against an XML Schema Definition (XSD), ensuring that an incoming message adheres to exact constraints on node sequence, child counts, data types, and value patterns before application logic runs.
2. **Support for Namespaces**: XML allows XML Namespaces (`xmlns`), enabling multiple distinct vocabularies or schemas to coexist within the same XML document without tag name collisions.
3. **Support for Attributes and Metadata**: Elements can contain both text contents and multiple metadata attributes (e.g., `<price currency="EUR" tax="included">19.99</price>`), providing flexible ways to distinguish payload data from descriptive metadata.
4. **Mixed Content Modeling**: XML excels at representing structured editorial text where tags are interwoven with natural language sentences (e.g., `<p>Hello <b>world</b>!</p>`), making it the premier format for technical publishing, legal documents, and digital typography.

#### Disadvantages of XML:
1. **High Overhead and Verbosity**: Every open tag requires a matching close tag (e.g., `<description>...</description>`), resulting in heavy payloads that consume significantly more network bandwidth than JSON.
2. **High Processing Overhead**: Parsing an XML Document Object Model (DOM) tree requires substantially more memory and CPU compute cycles compared to lightweight stream-based JSON parsers.
3. **Complex Query and Navigation APIs**: Extracting data from XML requires specialized querying tools like XPath or XSLT, which present a steep learning curve compared to straightforward JSON key navigation (`data['store']['name']`).
4. **Susceptibility to Security Vulnerabilities**: XML processors are historically vulnerable to specialized attacks such as XML External Entity (XXE) injection and Billion Laughs exponential entity expansion Denial-of-Service attacks, requiring careful parser hardening.

---

## 3. RESTful APIs

### 3.1 What is a RESTful API?
A RESTful API (Representational State Transfer) is an architectural style for designing networked web services, first formalized by Roy Fielding in his 2000 doctoral dissertation. Rather than treating remote communications as procedure calls executed across a network (as in RPC or SOAP), REST models the system as a collection of uniquely identified **resources** (such as `/products/`, `/users/42`, or `/orders/`). Clients interact with these resources by exchanging standard representations (most commonly JSON) using uniform, pre-existing HTTP operations.

### 3.2 Core Architectural Constraints of REST
To be classified as genuinely RESTful, a service must adhere to several fundamental architectural principles:
1. **Statelessness**: Every request sent from a client to the server must contain all the contextual information and authentication credentials necessary to understand and complete the request. The server never stores client session state between requests; session state resides entirely on the client side.
2. **Client-Server Separation**: The user interface concerns (the client) are completely separated from data storage and business logic concerns (the server). This enables the frontend to evolve independently (such as adding mobile apps or desktop clients) without impacting backend database architecture.
3. **Uniform Interface**: All system components interact through a standardized contract. This includes:
   - Resource identification via stable URIs (e.g., `https://api.store.com/v1/products/5`).
   - Manipulation of resources through representations (e.g., sending a JSON payload to modify state).
   - Self-descriptive messages (using standard MIME types and headers).
   - Hypermedia as the Engine of Application State (HATEOAS), where responses include navigational links directing the client to related actions.
4. **Cacheability**: Responses must explicitly define whether they are cacheable or non-cacheable (via `Cache-Control` or `ETag` headers), enabling intermediate proxies and clients to reuse cached responses to reduce server load and latency.
5. **Layered System**: The client cannot tell whether it is connected directly to the end server or to an intermediate proxy, load balancer, cache layer, or security gateway.

### 3.3 HTTP Verbs and Standard Status Codes

#### HTTP Verbs (Actions on Resources):
- `GET`: Safe and idempotent read operation to retrieve resource state.
- `POST`: Non-idempotent operation used to create subordinate resources or initiate processing.
- `PUT`: Idempotent operation replacing an identified resource in its entirety.
- `PATCH`: Modifies specific fields of an existing resource without full replacement.
- `DELETE`: Idempotent operation removing an identified resource.

#### Standard Status Code Categories:
- **`200 OK`**: Standard success response for successful `GET`, `PUT`, or `PATCH`.
- **`201 Created`**: Returned after a successful `POST` that produced a new resource, typically accompanied by a `Location` header.
- **`204 No Content`**: Returned when an action succeeds but returns no message body (common for `DELETE`).
- **`400 Bad Request`**: Client submitted malformed syntax or failed input validation.
- **`401 Unauthorized`**: Authentication is required and has failed or was not provided.
- **`403 Forbidden`**: The client is authenticated but lacks permission for the resource.
- **`404 Not Found`**: The requested resource URI does not exist on the server.
- **`500 Internal Server Error`**: An unexpected generic server-side failure occurred.

---

### 3.4 Advantages and Disadvantages of RESTful APIs

#### Advantages of RESTful APIs:
1. **Scalability and High Performance**: Statelessness allows backend servers to scale horizontally with ease behind load balancers because any server instance can handle any incoming request without needing shared memory sessions.
2. **Simplicity and Broad Tooling**: Built directly upon open HTTP/1.1 and HTTP/2 standards, RESTful APIs leverage existing web infrastructure (caching servers, CDN edges, SSL/TLS security, standard browser debugging consoles, and command-line tools like `curl`).
3. **Platform and Language Agnosticism**: Clients and servers can be written in entirely different programming languages and frameworks (e.g., a React Native mobile frontend communicating with a Python Django backend) as long as they exchange agreed-upon JSON representations.
4. **Independent Evolution**: The strict separation of client presentation from backend domain logic allows development teams to overhaul user interfaces or rewrite database layers without breaking backwards compatibility, provided URIs and contracts remain stable.

#### Disadvantages of RESTful APIs:
1. **Over-fetching and Under-fetching**: REST endpoints return fixed data models. A client may receive unnecessary fields it does not need (over-fetching), or may need to issue multiple sequential round-trip requests (e.g., fetch user, then fetch orders, then fetch order items) to gather related data (under-fetching).
2. **Lack of Formal Machine Contracts**: Unlike SOAP (with WSDL) or gRPC (with Protocol Buffers), standard REST does not inherently enforce a machine-readable schema, requiring external frameworks like OpenAPI/Swagger to document endpoints and validate contracts.
3. **Stateless Overhead**: Because the server preserves no session context, every individual request must transmit authentication tokens (such as Bearer JWT headers) and contextual parameters, slightly increasing total network request overhead.
4. **Inefficiency for Real-Time Streaming**: REST is founded on a unidirectional request-response paradigm. It is poorly suited for bidirectional, real-time streaming communication (such as collaborative canvases or financial market tickers), where protocols like WebSockets or gRPC are vastly superior.

