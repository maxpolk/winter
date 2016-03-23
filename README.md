# winter

Winter is a wiki computing platform.

A traditional wiki each URL identifies a resource made up of markup text.  Loading that resource causes the server to interpret the markup data and translate it into a useful HTML view, so that it looks like an encyclopedia entry or article.  Editing the resource (page) usually means editing the text markup data that is designed to easily translate into HTML paragraphs, tables, stylized text, or links to other resources, frequently other resources within the same wiki.  A web proxy is often included to cache repeated requests for the same resource to avoid having to reinterpret the same unchanged markup data time after time.

To extend the wiki, and supplant the simple built-in markup text, extensions or plugins are created with special new syntax to do more and more things.  The more content you want on a traditional wiki page, the more markup text you place into it.  Unfortunately this means that as page complexity grows, the difficulty of testing and validation grows, probably more than linearly.

Winter encourages only small, simple resources, made up code or data that references and composes sets of other resources.  By recursion, any arbitrarily complex content is supported.

# code or data resources

A code resource is any language or domain-specific language, where text markup language and Python 3 is interpreted internally, and other languages interpreted in external processes.  Every language, through language facility or library, will be required to support simple and natural references to other resources within the wiki.

A data resource can be immediate information like strings, numbers, lists, or maps, or else it can be a reference to external information like a call to a web API, an RSS news feed, a database query, a directory listing of files, a local system call, the output of a command or program, or anything else.

# flexible references

By coupling data resources, stored directly or indirectly in the wiki, with code resources that can refer to that data or other code resources, users will have the power to manipulate and test changes to the code and data to produce a large range of effects.  Code that assembles other resources, that in turn assembles other resources, means that no one resource ever needs to be complex.  A whole site of arbitrary complexity can then be created by small, simple, testable parts.  This establishes the architecture of flexible references to any accessible resource.

# resource classification

Users can classify code or data resources, then write tests for that class resource.  By writing code to validate a text markup language, and declaring a resource to be text markup language, we achieve automatic testing.  This establishes the architecture of automatic testing.

# staging changes

Instead of changing and releasing one resource at a time, a set of resources can be staged to be released at the same time.  Each user will have their own space to assemble multiple resource changes and bundle them into a single release.

# stable recomputation

Since a data resource reference an Internet URL, a fresh copy will be needed on demand or automatically according to some refresh period via a time attribute to external resources.

Since one resource ("observer") can refer to or observe another resource ("reference"), observers are automatically updated when one of their references change.  Changes to resources can create a cascade of changes to the resources that refer to them, so that a large set of resources can all get updated by changing a single resource.

Cyclical references are fine by means of a generation number.  For example, a data resource that is classfied as an integer named "A" can be declared to be "A(n) = A(n-1) + 1", where "n" is the generation number of the resource.

A set of related resources that refer to each other constitutes an entire generation, and must change in a stable fashion, so one resource update doesn't get too far ahead of other resource updates.  This is called a cascade in Winter.  Generations of data and stable recomputation of them are a key architectural concept of Winter.

# fast access to stable data

Rather than compute a resource inline with the request, Winter always delivers the last computed version of a resource so that as little CPU as possible is used to simply view resources.  The only time it will take to deliver content is the time it takes for static content to be returned.

A resource change results in a series of computations that always occur in the background to create a new version of resources that depend on it, recursively.  Since a browser displaying a resource deserves to know that a new version is being computed, a WebSocket is available to communicate that a new version is available, and even an expected time of arrival of that change.  Fast access of stable data is a key concept of Winter.

# software development for everyone

The goal of Winter is to bring software development to everyone by patching together smaller pieces of data and small functions to operate on them, and layering it into a web site.  No tool is needed other than a browser, and no skill is needed other than an ability to type just enough code to morph data into a desired shape.  No one page is ever complex.  Testing and releasing are built-in via resource classification.  Change sets are computed in a stable fashion.  Simplicity of data and code is a key concept of Winter.

# wind

To deploy Winter, it requires a MongoDB database to be running, which is deployed and administered separately.  Winter consists of four services "WIND", a metaphor of wind blowing in the winter, an acronym "Web, Init, Notify, Daemon."  The Init script runs on every server where Winter is deployed, reads from the database what should be running on that server, then is responsible to start, stop, monitor, and control the other three kinds of services on that server, the Web, Notify, and Daemon services.  Although the definitive version of resources exist in the database as code and data, a calculated version of each will exist, multiplied by the mime type and language variations of the resource, as normal files and delivered as static content.

A cache won't be necessary since every resource is always cached in the background.

# install

MongoDB installation is up to you.

To install Winter, use PyPi, which should pull in the dependencies:

    pip3 install winter

If you change the source and/or want to create a distribution, use the setup.py script:

    python3 setup.py sdist --formats=gztar,zip

# license

This project is licensed under version 3 of the GNU Affero General Public License, which you can read here: http://www.gnu.org/licenses/agpl-3.0.html

Developers should follow the "How to Apply These Terms to Your New Programs" section of the license located near the bottom.  For more help see: http://www.gnu.org/licenses/gpl-howto.html

Each source code file should have this comment near the top:

    This file is part of Winter, a wiki-based computing platform.
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

If that's too noisy for you, a minimal header at the top is:

    Copyright (C) <year>  <name of author>
    License located at http://www.gnu.org/licenses/agpl-3.0.html

Replace `<year>` with each year the source was prepared, and each year it was released, separated with comma, such as `2013,2015,2016`, but don't fill in the years when no changes were made to the file.  Replace `<name of author>` with your name.
