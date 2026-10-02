# URL Shortener

A small URL-shortening service built primarily as a **coding refresher project**.

The goal is not to build the most feature-rich or production-ready URL shortener. The goal is to rebuild confidence in writing code, reading documentation, making design decisions, debugging, and solving problems without relying on AI-generated implementations.

## Stack

* **Python**
* **FastAPI**
* **SQLite** initially
* **pytest** for testing
* Git for version control

Keep the stack intentionally small. Add dependencies only when there is a clear reason.

---

## Ground Rules

### 1. Write the implementation yourself

Do not ask AI to generate the implementation.

You may use:

* Official documentation
* Search engines
* Stack Overflow / GitHub issues
* Error messages and tracebacks
* AI for explanations or code review

Avoid:

> "Build this feature for me."

Prefer:

> "Explain how FastAPI handles dependency injection."

or:

> "Review this code for bugs and edge cases. Don't rewrite it."

### 2. Don't over-engineer

Start with:

```text
HTTP API
   ↓
Application logic
   ↓
SQLite
```

Don't introduce Redis, PostgreSQL, Docker, message queues, authentication, Kubernetes, etc. until the basic application works.

### 3. Understand everything you commit

If you cannot explain a piece of code, don't keep it just because it works.

---

# Initial Requirements

Build a service with the following endpoints.

### Create short URL

```http
POST /shorten
```

Request:

```json
{
  "url": "https://example.com/some/long/url"
}
```

Response should contain the generated short URL/code.

---

### Redirect

```http
GET /{short_code}
```

The service should redirect the client to the original URL.

Example:

```text
GET /a8Kx2

302 Found
Location: https://example.com/some/long/url
```

---

### Delete

```http
DELETE /{short_code}
```

Delete the corresponding shortened URL.

---

# Minimum Data Model

A shortened URL should contain at least:

```text
id
short_code
original_url
created_at
```

You may decide what additional fields are useful.

Think about:

* Which fields should be unique?
* Which fields should be indexed?
* What happens if two requests generate the same short code?
* Should deleting a nonexistent URL return an error?

---

# Suggested Development Order

Don't implement everything at once.

### Phase 1 — HTTP

Get FastAPI running.

Implement:

```text
POST /shorten
GET /{short_code}
```

Use an in-memory dictionary initially.

---

### Phase 2 — Persistence

Replace the dictionary with SQLite.

Learn enough SQL to implement the required operations yourself.

---

### Phase 3 — Validation & Errors

Handle things such as:

* malformed URLs
* nonexistent short codes
* duplicate short codes
* invalid request bodies
* empty values

Decide what HTTP status codes make sense.

---

### Phase 4 — Tests

Write tests for:

* creating a URL
* redirecting
* deleting
* nonexistent short codes
* invalid URLs
* collision handling

Try to find bugs **before** asking AI to review the code.

---

### Phase 5 — Improvements

Only after the basic version is working, consider:

* URL expiration
* custom aliases
* click counts
* rate limiting
* PostgreSQL
* Redis caching
* authentication
* metrics/logging

Each addition should answer a specific engineering question.

---

# Questions You Should Answer Yourself

Before looking for an implementation, try to reason about these.

### Short-code generation

* Random string or deterministic encoding?
* How long should the code be?
* Which characters are allowed?
* How likely are collisions?
* What happens when a collision occurs?

### Database

* What should be the primary key?
* Should `short_code` have a unique constraint?
* Which columns need indexes?
* What happens if two requests create the same code simultaneously?

### HTTP

* Should redirect use `301`, `302`, `303`, or `307`?
* What status code should an invalid URL produce?
* What should happen when a short code doesn't exist?

### Security

* What makes a URL "valid"?
* Can someone use your service for phishing?
* Could an attacker abuse the redirect endpoint?
* Should there be rate limiting?

You don't need perfect answers initially.

The point is to **think about the problem before searching for the answer**.

---

# Definition of Done — V1

V1 is finished when:

* [ ] The service starts locally.
* [ ] A URL can be shortened.
* [ ] A short code is generated.
* [ ] The short code resolves to the original URL.
* [ ] URLs survive application restarts.
* [ ] Invalid requests are handled.
* [ ] Missing short codes are handled.
* [ ] Short-code collisions are handled.
* [ ] Basic tests exist.
* [ ] You can explain the implementation without referring to AI.

---

# Suggested Project Structure

Don't treat this as mandatory.

Start simple and let the structure evolve.

```text
url-shortener/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   └── ...
│
├── tests/
│   └── ...
│
├── README.md
├── pyproject.toml
└── .gitignore
```

If you find yourself creating 25 files for a tiny application, that's probably a sign to stop and reconsider.

---

# AI Usage Policy

AI is allowed, but it should function as a **teacher/reviewer**, not as the programmer.

### Good uses

```text
"Explain this Python error."

"Explain how FastAPI dependency injection works."

"What edge cases should I consider for this API?"

"Review this function for bugs. Don't rewrite it."

"Explain the difference between 301 and 302."
```

### Avoid

```text
"Implement this endpoint."

"Write the database layer."

"Fix this entire project."

"Generate the tests."

"Build the whole application."
```

If you get stuck, first spend some time debugging yourself.

The objective is not to avoid documentation.

The objective is to avoid **outsourcing your thinking**.

---

# Reference

Use these when you need specific information. Don't waste hours trying to rediscover basic framework/API details from random blog posts.

## Python

**Python documentation**

https://docs.python.org/3/

Use for:

* language syntax
* standard library
* exceptions
* typing
* `datetime`
* `secrets`
* `urllib`
* file handling

---

## FastAPI

**FastAPI documentation**

https://fastapi.tiangolo.com/

Use for:

* routing
* request/response models
* validation
* dependency injection
* status codes
* middleware
* testing
* application structure

---

## Pydantic

**Pydantic documentation**

https://docs.pydantic.dev/

Use for:

* request validation
* response models
* type-based validation
* serialization

---

## SQLite

**SQLite documentation**

https://sqlite.org/docs.html

Use for:

* SQL syntax
* tables
* indexes
* constraints
* transactions
* concurrency
* SQLite-specific behavior

### SQL reference

https://sqlite.org/lang.html

---

## HTTP

**MDN — HTTP**

https://developer.mozilla.org/en-US/docs/Web/HTTP

Use for:

* HTTP methods
* status codes
* headers
* redirects
* caching
* requests/responses

This should be your first stop when you're unsure about HTTP behavior.

---

## HTTP Status Codes

**MDN — HTTP response status codes**

https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status

Useful when you're wondering:

> "What status code should I return here?"

---

## URL Syntax

**WHATWG URL Standard**

https://url.spec.whatwg.org/

Use when dealing with:

* URL parsing
* URL components
* schemes
* hosts
* ports
* paths
* query strings

Don't invent your own URL parser.

---

## Python URL Handling

**Python `urllib.parse`**

https://docs.python.org/3/library/urllib.parse.html

Useful when you need to parse or inspect URLs in Python.

---

## Testing

**pytest documentation**

https://docs.pytest.org/

Use for:

* writing tests
* fixtures
* parametrization
* assertions
* test organization

---

## Git

**Git documentation**

https://git-scm.com/doc

Useful when you forget:

```text
branch
commit
rebase
stash
reset
revert
```

---

# When You're Stuck

Use this order:

```text
1. Read the error message
        ↓
2. Inspect your code
        ↓
3. Check the official documentation
        ↓
4. Search for the specific problem
        ↓
5. Try a small experiment
        ↓
6. Ask AI for an explanation
```

Don't spend 3 hours trying to remember the exact syntax for something that takes 30 seconds to look up.

The goal is to **practice programming**, not practice memorizing documentation.

---

# Stretch Goal

Once V1 is complete, stop and write down:

> "How would I design this if I had 100 million URLs and 50,000 redirects per second?"

Don't implement it immediately.

Draw the architecture first.

Think about:

```text
Load Balancer
      ↓
API Servers
      ↓
Cache ─────── Database
      ↓
 Redirect
```

Then investigate which parts of that design are actually necessary and why.

That's where this small project can turn into a useful system-design exercise.
