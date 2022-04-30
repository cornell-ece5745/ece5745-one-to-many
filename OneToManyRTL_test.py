#=========================================================================
# OneToManyRTL_test
#=========================================================================

import pytest
import random

from pymtl3 import *
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from pymtl3.stdlib import stream

from OneToManyRTL import OneToManyRTL

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s ):

    # Instantiate models

    s.src  = stream.SourceRTL ( Bits8 )
    s.sink = stream.SinkRTL   ( Bits8 )
    s.dut  = OneToManyRTL()

    # Connect

    s.src.send //= s.dut.recv
    s.dut.send //= s.sink.recv

  def done( s ):
    return s.src.done() and s.sink.done()

  def line_trace( s ):
    return s.src.line_trace() + " > " + s.dut.line_trace() + " > " + s.sink.line_trace()

#-------------------------------------------------------------------------
# test_1
#-------------------------------------------------------------------------
# If we send in a one then dut should produce one message

def test_1( cmdline_opts ):

  th = TestHarness()

  th.set_param( "top.src.construct",  msgs=[Bits8(1)] )
  th.set_param( "top.sink.construct", msgs=[Bits8(1)] )

  run_sim( th, cmdline_opts, duts=['dut'] )

#-------------------------------------------------------------------------
# test_0
#-------------------------------------------------------------------------
# If we send in a zero then dut should produce no messages

def test_0( cmdline_opts ):

  th = TestHarness()

  th.set_param( "top.src.construct",  msgs=[Bits8(0)] )
  th.set_param( "top.sink.construct", msgs=[] )

  run_sim( th, cmdline_opts, duts=['dut'] )

#-------------------------------------------------------------------------
# test_2
#-------------------------------------------------------------------------
# If we send in a two then dut should produce two messages (2,1)

def test_2( cmdline_opts ):

  th = TestHarness()

  th.set_param( "top.src.construct",  msgs=[Bits8(2)] )
  th.set_param( "top.sink.construct", msgs=[Bits8(2),Bits8(1)] )

  run_sim( th, cmdline_opts, duts=['dut'] )

#-------------------------------------------------------------------------
# test_3
#-------------------------------------------------------------------------
# If we send in a two then dut should produce two messages (3,2,1)

def test_3( cmdline_opts ):

  th = TestHarness()

  th.set_param( "top.src.construct",  msgs=[Bits8(3)] )
  th.set_param( "top.sink.construct", msgs=[Bits8(3),Bits8(2),Bits8(1)] )

  run_sim( th, cmdline_opts, duts=['dut'] )

#-------------------------------------------------------------------------
# test_10
#-------------------------------------------------------------------------
# If we send in 10 then dut should produce 10 messages

def test_10( cmdline_opts ):

  th = TestHarness()

  resp_msgs = [ Bits8(x) for x in reversed(range(1,11)) ]

  th.set_param( "top.src.construct",  msgs=[Bits8(10)] )
  th.set_param( "top.sink.construct", msgs=resp_msgs )

  run_sim( th, cmdline_opts, duts=['dut'] )

#-------------------------------------------------------------------------
# test_parameterized
#-------------------------------------------------------------------------
# Example of a parameterized test

@pytest.mark.parametrize(
  "req_msg,resp_msgs",
  [( [Bits8(7)],  [ Bits8(x) for x in reversed(range(1,8))  ] ),
   ( [Bits8(13)], [ Bits8(x) for x in reversed(range(1,14)) ] ),
   ( [Bits8(27)], [ Bits8(x) for x in reversed(range(1,28)) ] )]
)
def test_param( req_msg, resp_msgs, cmdline_opts ):

  th = TestHarness()

  th.set_param( "top.src.construct",  msgs=req_msg   )
  th.set_param( "top.sink.construct", msgs=resp_msgs )

  run_sim( th, cmdline_opts, duts=['dut'] )

#-------------------------------------------------------------------------
# test_multiple
#-------------------------------------------------------------------------
# Send in multiple transactions

def test_multiple( cmdline_opts ):

  th = TestHarness()

  req_msgs  = [ Bits8(3), Bits8(2), Bits8(0), Bits8(1) ]
  resp_msgs = [
    Bits8(3), Bits8(2), Bits8(1),
    Bits8(2), Bits8(1),
    # no messages when input is zero
    Bits8(1),
  ]

  th.set_param( "top.src.construct",  msgs=req_msgs  )
  th.set_param( "top.sink.construct", msgs=resp_msgs )

  run_sim( th, cmdline_opts, duts=['dut'] )

#-------------------------------------------------------------------------
# test_multiple_delay
#-------------------------------------------------------------------------
# Send in multiple transactions with delays

def test_multiple_delay( cmdline_opts ):

  th = TestHarness()

  req_msgs  = [ Bits8(3), Bits8(2), Bits8(0), Bits8(1) ]
  resp_msgs = [
    Bits8(3), Bits8(2), Bits8(1),
    Bits8(2), Bits8(1),
    # no messages when input is zero
    Bits8(1),
  ]

  th.set_param( "top.src.construct",
                msgs=req_msgs, initial_delay=3, interval_delay=0 )

  th.set_param( "top.sink.construct",
                msgs=resp_msgs, initial_delay=10, interval_delay=5 )

  run_sim( th, cmdline_opts, duts=['dut'] )

#-------------------------------------------------------------------------
# test_random
#-------------------------------------------------------------------------
# Send in random transactions

def test_random( cmdline_opts ):

  th = TestHarness()

  req_msgs  = []
  resp_msgs = []
  for i in range(0,10):
    y = random.randint(0,20)
    req_msgs  += [ Bits8(y) ]
    resp_msgs += [ Bits8(x) for x in reversed(range(1,y+1)) ]

  th.set_param( "top.src.construct",  msgs=req_msgs  )
  th.set_param( "top.sink.construct", msgs=resp_msgs )

  run_sim( th, cmdline_opts, duts=['dut'] )

#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

req_msgs_3      = [ Bits8(3) ]
resp_msgs_3     = [ Bits8(3), Bits8(2), Bits8(1) ]

req_msgs_3_2    = [ Bits8(3), Bits8(2) ]
resp_msgs_3_2   = [ Bits8(3), Bits8(2), Bits8(1), Bits8(2), Bits8(1) ]

req_msgs_3_2_1  = [ Bits8(3), Bits8(2), Bits8(1) ]
resp_msgs_3_2_1 = [ Bits8(3), Bits8(2), Bits8(1), Bits8(2), Bits8(1), Bits8(1) ]

def mk_msgs( values ):
  req_msgs  = []
  resp_msgs = []
  for y in values:
    req_msgs  += [ Bits8(y) ]
    resp_msgs += [ Bits8(x) for x in reversed(range(1,y+1)) ]
  return req_msgs,resp_msgs

req_msgs_seq,resp_msgs_seq     = mk_msgs( range(1,10) )
req_msgs_large,resp_msgs_large = mk_msgs( [20,20,20,20,20] )
req_msgs_rand,resp_msgs_rand   = mk_msgs( random.sample(range(0,20),10) )

test_case_table = mk_test_case_table([
  (                   "req_msgs        resp_msgs        src_delay sink_delay"),
  [ "basic_3_0x0",     req_msgs_3,     resp_msgs_3,     0,        0,         ],
  [ "basic_3_2_0x0",   req_msgs_3_2,   resp_msgs_3_2,   0,        0,         ],
  [ "basic_3_2_1_0x0", req_msgs_3_2_1, resp_msgs_3_2_1, 0,        0,         ],
  [ "seq_0x0",         req_msgs_seq,   resp_msgs_seq,   0,        0,         ],
  [ "large_0x0",       req_msgs_large, resp_msgs_large, 0,        0,         ],
  [ "large_5x0",       req_msgs_large, resp_msgs_large, 5,        0,         ],
  [ "large_0x5",       req_msgs_large, resp_msgs_large, 0,        5,         ],
  [ "large_3x9",       req_msgs_large, resp_msgs_large, 3,        9,         ],
  [ "rand_0x0",        req_msgs_rand,  resp_msgs_rand,  0,        0,         ],
  [ "rand_5x0",        req_msgs_rand,  resp_msgs_rand,  5,        0,         ],
  [ "rand_0x5",        req_msgs_rand,  resp_msgs_rand,  0,        5,         ],
  [ "rand_3x9",        req_msgs_rand,  resp_msgs_rand,  3,        9,         ],
])

#-------------------------------------------------------------------------
# Test cases
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test_case( test_params, cmdline_opts ):

  th = TestHarness()

  th.set_param( "top.src.construct",
    msgs=test_params.req_msgs,
    initial_delay=test_params.src_delay,
    interval_delay=test_params.src_delay )

  th.set_param( "top.sink.construct",
    msgs=test_params.resp_msgs,
    initial_delay=test_params.src_delay,
    interval_delay=test_params.src_delay )

  run_sim( th, cmdline_opts, duts=['dut'] )

