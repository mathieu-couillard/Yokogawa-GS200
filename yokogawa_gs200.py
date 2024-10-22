import pyvisa as visa


class gs200:
    def __init__(self, address, verbatim=False, visa_backend=''):
        self._inst = visa.ResourceManager(visa_backend).open_resource(address)
        # self._inst.timeout = 2500
        self._inst.write_termination = '\r'
        self._inst.read_termination = '\n'
        # self._inst.inst.chunk_size=1024
        identity = self.identify()
        print("Identity: {}".format(identity))
        if "YOKOGAWA,GS210" not in identity or"YOKOGAWA,GS211" not in identity :
            Exception("WARNING: This IP:{} is not a Yokogawa GS200 DC source."
                      "\nSome commands may not work.".format(address))

        self.verbatim = verbatim  # Print every command before sending
#################
# Common Commands
#################


    def close(self):
        self._inst.close()

    def identify(self):
        return self._com("*IDN?")

    def idn(self):
        return self._com("*IDN?")

    def operation_complete(self):
        return self._com("*OPC?")
#################
# Output Command
#################
    def output(self, state='?'):
        states = {'true': ' on',
                  'on' : ' on',
                  True : ' on',
                  'false': ' off',
                  'off': ' off',
                  False: ' false',
                  '?': '?'
                  }
        if state in states:
            return self._com(':OUTPut{}'.format(states[state]))
        else:
            raise Exception('InvalideOutputStateException. Argument must be \'on\' or \'off\'.' )
#################
# Source Commands
#################

    def function(self, function='?'):
        functions={'curr': ' current',
                   'current': ' current',
                   'volt':' voltage',
                   'voltage': ' voltage',
                   '?':'?'
                   }
        if function in functions:
            return self._com('source:function{}'.format(functions[function]))
        else:
            raise Exception('InvalidefunctionException. Argument must be \'current\' or \'voltage\'' )


    def range(self, range='?'):
        # get function

        ranges_v = [0.01, 0.1, 1, 10, 30]
        ranges_i = [1,10,100,200]
        if self.function()=='CURR':
            ranges = ranges_i
        else:
            ranges = ranges_v
            
        if range in ranges or float(range) in ranges:        
            range = " " + str(range)
        elif range == '?':
            pass
        else:
            raise Exception('InvalidArgumentException. Range must be 0.01, 0.1, 1, 10, 30 for a voltage source or 1, 10, 100, 200 for a current source.')
        return self._com('source:range{}'.format(range))
            

    def level(self, level='?'):
        ranges = {0.01 : 0.012,
                  0.1  : 0.12,
                  1    : 1.2,
                  10   : 12.,
                  30   : 32.,
                  1    : 1.2,
                  10   : 12.,
                  100  : 120.,
                  200  : 200.
                  }
            
        if level == 'auto':
            level = " auto"
        elif level.isnumeric():
            max_level = float(ranges[float(self.range())])
            if abs(float(level)) <= max_level:
                 level = " " + str(level)
            else:
                raise Exception('OutOfRangeException: Range is set to \u00B1{}.'.format(max_level))
        elif level != '?':
            raise Exception('InvalidArgumentException: Level must be either numeric, \'auto\' or \'?\'.')
        
        return self._com('source:level{}'.format(level))
 
            
    def protection_voltage(self, voltage='?'):
        if str(voltage).isnumeric() and float(voltage)<=32:
            voltage = " " + voltage
        elif voltage != '?':
            raise Exception('InvalidArgumentException: Argument must be either a number below 32 or \'?\'.')
        
        return self._com(':SOURce:PROTection:VOLTage{}'.format(voltage))
            
    def protection_current(self, current='?'):
         if str(current).isnumeric() and float(current)<=200:
            current = " " + current
         elif current != '?':
            raise Exception('InvalidArgumentException: Argument must be either a number below 200 or \'?\'.')

         return self._com(':SOURce:PROTection:CURRent{}'.format(current))
###############
# Program Commands
###############


###############
# Sense Commands
###############


###############
# Read Commands
###############
    def initiate(self):
        return self._com(':INITiate')

    def fetch(self):
         return self._com(':FETCh?')

    def read(self):
        return self._com(':READ?')

    def measure(self):
        return self._com(':MEASure?')
    
###############
# Trace Commands
###############

###############
# Route Commands (BNC I/O)
###############
    def bnc_out(self, option='?'):
        option = option.lower()
        options ={'trig', 'trigger'
                  'output', 'outp',
                  'read', 'ready',
                 }

        if option in options:
            option = " " + option
        elif option != '?':
            raise Exception('InvalidArgumentException: Argument must be either \'trigger\',  \'output \',  \'ready\' or \'?\'.')
        
        return self._com(':ROUTe:BNCO{}'.format(option))

    
    def bnc_in(self, option='?'):
        option = option.lower()
        options ={'trig', 'trigger'
                  'output', 'outp',
                 }

        if option in options:
            option = " " + option
        elif option != '?':
            raise Exception('InvalidArgumentException: Argument must be either \'trigger\',  \'output \' or \'?\'.')
            
        return self._com(':ROUTe:BNCI{}'.format(option))
    
###############
# System Commands
###############

    def error(self):
        return self._com(':SYSTem:ERRor')
        

    def local(self):
        return self._com(':SYSTem:LOCal')
    
    def remote(self):
        return self._com(':SYSTem:REMote')


    def line_frequency(self):
        # The GS200 automatically measures the line frequency
        return self._com(':SYSTem:LFRequency?')

        
###############
# Status Commands
###############
    def condition(self):
        return self._com(':STATus:CONDition?')
        
    def event(self):
        return self._com(':STATus:EVENt?')
    
    def status_enable(self, register='?'):
        if 
        return self._com(':STATus:ENABle{}'.format(register))
        
    def status_error(self):
        # Same as error()
        return self._com(':STATus:ERRor?')

###############
# Communication Command
###############
    def _com(self, cmd):
        if self.verbatim:
            print(cmd)
        if cmd[-1] == '?':
            value = self._inst.query(cmd)
            if value.isnumeric():
                return float(value)
            else:
                return value
        else:
            self._inst.write(cmd)
            return "Sent: " + cmd




if __name__ == '__main__':
    addr='192.168.*.*'
    source = gs200(addr, visa_backend='@py')
    source.function('current')
    
