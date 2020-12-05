def parse_file(location):
    #opens and reads file
    f = open(location, 'r')
    file = f.read()
    len_file = len(file)

    #extract title (in progress)
    '''start_key = ['/large', 'bf']
    start_window = [len(i) for i in start_key]
    found_indicators = [False for i in start_key]
    bound = len_file - len(start_key[0])
    found_start = False
    title = ''
    for i in range(0, bound):
        if i == bound-1:
            title = None

        for j in range(len(start_window)):
            if file[i:i+start_window[j]].lower() == start_key[j]:
                found_indicators[j] = True
                break
        found_start = True
        for ind in found_indicators:
            if ind == False:
                found_start = False
        if found_start is True:
            index = i+1
            break'''



    #extract abstract
    index = 0

    window = len('abstract')
    abstract = ''
    bound = len_file - window
    #find where abstract starts
    for i in range(bound):
        if file[i:i+window].lower() == 'abstract':
            index = i + window
            break
        if i == bound-1:
            abstract = None
    if abstract is not None:
        abstract = ''
        start = False
        finish_key1 = '\end{abstract}'
        finish_key2 = 'Introduction'
        window1 = len(finish_key1)
        window2 = len(finish_key2)

        #add till end
        for i in range(index, bound):
            if i is bound-1:
                abstract = None
            if start is False and file[i].isalpha() is True:
                start = True
                abstract += file[i]
            elif start is True:
                if file[i:i+window1] == finish_key1 or file[i:i+window2] == finish_key2:
                    break
                else:

                    abstract+=file[i]


    #extract introduction
    index = 0
    window = len('introduction')
    bound = len_file - window
    intro = ''
    #find where intro starts
    for i in range(bound):
        if file[i:i+window].lower() == 'introduction':
            index = i + window
            break
        if i == bound-1:
            intro = None
    end_intro_index = 0
    if intro is not None:
        intro = ''
        start = False
        finish_key1 = '\section'
        finish_keyword2 = '\newsec'
        window1 = len(finish_key1)
        #add till end
        for i in range(index, bound):
            if i is bound-1:
                intro = None
            if start is False and file[i].isalpha() is True:
                start = True
                intro += file[i]
            elif start is True:
                if file[i:i+window1] == finish_key1:
                    end_intro_index = i+window1
                    break
                else:
                    intro+=file[i]
    #extract conclusion

                #possible keywords: \section{Discussions}
                #section/newsection

    index = 0
    window = len('summary and discussions')
    bound = len_file - window
    start_key = [ 'conclusion','discussion', 'future', 'summary and discussions', 'outlook']
    start_window = [len(i) for i in start_key]
    break_loop = False
    concl = ''
    back_count = 13
    #find where conclusion starts
    for i in range(end_intro_index, bound):
        if i == bound-1:
            concl = None
        if file[i] =='\\':
            back_count = 0
        if back_count <= 12:
            for j in range(len(start_window)):
                if file[i:i+start_window[j]].lower() == start_key[j]:
                    index = i + start_window[j]
                    break_loop = True
                    #print(file[i:i+start_window[j]], start_key[j])
                    break
            if break_loop:
                break
            back_count+=1
    if concl is not None:
        concl = ''
        start = False
        finish_key =['bibliography', 'acknowledgments', 'reference']
        finish_window = [len(i) for i in finish_key]

        key_found = False
        #add till end
        for i in range(index, bound):
            if i is bound-1:
                concl = None
            if start is False and file[i].isalpha() is True:
                start = True
                concl += file[i]
            elif start is True:
                for j in range(len(finish_window)):
                    if file[i:i+finish_window[j]].lower() == finish_key[j]:
                        key_found = True
                if key_found is True:
                    break
                else:
                    concl+=file[i]
    array = [abstract, intro, concl]
    clean = []
    for sec in array:
        if sec is None:
            clean.append(sec)
        else:
            cool = clean_section(sec)
            clean.append(cool.replace('\n', ' ').replace('\r', ''))
    return clean

def clean_section(section):
    #gets rid of extra syntax
    leng = len(section)
    index = 0
    for i in range(leng-1, -1, -1):
        if section[i] == '.':
            index = i+1
            break
    section = section[:index]
    leng = len(section)
    start_sent=0
    not_start = False
    start_start = True
    new_sec1 = ''

    #cleans tags in between sentences
    for i in range(leng):
        if start_start:
            if section[i].isalpha() and section[i].isupper():
                start_start = False
                start_sent = i
            continue
        if not_start:
            if section[i].isalpha() and section[i].isupper():
                not_start = False
                start_sent = i
        if not not_start and section[i] == '.':
            index = i+1
            new_sec1 += section[start_sent:index]
            not_start = True

    #delete citation
    new_sec2 = ''
    start_sent = 0
    citation = False
    cite = ['\\cite']
    for i in range(leng - len(cite)):
        for word in cite:
            if new_sec1[i:i+len(word)] == word:
                new_sec2+= new_sec1[start_sent:i]
                citation = True
        if citation:
            if new_sec1[i] =='}':
                citation = False
                start_sent = i+1
    new_sec2+=new_sec1[start_sent:]

    #get rid of math ew
    start_sent = 0

    new_sec1=''
    dollar_counter =0
    back_slash = False
    leng = len(new_sec2)
    for i in range(leng):
        if new_sec2[i] == '\\':
            back_slash = True
        if new_sec2[i] == '$':
            dollar_counter +=1
        if new_sec2[i] == '.':
            index = i+1
            if dollar_counter < 2 and not back_slash:
                new_sec1 += new_sec2[start_sent:index]
            start_sent = index
            dollar_counter =0
            back_slash = False


    return new_sec1

'''section = parse_file('/Users/nadiawaid/Documents/UROP/2003/0304044')

print(section)'''

#sections to go back to: 0301055
