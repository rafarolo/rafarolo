<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg?v=8db893c5b">
  <img alt="Rafael Rôlo — Specialist & Tech Lead, Capital Markets. 17 years on the JVM, 964 pull requests, 963 code reviews, 5 sectors served." src="assets/banner-light.svg?v=63c58326b">
</picture>

<br>
<br>

- I build the platform behind **R$130B+ in issued assets** — 40-odd services, Kotlin and Spring on Azure
- I led its move off Python, JavaScript and TypeScript onto **Kotlin and hexagonal architecture**
- I review as much as I write: **963 reviews against 964 pull requests of my own**, for 17 engineers
- Sectors served: **capital markets · banking · insurance · government · e-commerce**

All of it in private corporate repositories, which is why the contribution graph below is
green and unclickable.

<br>

### Pull requests per year

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/prs-dark.svg?v=d9a5261cb">
  <img alt="Pull requests per year: 158 authored and 201 reviewed in 2023, 173 and 221 in 2024, 217 and 278 in 2025, 416 and 263 in 2026 to 4 October." src="assets/prs-light.svg?v=3c983315b">
</picture>

<br>


<br>

### Selected work

| | Period&nbsp;&nbsp;&nbsp;&nbsp; | Delivery | What it involved |
|:-:|---|---|---|
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/tl-0-dark.svg?v=aca01a77b"><img src="assets/tl-0-light.svg?v=87693279b" width="20" height="20" alt=""></picture> | `2025‑2026` | **OpenSec, an API for partners** | 22 endpoints across 8 service families · documentation kits built by an automated pipeline |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/tl-1-dark.svg?v=7e9340c5b"><img src="assets/tl-1-light.svg?v=cb069ce3b" width="20" height="20" alt=""></picture> | `2023‑2026` | **New cluster, new region, one pipeline** | every application rewritten into a single GitHub Actions pipeline · Azure subscription and AKS migration |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/tl-2-dark.svg?v=f9373953b"><img src="assets/tl-2-light.svg?v=ede0eaa4b" width="20" height="20" alt=""></picture> | `2023‑2026` | **Passwordless, and routes that stay inside** | Entra ID workload identities on SQL Server and Postgres · service-to-service traffic on cluster-internal DNS |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/tl-3-dark.svg?v=23648e36b"><img src="assets/tl-3-light.svg?v=78c76e11b" width="20" height="20" alt=""></picture> | `2023‑2026` | **Kotlin as the platform language** | off Python, JavaScript and TypeScript · hexagonal architecture · R$130B+ in issued assets |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/tl-4-dark.svg?v=2a0103fbb"><img src="assets/tl-4-light.svg?v=6149f9c4b" width="20" height="20" alt=""></picture> | `2021‑2023` | **Open Banking, certified** | every BACEN and FEBRABAN phase through Raidiam conformance · insurance home in a 22M-customer bank app |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/tl-5-dark.svg?v=f95f0155b"><img src="assets/tl-5-light.svg?v=139f5d1ab" width="20" height="20" alt=""></picture> | `2020‑2021` | **Claims analytics on GCP** | predictive engine for suspicious claims at a 7M-client insurer, beside a COBOL/CICS core |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/tl-6-dark.svg?v=2b30283cb"><img src="assets/tl-6-light.svg?v=0831e5a6b" width="20" height="20" alt=""></picture> | `2019‑2020` | **WebSphere to Kubernetes** | retail insurance systems onto Liberty on IBM Cloud Private, OpenShift pipeline |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/tl-7-dark.svg?v=699d8679b"><img src="assets/tl-7-light.svg?v=05dec4f7b" width="20" height="20" alt=""></picture> | `2014‑2015` | **A study area, ten times faster** | found the data bottleneck in a geomarketing platform's core calculation |

<br>

### Worked examples

Three of the things above, extracted and made runnable. Each takes a handful of failures
that give no error at all, and proves every one with a test that counts what actually
happened.

| | |
|---|---|
| [**spring-boot-azure-passwordless**](https://github.com/rafarolo/spring-boot-azure-passwordless) | The token is the password and it expires under the pool. `CREATE USER` goes by object ID, and the SID is not the object ID with the dashes removed. |
| [**spring-boot-cache-patterns**](https://github.com/rafarolo/spring-boot-cache-patterns) | A cached method called from inside its own bean is not cached. Concurrent misses on one key all compute. A cache that is not working does not throw. |
| [**spring-boot-messaging-outbox**](https://github.com/rafarolo/spring-boot-messaging-outbox) | Publishing from the service body is wrong in both orderings. At-least-once is the contract, not a caveat. A poison record blocks a partition, not a topic. |

Spring Boot 4.1, Kotlin, Java 21. Tests that need Docker skip locally and run in CI.

<br>


<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/dot-dark.svg?v=d2cd0a46b">
  <img alt="" src="assets/dot-light.svg?v=4aa80b41b">
</picture>

<br>

### Stack

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/radar-dark.svg?v=5c8316ecb">
  <img alt="Radar comparing depth in years against share of the last twelve months of pull requests, across backend, security, cloud, observability and data." src="assets/radar-light.svg?v=c83944a2b">
</picture>

<br>

#### Main stack today

| | |
|---|---|
| **Cloud** | `Azure` `AKS` `Docker` `Pulumi` `GitHub Actions` |
| **Language** | `Kotlin 2.2` `Java 21` |
| **Framework** | `Spring Boot 3.5` · Cloud, Data, Security, Cache, Retry, Circuit Breaker, AOP, Actuator |
| **Security** | `OAuth2` `OpenID Connect` `JWT` `Keycloak` `Entra ID` |
| **Data** | `PostgreSQL` `SQL Server` `MongoDB` `Cosmos DB` |
| **Observability** | `Grafana` `Prometheus` `OpenTelemetry` |
| **APIs** | `OpenAPI` `GraphQL` |

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/tenure-dark.svg?v=5afe24afb">
  <img alt="Years with each technology, longest first: 17 Java; 14 PostgreSQL; 12 MongoDB; 11 Spring Boot and SQL Server; 7 Spring Security, OpenAPI, Kubernetes, Docker and SonarQube; 5 AWS, Prometheus and Grafana; 3 Kotlin, Azure, Pulumi, GitHub Actions, Cosmos DB, GraphQL and OpenTelemetry; 2 Airflow and Spring AI; 1 GCP." src="assets/tenure-light.svg?v=edb93425b">
</picture>

<details>
<summary>Years as text</summary>

| Years | Technology |
|---|---|
| `17` | `Java` |
| `14` | `PostgreSQL` |
| `12` | `MongoDB` |
| `11` | `Spring Boot` `SQL Server` |
| `7` | `Spring Security` `OpenAPI` `Kubernetes` `Docker` `SonarQube` |
| `5` | `AWS` `Prometheus` `Grafana` |
| `3` | `Kotlin` `Azure` `Pulumi` `GitHub Actions` `Cosmos DB` `GraphQL` `OpenTelemetry` |
| `2` | `Airflow` `Spring AI` |
| `1` | `GCP` |

`OAuth2` `OpenID Connect` `JWT` `Keycloak` `Entra ID` `FAPI` `Workload Identity`

</details>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/dot-dark.svg?v=d2cd0a46b">
  <img alt="" src="assets/dot-light.svg?v=4aa80b41b">
</picture>

<br>

### Artifact of my life

`my.life:rafael.rolo`, laid out the way I'd lay out a service<br>
Domain at the core, stack as adapters, because the stack is the part that gets replaced.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/archetype-dark.svg?v=fa1740d6b">
  <img alt="A package tree under life, the source root of my.life:rafael.rolo. Under professional: domain, which does not get replaced; practice; and adapters, swappable on purpose. Under person: languages, education, published work." src="assets/archetype-light.svg?v=41ffb582b">
</picture>

<br>
<br>

<p align="center">
  <a href="https://linkedin.com/in/rafarolo"><img src="assets/linkedin.svg?v=0186622ab" alt="LinkedIn: rafarolo" height="28"></a>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://stackexchange.com/users/7394006/"><img src="assets/stackexchange.svg?v=0d65e882b" alt="Stack Exchange profile" height="28"></a>
</p>

<p align="center">
  <img src="assets/location.svg?v=a7d87508b" alt="São Paulo, Brasil" height="28">
</p>


<a href="https://1drv.ms/v/s!AsFSV30GJkPCiK9v6BW51rsUyXCeVA?s=256&g=1">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/skyline-dark.svg?v=5341acbdb">
    <img alt="To an artificial mind, all reality is virtual — a city skyline at dusk." src="assets/skyline-light.svg?v=f78de6bcb">
  </picture>
</a>
