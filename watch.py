#!/usr/bin/python
import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)

#gpio pin the target switch is on
target = 9
#gpio pin the LED will be on
led = 10
#gpio pin the Relay will be on
relay = 11
#set hitpoints for target
hp = 30

GPIO.setup(led, GPIO.OUT)
GPIO.setup(relay, GPIO.OUT)
GPIO.setup(target, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(relay, 0)
GPIO.output(led, 0)

prev_input = 0

def listenmode( hp , prev_input , iterations):
 print("Iterations %d") % iterations
 while (iterations != 0):
  input = GPIO.input(target)
  #print input
  if (input):
   print "Input: %d" % input
   hp = hp - 1
   if (hp == 28):
    print "double tap detected %d" % hp
    #turn on relay, keep on for relayiterations = 243 or until tapped again. 243 = one minute on raspberry pi b+
    relayiterations = 243
    print "double tap holding %d" % hp
    GPIO.output(relay, 1)
    while(relayiterations != 0):
     #debounce to give user time to move away
     time.sleep(0.25)
     input = GPIO.input(target)
     prev_input = 0
     input = GPIO.input(target)
     if ((not prev_input) and input):
      print "cancel double tap holding %d" % input
      GPIO.output(relay, 0)
      break
     #else:
      #print "continue double tap holding %d" % input      
     #time.sleep(0.05)
     relayiterations = relayiterations - 1
    #timeout
    GPIO.output(relay, 0)
     #debug - takes a billion years to print
     #print relayiterations
      
   if (hp == 29):
    print "single tap detected %d" % hp
    GPIO.output(relay, 0)
   if (hp < 28):
    print "hold detected %d" % hp
    while True:
     prev_input = 0
     input = GPIO.input(target)
     if ((not prev_input) and input):
      print "hold detected %d" % hp
      GPIO.output(relay, 1)
     else:
      GPIO.output(relay, 0)
      break
   #prev_input = input
   #return ( hp, prev_input )

   #slight pause to debounce
   time.sleep(0.25)
  iterations = iterations - 1
  #print iterations
 return ( hp, prev_input )

while True:
 prev_input = 0
 hp = 30
 input = GPIO.input(target)
 if ((not prev_input) and input):
  print "input %s, previously %s" % (input, prev_input)
  print "HP: %d" % hp
  iterations = 100000
  #print "Iterations: %s" % iterations
  GPIO.output(led, 1)
  hp, prev_input = listenmode( hp, prev_input, iterations )
  GPIO.output(led, 0)
  print "HP: %d" % hp
 
 time.sleep(.05)

GPIO.cleanup()
