import board
import neopixel
import sys

def data_indicator_light(state):
    pixels = neopixel.NeoPixel(board.D12, 2)
    
    if state == '1':
        pixels.fill((0,150,150))
        
    if state == '0':
        pixels.fill((255,0,0))
        
    if state == '2':
        pixels.fill((0,255,0))
    
    if state == '3':
        pixels.fill((255,255,255))
    
    
if __name__ == '__main__' :
    
    data_indicator_light(*sys.argv[1:])