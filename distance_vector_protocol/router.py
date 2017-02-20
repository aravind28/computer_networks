# Python 2.7
import os.path
import socket
import table
import threading
import util
import struct

_CONFIG_UPDATE_INTERVAL_SEC = 5

_MAX_UPDATE_MSG_SIZE = 1024
_BASE_ID = 8000

def _ToPort(router_id):
  return _BASE_ID + router_id

def _ToRouterId(port):
  return port - _BASE_ID

class Router:
  def __init__(self, config_filename):
    # ForwardingTable has 3 columns (DestinationId,NextHop,Cost). It's
    # threadsafe
    self._forwarding_table = table.ForwardingTable()
    # Config file has router_id, neighbors, and link cost to reach them
    self._config_filename = config_filename
    self._router_id = None
    # Socket used to send/recv update messages (using UDP)
    self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  def start(self):
    # Start a periodic closure to update config
    self._config_updater = util.PeriodicClosure(
        self.load_config, _CONFIG_UPDATE_INTERVAL_SEC)
    self._config_updater.start()
    # keep a list of neighbour routers to whom the
    # router should send update message
    self.neighbour_routers = []
    # keep a copy of the actual table to check if
    # the values in config file changes
    self.copy_of_forwarding_table = {}
    while True: pass

  def stop(self):
    if self._config_updater:
      self._config_updater.stop()

  def load_config(self):
    assert os.path.isfile(self._config_filename)
    with open(self._config_filename, 'r') as f:
      router_id = int(f.readline().strip())
      # Only set router_id when first initialize
      if not self._router_id:
        self._socket.bind(('localhost', _ToPort(router_id)))
        self._router_id = router_id

      lines = f.readlines()
      # initialize forwarding table
      if self._forwarding_table._table == {}:
        self._forwarding_table._table[self._router_id] = (0, 0)
        for i in range(len(lines)):
          line = lines[i].split(",")
          if line[1]:
           self._forwarding_table._table[int(line[0])] = (int(line[0]), int(line[1].strip()))
           self.copy_of_forwarding_table[int(line[0])] = (int(line[0]), int(line[1].strip()))
           self.neighbour_routers.append(int(line[0]))
          else:
           self._forwarding_table._table[line[0]] = (0, 0)
           self.copy_of_forwarding_table[line[0]] = (0, 0)

        print "Initialization of Forwarding Table"
        print self._forwarding_table
      # end of initialization

      # modify values in forwarding table if value in config file changes
      for line in lines:
        self.check_router_no = int(line.split(",")[0])
        self.check_cost = int(line.split(",")[1].strip())
        if self.check_router_no in self.copy_of_forwarding_table.keys():
          if self.check_cost != self.copy_of_forwarding_table.get(self.check_router_no)[1]:
            self.copy_of_forwarding_table[self.check_router_no] = (0, self.check_cost)
            self._forwarding_table._table[self.check_router_no] = (0, self.check_cost)
            print "Change of values in Config File"
            print self._forwarding_table
        else:
          print "New Neighbours Added in Config File"
          self.copy_of_forwarding_table[self.check_router_no] = (0, self.check_cost)
          self._forwarding_table._table[self.check_router_no] = (0, self.check_cost)

    # start receiving data from all neighbours
    self._socket.settimeout(0.5)
    self.incoming_tables = []
    try:
      while True:
        self.data, addr = self._socket.recvfrom(2048)
        if not self.data:
          break
        if _ToPort(self._router_id) != addr[1]:
          self.incoming_tables.append(self.data)
          # append router id from which data is received, so that
          # it can be added in the hop information
          self.incoming_tables.append(_ToRouterId(addr[1]))
    except socket.timeout:
      pass
    # finish receiving data from neighbours

    # update forwarding table of router based on received data
    while self.incoming_tables:
      # extract the router id from which data is received
      # this is the hop router
      self.from_router = self.incoming_tables.pop()
      self.val = self.incoming_tables.pop()
      self.count = struct.unpack('!H', self.val[0:2])[0]
      # an index value to extract router id and cost
      self.j = 2
      for i in range(self.count):
        self.router_no = struct.unpack('!H', self.val[self.j: self.j + 2])[0]
        self.cost = struct.unpack('!H', self.val[self.j + 2: self.j + 4])[0]
        self.j += 4
        # if new router found, add to table and include the hop for that router
        if self.router_no not in self._forwarding_table._table.keys():
          self.cost_to_hop_router = self._forwarding_table._table.get(self.from_router)[1]
          self._forwarding_table._table[self.router_no] = (self.from_router, self.cost_to_hop_router + self.cost)
        # check and modify the cost based on update message
        else:
          self.existing_cost = self._forwarding_table._table.get(self.router_no)[1]
          self.cost_to_hop_router = self._forwarding_table._table.get(self.from_router)[1]
          self.new_cost = self.cost_to_hop_router + self.cost
          if self.new_cost < self.existing_cost:
            self._forwarding_table._table[self.router_no] = (self.from_router, self.new_cost)
    print self._forwarding_table

    # making the update message
    self.update_msg = struct.pack('!H', len(self._forwarding_table._table.keys()))
    for key in self._forwarding_table._table.keys():
      self.update_msg += struct.pack('!H', key)
      self.update_msg += struct.pack('!H', self._forwarding_table._table.get(key)[1])
    # end of making update message

    # send the forwarding table to all neighbours
    print "List of neighbours:", self.neighbour_routers
    for neighbour_router in self.neighbour_routers:
      try:
        self._socket.sendto(self.update_msg, ('localhost', _ToPort(neighbour_router)))
      except:
        pass
    # finish sending to all neighbours
