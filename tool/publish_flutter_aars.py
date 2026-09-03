# import glob
# import os
# import shutil
# import xml.etree.ElementTree as ET
#
#
# repository_root = os.path.dirname(
#     os.path.dirname(os.path.abspath(__file__))
# )
#
# generated_repository = os.path.join(
#     repository_root,
#     "build",
#     "host",
#     "outputs",
#     "repo",
# )
#
# github_group = os.environ.get(
#     "GROUP",
#     "com.github.DhruvPanchalSL",
# )
#
# repository_name = os.environ.get(
#     "ARTIFACT",
#     "jitlabtestingmodule",
# )
#
# release_version = os.environ.get(
#     "VERSION",
#     "1.0.0",
# )
#
# published_group = "{}.{}".format(
#     github_group,
#     repository_name,
# )
#
# source_repository = os.path.join(
#     generated_repository,
#     *published_group.split(".")
# )
#
# maven_repository_root = os.environ.get(
#     "MAVEN_LOCAL_REPOSITORY",
#     os.path.join(os.path.expanduser("~"), ".m2", "repository"),
# )
#
# maven_local = os.path.join(
#     maven_repository_root,
#     *published_group.split(".")
# )
#
# maven_namespace = "http://maven.apache.org/POM/4.0.0"
# ET.register_namespace("", maven_namespace)
#
# for artifact_name in ("flutter_debug", "flutter_release"):
#     artifact_root = os.path.join(source_repository, artifact_name)
#     aar_files = glob.glob(os.path.join(artifact_root, "*", "*.aar"))
#
#     if len(aar_files) != 1:
#         raise RuntimeError(
#             "Expected exactly one AAR for {}, found {}".format(
#                 artifact_name,
#                 len(aar_files),
#             )
#         )
#
#     source_aar = aar_files[0]
#     source_pom = os.path.splitext(source_aar)[0] + ".pom"
#
#     if not os.path.isfile(source_pom):
#         raise IOError("Missing POM: {}".format(source_pom))
#
#     destination = os.path.join(
#         maven_local,
#         artifact_name,
#         release_version,
#     )
#
#     if not os.path.isdir(destination):
#         os.makedirs(destination)
#
#     destination_aar = os.path.join(
#         destination,
#         "{}-{}.aar".format(artifact_name, release_version),
#     )
#
#     destination_pom = os.path.join(
#         destination,
#         "{}-{}.pom".format(artifact_name, release_version),
#     )
#
#     shutil.copy2(source_aar, destination_aar)
#
#     pom_tree = ET.parse(source_pom)
#     pom_root = pom_tree.getroot()
#
#     pom_root.find(
#         "{" + maven_namespace + "}groupId"
#     ).text = published_group
#
#     pom_root.find(
#         "{" + maven_namespace + "}artifactId"
#     ).text = artifact_name
#
#     pom_root.find(
#         "{" + maven_namespace + "}version"
#     ).text = release_version
#
#     pom_tree.write(
#         destination_pom,
#         encoding="utf-8",
#         xml_declaration=True,
#     )
#
#     print(
#         "Published {}:{}:{}".format(
#             published_group,
#             artifact_name,
#             release_version,
#         )
#     )
#
# # --- Aggregator POM for the bare repo coordinate (com.github.User:Repo:Version) ---
# # JitPack's multi-module docs describe generating a root artifact named after
# # the repo itself, separate from the individual module artifacts above. We
# # publish it manually here so JitPack's discovery step has something real to
# # find under the bare "com.github.User:Repo:Version" coordinate.
# aggregator_group = github_group  # e.g. com.github.DhruvPanchalSL (no repo suffix)
# aggregator_artifact = repository_name  # e.g. jitlabtestingmodule2
#
# aggregator_dir = os.path.join(
#     maven_repository_root,
#     *aggregator_group.split("."),
#     aggregator_artifact,
#     release_version,
# )
#
# if not os.path.isdir(aggregator_dir):
#     os.makedirs(aggregator_dir)
#
# aggregator_pom_path = os.path.join(
#     aggregator_dir,
#     "{}-{}.pom".format(aggregator_artifact, release_version),
# )
#
# dependency_xml = "".join(
#     """
#     <dependency>
#       <groupId>{group}</groupId>
#       <artifactId>{artifact}</artifactId>
#       <version>{version}</version>
#       <type>aar</type>
#     </dependency>""".format(
#         group=published_group,
#         artifact=module_name,
#         version=release_version,
#     )
#     for module_name in ("flutter_debug", "flutter_release")
# )
#
# aggregator_pom_xml = """<?xml version="1.0" encoding="UTF-8"?>
# <project xmlns="http://maven.apache.org/POM/4.0.0">
#   <modelVersion>4.0.0</modelVersion>
#   <groupId>{group}</groupId>
#   <artifactId>{artifact}</artifactId>
#   <version>{version}</version>
#   <packaging>pom</packaging>
#   <dependencies>{dependencies}
#   </dependencies>
# </project>
# """.format(
#     group=aggregator_group,
#     artifact=aggregator_artifact,
#     version=release_version,
#     dependencies=dependency_xml,
# )
#
# with open(aggregator_pom_path, "w", encoding="utf-8") as aggregator_file:
#     aggregator_file.write(aggregator_pom_xml)
#
# print("Published aggregator {}:{}:{}".format(
#     aggregator_group,
#     aggregator_artifact,
#     release_version,
# ))
#
# # Keep one canonical copy in ~/.m2 for JitPack's artifact discovery. The
# # project-directory Maven repository is generated and no longer needed here.
# shutil.rmtree(generated_repository)
# print("Removed temporary Flutter Maven repository: {}".format(
#     generated_repository,
# ))

import glob
import os
import shutil
import xml.etree.ElementTree as ET


repository_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

generated_repository = os.path.join(
    repository_root,
    "build",
    "host",
    "outputs",
    "repo",
)

github_group = os.environ.get(
    "GROUP",
    "com.github.DhruvPanchalSL",
)

repository_name = os.environ.get(
    "ARTIFACT",
    "jitlabtestingmodule",
)

# Always publish as 1.0 — see note in configure_flutter_aars.py. JitPack's
# discovery step for this project always expects 1.0, regardless of the
# actual git tag, so we match that here to keep publish location and
# discovery expectation aligned.
release_version = "1.0"

published_group = "{}.{}".format(
    github_group,
    repository_name,
)

source_repository = os.path.join(
    generated_repository,
    *published_group.split(".")
)

maven_repository_root = os.environ.get(
    "MAVEN_LOCAL_REPOSITORY",
    os.path.join(os.path.expanduser("~"), ".m2", "repository"),
)

maven_local = os.path.join(
    maven_repository_root,
    *published_group.split(".")
)

maven_namespace = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", maven_namespace)

for artifact_name in ("flutter_debug", "flutter_release"):
    artifact_root = os.path.join(source_repository, artifact_name)
    aar_files = glob.glob(os.path.join(artifact_root, "*", "*.aar"))

    if len(aar_files) != 1:
        raise RuntimeError(
            "Expected exactly one AAR for {}, found {}".format(
                artifact_name,
                len(aar_files),
            )
        )

    source_aar = aar_files[0]
    source_pom = os.path.splitext(source_aar)[0] + ".pom"

    if not os.path.isfile(source_pom):
        raise IOError("Missing POM: {}".format(source_pom))

    destination = os.path.join(
        maven_local,
        artifact_name,
        release_version,
    )

    if not os.path.isdir(destination):
        os.makedirs(destination)

    destination_aar = os.path.join(
        destination,
        "{}-{}.aar".format(artifact_name, release_version),
    )

    destination_pom = os.path.join(
        destination,
        "{}-{}.pom".format(artifact_name, release_version),
    )

    shutil.copy2(source_aar, destination_aar)

    pom_tree = ET.parse(source_pom)
    pom_root = pom_tree.getroot()

    pom_root.find(
        "{" + maven_namespace + "}groupId"
    ).text = published_group

    pom_root.find(
        "{" + maven_namespace + "}artifactId"
    ).text = artifact_name

    pom_root.find(
        "{" + maven_namespace + "}version"
    ).text = release_version

    pom_tree.write(
        destination_pom,
        encoding="utf-8",
        xml_declaration=True,
    )

    print(
        "Published {}:{}:{}".format(
            published_group,
            artifact_name,
            release_version,
        )
    )

# --- Aggregator POM for the bare repo coordinate (com.github.User:Repo:Version) ---
aggregator_group = github_group
aggregator_artifact = repository_name

aggregator_dir = os.path.join(
    maven_repository_root,
    *aggregator_group.split("."),
    aggregator_artifact,
    release_version,
)

if not os.path.isdir(aggregator_dir):
    os.makedirs(aggregator_dir)

aggregator_pom_path = os.path.join(
    aggregator_dir,
    "{}-{}.pom".format(aggregator_artifact, release_version),
)

dependency_xml = "".join(
    """
    <dependency>
      <groupId>{group}</groupId>
      <artifactId>{artifact}</artifactId>
      <version>{version}</version>
      <type>aar</type>
    </dependency>""".format(
        group=published_group,
        artifact=module_name,
        version=release_version,
    )
    for module_name in ("flutter_debug", "flutter_release")
)

aggregator_pom_xml = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>{group}</groupId>
  <artifactId>{artifact}</artifactId>
  <version>{version}</version>
  <packaging>pom</packaging>
  <dependencies>{dependencies}
  </dependencies>
</project>
""".format(
    group=aggregator_group,
    artifact=aggregator_artifact,
    version=release_version,
    dependencies=dependency_xml,
)

with open(aggregator_pom_path, "w", encoding="utf-8") as aggregator_file:
    aggregator_file.write(aggregator_pom_xml)

print("Published aggregator {}:{}:{}".format(
    aggregator_group,
    aggregator_artifact,
    release_version,
))

# Keep one canonical copy in ~/.m2 for JitPack's artifact discovery. The
# project-directory Maven repository is generated and no longer needed here.
shutil.rmtree(generated_repository)
print("Removed temporary Flutter Maven repository: {}".format(
    generated_repository,
))