# core
import time

class Global:
  AppConfig = None
  MonitoredHosts = {}

  @staticmethod
  def initMonitoredHosts():
    count = 0
    for HostId in Global.AppConfig['hosts']:
      HostMac = Global.AppConfig['hosts'][HostId]['mac']
      Global.MonitoredHosts[HostMac] = {
        'id': HostId,
        'mac': HostMac,
        'state': 'offline',
        'ip': None,
        'DateTimeUpdated': time.time()
      }
      count += 1
    return count
  
  @staticmethod
  def isMonitoredMac(TestMac):
    return TestMac in Global.MonitoredHosts

  @staticmethod
  def getMonitoredMacStatus(mac):
    if mac not in Global.MonitoredHosts:
      raise Exception(f'MAC address not monitored: {mac}')

    return Global.MonitoredHosts[mac]['state']

  @staticmethod
  def setMonitoredHostState(mac, NewState, NewIp):
    if mac not in Global.MonitoredHosts:
      raise Exception(f'MAC address not monitored: {mac}')

    if Global.MonitoredHosts[mac]['state'] == NewState:
      raise Exception(f'MAC status already set to {NewState}')
    
    Global.MonitoredHosts[mac]['state'] = NewState
    Global.MonitoredHosts[mac]['ip'] = NewIp
    Global.MonitoredHosts[mac]['DateTimeUpdated'] = time.time()

    return Global.MonitoredHosts[mac]

