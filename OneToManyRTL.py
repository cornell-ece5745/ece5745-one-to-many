#=========================================================================
# One To Many RTL Model
#=========================================================================

from pymtl3 import *
from pymtl3.stdlib import stream

class OneToManyRTL( Component ):

  # Constructor

  def construct( s ):

    # Interface

    s.recv = stream.ifcs.RecvIfcRTL( Bits8 )
    s.send = stream.ifcs.SendIfcRTL( Bits8 )

    # Queues to buffer input

    s.inq = stream.NormalQueueRTL( Bits8, 2 )
    s.inq.recv //= s.recv

    # Counter

    s.count      = Wire( Bits8 )
    s.count_next = Wire( Bits8 )

    @update_ff
    def count_update():
      if s.reset:
        s.count <<= 0
      else:
        s.count <<= s.count_next

    # Logic

    @update
    def logic():

      # We are ready to process another transaction if counter is zero

      s.inq.send.rdy @= ( s.count == 0 )

      # We have a valid output message as long as counter is not zero

      s.send.val @= ( s.count > 0 )

      # If we have a new transaction, update the counter

      if s.inq.send.val and s.inq.send.rdy:
        s.count_next @= s.inq.send.msg

      # The output message is always the counter

      s.send.msg @= s.count

      # If we are able to send the transaction, then decrement counter

      if s.send.val and s.send.rdy:
        s.count_next @= s.count - 1

  # Line tracing

  def line_trace( s ):
    return f"{s.recv}({s.count}){s.send}"

