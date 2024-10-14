# core
import subprocess
import xml.etree.ElementTree as ET
import time

# community
from scapy.all import Ether, ARP, srp
from yaml import load, dump
import yaml
try:
  from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
  from yaml import Loader, Dumper
import apprise

# custom
import PingMonitor
from GlobalVars import Global, HostState

def getAppConfig():
  with open('conf/py-presence.yaml','r') as infile:
    return yaml.load(infile, Loader=Loader)
  
def scanWithScapy():
  interface = "wlan0"
  IpRange = "192.168.108.0/24"
  BroadcastMac = 'ff:ff:ff:ff:ff:ff'

  macs = {}
  packet = Ether(dst=BroadcastMac)/ARP(pdst = IpRange)
  ans, unans = srp(packet, timeout = 2, iface = interface, inter = 0.1)
  for send, recv in ans:
    print (f'src: {recv.src}, ip: {recv.psrc}')
    macs[recv.src] = recv.psrc

  return macs

def getChangedMonitors(discovered):
  ChangedMacs = []
  AppriseInstance = apprise.Apprise()
  AppriseInstance.add(Global.AppConfig['notify']['apprise'])

  for OnlineMac in discovered.keys():
    if Global.isMonitoredMac(OnlineMac) \
      and Global.getMonitoredMacStatus(OnlineMac) == HostState.OFFLINE:
      NewState = Global.setMonitoredHostState(OnlineMac, HostState.ONLINE, discovered[OnlineMac])
      ChangedMacs.append(NewState)
      AppriseInstance.notify(
        body=f'Host {Global.MonitoredHosts[OnlineMac].id} ({Global.MonitoredHosts[OnlineMac].ip}) is in network',
        title = 'Host in network'
      )
  return ChangedMacs
  
Global.AppConfig = getAppConfig()
HostCount = Global.initMonitoredHosts()
print (f'Hosts monitored: {HostCount}')

PingMonitor.start()

print (f'Monitor frequency sec: {Global.AppConfig["monitor"]["frequency_sec"]}')
# print (f'MQTT host: {Global.AppConfig["monitor"]["mqtt_host"]}')
while True:
  FoundMacs = scanWithScapy()
  ChangedHosts = getChangedMonitors(FoundMacs)
  if len(ChangedHosts) > 0:
    for host in ChangedHosts:
      print (f'MAC online: {host}')
  time.sleep(Global.AppConfig['monitor']['frequency_sec'])
# scanWithNmap()
