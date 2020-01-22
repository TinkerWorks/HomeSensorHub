#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#           bme280.py
#  Read data from a digital pressure sensor.
#
#  Official datasheet available from :
#  https://www.bosch-sensortec.com/bst/products/all_products/bme280
#
# Author : Matt Hawkins
# Date   : 21/01/2018
#
# https://www.raspberrypi-spy.co.uk/
#
#--------------------------------------
import smbus
import time
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte

DEVICE = 0x39 # Default device I2C address

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

DATA0LOW = 0X14
DATA0HIGH = 0X15
DATA1LOW = 0X16
DATA1HIGH = 0X17

# Nominal 400 ms integration.
# Specifies the integration time in 2.7-ms intervals
# 400/2.7 = 148
NOM_INTEG_CYCLE = 148

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

def getShort(data, index):
  # return two bytes from data as a signed 16-bit value
  return c_short((data[index+1] << 8) + data[index]).value

def getUShort(data, index):
  # return two bytes from data as an unsigned 16-bit value
  return (data[index+1] << 8) + data[index]

def getChar(data,index):
  # return one byte from data as a signed char
  result = data[index]
  if result > 127:
    result -= 256
  return result

def getUChar(data,index):
  # return one byte from data as an unsigned char
  result =  data[index] & 0xFF
  return result

def readBME280ID(addr=DEVICE):
  # Chip ID Register Address
  REG_ID     = 0x12
  (rawread, constant) = bus.read_i2c_block_data(addr, REG_ID | COMMAND_CMD | TRANSACTION, 2)
  part_no = (rawread >> 4) & 0xF
  rev_no  = (rawread >> 0) & 0xF

  print(bin(rawread))
  print(bin(constant))

  return (part_no, rev_no)

def readBME280All(addr=DEVICE):
  DATA_REG = 0x14
  (data0low, )  = bus.read_i2c_block_data(addr, COMMAND_CMD | TRANSACTION | DATA0LOW, 1)
  (data0high, ) = bus.read_i2c_block_data(addr, COMMAND_CMD | TRANSACTION | DATA0HIGH, 1)
  (data1low, )  = bus.read_i2c_block_data(addr, COMMAND_CMD | TRANSACTION | DATA1LOW, 1)
  (data1high, ) = bus.read_i2c_block_data(addr, COMMAND_CMD | TRANSACTION | DATA1HIGH, 1)

  #data0 = data0high << 8 | data0low
  #data1 = data1high << 8 | data1low

  ch0 = data0 = data0high * 256 + data0low
  ch1 = data1 = data1high * 256 + data1low

  Lux = calculateLux(ch0, ch1, 2, NOM_INTEG_CYCLE);

  print("data 0 " + hex(data0))
  print("data 1 " + hex(data1))

  print("Lux: ", Lux)

  return Lux

def WaveShare_TSL2581(addr=DEVICE):
  bus.write_byte_data(COMMAND_CMD  | CONTROL, CONTROL_POWERON);


def TSL2581_config(addr=DEVICE):
  bus.write_byte_data(addr, COMMAND_CMD | TIMING, INTEGRATIONTIME_400MS)  # 400MS
  bus.write_byte_data(addr, COMMAND_CMD | CONTROL, ADC_EN | CONTROL_POWERON)
  bus.write_byte_data(addr, COMMAND_CMD | INTERRUPT, INTR_INTER_MODE) # Every ADC cycle generates interrupt
  bus.write_byte_data(addr, COMMAND_CMD | ANALOG, GAIN_16X) #GAIN = 16

# Arguments: unsigned int iGain - gain, where 0:1X, 1:8X, 2:16X, 3:128X
# unsigned int tIntCycles - INTEG_CYCLES defined in Timing Register
def calculateLux(ch0, ch1, iGain, tIntCycles):
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
  if (tIntCycles == NOM_INTEG_CYCLE):
    chScale0 = 65536
    #chScale0 = (1 << (CH_SCALE))
  else:
    chScale0 = (NOM_INTEG_CYCLE << CH_SCALE) / tIntCycles

  if (iGain == 0): # 1x gain
      chScale1 = chScale0; # No scale. Nominal setting
  elif (iGain == 1): # 8x gain
      chScale0 = chScale0 >> 3; # Scale/multiply value by 1/8
      chScale1 = chScale0;
  elif (iGain == 2): # 16x gain
      chScale0 = chScale0 >> 4; # Scale/multiply value by 1/16
      chScale1 = chScale0;
  elif (iGain == 3): # 128x gain
      chScale1 = chScale0 / CH1GAIN128X;
      chScale0 = chScale0 / CH0GAIN128X;

  # scale the channel values
  channel0 = (ch0 * chScale0) >>  CH_SCALE
  channel1 = (ch1 * chScale1) >>  CH_SCALE

  print("ch 0 " + hex(ch0))
  print("ch 1 " + hex(ch1))

  print("channel 0 " + hex(channel0))
  print("channel 1 " + hex(channel1))

  # find the ratio of the channel values (Channel1/Channel0)
  if (channel0 != 0):
    ratio1 = (channel1 << (RATIO_SCALE + 1)) / channel0

  ratio = (ratio1 + 1) >> 1 # round the ratio value

  if ((ratio >= 0) and (ratio <= K1C)):
    b = B1C
    m = M1C
  elif (ratio <= K2C):
    b = B2C
    m = M2C
  elif (ratio <= K3C):
    b = B3C
    m = M3C
  elif (ratio <= K4C): #276
    b = B4C
    m = M4C
  elif (ratio > K5C): #276
    b = B5C
    m = M5C

  temp = ((channel0 * b) - (channel1 * m))
  #  temp += (1 << (LUX_SCALE - 1))
  temp = temp + 32768               # round lsb (2^(LUX_SCALE-1))
  lux_temp = temp >> LUX_SCALE      # strip off fractional portion
  return (lux_temp)                 # Signal I2C had no errors


def main():

  (part_no, rev_no) = readBME280ID()
  print ("Part Number     :", part_no)
  print ("Revision NUmber :", rev_no)

  TSL2581_config()
  time.sleep(1)

  # while True:
  readBME280All()


    #time.sleep(2)

if __name__=="__main__":
   main()
