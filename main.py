import network
import time
import socket
from machine import Pin

led = Pin('LED', Pin.OUT)

def web_page(state):
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>LED Control</title>
            </head>
            <body>
                <form action="./lighton">
                    <input type="submit" value="Light on" />
                </form>
                <form action="./lightoff">
                    <input type="submit" value="Light off" />
                </form>
                <p>LED is {state}</p>
            </body>
            </html>
            """
    return str(html)

def ap_mode(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    while ap.active() == False:
        pass
    
    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
    s.bind(('', 80)) #port binding
    s.listen(5) # number of connectable devices

    led_status = 'Off'
    
    while True:
      conn, addr = s.accept()
      print('Got a connection from %s' % str(addr))
      request = conn.recv(1024)
      print('Content = %s' % str(request))
      request = str(request)

      try:
          request = request.split()[1]
      except IndexError:
          pass
        
      if request == '/lighton?':
          led.on()
          led_status = 'On'
      elif request =='/lightoff?':
          led.off()
          led_status = 'Off'

      response = web_page(led_status)
      conn.send(response)
      conn.close()



ap_mode('NAME','PASSWORD')