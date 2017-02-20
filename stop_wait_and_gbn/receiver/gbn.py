import udt

# Go-Back-N reliable transport protocol
class GoBackN:
  # "msg_handler" is used to deliver messages to application layer when it's ready
  def __init__(self, local_port, remote_port, msg_handler):
    self.network_layer = udt.NetworkLayer(local_port, remote_port, self)
    self.msg_handler = msg_handler

  # "send" is called by application. Return true on success, false otherwise
  def send(self, msg):
    # call self.network_layer.send() to send to network layer
    pass

  # "handler" to be called by network layer when packet is ready
  def handle_arrival_msg(self):
    msg = self.network_layer.recv()
    # call self.msg_handler() to deliver to application layer
    pass

  # shutdown
  def shutdown(self):
    # class.
    self.network_layer.shutdown()
