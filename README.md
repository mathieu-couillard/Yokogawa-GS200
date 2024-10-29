# Yokogawa-GS200
Python driver for for Yokogawa GS200 DC voltage/current source.
This driver does not include all the commands. The sense commands have not been written yet.

# Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Requirements
pyvisa

visa backend (ivi, pyvisa-py, R&S)

# Usage

Methods with write and query will default to the query when no argument is given.
```
source.level() # query the set level
source.level(0.1) # set the level 0.1 volts or amperes depending on the set function is constant voltage or constant current, respectively. 
```

Simple examples code to set to the device to constant current of 150 mA and a protection voltage limit of 1 V.

```
addr='TCPIP::192.168.0.125::INSTR'
source = gs200(addr, visa_backend='@py')
source.function('current') # Set to constant current
source.level(0.15)  # Set level to 150 mA
source.protection_voltage(1) # Set protection voltage to 1 V
source.output(True) # turn on output
    
print(source.level()) # Get the set level and print value
source.output(False)

```
