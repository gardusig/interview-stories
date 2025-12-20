# Orkes: Conductor (Workflow Orchestration Platform)

## Unblocking Enterprise Adoption by Delivering a Go SDK from Scratch

**Context**  
A large enterprise prospect evaluating Orkes required a **Go SDK as a hard prerequisite** to proceed with adoption. At the time, Conductor officially supported only Java and Python SDKs, making Go support a **deal-blocking gap**.

**Goal**  
Unblock the customer evaluation within **~4 weeks** by delivering a stable Go SDK with core functionality, while designing a path to a **fully production-grade SDK within ~3 months**.

**Approach**  
- Volunteered to own the Go SDK end-to-end despite limited prior Go experience.
- Defined and executed a **phased delivery plan**:
  - **Phase 1 (≈1 month):**
    - Core workflow and task APIs
    - Authentication and configuration
    - Basic error handling and retries
    - Stability sufficient for customer evaluation
  - **Phase 2 (≈3 months):**
    - Expanded API surface to match existing SDKs
    - Improved ergonomics and retries
    - Documentation and examples
    - Long-term maintainability and versioning
- Analyzed existing **Java and Python SDKs** to extract shared abstractions, error semantics, and API consistency.
- Ramped up in Go by building focused prototypes and adopting **Go-native idioms** instead of performing a direct port.
- Designed a **stable public interface** with explicit versioning and backward compatibility guarantees.
- Worked directly with the customer during Phase 1, incorporating real usage feedback into API design.
- Coordinated closely with the core platform team to validate backend compatibility as SDK coverage expanded.

**Outcome**  
- Delivered a functional Go SDK within **~4 weeks**, unblocking the enterprise evaluation.
- Completed a **production-ready Go SDK within ~3 months**, covering the majority of platform APIs.
- The customer signed on, directly contributing to revenue.
- The Go SDK became an **official, supported integration** and a foundation for future customers.
- Demonstrated incremental delivery under customer pressure without sacrificing long-term SDK quality.

---

## Scaling from One SDK to a Cross-Language SDK Ecosystem

**Context**  
As Orkes grew, enterprise customers required SDK support across multiple languages. The platform scaled from **1 SDK to 5 (Java, Python, Go, C#, JavaScript)**, but development, testing, and releases were largely **manual, inconsistent, and error-prone**.

**Goal**  
Take ownership of the SDK ecosystem to:
- Maintain **feature parity** across languages  
- Improve adoption and usability  
- Optimize performance where relevant  
- Eliminate manual friction in testing and releases  

**Approach**  
- Standardized SDK architecture using **Swagger/OpenAPI–generated code** as a shared baseline.
- Layered **language-specific customizations** to preserve idiomatic usage, annotations, concurrency models, and ergonomics.
- Coordinated development across languages to keep APIs and behavior consistent despite runtime differences.
- Designed and implemented a **unified CI/CD pipeline** that:
  - Automatically ran unit and integration tests
  - Built SDK artifacts
  - Published releases to package managers (e.g., PyPI, npm) on merge to main
- Improved developer experience with **Dockerized local workflows** and predictable tooling, enabling rapid context-switching across SDKs.

**Outcome**  
- Scaled from **1 → 5 production SDKs** without increasing operational overhead.
- Release cycles became **fully automated**, significantly reducing manual errors and release latency.
- SDKs transitioned from a scaling bottleneck to a **repeatable, maintainable platform capability**.
- Customers onboarded more easily across diverse tech stacks, increasing platform adoption.

---

## Improving Python SDK Throughput with Data-Driven Concurrency Decisions

**Context**  
High-volume customers using the Python SDK experienced throughput limitations under load. An initial proposal focused on **multithreading with a single polling loop**, primarily optimizing I/O-bound behavior.

**Goal**  
Maximize throughput for both **I/O- and CPU-heavy workflows** while preserving correctness and operational safety.

**Approach**  
- Proposed an alternative design based on **multiprocessing with batch polling** to:
  - Bypass Python’s GIL for CPU-bound workloads
  - Reduce polling overhead by processing tasks in batches
- Built a proof of concept and ran load tests comparing:
  - Multithreading + single poll
  - Multiprocessing + batch poll
- During testing, detected anomalous behavior: queue size remained constant despite active workers.
- Investigated beyond the SDK layer and identified a **server-side bug**: missing acknowledgment logic caused batch-polled tasks to be requeued indefinitely.
- Validated the root cause with the backend team.
- Contributed a fix **upstream to Netflix OSS**, where the behavior originated.

**Outcome**  
- Team aligned on **multiprocessing + batch polling**, backed by benchmark data.
- Achieved **~20% throughput improvement** in high-volume workflows.
- Prevented a latent production issue where queues could silently grow under load.
- Open-source contribution was accepted, reducing long-term maintenance risk.

---

## Reducing SDK Onboarding Friction Through Code-Driven Documentation

**Context**  
Despite functional SDKs, support tickets and customer feedback consistently pointed to **confusing onboarding and unclear usage patterns**, increasing support load and slowing adoption.

**Goal**  
Reduce customer friction and support volume by making SDK onboarding intuitive and consistent across languages.

**Approach**  
- Reviewed support tickets, customer feedback, and recurring questions to identify common pain points.
- Proposed a **code-first documentation model**, prioritizing real, working examples over abstract explanations.
- Reused **integration and end-to-end tests** as the source of truth for documentation examples.
- Created **side-by-side, multi-language snippets** to help users map concepts across SDKs.
- Collaborated with the tech writing team to restructure documentation for clarity and consistency.
- Iterated continuously based on customer and internal feedback.

**Outcome**  
- SDK-related onboarding and usage tickets dropped by **~75%**.
- Customers onboarded faster with fewer clarification cycles.
- Engineering time spent on repetitive support questions was significantly reduced.
- Documentation became a trusted reference for both customers and internal engineers.
