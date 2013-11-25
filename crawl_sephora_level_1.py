#!/usr/bin/python2.7

""" Crawls sephora reviews, level 1: product listings.
    See crawl_sephora_level_2.py for crawling product reviews.
"""

import argparse
import os
import utils

CATEGORIES = {
    'bath_and_body': 'http://reviews.sephora.com/8723/cat140014/category.htm',
    'fragrance': 'http://reviews.sephora.com/8723/cat160006/category.htm',
    'hair': 'http://reviews.sephora.com/8723/cat130038/category.htm',
    'makeup': 'http://reviews.sephora.com/8723/cat140006/category.htm',
    'men': 'http://reviews.sephora.com/8723/cat130044/category.htm',
    'skin_care': 'http://reviews.sephora.com/8723/cat150006/category.htm',
    'tools_and_brushes':
        'http://reviews.sephora.com/8723/cat130042/category.htm',
}

def get_url_for_page(base_url, page_num):
  return '%s?pageNumber=%d' % (base_url, page_num)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--output_dir', required=True)
  parser.add_argument('--overwrite', action='store_true')
  args = parser.parse_args()

  for category, url in CATEGORIES.items():
    print '######## Processing category: %s ########' % category
    output_path = '%s/%s-1.html' % (args.output_dir, category)
    assert utils.download_with_retries(url, output_path, args.overwrite)
    with open(output_path, 'r') as fp:
      content = fp.read()
    num_pages = utils.get_num_pages(content)
    assert num_pages > 0
    print '#### %d pages in category ####' % num_pages
    for i in range(2, num_pages+1):
      output_path = '%s/%s-%d.html' % (args.output_dir, category, i)
      assert utils.download_with_retries(
          get_url_for_page(url, i), output_path, args.overwrite)

if __name__ == '__main__':
  main()

