#!/usr/bin/python2.7

import os
import time

######## Downloading utils ########

WGET = '/opt/local/bin/wget'
RETRIES = 10
SLEEP_SEC = 10

def download_with_sleep(url, output_path, sleep_sec=SLEEP_SEC):
  assert not os.path.isfile(output_path)
  print 'Sleeping for %d seconds' % sleep_sec
  time.sleep(sleep_sec)
  command = '%s "%s" -q -O "%s"' % (WGET, url, output_path)
  print 'Running command: %s' % command
  r = os.system(command)
  if r == 0:
    assert os.path.isfile(output_path)
    return True
  if os.path.isfile(output_path):
    os.remove(output_path)
  return False

def download_with_retries(url, output_path, overwrite, retries=RETRIES):
  if os.path.isfile(output_path):
    if not overwrite:
      print '%s exists and not overwritable, skipping' % output_path
      return True
    os.remove(output_path)
  for i in range(retries):
    if download_with_sleep(url, output_path):
      print 'Downloading %s succeeded' % url
      return True
    print 'Downloading %s failed (%d)' % (url, i+1)
  print 'Downloading %s failed permanently' % url
  return False

######## Parsing utils ########

PAGE_NUMBER_LABEL = '<span class="BVRRPageLink BVRRPageNumber">'

def get_num_pages(content):
  # By default there is only one page, in which case PAGE_NUMBER_LABEL will
  # not be found.
  num_pages = 1
  start = 0
  while True:
    p0 = content.find(PAGE_NUMBER_LABEL, start)
    if p0 < 0:
      break
    p2 = content.find('</a>\n</span>', p0)
    p1 = content.rfind('>', p0, p2)
    assert p1 > p0
    assert p2 > p1
    num_pages = max(num_pages, int(content[p1+1:p2]))
    start = p2+1
  return num_pages

