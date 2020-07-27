#!/usr/bin/env python3
import logging
import smbus
import time
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte

class TSL258x:

    addr = 0x39 # Default device I2C address

    COMMAND_CMD = 0x80
    TRANSACTION = 0x40

    CONTROL =   0x00
    TIMING =    0x01
    INTERRUPT = 0X02
    THLLOW = 0x03
    THLHIGH = 0X04
    THHLOW = 0x05
    THHHIGH = 0X06
    ANALOG = 0X07

    ADC_EN = 0X02
    CONTROL_POWERON =   0x01
    CONTROL_POWEROFF =  0x00
    INTR_TEST_MODE = 0X30
    INTR_INTER_MODE = 0X1F

    INTEGRATIONTIME_Manual = 0x00
    INTEGRATIONTIME_2Z7MS = 0xFF
    INTEGRATIONTIME_5Z4MS = 0xFE
    INTEGRATIONTIME_51Z3MS = 0xED
    INTEGRATIONTIME_100MS = 0xDB
    INTEGRATIONTIME_200MS = 0xB6
    INTEGRATIONTIME_400MS = 0x6C
    INTEGRATIONTIME_688MS = 0x01

    GAIN_1X = 0x00
    GAIN_8X = 0x01
    GAIN_16X = 0x02
    GAIN_111X = 0x03

    REG_ID = 0x12

    DATA0LOW = 0X14
    DATA0HIGH = 0X15
    DATA1LOW = 0X16
    DATA1HIGH = 0X17

    # Nominal 400 ms integration.
    # Specifies the integration time in 2.7-ms intervals
    # 400/2.7 = 148
    NOMINAL_INTEGRATION_CYCLES = 148

    # scale channel values by 2^16
    CH_SCALE = 16

    LUX_SCALE   = 16 # scale by 2^16
    RATIO_SCALE = 9  # scale ratio by 2^9

    #---------------------------------------------------
    # Gain scaling factors
    #---------------------------------------------------
    CH0GAIN128X = 107 # 128X gain scalar for Ch0
    CH1GAIN128X = 115 # 128X gain scalar for Ch1

    #---------------------------------------------------
    K1C = 0x009A # 0.30 * 2^RATIO_SCALE
    B1C = 0x2148 # 0.130 * 2^LUX_SCALE
    M1C = 0x3d71 # 0.240 * 2^LUX_SCALE

    K2C = 0x00c3 # 0.38 * 2^RATIO_SCALE
    B2C = 0x2a37 # 0.1649 * 2^LUX_SCALE
    M2C = 0x5b30 # 0.3562 * 2^LUX_SCALE

    K3C = 0x00e6 # 0.45 * 2^RATIO_SCALE
    B3C = 0x18ef # 0.0974 * 2^LUX_SCALE
    M3C = 0x2db9 # 0.1786 * 2^LUX_SCALE

    K4C = 0x0114 # 0.54 * 2^RATIO_SCALE
    B4C = 0x0fdf # 0.062 * 2^LUX_SCALE
    M4C = 0x199a # 0.10 * 2^LUX_SCALE

    K5C = 0x0114 # 0.54 * 2^RATIO_SCALE
    B5C = 0x0000 # 0.00000 * 2^LUX_SCALE
    M5C = 0x0000 # 0.00000 * 2^LUX_SCALE


    bus = smbus.SMBus(1) # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
                         # Rev 1 Pi uses bus 0

    def __init__(self):
        self.gain_map = { 1 : self.GAIN_1X,
                          8 : self.GAIN_8X,
                         16 : self.GAIN_16X,
                        111 : self.GAIN_111X}

        self.integration_map = { 1 : self.INTEGRATIONTIME_2Z7MS,
                                 2 : self.INTEGRATIONTIME_5Z4MS,
                                19 : self.INTEGRATIONTIME_51Z3MS,
                                37 : self.INTEGRATIONTIME_100MS,
                                74 : self.INTEGRATIONTIME_200MS,
                               148 : self.INTEGRATIONTIME_400MS,
                               255 : self.INTEGRATIONTIME_688MS}

    def probe():
        tsl = TSL258x()
        try:
            (part_no, rev_no) = tsl.readID()
            return tsl
        except OSError as ose:
            return None

    def readID(self):
      # Chip ID Register Address
      REG_REQUEST = self.REG_ID | self.COMMAND_CMD | self.TRANSACTION
      (rawread, constant) = self.bus.read_i2c_block_data(self.addr, REG_REQUEST, 2)

      part_no = (rawread >> 4) & 0xF
      rev_no  = (rawread >> 0) & 0xF
      return (part_no, rev_no)

    @property
    def part_no(self):
        (part_no, rev_no) = self.readID()
        return part_no

    @property
    def rev_no(self):
        (part_no, rev_no) = self.readID()
        return rev_no

    def read(self):
      (data0low, )  = self.bus.read_i2c_block_data(self.addr, self.COMMAND_CMD | self.TRANSACTION | self.DATA0LOW, 1)
      (data0high, ) = self.bus.read_i2c_block_data(self.addr, self.COMMAND_CMD | self.TRANSACTION | self.DATA0HIGH, 1)
      (data1low, )  = self.bus.read_i2c_block_data(self.addr, self.COMMAND_CMD | self.TRANSACTION | self.DATA1LOW, 1)
      (data1high, ) = self.bus.read_i2c_block_data(self.addr, self.COMMAND_CMD | self.TRANSACTION | self.DATA1HIGH, 1)

      ch0 = ch0 = data0high * 256 + data0low
      ch1 = ch1 = data1high * 256 + data1low

      logging.debug("Channel ALL value: 0x%x " % ch0)
      logging.debug("Channel  IR value: 0x%x " % ch1)

      Lux = self.calculateLux(ch0, ch1);

      logging.debug("Light: %d lux" % Lux)

      return Lux

    def power_on(self):
      bus.write_byte_data(self.COMMAND_CMD | self.CONTROL, self.CONTROL_POWERON);

    def config(self, gain = 16, integration_cycles = NOMINAL_INTEGRATION_CYCLES):

      self.integration_cycles = integration_cycles
      timing_value = self.integration_map[integration_cycles]

      self.bus.write_byte_data(self.addr, self.COMMAND_CMD | self.TIMING, timing_value)


      self.bus.write_byte_data(self.addr, self.COMMAND_CMD | self.CONTROL, self.ADC_EN | self.CONTROL_POWERON)
      # Every ADC cycle generates interrupt
      self.bus.write_byte_data(self.addr, self.COMMAND_CMD | self.INTERRUPT, self.INTR_INTER_MODE)
      #GAIN = 16

      self.gain = gain
      gain_value = self.gain_map[self.gain]

      self.bus.write_byte_data(self.addr, self.COMMAND_CMD | self.ANALOG, gain_value)

    # Arguments: unsigned int iGain - gain, where 0:1X, 1:8X, 2:16X, 3:128X
    # unsigned int tIntCycles - INTEG_CYCLES defined in Timing Register
    def calculateLux(self, ch0, ch1):
      chScale0 = 0
      chScale1 = 0
      channel1 = 0
      channel0 = 0
      temp = 0
      ratio1 = 0
      ratio = 0
      lux_temp = 0
      b = 0
      m = 0

      # No scaling if nominal integration (148 cycles or 400 ms) is used
      if (self.integration_cycles == self.NOMINAL_INTEGRATION_CYCLES):
        chScale0 = 65536
        #chScale0 = (1 << (CH_SCALE))
      else:
        chScale0 = (NOMINAL_INTEGRATION_CYCLES << CH_SCALE) / tIntCycles

      if (self.gain == 1): # 1x gain
          chScale1 = chScale0; # No scale. Nominal setting
      elif (self.gain == 8): # 8x gain
          chScale0 = chScale0 >> 3; # Scale/multiply value by 1/8
          chScale1 = chScale0;
      elif (self.gain == 16): # 16x gain
          chScale0 = chScale0 >> 4; # Scale/multiply value by 1/16
          chScale1 = chScale0;
      elif (self.gain == 111): # 128x gain
          chScale1 = chScale0 / CH1GAIN128X;
          chScale0 = chScale0 / CH0GAIN128X;

      # scale the channel values
      channel0 = (ch0 * chScale0) >>  self.CH_SCALE
      channel1 = (ch1 * chScale1) >>  self.CH_SCALE

      # find the ratio of the channel values (Channel1 / Channel0)
      if (channel0 != 0):
        ratio1 = (channel1 << (self.RATIO_SCALE + 1)) / channel0

      ratio = (ratio1 + 1) / 2 # round the ratio value

      if ((ratio >= 0) and (ratio <= self.K1C)):
        b = self.B1C
        m = self.M1C
      elif (ratio <= self.K2C):
        b = self.B2C
        m = self.M2C
      elif (ratio <= self.K3C):
        b = self.B3C
        m = self.M3C
      elif (ratio <= self.K4C): #276
        b = self.B4C
        m = self.M4C
      elif (ratio > self.K5C): #276
        b = self.B5C
        m = self.M5C

      temp = ((channel0 * b) - (channel1 * m))
      #  temp += (1 << (LUX_SCALE - 1))
      temp = temp + 32768               # round lsb (2^(LUX_SCALE-1))
      lux_temp = temp >> self.LUX_SCALE      # strip off fractional portion
      return (lux_temp)                 # Signal I2C had no errors

