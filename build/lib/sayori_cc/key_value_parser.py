# Code by NDRAEY (c) 2023

def parse_key_value_file(data: str):
    spl = [i.strip() for i in data.split("\n") if i.strip()]
    spll = len(spl)
    out = {}

    i = 0
    while i < spll:
        elem = spl[i]

        if not len(elem):  # Newline
            i += 1
            continue
        elif elem[0] == "#":  # Comment
            i += 1
            continue
        
        el = elem.split("=")
        if len(el) != 2 or el[1] == '':  # Invalid entry
            i += 1
            continue

        el[0], el[1] = el[0].strip(), el[1].strip()

        if el[1][-1] == "\\":
            el[1] = el[1][:-1]
            i+=1
            while i < spll and spl[i].strip()[-1] == "\\":
                el[1] += spl[i].strip()[:-1]
                i += 1
            el[1] += spl[i].strip() if i < spll else ""

        out[el[0]] = el[1]
        
        i += 1
    return out

if __name__=="__main__":
    from pprint import pprint
    test = '''
    file = "Hello.txt" a b c
    ABC = 12345
    # This is a comment

    Newlines = ""

    # Invalid strings are ignored

    Invalid
    Invalid2 = 

    Multiline = a \\
                b \\
                c
    '''

    pprint(parse_key_value_file(test))
