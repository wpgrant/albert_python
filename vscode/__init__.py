# -*- coding: utf-8 -*-
# Copyright (c) 2024 Manuel Schneider

"""
Opens a project in vscode
"""

from albert import *
from pathlib import Path  
import subprocess

md_iid = '2.3'
md_version = '1.0'
md_name = 'VSCode'
md_description = 'Open project in vscode'
md_license = 'MIT'
md_url = 'xx'
md_authors = '@wpgrant'

class Plugin(PluginInstance, TriggerQueryHandler):

  def __init__(self):
    PluginInstance.__init__(self)    
    TriggerQueryHandler.__init__(
      self, self.id, self.name, self.description,
      defaultTrigger='vs '
    )
    self.iconUrls = [f"file:{Path(__file__).parent}/vscode.svg"]

  def handleTriggerQuery(self, query):
    s = query.string.strip()
    
    if s:      
      self.getDirectoryOptions(query)
      
    else:
      query.add(
        StandardItem(
          id=md_iid,
          text=md_name,
          subtext=md_description,
          iconUrls=self.iconUrls,
        )
      )

  def getDirectoryOptions(self, query):
    s = query.string.strip()
    # zoxide query <query> --list
    result = subprocess.run(['zoxide', 'query', s, '--list'], stdout=subprocess.PIPE)
    strResult = result.stdout.decode('utf-8') 
    entries = strResult.split('\n')
    entries.remove('')
    for entry in entries[0:5]:
      txt = f"Open Project {entry}"
      print(txt)
      query.add(
        StandardItem(
          id=md_iid,
          text=md_name,
          subtext=txt,
          iconUrls=self.iconUrls,
          actions=[Action("open", md_description, lambda e=entry: runDetachedProcess(["code", e],"."))]
        )
      )    

  def configWidget(self):
    return [{ 'type': 'label', 'text': __doc__.strip() }]
  