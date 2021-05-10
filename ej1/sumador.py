from nmigen import *
from nmigen_cocotb import run
import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
from random import getrandbits


class Stream(Record):
    def __init__(self, width, **kwargs):
        Record.__init__(self, [('data', signed(width)), ('valid', 1), ('ready', 1)], **kwargs)

    def accepted(self):
        return self.valid & self.ready

    class Driver:
        def __init__(self, clk, dut, prefix):
            self.clk = clk
            self.data = getattr(dut, prefix + 'data')
            self.valid = getattr(dut, prefix + 'valid')
            self.ready = getattr(dut, prefix + 'ready')

        async def send(self, data):
            self.valid <= 1
            for d in data:
                self.data <= d
                await RisingEdge(self.clk)
                while self.ready.value == 0:
                    await RisingEdge(self.clk)
            self.valid <= 0

        async def recv(self, count):
            self.ready <= 1
            data = []
            for _ in range(count):
                await RisingEdge(self.clk)
                while self.valid.value == 0:
                    await RisingEdge(self.clk)
                data.append(self.data.value.integer)
            self.ready <= 0
            return data

class Sumador(Elaboratable):
    def __init__(self, width):
        self.a = Stream(width, name='a')
        self.b = Stream(width, name='b')
        self.r = Stream(width + 1, name='r') #output width = input width + 1

    def elaborate(self, platform):
        m = Module()
        sync = m.d.sync
        comb = m.d.comb

        print(self.a.data.shape())
        print(self.b.data.shape())
        print(self.r.data.shape())

        with m.If(self.r.accepted()):
            sync += self.r.valid.eq(0)

        with m.If(self.a.accepted() & self.b.accepted()):
            
            sync += [
                self.r.valid.eq(1),
                self.r.data.eq((self.a.data + self.b.data)) # Ya genera un numero 2'c de 9 bits 
                                                            # Suma 2 2'c de 8 bits
            ]
        comb += self.a.ready.eq((~self.r.valid) | (self.r.accepted()))
        comb += self.b.ready.eq((~self.r.valid) | (self.r.accepted()))
        return m


async def init_test(dut):
    cocotb.fork(Clock(dut.clk, 10, 'ns').start())
    dut.rst <= 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst <= 0


@cocotb.test()
async def burst(dut):
    await init_test(dut)

    stream_input_a = Stream.Driver(dut.clk, dut, 'a__')
    stream_input_b = Stream.Driver(dut.clk, dut, 'b__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')

    N = 100
    width = len(dut.a__data)
    mask = int('1' * (width+1), 2)

    data1 = [getrandbits(width) for _ in range(N)]
    data2 = [getrandbits(width) for _ in range(N)]
    
    ### Sumo en 2'c de 9 bits
    expected = []
    for (d1,d2) in zip(data1,data2):
        expected.append(
            d1 + ((d1 >> width-1)<<width) +
            d2 + ((d2 >> width-1)<<width) & mask)
    #convierto d1 y d2 a 2'c de 9 bits

    cocotb.fork(stream_input_a.send(data1))
    cocotb.fork(stream_input_b.send(data2))
    
    recved = await stream_output.recv(N)

    assert recved == expected

@cocotb.test()
async def limit_cases(dut):
    await init_test(dut)

    stream_input_a = Stream.Driver(dut.clk, dut, 'a__')
    stream_input_b = Stream.Driver(dut.clk, dut, 'b__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')

    cocotb.fork(stream_input_a.send([128]))
    cocotb.fork(stream_input_b.send([128]))
    
    recved = await stream_output.recv(1)

    assert recved == [256] 

    cocotb.fork(stream_input_a.send([0]))
    cocotb.fork(stream_input_b.send([0]))
    
    recved = await stream_output.recv(1)

    assert recved == [0]

    cocotb.fork(stream_input_a.send([0b10000001])) #-127
    cocotb.fork(stream_input_b.send([0b01111111])) #127
    
    recved = await stream_output.recv(1)

    assert recved == [0]


if __name__ == '__main__':
    core = Sumador(8)
    run(
        core, 'sumador',
        ports=
        [
            *list(core.a.fields.values()),
            *list(core.b.fields.values()),
            *list(core.r.fields.values())
        ],
        vcd_file='sumador.vcd'
    )