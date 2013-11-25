#!/usr/bin/python2.7

""" Crawls sephora reviews, level 2: product reviews.
    See crawl_sephora_level_1.py for crawling product listings.
"""

import argparse
import os
import re
import utils

PRODUCT_URL_PATTERN = 'http://reviews.sephora.com/8723/P(?P<id>\d+)/reviews.htm'
PRODUCT_PROG = re.compile(PRODUCT_URL_PATTERN)

def get_product_ids(product_file):
  with open(product_file, 'r') as fp:
    content = fp.read()
  p0 = content.find('<h1 class="BVRRSSortRowLabel">')
  assert p0 > 0
  raw_product_ids = PRODUCT_PROG.findall(content[p0:])
  # Check that each product id appears exactly three times.
  assert len(raw_product_ids) % 3 == 0
  for i in range(0, len(raw_product_ids), 3):
    assert raw_product_ids[i] == raw_product_ids[i+1]
    assert raw_product_ids[i+1] == raw_product_ids[i+2]
  return sorted(['P%s' % id for id in raw_product_ids[::3]])

def get_url_for_product(product_id):
  return 'http://reviews.sephora.com/8723/%s/reviews.htm' % product_id

def get_url_for_page(base_url, page_num):
  return '%s?page=%d' % (base_url, page_num)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--product_dir', required=True)
  parser.add_argument('--output_dir', required=True)
  parser.add_argument('--overwrite', action='store_true')
  args = parser.parse_args()

  product_pages = [f for f in os.listdir(args.product_dir)
                   if f.endswith('.html')]
  print 'Processing %d product pages' % len(product_pages)

  for i in range(len(product_pages)):
    product_page = product_pages[i]
    print '######## Processing %d/%d product pages: %s ########' % (
        i+1, len(product_pages), product_page)
    product_file = '%s/%s' % (args.product_dir, product_page)
    product_ids = get_product_ids(product_file)
    print '#### %d product ids in page ####' % len(product_ids)
    # Sanity check.
    assert len(product_ids) > 0
    assert len(product_ids) <= 20
    for j in range(len(product_ids)):
      product_id = product_ids[j]
      print '######## Processing %d/%d product ids: %s ########' % (
          j+1, len(product_ids), product_id)
      url = get_url_for_product(product_id)
      output_dir = '%s/%s' % (args.output_dir, product_id)
      if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
      output_path = '%s/1.html' % output_dir
      assert utils.download_with_retries(url, output_path, args.overwrite)
      with open(output_path, 'r') as fp:
        content = fp.read()
      num_pages = utils.get_num_pages(content)
      assert num_pages > 0
      print '#### %d pages for product id ####' % num_pages
      for k in range(2, num_pages+1):
        output_path = '%s/%d.html' % (output_dir, k)
        assert utils.download_with_retries(
            get_url_for_page(url, k), output_path, args.overwrite)

if __name__ == '__main__':
  main()

