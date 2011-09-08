#!/usr/bin/python

# plethora.py - Python Lightweight Executable Tester

import sys
import csv
from subprocess import Popen, PIPE, STDOUT

if len(sys.argv) == 1:
  print "This program requires a recipe file."
  print "Ex: plth.py </path/to/recipe_file.txt>"
  sys.exit()

try:
   open(sys.argv[1])
except IOError as e:
   print 'Recipe file "', sys.argv[1], '" not found.  Check the location and try again.'
   sys.exit(1)
 
"""Read the recipe file."""
cmdlines = []
test_report = []
input_file = open(sys.argv[1])
for line in input_file:
  cmdlines.append(line)

"""
Remove the cmdline target executable, as listed in the recipe file, 
from the top of the stack, before processing.
"""
cli_target = cmdlines[0].replace(',','').replace('\"','').strip()
cmdlines.pop(0)
#TODO: use csv.Sniffer, if possible, to be more forgiving of different CSV types
reader = csv.reader(cmdlines, delimiter=',', quotechar='"') 

""" Do most of the work here.  Eventually modularize this. """

fail_count = 0
pass_count = 0
for row in reader:
  test_result=''
  execution_record=[]
  params = row[0]
  expected_substring = row[1]
  cmd = cli_target + " " + params.strip()
#TODO: Implement timeouts
  print "EXECUTING COMMAND: ", cmd
  p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

  p.wait()
  return_code = p.returncode
  
  """ 
  Determine whether the output (first checking stdin then stderr)
  matches what we want to see contained therein.
  """
  std_output = p.stdout.read()
  output_scan = std_output.find(expected_substring)
  if output_scan == -1:
     test_result = "FAIL"
     fail_count += 1
  else:
     test_result = "PASS"
     pass_count += 1

  """ Summarize results of this test. """
#  print "Search result: ", output_scan
  execution_record.append(cmd)
  execution_record.append(return_code)
  execution_record.append(expected_substring)
  execution_record.append(test_result)
  execution_record.append(std_output)
  test_report.append(execution_record) 

""" Print results """

for record in test_report:
#TODO: output this to a text document, preferably nicely formatted.
  test_executed_command = record[0]
  test_return_code = record[1]
  test_substring = record[2]
  test_result = record[3]
  test_std_output = record[4]
  print '+ Command: ', test_executed_command
  print '+ Return Code: ', test_return_code
  print '+ Test result:', test_result
  print '`- Expected content (substring): "', test_substring, '"'
  print '`- Output: \n'
  print test_std_output
  print '-----------------------------------------------------\n';
print '=====================================================';
print 'Total number of passing tests: ', pass_count
print 'Total number of failing tests: ', fail_count
print '=====================================================';
 
