from Tkinter import *
import tkSimpleDialog
import tkMessageBox

#Set up GUIs
root=Tk()
#w=Label(root,text="Search Engine")
#w.pack()

#Welcome the User

#Get user info
page_name=tkSimpleDialog.askstring("JINNI-PYTHON SEARCH ENGINE","Enter the seed page here")

word=tkSimpleDialog.askstring("JINNI-PYTHON SEARCH ENGINE","Enter word to search")

output="The seed page was: %s as given by user."%(page_name)








#****WEB CRAWLING****
def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""
    
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph



#****INDEX BUILDING****
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

    
#****RANKING THE PAGES******

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    #print ranks	
    return ranks

def quick_sort(url_lst,ranks):
    url_sorted_worse=[]
    url_sorted_better=[]
    if len(url_lst)<=1:
        return url_lst
    pivot=url_lst[0]
    for url in url_lst[1:]:
        if ranks[url]<=ranks[pivot]:
            url_sorted_worse.append(url)
        else:
            url_sorted_better.append(url)
    return quick_sort(url_sorted_better,ranks)+[pivot]+quick_sort(url_sorted_worse,ranks)

        
def ordered_search(index, ranks, keyword):
    if keyword in index:
        all_urls=index[keyword]
    else:
        return None
    return quick_sort(all_urls,ranks)


#*****MAIN********




#index, graph = crawl_web('http://udacity.com/cs101x/urank/index.html')
index, graph = crawl_web(page_name)
ranks = compute_ranks(graph)
#print ordered_search(index, ranks, 'Hummus')
print ordered_search(index, ranks, word)
#>>> ['http://udacity.com/cs101x/urank/kathleen.html',
#    'http://udacity.com/cs101x/urank/nickel.html',
#    'http://udacity.com/cs101x/urank/arsenic.html',
#    'http://udacity.com/cs101x/urank/hummus.html',
#    'http://udacity.com/cs101x/urank/index.html']

#print ordered_search(index, ranks, 'the')
#>>> ['http://udacity.com/cs101x/urank/nickel.html',
#    'http://udacity.com/cs101x/urank/arsenic.html',
#    'http://udacity.com/cs101x/urank/hummus.html',
#    'http://udacity.com/cs101x/urank/index.html']


print " "
print "                         JINNI-PYTHON SEARCH ENGINE                                        "
print "  "
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
print " "
print " "
output+=" "
output+="And outputs are:      "
output+=" "
pp=ordered_search(index, ranks, 'Hummus')
for xp in pp:
	print "Go to site: ",xp
	output+=xp
	output+=" "
print " "
print " "
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
#print ordered_search(index, ranks, 'babaganoush')
#>>> None

tkMessageBox.showinfo("Results",output)
