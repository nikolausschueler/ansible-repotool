= Helper for simple repo hosting

== What is it?

A tool to simplify work with a simple repo setup that just consists of some repositories on a server.

If you are like me, your own repo hosting may just consist of repos on a server, no GitHub, GitLab or other sophisticated hosting solution.

This tool is intended to ease administration of such a repo setup. It works with Git and Mercurial repositories.

== Current state

What is implemented so far? The tool allows you to list your server repos. It creates a CSV file that tells you

* what type the repo is (Git or Mercurial (aka "hg")),
* the path on the server,
* if it is bare or not,
* if it is a Git repo: does it conform to the Git server repo naming convention?

For a Git repo, bare means that it was created as bare (with "git init --bare"). 
For a Mercurial repo, this means that it does not contain checked out files. In other words, after repo creation, "hg up null" was run in the repo.

The "conform" field only applies to Git. It means that a bare repo ends in ".git", the common naming convention for Git server repos.

== Assumptions

The tool assumes that all your repositories are in a directory "repo" inside your home on the server. Without this assumption, this tool would have to scan, for example, your whole home directory, which might take quite a long time.

== Usage

The tool assumes that you have an inventory file, this should contain a group
for your servers, like so

....
[dvcs_servers]
example.com
....

The `dvcs_servers` are used in the playbook.

The inventory file is not checked in to version control, your server may not be
the same as mine ;-)

== Plans

* Add backup and restore.
* Add creation of server-side repos.
