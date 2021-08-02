"""
pygofile
~~~~~~~~~

MIT License

Copyright (c) 2021 GautamKumar <https://github.com/gautamajay52>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import datetime
import os
from typing import Any, Dict
from urllib.parse import urljoin

from aiohttp import ClientSession

__author__ = "https://github.com/gautamajay52"


class NotAuthenticated(Exception):
    pass


class ServerError(Exception):
    pass


class Gofile:
    """
    Base class for all methods of Gofile API.

    Parameters:
        token (`str`, optional ):
            Gofile API token.
            The access token of an account. Can be retrieved from the profile page.

            if set, your account wil be used else a guest account will be created.
    """

    API: str = "https://{server}.gofile.io/"
    session = ClientSession

    def __init__(self, token=None) -> None:
        self.token = token

    async def upload(
        self,
        file: str,
        description: str = "",
        password: str = "",
        tags: str = "",
        expire: str = "",
        folder_id: str = "",
    ) -> Dict[str, str]:
        """
        Upload one file on a specific server.
        If you specify a folder_id, the file will be added to this folder.

        Parameters:
            file (``str``, optional ):
                Must contain one file.
                If you want to upload multiple files,
                call uploadFile again and specify the folderId of the first file uploaded.

            token (``str``, optional ):
                The access token of an account. Can be retrieved from the profile page.
                If valid, the file will be added to this account.

                If undefined, a guest account will be created to receive the file.

            folder_id (``str``, optional ):
                The ID of a folder.
                If valid, the file will be added to this folder.
                If undefined, a new folder will be created to receive the file.

                When using the folderId, you must pass the account token.

            description (``str``, optional ):
                If valid, will set a description for the newly created folder.
                Markdown syntax can be used.

                Not applicable if you specify a folderId.

            password (``str``, optional ):
                If valid, will set a password for the newly created folder.
                min length of password is 4

                Not applicable if you specify a folderId.

            tags (``str``, optional ):
                If valid, will set tags for the newly created folder.
                If multiple tags, seperate them with comma (`example` : `"tags1,tags2"`)

                Not applicable if you specify a folderId.

            expire (``str``, optional ):
                If valid, will set an expiration date for the newly created folder.
                Must be in the form of unix timestamp. (`Format`: `yyyy-mm-dd``)

                Not applicable if you specify a folderId.

        """
        if not os.path.isfile(file):
            raise ValueError("Only file supported")
        elif password and len(str(password)) < 4:
            raise ValueError("password is too short (min len 4)")

        data_ = self.serialize(
            file=file,
            description=description,
            password=password,
            tags=tags,
            expire=expire,
            folder_id=folder_id,
        )

        if self.token:
            data_["token"] = self.token

        async with self.session() as session:
            with open(file, "rb") as _file:
                data_["file"] = _file
                server = await self.server(session)
                url = urljoin(self.API.format(server=server), "uploadFile")
                data = await session.post(url, data=data_)
        return self.parse_json(await data.json())

    async def get_account_details(self, all_details=False) -> Dict[str, str]:
        """
        Retrieving specific account information

        Parameters:
            all_details (`bool` , optional ):
                If set, all details will be returned.

                If undefined, minimal information will be returned.
        """
        if not self.token:
            raise NotAuthenticated("You must provide token.")
        async with self.session() as session:
            url = urljoin(
                self.API.format(server="api"),
                "getAccountDetails?token={token}&allDetails={allDetails}",
            )
            data = await session.get(
                url.format(token=self.token, allDetails=all_details)
            )
        return self.parse_json(await data.json())

    async def delete_content(self, content_id: str) -> Dict[str, str]:
        """
        Delete file or folder

        Parameters:
            content_id (``str``):
                The file or folder ID.
        """
        if not self.token:
            raise NotAuthenticated("You must provide token.")
        async with self.session() as session:
            data = {"contentId": content_id, "token": self.token}
            url = urljoin(self.API.format(server="api"), "deleteContent")
            data = await session.delete(url, data=data)
        return self.parse_json(await data.json())

    async def set_folder_options(
        self, folder_id: str, option: str, value: str
    ) -> Dict[str, str]:
        """
        Set an option on a folder

        Parameters:
            folder_id (``str``):
                The folder ID.

            option (``str``):
                Can be "private", "password", "description", "expire" or "tags".

            value (``str``):
                The value of the option to be defined.

                For "private", can be "true" or "false".

                For "password", must be the password. (``Min len 4``)

                For "description", must be the description.

                For "expire", must be the expiration date in the form of unix timestamp (`Format`: `yyyy-mm-dd``).

                For "tags", must be a comma seperated list of tags.

        You can have only one option and value at a time.
        """
        if not self.token:
            raise NotAuthenticated("You must provide token.")
        async with self.session() as session:
            data = {
                "token": self.token,
                "folderId": folder_id,
                "option": option,
                "value": str(value).replace(" ", "") if option == "tags" else value,
            }
            url = urljoin(self.API.format(server="api"), "setFolderOptions")
            data = await session.put(url, data=data)
            data = await data.json()
        return self.parse_json(data)

    async def create_folder(
        self, parent_folder_id: str, folder_name: str
    ) -> Dict[str, str]:
        """
        Create a new folder

        Parameters:
            parent_folder_id (``str``):
                The parent folder ID.

            folder_name (``str``):
                The name of the created folder.
        """
        if not self.token:
            raise NotAuthenticated("You must provide token.")

        async with self.session() as session:
            data = {
                "token": self.token,
                "folderName": folder_name,
                "parentFolderId": parent_folder_id,
            }
            url = urljoin(self.API.format(server="api"), "createFolder")
            data = await session.put(url, data=data)
            data = await data.json()
        return self.parse_json(data)

    async def server(self, session: ClientSession) -> Dict[str, str]:
        """
        To get server name form Gofile API
        """
        url = urljoin(self.API.format(server="api"), "getServer")
        server = await (await session.get(url)).json()
        server = self.parse_json(server)
        return server["server"]

    @staticmethod
    def serialize(**kwargs) -> Dict[str, str]:
        """
        Just to parse input values to a dict
        """
        data = {}
        for k, v in kwargs.items():
            if k == "folder_id" and v:
                data = {}
                data["folderId"] = v
                return data
            elif k == "description" and v:
                data[k] = str(v)
            elif k == "password" and v:
                data[k] = str(v)
            elif k == "tags" and v:
                data[k] = str(v).replace(" ", "")
            elif k == "expire" and v:
                year, mon, day = (int(a) for a in str(v).split("-"))
                timestamp = datetime.datetime(year, mon, day).timestamp()
                data[k] = str(timestamp).split(".", maxsplit=1)[0]
        return data

    @staticmethod
    def parse_json(json_) -> Dict[str, str]:
        """
        parse final json and send data as dict
        """
        if json_["status"] == "ok":
            return json_["data"]
        raise ServerError(json_["status"])
