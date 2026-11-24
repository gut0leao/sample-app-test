"""Check release JAR contents and stage the JARs and original Maven POMs."""

import hashlib
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
NS = {"m": "http://maven.apache.org/POM/4.0.0"}
parent = ET.parse(ROOT / "pom.xml").getroot()
version = parent.findtext("m:version", namespaces=NS)
app = ET.parse(ROOT / "sample-app/pom.xml").getroot()
logging = ET.parse(ROOT / "sample-logging/pom.xml").getroot()
deps = app.findall("m:dependencies/m:dependency", NS)
assert [d.findtext("m:artifactId", namespaces=NS) for d in deps] == ["sample-logging"]
core = logging.find("m:dependencies/m:dependency", NS)
assert core.findtext("m:artifactId", namespaces=NS) == "log4j-core"
assert core.findtext("m:version", namespaces=NS) == "2.14.1"

fat = ROOT / f"sample-app/target/sample-app-{version}-all.jar"
coordinates = [
    ("io.github.gut0leao", "sample-app", version),
    ("io.github.gut0leao", "sample-logging", version),
    ("org.apache.logging.log4j", "log4j-core", "2.14.1"),
    ("org.apache.logging.log4j", "log4j-api", "2.14.1"),
]
with ZipFile(fat) as jar:
    for group, artifact, expected_version in coordinates:
        prefix = f"META-INF/maven/{group}/{artifact}"
        properties = jar.read(f"{prefix}/pom.properties").decode()
        assert f"version={expected_version}" in properties, prefix
        metadata = ET.fromstring(jar.read(f"{prefix}/pom.xml"))
        assert metadata.findtext("m:artifactId", namespaces=NS) == artifact
    for entry in (
        "io/github/gut0leao/sample/app/Main.class",
        "io/github/gut0leao/sample/logging/SampleLogger.class",
    ):
        assert int.from_bytes(jar.read(entry)[6:8], "big") == 61, entry
    assert "org/apache/logging/log4j/core/LoggerContext.class" in jar.namelist()
    assert "org/apache/logging/log4j/LogManager.class" in jar.namelist()
    assert "META-INF/org/apache/logging/log4j/core/config/plugins/Log4j2Plugins.dat" in jar.namelist()
    assert "META-INF/LICENSE" in jar.namelist()
    assert "META-INF/NOTICE" in jar.namelist()
    assert "Main-Class: io.github.gut0leao.sample.app.Main" in jar.read("META-INF/MANIFEST.MF").decode()

dist = ROOT / "dist"
if dist.exists():
    shutil.rmtree(dist)
dist.mkdir()
for module in ("sample-app", "sample-logging"):
    thin = ROOT / module / "target" / f"{module}-{version}.jar"
    with ZipFile(thin) as jar:
        assert not any(n.startswith("org/apache/logging/log4j/") for n in jar.namelist())
    shutil.copy2(thin, dist / thin.name)
    shutil.copy2(ROOT / module / "pom.xml", dist / f"{module}-{version}.pom")
shutil.copy2(ROOT / "pom.xml", dist / f"sample-parent-{version}.pom")
shutil.copy2(fat, dist / fat.name)
with (dist / "SHA256SUMS").open("w") as sums:
    for path in sorted(dist.iterdir()):
        if path.name != "SHA256SUMS":
            sums.write(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n")
print(f"Verified Java 17 classes, thin JARs, dependency metadata and {len(list(dist.iterdir()))} release assets.")
