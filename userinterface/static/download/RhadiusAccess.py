# ######################################################################### #
#    This file is part of nanothings.                                       #
#                                                                           #
#    nanothings is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU Affero GPL as published by               #
#    the Free Software Foundation, either version 3 of the License, or      #
#    (at your option) any later version.                                    #
#                                                                           #
#    nanothings is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#    GNU Affero GPL for more details.                                       #
#                                                                           #
#    You should have received a copy of the GNU Affero GPL                  #
#    along with nanothings.  If not, see <http://www.gnu.org/licenses/>.    #
# ######################################################################### #
#!/usr/bin/env python

import omero.scripts as scripts

try:
    from PIL import Image
except ImportError:
    import Image
import requests

from omero.gateway import BlitzGateway
import os


class ScriptsManager(object):
    def __init__(self, user="root", pwd="omero", host="localhost", port=4064):
        self.conn = BlitzGateway(user, pwd, host=host, port=port)
        result = self.conn.connect()
        if not result:
            raise RuntimeError("Cannot connect to <{0}>".format(host) +
                               " with user <{0}>.".format(user))
        self.svc = self.conn.getScriptService()

    def list(self):
        return self.svc.getScripts()

    def delete(self, id):
        try:
            self.svc.deleteScript(id)
        except Exception, e:
            raise RuntimeError("Failed to delete script: " +
                               "{0} ({1})".format(id, e))

    def upload(self, folder_name, script_name, script):
        import omero

        path = os.path.join(folder_name,
                            script_name + ".py")
        try:
            id = self.svc.uploadOfficialScript(path,
                                               script)
        except omero.SecurityViolation, sv:
            raise RuntimeError("SecurityViolation: {0}".format(
                sv.message))
        except Exception, aue:
            if "editScript" in aue.message:
                self.delete(self.get_id_from_path(folder_name,
                                                  script_name))
                id = self.svc.uploadOfficialScript(path,
                                                   script)
            else:
                raise RuntimeError("ApiUsageException: {0}".format(
                    aue.message))

    def get_id_from_path(self, folder_path, file_path):
        for script in self.list():
            path = script.getPath().getValue()
            name = script.getName().getValue()
            if path == "/" + folder_path + "/" and \
                            name == file_path + ".py":
                return script.getId().getValue()
        return "-1"


def simple_input(type, identifier, group_num, description, optional):
    """Builds a generic input () string."""
    s = """\
                            scripts.{0}("{1}", #input identifier
                                        optional={4},
                                        grouping="{2}",
                                        description="{3}"),
""".format(type, identifier, group_num, description, optional)
    return s


def build_inputs(inputs_json):
    s = ""
    group_num = 2
    for input in inputs_json:
        if input["type"] == "url_list":
            s += simple_input("String",
                              input["label"],
                              group_num,
                              input["description"],
                              str(not input["required"]))
        elif input["type"] == "string":
            s += simple_input("String",
                              input["label"],
                              group_num,
                              input["description"],
                              str(not input["required"]))
        elif input["type"] == "int":
            s += simple_input("Int",
                              input["label"],
                              group_num,
                              input["description"],
                              str(not input["required"]))
        else:
            raise RuntimeError("Input type <{0}> not recognized".format(input["type"]))
        group_num += 1
    return s


def build_image_upload(json):
    s = ""
    for input in json:
        if input["type"] == "url_list":
            s += """\
                    if annotation.getValue() == scriptParams["{0}"]:
                        omeTiffImage = image.exportOmeTiff()
                        loader.upload(url, omeTiffImage)
                        urls["{1}"] = urls.get("{1}","")+urllib.quote(loaderout+url,":/=?&")+"||"

""".format(input["label"],
           input["name"])
    return s


def build_data(json):
    s = ""
    for input in json:
        if input["type"] == "url_list":
            s += """\
        data["{0}"] = urls.get("{0}", "")[:-2]
""".format(input["name"])
        else:
            s += """\
        data["{0}"] = scriptParams.get("{1}","")
""".format(input["name"], input["label"])
    return s


if __name__ == "__main__":
    client = scripts.client("WebValley Processing",
                            "This code enables for the creation of processing scripts.",
                            scripts.String("Folder Name", optional=False, grouping="1",
                                           description="Folder Name where analysis scripts will be created"),

                            scripts.String("Rhadius Server URL",
                                           optional=False,
                                           grouping="2",
                                           default="https://rhadius.fbk.eu",
                                           description="Base Url of the Rhadius server"),

                            scripts.String("WebDAV URL",
                                           optional=False,
                                           grouping="3",
                                           default="http://rebalton.com/oc/files/webdav.php/upload_folder/",
                                           description="WebDAV URL for image uploading"),
                            scripts.String("WebDAV Username",
                                           optional=False,
                                           grouping="3.1",
                                           default="prova",
                                           description="WebDAV Username for image uploading"),
                            scripts.String("WebDAV Password",
                                           optional=False,
                                           grouping="3.1",
                                           default="prova",
                                           description="WebDAV Password for image uploading"),
                            scripts.String("Public WebDAV URL",
                                           optional=False,
                                           grouping="3.1",
                                           default="http://rebalton.com/oc/public.php?service=files&t=22ce2e47e0c573a25bcf9fd637bfcb3d&path=/",
                                           description="Public URL for uploaded WebDAV images (this must be reachable from the Rhadius server)"),

                            scripts.String("Omero Server Host",
                                           optional=False,
                                           grouping="4",
                                           default="localhost",
                                           description=""),
                            scripts.Int("Omero Server Port",
                                        optional=False,
                                        grouping="4.1",
                                        default=4064,
                                        description=""),
                            scripts.String("Omero Server Admin Username",
                                           optional=False,
                                           grouping="4.1",
                                           default="root",
                                           description=""),
                            scripts.String("Omero Server Admin Password",
                                           optional=False,
                                           grouping="4.1",
                                           default="omero",
                                           description=""),
                            version="0.1",
                            authors=["WebvalleyTeam 2013"],
                            institutions=["FBK"],
                            contact="webvalley@fbk.eu")

    scriptParams = {}
    for key in client.getInputKeys():
        if client.getInput(key):
            scriptParams[key] = client.getInput(key, unwrap=True)

    server_url = scriptParams["Rhadius Server URL"]  # url of the analysis server
    url_process_list = server_url + "/process/list/"  # url for retriving process list
    url_process_details = server_url + "/process/detail/"  # url for process details (inputs and ouputs definitions)
    url_process_run = server_url + "/process/run/"  # url for running processes

    # webdav url,user and password for image uploading
    webdav_url = scriptParams["WebDAV URL"]
    DAV_username = scriptParams["WebDAV Username"]
    DAV_password = scriptParams["WebDAV Password"]
    public_webdav_url = scriptParams["Public WebDAV URL"]

    availableProcesses = requests.get(url_process_list).json()

    for process in availableProcesses:
        jsonData = requests.get(url_process_details + str(process["id"])).json()

        url_list_needed = False
        for input in jsonData["inputs"]:
            if input["type"] == "url_list":
                url_list_needed = True

        if url_list_needed:
            image_input_declaration = """\
                            scripts.String("Data_Type", optional=False, grouping="1",
                                           description="Choose source of images (only Image supported)",
                                           values=dataTypes, default="Image"),
                            scripts.List("IDs", optional=False, grouping="1.1",
                                         description="List of Image IDs to change annotations for.").ofType(rlong(0)),
"""
            image_looping = """\
        # establish connection to omero
        conn = BlitzGateway(client_obj=client)

        #get objects
        objects, logMessage = scriptUtil.getObjects(conn, scriptParams)

        # gather all images
        images = []

        if scriptParams["Data_Type"] == "Dataset":
            for dataSet in objects:
                images.extend(list(dataSet.listChildren()))
            if not images:
                print "No images found in selected dataset."
        else:
            images = objects

        loader = DAVLoader(loaderin, '{username}', '{password}')
        relativepath = "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
        loader.mkdir(relativepath)


        # go through each image
        urls = dict()
        for image in images:
            for annotation in image.listAnnotations():
                if isinstance(annotation, omero.gateway.TagAnnotationWrapper):
                    url = relativepath+"/"+os.path.basename(image.getName())
""".format(username=DAV_username,
           password=DAV_password)

        else:
            image_input_declaration = ""
            image_looping = ""

        finalCode = """\
#!/usr/bin/env python

from omero.gateway import BlitzGateway            # used for connecting to the server
import omero                        # contains general OMERO content
import omero.util.script_utils as scriptUtil        # used for making the user interface
from omero.rtypes import *                # imports rstring + other data types
import omero.scripts as scripts                # allows for making user interface
from numpy import *                    # for array representations
import os
import random
import string
import requests
import urllib

try:
    from PIL import Image
except ImportError:
    import Image

import omero.clients
from omero import client_wrapper
from time import sleep
from requests import Request, Session

class DAVLoader(object):

    def __init__(self, url, user, password):
        self.__url = url
        self.__user = user
        self.__password = password
        self.__s = Session()

        self.__req = Request('HEAD', url=self.__url).prepare()

        if self.__user is not None:
            self.__req.prepare_auth(auth=(self.__user, self.__password))

        if self.__s.send(self.__req).status_code != 200:
            raise requests.exceptions.HTTPError()

    def __request(self, method, data, path, match_codes):
        r = self.__req
        r.prepare_method(method)
        r.prepare_body(data=data, files=None)
        r.prepare_url(url=self.__url+path, params=None)
        return self.__s.send(r).status_code in match_codes

    def __retrieve(self, method, data, path, match_codes):
        r = self.__req
        r.prepare_method(method)
        r.prepare_body(data=data, files=None)
        r.prepare_url(url=self.__url+path, params=None)
        resp = self.__s.send(r)
        if resp.status_code in match_codes:
            return resp.content
        return False

    def upload(self, path, data):
        return self.__request('PUT', data, path, [201])

    def mkdir(self, path):
        if self.__request('HEAD', None, path, [200]):
            return True
        return self.__request('MKCOL', None, path, [201])

    def delete(self, path):
        return self.__request('DELETE', None, path, [201, 202, 204])

    def download(self, path):
        return self.__retrieve('GET', None, path, [200])

loaderout = "{public_webdav_url}"
loaderin  = "{webdav_url}"

if __name__ == "__main__":

    dataTypes = [rstring('Dataset'), rstring('Image')]

    client = scripts.client("{script_name}",
                            \"\"\"{description}\"\"\",
{image_input_declaration}
{inputs}
                            version="0.1",
                            authors=["{author}", ""],
                            institutions=["WebValley"],
                            contact="webvalley@fbk.eu", )

    try:
        # process the list of args above.
        scriptParams = dict()
        for key in client.getInputKeys():
            if client.getInput(key):
                scriptParams[key] = client.getInput(key, unwrap=True)

{image_looping}

{image_upload}

        data = dict()

{build_data}

        response = requests.post("{url_process_run}",data=data).json()

        if response["success"]:
            polling_url =response["polling_url"]
            running = True
            while running:
                status = requests.get("{server_url}"+polling_url).json()
                running = not status["finished"]
                sleep(3)
            if status["status"] == "SUCCESS":
                client.setOutput("Message", rstring(str(status["result"])))
            else:
                client.setOutput("Message", rstring("Process failed"))
        else:
            client.setOutput("Message", rstring("Process failed, invalid input parameters"))


    finally:
        client.closeSession()
""".format(image_input_declaration=image_input_declaration,
           image_looping=image_looping,
           script_name=jsonData["code"],
           description=jsonData["description"],
           inputs=build_inputs(jsonData["inputs"]),
           author=jsonData["author"],
           image_upload=build_image_upload(jsonData["inputs"]),
           build_data=build_data(jsonData["inputs"]),
           url_process_run=url_process_run + process["code"] + "/" + str(process["id"]),
           server_url=server_url,
           webdav_url=webdav_url,
           public_webdav_url=public_webdav_url
        )

        sm = ScriptsManager(user=scriptParams["Omero Server Admin Username"],
                            pwd=scriptParams["Omero Server Admin Password"], host=scriptParams["Omero Server Host"],
                            port=scriptParams["Omero Server Port"])
        sm.upload("/" + scriptParams["Folder Name"] + "/", process["code"], finalCode)
