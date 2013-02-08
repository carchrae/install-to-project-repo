#Install to Project Repo
A Python script for easily installing libraries to an in-project Maven repository. It creates a repository in the root folder of the project complete with poms, checksums and metadata. It also outputs the appropriate dependencies xml to be inserted in your `pom` file.


##What it does
* When run in standard mode it looks for all jars in the `lib` folder:

        artifactId.jar

* When run with `-d` modifier it removes all successfully installed jars from the `lib` folder.

* After successful installation of all jars it prints out all according dependencies for your `pom` and saves them to a file in ./repo/


##Using

Just run it from the folder containing your lib folder. 

After the script is complete copy-paste the generated dependencies xml to your `pom` under `dependencies` tag and add the following under the `repositories` tag:

    <repository>
      <id>project</id>
      <url>file://${project.basedir}/repo</url>
    </repository>

For more details please read [this StackOverflow answer](http://stackoverflow.com/a/7623805/485115).


