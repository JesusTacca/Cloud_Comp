""" Assignment 6: PageRank. """
from bs4 import BeautifulSoup
from sortedcontainers import SortedList, SortedSet, SortedDict
from collections import Counter
import glob
import os


def compute_pagerank(urls, inlinks, outlinks, b=.85, iters=20):
    page_ranks = SortedDict().fromkeys(urls, 1.0)
    for i in range(iters):
        for url in urls:
            rank = (1.0 / len(urls)) * (1.0 - b) + b * sum([page_ranks[w] / len(outlinks[w]) for w in inlinks[url]])
            page_ranks[url] = rank
    return page_ranks


def get_top_pageranks(inlinks, outlinks, b, n=50, iters=20):
    urls = SortedList(inlinks.keys())
    page_ranks = compute_pagerank(urls, inlinks, outlinks, b, iters)  # can just take items
    return sorted(page_ranks.items(), key=lambda x: x[1], reverse=True)[:n]


def read_names(path):
    """ Do not mofify. Returns a SortedSet of names in the data directory. """
    return SortedSet([os.path.basename(n) for n in glob.glob(path + os.sep + '*')])


def get_links(names, html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')

    for url in soup.find_all('a', href=True):
        if url.get('href', False).startswith('/wiki/'):
            name = url['href'].split('/wiki/', 1)[1]
            if name in names:
                links.append(name)
    return SortedSet(links)

def read_links(path):
    names = read_names(path)
    inlinks = SortedDict([[name, []] for name in names])
    outlinks = SortedDict([[name, []] for name in names])

    for name_file in glob.glob(path + os.sep + '*'):
        curr_name = name_file[5:]
        for link in get_links(names, open(name_file)):
            if curr_name == link:
                continue
            outlinks[curr_name].append(link)
            inlinks[link].append(curr_name)

    for key in inlinks:
        inlinks[key] = SortedSet(inlinks[key])
        outlinks[key] = SortedSet(outlinks[key])

    return inlinks, outlinks


def print_top_pageranks(topn):
    """ Do not modify. Print a list of name/pagerank tuples. """
    print('Top page ranks:\n%s' % ('\n'.join('%s\t%.5f' % (u, v) for u, v in topn)))


def main():
    if not os.path.exists('data'):  # download and unzip data
       from urllib.request import urlretrieve
       import tarfile
       urlretrieve('http://cs.iit.edu/~culotta/cs429/pagerank.tgz', 'pagerank.tgz')
       tar = tarfile.open('pagerank.tgz')
       tar.extractall()
       tar.close()

    inlinks, outlinks = read_links('data')
    #print('read %d people with a total of %d inlinks' % (len(inlinks), sum(len(v) for v in inlinks.values())))
    #print('read %d people with a total of %d outlinks' % (len(outlinks), sum(len(v) for v in outlinks.values())))
    topn = get_top_pageranks(inlinks, outlinks, b=.8, n=509, iters=10)
    print_top_pageranks(topn)


if __name__ == '__main__':
    main()
