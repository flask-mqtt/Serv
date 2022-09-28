
def write_file(filename,str_):    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(str_)