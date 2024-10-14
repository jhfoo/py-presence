def printHost(host):
  for child in host:
    print (child)
    print (child.attrib)

def scanWithNmap():
  result = subprocess.run(['nmap','-sn','-oX','-','192.168.108.0/24'], 
    capture_output=True,
    text=True)
  root = ET.fromstring(result.stdout)
  # doc = untangle.parse(result.stdout)
  print (root)
  for child in root:
    if 'tag' in child:
      print (f'element tag: {child.tag}')
      print (child)
      if child.tag == 'host':
        printHost(child)
    else:
      print ('node:')
      print (f'child tag: {child.tag}')
      if child.tag == 'host':
        printHost(child)
      else:
        print(child)
        print (f'children: {len(child)}')
        for grandchild in child:
          if grandchild.tag == 'host':
            printHost(f'hosts: {grandchild}')
          print (f'element tag: {grandchild.tag}')
  # for child in doc.root.child:
  #   print (f'child: {child["name"]}')