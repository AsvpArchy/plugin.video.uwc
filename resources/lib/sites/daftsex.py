'''
    Ultimate Whitecream
    Copyright (C) 2016 Whitecream, hdgdl
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib2
import os
import re
import sys

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils

@utils.url_dispatcher.register('610')
def Main():
    utils.addDir('[COLOR hotpink]Search[/COLOR]','https://daftsex.com/video/',613,'','')
    List('https://daftsex.com/hot')
    xbmcplugin.endOfDirectory(utils.addon_handle)

	
@utils.url_dispatcher.register('611', ['url'], ['page'])
def List(url, page=0):
    try:
        postRequest = {'page' : str(page)}
        response = utils.postHtml(url, form_data=postRequest,headers={},compression=False)
    except:
        return None
    match = re.compile(r'<div class="video-item">[^"]+"/watch/([^"]+)"[^/]+/[^/]+/[^/]+/([^"]+)" alt="([^"]+)', re.DOTALL | re.IGNORECASE).findall(response)
    for video, img, name in match:
        name = utils.cleantext(name)
        img = "https:/" + img
        utils.addDownLink(name, video, 612, img, '')
    npage = page + 1
    utils.addDir('Next Page (' + str(npage) + ')', url, 611, '', npage)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('612', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    url = url.replace("_", "&id=")
    response = utils.getHtml('http://daxab.com/player/?oid=' + url + '&color=f12b24', 'https://daxab.com/')

    token = re.compile('access_token: "([^"]+)', re.DOTALL | re.IGNORECASE).findall(response)
    videos = re.compile('id: "([^"]+)', re.DOTALL | re.IGNORECASE).findall(response)
    extra_key = re.compile('sig: "([^"]+)', re.DOTALL | re.IGNORECASE).findall(response)
    ckey = re.compile('c_key: "([^"]+)",', re.DOTALL | re.IGNORECASE).findall(response)

    response = utils.getHtml ("https://crazycloud.ru/method/video.get?callback=jQuery31108732364196646363_1490030654100&token=" + token[0] + "&videos=" + videos[0] + "&extra_key=" + extra_key[0] + "&ckey=" + ckey[0] + "&_=1490030654101", "https://daxab.com/")
    videourl = ""
    match_240 = re.compile('"mp4_240":"([^"]+)', re.DOTALL | re.IGNORECASE).findall(response)
    match_360 = re.compile('"mp4_360":"([^"]+)', re.DOTALL | re.IGNORECASE).findall(response)
    match_480 = re.compile('"mp4_480":"([^"]+)', re.DOTALL | re.IGNORECASE).findall(response)
    match_720 = re.compile('"mp4_720":"([^"]+)', re.DOTALL | re.IGNORECASE).findall(response)
    match_1080 = re.compile('"mp4_1080":"([^"]+)', re.DOTALL | re.IGNORECASE).findall(response)
    if match_240: 
        videourl = match_240[0].replace("\\","")
    if match_360: 
        videourl = match_360[0].replace("\\","")
    if match_480: 
        videourl = match_480[0].replace("\\","")
    if match_720: 
        videourl = match_720[0].replace("\\","")
    if match_1080: 
        videourl = match_1080[0].replace("\\","")
        
    if videourl:
        utils.playvid(videourl, name, download)
    else:
        utils.notify('Oh oh','Couldn\'t find a video')

		 
@utils.url_dispatcher.register('613', ['url'], ['keyword'])
def Search(url, keyword=None):
    searchUrl = url
    xbmc.log("Search: " + searchUrl)
    if not keyword:
        utils.searchDir(url, 613)
    else:
        title = keyword.replace(' ','_')
        searchUrl = searchUrl + title
        xbmc.log("Search: " + searchUrl)
        List(searchUrl)