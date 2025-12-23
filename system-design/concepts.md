- [1. API Design](#1-api-design)
  - [REST vs gRPC vs WebSocket](#rest-vs-grpc-vs-websocket)
  - [Idempotency](#idempotency)
  - [Versioning Strategies](#versioning-strategies)
  - [Pagination](#pagination)
  - [HTTP Error Handling](#http-error-handling)
  - [HTTP Parameters](#http-parameters)
- [2. SQL vs NoSQL Tradeoffs](#2-sql-vs-nosql-tradeoffs)
  - [SQL Databases](#sql-databases)
  - [Use SQL when:](#use-sql-when)
  - [Indexes in SQL Databases](#indexes-in-sql-databases)
  - [SQL rule:](#sql-rule)
  - [NoSQL Databases](#nosql-databases)
  - [Use NoSQL when:](#use-nosql-when)
  - [Indexes in NoSQL Databases](#indexes-in-nosql-databases)
  - [Tradeoffs in NoSQL Indexes](#tradeoffs-in-nosql-indexes)
  - [NoSQL Rule](#nosql-rule)
- [3. Concurrency](#3-concurrency)
  - [Race Conditions](#race-conditions)
  - [Locking Strategies](#locking-strategies)
    - [Optimistic Locking](#optimistic-locking)
    - [Pessimistic Locking](#pessimistic-locking)
- [4. Caching](#4-caching)
  - [What to Cache?](#what-to-cache)
  - [Where to Cache?](#where-to-cache)
  - [Cache Invalidation](#cache-invalidation)
  - [Failure Modes](#failure-modes)
  - [Caching Patterns](#caching-patterns)
  - [Key Concepts](#key-concepts)
- [5. Async Processing \& Messaging](#5-async-processing--messaging)
  - [Delivery Semantics](#delivery-semantics)
  - [Idempotent Consumers](#idempotent-consumers)
  - [Other Concepts](#other-concepts)
- [6. Horizontal Scaling](#6-horizontal-scaling)
  - [Core Techniques](#core-techniques)
  - [Bottlenecks](#bottlenecks)
  - [Tradeoffs](#tradeoffs)
- [7. Failure Handling \& Reliability](#7-failure-handling--reliability)
- [8. Observability](#8-observability)
  - [Signals](#signals)
  - [Correlation IDs](#correlation-ids)
  - [SLIs / SLOs](#slis--slos)

## 1. API Design

### REST vs gRPC vs WebSocket

* **REST**
  * Human-readable, easy debugging (curl, browser)
  * Works naturally over HTTP
  * Flexible but weaker contracts
    * Enforced via documentation / OpenAPI, not at the protocol level
* **gRPC**
  * Strong contracts via protobuf
  * Lower latency, smaller payloads
  * Built-in streaming
  * Harder to debug, limited native browser support
* **WebSockets**
  * Persistent, bidirectional connection
  * Server can push updates (no polling)
  * Low latency for real-time data
  * Harder to scale (stateful connections)

**Rule of thumb**:
- REST → public/external request–response APIs  
- gRPC → internal service-to-service communication  
- WebSockets → real-time client updates

---

### Idempotency

* An operation is **idempotent** if repeating it produces the same result.
* Required for safe retries under failures.

**Examples**:

* `PUT /trips/{id}` → idempotent
* `POST /trips` → not idempotent by default

---

### Versioning Strategies

* **URI-based**: `/v1/trips`
* **Header-based**: `Accept-Version: v1`

**Tradeoff**:

* URI-based is explicit and easy
* Header-based keeps URLs clean but harder to debug

---

### Pagination

Pagination is used to return large datasets in smaller, manageable chunks while maintaining performance and correctness.

* **Offset-based pagination**: `?offset=100&limit=20`
  * Uses row offsets to skip records
  * Easy to implement and understand
  * Performance degrades for large offsets (DB must scan/skips rows)
  * Results become inconsistent when rows are inserted or deleted

  **Example issue**:
  - Page 1 returns items 1–20
  - A new item is inserted at the top
  - Page 2 now skips or duplicates items

* **Cursor-based pagination**: `?cursor=abc123`
  * Uses a stable cursor (e.g. last seen ID or timestamp)
  * Maintains consistent ordering across pages
  * Efficient for large datasets
  * Requires a well-defined sort key (ID, timestamp)

  **Example**:
  - `GET /trips?after=trip_123&limit=20`
  - Returns trips created after `trip_123`

**Preferred for production**: Cursor-based pagination, especially for high-traffic or frequently updated datasets.

---

### HTTP Error Handling

* Use meaningful HTTP status codes to clearly communicate failure types

  * `400` Bad Request — invalid or malformed input
  * `401` Unauthorized — missing or invalid authentication token
  * `403` Forbidden — authenticated but not allowed to perform the operation
  * `404` Not Found — resource does not exist
  * `409` Conflict — request conflicts with current state
  * `500` Internal Server Error — unexpected server failure

---

### HTTP Parameters

* **Path params** → resource identity
  * `/trips/{tripId}`
* **Query params** → filtering, sorting, pagination
  * `?status=active&limit=20`
* **Headers** → metadata
  * Auth tokens
  * Trace IDs
  * Idempotency keys

---

## 2. SQL vs NoSQL Tradeoffs

### SQL Databases

* **Strong consistency**
  * Reads always reflect the latest committed write.
  * Important when correctness matters more than latency (e.g. payments, balances).
* **ACID transactions**
  * **Atomicity** — all operations in a transaction succeed or none do.
    * Prevents partial updates (e.g. money debited but not credited).
  * **Consistency** — the database moves from one valid state to another.
    * Enforces constraints like foreign keys, uniqueness, and invariants.
  * **Isolation** — concurrent transactions do not interfere incorrectly.
    * Prevents issues like dirty reads and lost updates.
  * **Durability** — once a transaction commits, it will survive crashes.
    * Data is persisted to disk and recoverable after failures.
* **Joins and complex queries**
  * Supports relational queries across multiple tables.
  * Enables expressive querying without duplicating data.
* **Rigid schema**
  * Schema must be defined upfront and enforced by the database.
  * Prevents invalid data but makes schema evolution more expensive.
* **Typically vertical scaling**
  * Performance is often improved by scaling a single node (more CPU/RAM).
  * Horizontal scaling is possible but more complex (sharding, replicas).

### Use SQL when:

* Financial data
* Strong invariants
* Complex relationships

### Indexes in SQL Databases

An index is a **separate data structure** (usually a B-tree) that maps:

> column values → row locations

This allows the database to find data **without scanning the entire table**.

* Improve read performance by avoiding full table scans.
  * Example: querying trips by `rider_id` without an index requires scanning all trips.
  * With an index on `rider_id`, the database jumps directly to matching rows.
* Add overhead to writes.
  * Every insert, update, or delete must also update the index.
  * Example: adding an index on `status` means every trip status change updates both the table and the index.
* Consume additional storage.
  * Indexes store copies of key values and pointers to rows.
  * Multiple indexes can significantly increase storage costs.
* Flexible and ad-hoc.
  * Indexes can usually be added later.
  * Supports a wide variety of query patterns (filters, joins, sorting).

### SQL rule:
Index only what you query frequently.

* Good index: `GET /trips?driver_id=123&status=ACTIVE`
  → composite index on `(driver_id, status)`
* Bad index: fields rarely used in filters or sorting

---

### NoSQL Databases

* **Horizontal scaling**
  * Built to scale by adding more nodes rather than upgrading a single machine.
  * Data is automatically partitioned and distributed across nodes.
* **High write throughput**
  * Optimized for fast inserts and updates at scale.
  * Avoids costly joins and complex multi-row transactions.
* **Eventual consistency**
  * Writes propagate asynchronously to replicas.
  * Reads may temporarily return stale data, but the system converges over time.
* **Denormalized data model**
  * Data is intentionally duplicated to match query patterns.
  * Minimizes read-time computation and eliminates joins.

### Use NoSQL when:
* Very high traffic or unpredictable load
* Simple, well-defined access patterns
* Systems that can tolerate temporary inconsistency
* Real-time or large-scale workloads

### Indexes in NoSQL Databases

In NoSQL systems, indexes are **part of the data model**, not an afterthought.  
They must be designed **before data is written**, based on known access patterns.

* **Primary key**
  * Always exists and defines how data is physically stored.
  * Composed of a **partition key** and an optional **sort key**.
  * Determines:
    * Which node stores the data
    * How data is ordered within a partition
  * Optimized for direct key-based lookups and range queries.
  * **Example**:
    * `PK: user_id`
      > Fast lookup by user ID, but no support for other query patterns.
* **Secondary indexes**
  * Explicitly defined to support additional query patterns.
  * Internally behave like separate tables that replicate data.
  * Types:
    * **GSI (Global Secondary Index)** — different partition and/or sort keys
      * New partition key allowed
      * Queries across users/entities
      * Eventually consistent by default
    * **LSI (Local Secondary Index)** — same partition key, different sort key
      * Same partition key
      * Only different sorting
      * Strongly consistent reads supported
* **Base table**
  * Table: `Orders`
  * **Partition key (PK):** `user_id`
  * **Sort key (SK):** `order_id`
  * GSI **Partition key**: `status`
  * GSI **Sort key**: `created_at`

  Example item:
  ```json
  {
    "user_id": "u123",
    "order_id": "o987",
    "status": "SHIPPED",
    "created_at": "2025-01-10",
    "total": 150.00
  }
  ```

  Query:
  ```
  Get all SHIPPED orders sorted by creation date
  PK = "SHIPPED"
  SK begins with "2025-01"
  ```

### Tradeoffs in NoSQL Indexes
* Writes are more expensive (base table + indexes).
* Indexes consume additional throughput and storage.
* Queries are limited to predefined access patterns.
* Poor key design can cause hot partitions and throttling.

### NoSQL Rule
Model your data around queries.
Changing access patterns later is expensive and often requires data migration.

---

## 3. Concurrency

### Race Conditions

* Occur when multiple writers update shared state concurrently
* Leads to lost updates, double processing, or invalid states

**Example**: Two drivers accept the same ride at the same time → both think they won.

### Locking Strategies

---

#### Optimistic Locking
* Assumes conflicts are **rare**
* No lock upfront — detect conflicts at write time

**How it works**
* Attach a `version` / `etag` / `updated_at` field
* Update succeeds only if the version matches
* On conflict → retry or fail

**Example**
```sql
UPDATE rides
SET status = 'ASSIGNED', version = version + 1
WHERE ride_id = 42 AND version = 3;
```

**Pros**
* High throughput
* No blocking
* Scales well under low contention

**Cons**
* Retries under contention
* Clients must handle failures

#### Pessimistic Locking

* Assumes conflicts are **common**
* Lock resource before modifying it

**How it works**
* Acquire lock (row lock, mutex, distributed lock)
* Perform update
* Release lock

**Example**
```sql
SELECT * FROM rides
WHERE ride_id = 42
FOR UPDATE;

UPDATE rides
SET status = 'ASSIGNED', driver_id = 7
WHERE ride_id = 42 AND status = 'AVAILABLE';
```

**Pros**
* Strong consistency
* No retries needed

**Cons**
* Lower throughput
* Risk of deadlocks
* Harder to scale in distributed systems


## 4. Caching

### What to Cache?

* Read-heavy data
* Expensive computations
* Slowly changing data

---

### Where to Cache?

* Client-side (browser, mobile)
* CDN
* Application cache (Redis)
* Database cache

---

### Cache Invalidation

* TTL-based expiration
* Write-through invalidation
* Event-based invalidation

**Hard truth**: Cache invalidation is one of the hardest problems.

---

### Failure Modes

* Stale data
* Cache stampede
* Hot keys

---

### Caching Patterns

* **Cache-aside** (most common)
* Read-through
* Write-through
* Write-behind

---

### Key Concepts

* TTLs
* Cache stampede mitigation (locks, jitter)
* Hot key sharding
* Consistency tradeoffs

---

## 5. Async Processing & Messaging

### Delivery Semantics

* At-most-once
* At-least-once (most common)
* Exactly-once (rare, expensive)

---

### Idempotent Consumers

* Consumers must handle duplicate messages safely
* Use deduplication keys or conditional updates

---

### Other Concepts

* Dead-letter queues
* Ordering guarantees
* Partitioned consumers

**Rule**: Make consumers idempotent, not queues exactly-once.

---

## 6. Horizontal Scaling

### Core Techniques

* Stateless services
* Load balancers
* Sharding
* Partitioning strategies

---

### Bottlenecks

* Databases
* Hot partitions
* Central coordination points

---

### Tradeoffs

* More nodes → more coordination
* Sharding complicates queries
* Resharding is painful

---

## 7. Failure Handling & Reliability

* Retries with exponential backoff
* Timeouts everywhere
* Circuit breakers
* Graceful degradation

**Goal**: Fail fast and fail safely.

---

## 8. Observability

### Signals

* **Logs**: discrete events
* **Metrics**: aggregated numbers
* **Traces**: request flows

---

### Correlation IDs

* Propagate request IDs across services
* Required for debugging distributed systems

---

### SLIs / SLOs

* SLI: measurement (latency, error rate)
* SLO: target (99.9% availability)
