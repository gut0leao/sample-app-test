# Sample application

A small Java 17 Maven project for learning binary artifact management,
dependency analysis and software composition analysis (SCA).

**Contains intentionally vulnerable dependencies. Do not use in production.**

## Modules and runtime dependencies

```text
sample-parent (1.0.0)
├── sample-logging
│   └── log4j-core:2.14.1 (direct)
│       └── log4j-api:2.14.1 (transitive)
└── sample-app
    └── sample-logging:1.0.0 (direct)
        └── log4j-core:2.14.1 (transitive)
            └── log4j-api:2.14.1 (transitive)
```

`sample-app/pom.xml` declares only `sample-logging`. JUnit is inherited for tests
and is excluded from runtime JARs. The app logs a fixed greeting and exits.
It has no network services, endpoints or exploit code and ignores arguments.

## Build and run

Requires JDK 17, Maven 3.8.6+ and Python 3 for artifact verification.

```sh
mvn clean install
python3 scripts/verify-artifacts.py
java -jar sample-app/target/sample-app-1.0.0-all.jar
```

Output: `Hello from sample-app!`

The build generates conventional JARs in each module's `target/` directory and
an executable Fat JAR with the `all` classifier. The verifier copies the three
JARs, parent/module POMs and checksums to `dist/`.

The Fat JAR keeps dependency classes, `META-INF/maven/**/pom.xml` and
`pom.properties`, service descriptors, licenses and notices. Dependencies are
neither relocated nor minimized. Conventional JARs contain only their module's
code and resources; use the Fat JAR for a standalone run.

## Dependency tree

After `mvn clean install`:

```sh
mvn dependency:tree
mvn -pl sample-app dependency:tree -Dscope=runtime
```

## Downloads and release

- [Release v1.0.0](https://github.com/gut0leao/sample-app-test/releases/tag/v1.0.0)
- [Application JAR](https://github.com/gut0leao/sample-app-test/releases/download/v1.0.0/sample-app-1.0.0.jar)
- [Logging JAR](https://github.com/gut0leao/sample-app-test/releases/download/v1.0.0/sample-logging-1.0.0.jar)
- [Executable Fat JAR](https://github.com/gut0leao/sample-app-test/releases/download/v1.0.0/sample-app-1.0.0-all.jar)

Release assets also include `sample-parent-1.0.0.pom`, `sample-app-1.0.0.pom`,
`sample-logging-1.0.0.pom` and `SHA256SUMS`. Download links work after publication.
Verify downloaded files with `sha256sum --check SHA256SUMS`.

The workflow builds, tests and verifies JAR metadata on pushes and pull requests.
To publish the initial release, commit and push this project to the repository,
then push its tag:

```sh
git tag v1.0.0
git push origin v1.0.0
```

The tag workflow publishes the assets using the release notes in
`.github/release-notes/v1.0.0.md`, then downloads them and checks their hashes.
The repository must allow GitHub Actions to write release contents.

## Known vulnerabilities

Log4j Core 2.14.1 is deliberately included to make **CVE-2021-44228 (Log4Shell)**
visible through transitive dependency and binary analysis. Other expected
findings include CVE-2021-45046, CVE-2021-45105 and CVE-2021-44832.
See the [Log4j security advisories](https://logging.apache.org/security.html).
Findings depend on the scanner database and configuration; the list is not exhaustive.
The presence of a vulnerable component does not establish runtime exploitability.

## License

Original code uses the [MIT License](LICENSE). Bundled dependencies retain their
own licenses; Log4j uses the Apache License 2.0.
