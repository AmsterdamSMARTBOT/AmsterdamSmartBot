'''
Created on 06 giu 2017

@author: ROCCO - GERARDO
'''

import aiml

# Create the kernel and learn AIML files   
def initializeBot():
    kernel = aiml.Kernel()
    kernel.learn("std-startup.xml")
    kernel.respond("load aiml b")
    return kernel