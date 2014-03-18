#! /usr/bin/env python
# Copyright (C) 2013  Max Polk
# License located at http://www.gnu.org/licenses/agpl-3.0.html
'''
Experimental app server that runs under python as main or gunicorn as app:application.
'''
import os
import bottle  # for bottle.default_app
from bottle import get, post, put, delete, template, run, request, response
import re

# Change working directory so relative paths and template lookup work again
installpath = os.path.dirname (__file__)
if (installpath != ""):
    os.chdir (installpath)

# Remote object reference, lazy initialized
sysinfo = None

def normalizeResource (resource):
    '''Fix unruly slashes in the resource path.'''
    # Replace multiple slashes with one slash throughout entire path
    resource = re.sub (r'//+', r'/', resource)
    # If after all replacement, there is only one slash left and nothing else, remove it
    resource = re.sub (r'^/$', r'', resource)
    return resource

def normalizeScriptName (request):
    '''
    Use what upstream proxy says our SCRIPT_NAME is.
    See also http://flask.pocoo.org/snippets/35/
    '''
    script_name = request.get_header ('X_SCRIPT_NAME')
    if (script_name):
        request.environ['SCRIPT_NAME'] = script_name
    return script_name

@get ('/abc')
def rootGetAbc ():
    '''Generic dump of information about request.'''
    normalizeScriptName (request)
    # Populate some data for user to see
    result = [
        "route: '/'",
        "method: " + request.method,
        "path: " + request.path,
        "url: " + request.url,
        "script_name: " + request.script_name
    ]
    if (request.auth):
        result.append ("auth: " + request.auth[0] + ":" + request.auth[1])
    else:
        result.append ("auth: (none)")
    return template ('main.tpl', result=result,
                     headers=request.headers,
                     environ=request.environ)

@get ('/json')
def helloGetJson ():
    '''Example getting json data.'''
    normalizeScriptName (request)
    response.content_type = 'application/json'
    return '{"x":23, "y": [1, 2, 3]}'

@post ('/')
def helloRootPost ():
    '''Special case of post to resource when resource is empty.'''
    normalizeScriptName (request)
    return helloResourcePost ('')

@get ('/')
def helloRootGet  ():
    '''Special case of get of resource when resource is empty.'''
    normalizeScriptName (request)
    return template ('root.tpl', links = [
        'abc', 'abc/+', 'json', 'json/+/history?page=3&size=20', 'x/y/z', '+'])

@get ('/+')
def helloRootAllMetadata ():
    '''Special case of list metadata for resource when resource is empty.'''
    normalizeScriptName (request)
    return helloResourceAllMetadata ('')

@get ('/+/history')
def helloRootHistory ():
    '''Special case of list history for resource when resource is empty.'''
    normalizeScriptName (request)
    return helloResourceHistory ('')

@get ('/<resource:path>/+')
def helloResourceAllMetadata (resource):
    '''List all metadata associated with a resource.'''
    normalizeScriptName (request)
    resource = normalizeResource (resource)
    if (resource == ''):
        import pymongo
        client = pymongo.MongoClient ("localhost", 27017)
        db = client.wiki                        # database dedicated to the wiki
        return template ("The database name is '{{name}}'", name=db.name)
        #=======================================================================
        # db.my_collection                        # Collection(Database(MongoClient('localhost', 27017), u'wiki'), u'my_collection')
        # db.my_collection.save({"x": 10})        # ObjectId('4aba15ebe23f6b53b0000000')
        # db.my_collection.save({"x": 8})         # ObjectId('4aba160ee23f6b543e000000')
        # db.my_collection.save({"x": 11})        # ObjectId('4aba160ee23f6b543e000002')
        # db.my_collection.find_one()             # {u'x': 10, u'_id': ObjectId('4aba15ebe23f6b53b0000000')}
        # for item in db.my_collection.find():
        #     print (item["x"])
        # db.my_collection.create_index("x")      # u'x_1'
        # for item in db.my_collection.find().sort("x", pymongo.ASCENDING):
        #     print (item["x"])
        # [item["x"] for item in db.my_collection.find().limit(2).skip(1)]        # [8, 11]
        #=======================================================================
    return template ("List all metadata associated with resource '/{{resource}}'", resource=resource)

@get ('/<resource:path>/+/history')
def helloResourceHistory (resource):
    '''History associated with a resource.'''
    normalizeScriptName (request)
    resource = normalizeResource (resource)
    # Pagination
    pagenum = request.query.page or '1'
    pagesize = request.query.size or '10'
    # Result
    return template (
        "Obtain history associated with resource '/{{resource}}', page {{page}} size {{size}}",
        resource=resource, page=pagenum, size=pagesize)

@get ('/<resource:path>')
def helloResourceGet (resource):
    '''Get a resource.'''
    normalizeScriptName (request)
    resource = normalizeResource (resource)
    return template ("Get resource '/{{resource}}'", resource=resource)

@put ('/<resource:path>')
def helloResourcePut (resource):
    '''Put a new version of the resource, possibly creating it for the first time.'''
    normalizeScriptName (request)
    resource = normalizeResource (resource)
    return template ("Put new version of resource '/{{resource}}'", resource=resource)

@post ('/<resource:path>')
def helloResourcePost (resource):
    '''Post a new child resource underneath the specified resource.'''
    normalizeScriptName (request)
    resource = normalizeResource (resource)
    return template ("Post child resource under '/{{resource}}'", resource=resource)

@delete ('/<resource:path>')
def helloResourceDelete (resource):
    '''Delete a resource.'''
    normalizeScriptName (request)
    resource = normalizeResource (resource)
    return template ("Put new version of resource '/{{resource}}'", resource=resource)

# Run from command line or run as a service
if __name__ == "__main__":
    run (host='127.0.0.1', port=8003)
else:
    application = bottle.default_app ()
