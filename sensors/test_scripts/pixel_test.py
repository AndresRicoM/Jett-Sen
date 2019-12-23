import board
import neopixel

pixels = neopixel.NeoPixel(board.D12, 2)
    
pixels.fill((255,255,0))
