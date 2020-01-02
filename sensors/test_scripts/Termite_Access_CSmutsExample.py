
# coding=utf-8
#******************************************************************************/

#  ████████╗███████╗██████╗ ███╗   ███╗██╗████████╗███████╗███████╗     \         /
#  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║╚══██╔══╝██╔════╝██╔════╝      `-.`-'.-'
#     ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║   █████╗  ███████╗      ,:--.--:.
#     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║   ██╔══╝  ╚════██║     / |  |  | \
#     ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║   ██║   ███████╗███████║      /\  |  /\
#     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝   ╚═╝   ╚══════╝╚══════╝      | `.:.' |

#Carson Smuts - MIT 2019
#******************************************************************************/

# Example showing the use of TerMITe Access module
# WRITTEN FOR HACK A BIKE Project


import Termite_Access
import time
from time import sleep


print("TerMITe Connecting....")
myTermite = Termite_Access.termiteObject()
#myTermite2 = Termite_Access.termiteObject()

# Switch to JSON - this is optional
myTermite.activateCSV()

while True:
    time.sleep(0.1)
    #tmtValue = myTermite.termiteRunner()
    #myTermite.termiteValue
    print(myTermite.termiteValue)
 #   print(myTermite2.termiteValue)

