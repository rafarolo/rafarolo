<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Rafael M. Rôlo — Specialist & Tech Lead, Capital Markets" src="assets/banner-light.svg">
</picture>

Twenty years on the JVM — sixteen in Java, four in Kotlin and Spring, six leading teams.
I work where a wrong number has a settlement date: custody positions, asset and liability
ledgers, regulatory reporting.

The two middle numbers up there are the job. 798 pull requests of my own, and 906 reviews
on other people's, across seventeen engineers. Reviewing isn't overhead stacked on top of
building — on a platform of forty-odd services it's most of how the thing stays coherent.
The rest of the work is choosing between two defensible answers and making that choice
cheap to change later.

## Selected work

**Passwordless database access** — Entra ID workload identities across production services,
on both SQL Server and Postgres. The identity belongs to the workload rather than a person,
which is what makes it revocable, and `CREATE USER` has to go by object ID, not by name.

**Asset and liability through one contract** — both sides answer from a single endpoint, so
the shape of the answer stops depending on who asked for it.

**A staging database worth trusting** — production-to-staging copy with deterministic PII
masking applied at the source, plus an automated schema-drift gate across 170+ tables.

**Deploy provenance** — in a pipeline where the deploy leaves the pull request before the
merge does, a workflow run's `headSha` is not what reached production. Most of the value is
knowing where to read what did.

**Settlement dates that agree** — one B3 date field carrying five different names across
five systems, and deciding which of them a public API is allowed to answer with.

**Coverage as a constraint, not a report** — core service from 74.7% to 88%, holding zero
bugs and zero vulnerabilities along the way.

## Stack

Kotlin and Java on Spring Boot · Postgres, SQL Server, Cosmos DB · Azure with Pulumi, AKS
and GitHub Actions · Airflow for ingestion · Prometheus, Grafana and SonarQube

---

[LinkedIn](https://linkedin.com/in/rafarolo) · [Stack Exchange](https://stackexchange.com/users/7394006/)

*To an artificial mind, all reality is [virtual](https://1drv.ms/v/s!AsFSV30GJkPCiK9v6BW51rsUyXCeVA?s=256&g=1).* ☄️
