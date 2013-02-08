#!/usr/bin/python

# Install to Project Repo
# A script for installing jars to an in-project Maven repository. 
# v0.1.1
# 
# MIT License
# (c) 2012, Nikita Volkov. All rights reserved.
# simplified version adapted by Tom Carchrae
# https://github.com/carchrae/install-to-project-repo



import os
import re
import shutil


def jars(dir):
  return [dir + "/" + f for f in os.listdir(dir) if f.lower().endswith(".jar")]

def parse_by_eclipse_standard(path):
  file = os.path.splitext(os.path.basename(path))[0]

  return {
  "group": "local",
	"name": file,
	"version": "1.0",
	"snapshot": "",
	"source": ""
  }


def maven_dependencies(parsing_results):
  def artifact(parsing):
    return {
      "groupId": parsing["group"], 
      "artifactId": parsing["name"],
      "version": parsing["version"] + ("-SNAPSHOT" if parsing["snapshot"] else "")
    }
  def maven_dependency(artifact):
    return """
<dependency>
  <groupId>%(groupId)s</groupId>
  <artifactId>%(artifactId)s</artifactId>
  <version>%(version)s</version>
</dependency>
""" % artifact
  def unique_artifacts():
    artifacts = []
    for (_, parsing) in parsing_results:
      a = artifact(parsing)
      if a not in artifacts:
        artifacts.append(a)
    return artifacts

  return "\n".join([maven_dependency(a).strip() for a in unique_artifacts()])


def install(path, parsing):
  os.system(
    "mvn install:install-file" + \
    " -Dfile=" + path + \
    " -DgroupId=" + parsing["group"] + \
    " -DartifactId=" + parsing["name"] + \
    " -Dversion=" + parsing["version"] + ("-SNAPSHOT" if parsing["snapshot"] else "") + \
    " -Dpackaging=jar" + \
    " -DlocalRepositoryPath=repo" + \
    " -DcreateChecksum=true" + \
    (" -Dclassifier=sources" if parsing["source"] else "")
  )

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-d", "--delete", 
                  dest="delete", action="store_true", default=False, 
                  help="Delete successfully installed libs in source location")
(options, args) = parser.parse_args()


parsings = (
  [(path, parse_by_eclipse_standard(path)) for path in jars("lib")]
)

unparsable_files = [r[0] for r in parsings if r[1] == None]
if unparsable_files:
  print "The following files could not be parsed:"
  for f in unparsable_files:
    print "| - " + f


parsings = [p for p in parsings if p[1] != None]

for (path, parsing) in parsings:
  install(path, parsing)
  if options.delete:
    os.remove(path)

print maven_dependencies(parsings)
print "These dependenceis have also been saved in the file : repo/dependencies.txt"
f = open('repo/dependencies.txt', 'w')
f.write(maven_dependencies(parsings))
