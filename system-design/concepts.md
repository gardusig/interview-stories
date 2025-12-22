- [API Design](#api-design)
  - [REST vs gRPC vs WebSocket](#rest-vs-grpc-vs-websocket)
  - [Idempotency](#idempotency)
  - [Versioning Strategies](#versioning-strategies)
  - [Pagination](#pagination)
  - [HTTP Error Handling](#http-error-handling)
  - [HTTP Parameters](#http-parameters)
- [SQL vs NoSQL Tradeoffs](#sql-vs-nosql-tradeoffs)
  - [SQL Databases](#sql-databases)
  - [NoSQL Databases](#nosql-databases)
  - [Keys \& Indexes](#keys--indexes)
- [Consistency \& Concurrency](#consistency--concurrency)
  - [Consistency Models](#consistency-models)
  - [Race Conditions](#race-conditions)
  - [Locking Strategies](#locking-strategies)
  - [Common Patterns](#common-patterns)
- [Caching](#caching)
  - [What to Cache?](#what-to-cache)
  - [Where to Cache?](#where-to-cache)
  - [Cache Invalidation](#cache-invalidation)
  - [Failure Modes](#failure-modes)
  - [Caching Patterns](#caching-patterns)
  - [Key Concepts](#key-concepts)
- [Async Processing \& Messaging](#async-processing--messaging)
  - [Delivery Semantics](#delivery-semantics)
  - [Idempotent Consumers](#idempotent-consumers)
  - [Other Concepts](#other-concepts)
- [Horizontal Scaling](#horizontal-scaling)
  - [Core Techniques](#core-techniques)
  - [Bottlenecks](#bottlenecks)
  - [Tradeoffs](#tradeoffs)
- [Failure Handling \& Reliability](#failure-handling--reliability)
- [Observability](#observability)
  - [Signals](#signals)
  - [Correlation IDs](#correlation-ids)
  - [SLIs / SLOs](#slis--slos)
- [Data Freshness \& Latency Tradeoffs](#data-freshness--latency-tradeoffs)
- [Security \& Abuse](#security--abuse)
  - [Core Concepts](#core-concepts)
  - [Common Problems](#common-problems)


## API Design

### REST vs gRPC vs WebSocket

* **REST**
  * Human-readable, easy debugging (curl, browser)
  * Works naturally over HTTP
  * Flexible but weaker contracts
* **gRPC**
  * Strong contracts via protobuf
  * Lower latency, smaller payloads
  * Built-in streaming
  * Harder to debug, limited browser support
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

## SQL vs NoSQL Tradeoffs

### SQL Databases

* Strong consistency
* ACID transactions
* Joins and complex queries
* Rigid schema
* Typically vertical scaling

**Use when**:

* Financial data
* Strong invariants
* Complex relationships

---

### NoSQL Databases

* Horizontal scaling
* High write throughput
* Eventual consistency
* Denormalized data

**Use when**:

* High traffic systems
* Simple access patterns
* Real-time or large-scale workloads

---

### Keys & Indexes

* **Primary key** → unique row identifier
* **Partition key** → determines data distribution
* **Sort key** → ordering within a partition

**Indexes**:

* Speed up reads
* Slow down writes
* Increase storage usage

**Rule**: Index only what you query frequently.

---

## Consistency & Concurrency

### Consistency Models

* **Strong consistency**: reads always see latest write
* **Eventual consistency**: replicas converge over time
* **Read-after-write consistency**: guarantees for same client

---

### Race Conditions

* Occur when multiple writers update shared state concurrently

**Example**: Two drivers accept the same ride simultaneously.

---

### Locking Strategies

* **Optimistic locking**

  * Version field
  * Retry on conflict
* **Pessimistic locking**

  * Lock resource before update
  * Lower throughput

---

### Common Patterns

* Compare-and-swap
* Conditional updates
* Version fields
* Idempotency keys

---

## Caching

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

## Async Processing & Messaging

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

## Horizontal Scaling

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

## Failure Handling & Reliability

* Retries with exponential backoff
* Timeouts everywhere
* Circuit breakers
* Graceful degradation

**Goal**: Fail fast and fail safely.

---

## Observability

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

---

## Data Freshness & Latency Tradeoffs

* **Real-time**: milliseconds (rides, payments)
* **Eventually consistent**: seconds to minutes
* **Approximate**: analytics, counters

**Tradeoff**: Freshness vs cost vs complexity.

---

## Security & Abuse

### Core Concepts

* Authentication & authorization
* Rate limiting
* Input validation
* PII handling

---

### Common Problems

* DDoS attacks
* Credential stuffing
* Abuse of free endpoints

**Mitigations**:

* Rate limits
* Quotas
* WAFs
* Auditing
