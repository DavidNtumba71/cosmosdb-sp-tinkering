import csv

'''take one large csv file and partition it'''


def count_rows(csv_file_name):
    with open(csv_file_name, encoding='utf-8-sig') as csv_file:
        movies_reader = csv.reader(csv_file, delimiter=';')
        return len(list(movies_reader))


file_name = "movies.csv"
counted_rows = count_rows(file_name)

print(f'found {counted_rows} rows in {file_name}.')
PARTITIONS = 3
rows_partitioned = round((counted_rows / PARTITIONS))

print(f'dividing {counted_rows} rows into {PARTITIONS} files with {rows_partitioned} rows each.')


def write_chunk(part, lines):
    with open('../tmp/split_csv_python/data_part_'+ str(part) +'.csv', 'w') as f_out:
        f_out.write(header)
        f_out.writelines(lines)

partition_ranges = lambda index, partition, size: tuple((round(index * size/partition), round((index+1)/partition*size)))


def set_partition_ranges(partitions, total):
    return [(partition_ranges(index, partitions, total))for index in range(partitions)]


def write_partition(header, index, lines):
    with open(f'{file_name}_{index}.csv', 'w', encoding='utf-8-sig') as output_file:
        output_file.write(header)
        output_file.writelines(lines)
        return True


p = set_partition_ranges(PARTITIONS, counted_rows)
print(p)

first = lambda x: x[0]
last  = lambda x: x[1] 

def gather_header(file_name):
    header = []
    with open(file_name, "r", encoding='utf-8-sig') as csv_file:
        header = csv_file.readline()
    return header

def gather_lines(file_name):
    line = []
    with open(file_name, "r", encoding='utf-8-sig') as csv_file:
        movies_reader = csv.reader(csv_file, delimiter=';')
        line = [line for i, line in enumerate(movies_reader) if i < last(p[0])]
    return line

def five():
    with open(file_name, "r", encoding='utf-8-sig') as csv_file:
        movies_reader = csv.reader(csv_file, delimiter=';')
        header = csv_file.readline()
        [write_partition(header, 0, line) for i, line in enumerate(movies_reader) if i >= first(p[0]) and i < last(p[0])]

lines = gather_lines(file_name) 
print(len(lines))

#joined = "\n".join(lines)



header = gather_header(file_name)
print(header)
#write_partition(header, 0, joined)

with open(file_name, "r", encoding='utf-8-sig') as csv_file:
    movies_reader = csv.reader(csv_file, delimiter=';')
    lines = csv_file.readlines()
    for index in range(100):
        write_partition(header, 0, lines[index])

print("completed")
    # tuple (start, end)
    # (index*part, ((end/(split/index))-1))
    #(0,24) from 100 part in 4
    #() = (0*25, ((100/(4/1)-1)) (1/4*100)  25
    #() = (1*25, ((100/(4/2))-1)) - (2/4*100) 50
    #() = (2*25, ((100/(4/3)-1)) -  (3/4*100) 75
    #() = (3*25, ((100/4)-1))       (4/4 * 100) 100

#with open(file_name, "r") as f:
#    count = 0
#    header = f.readline()
#    lines = []
#    for line in f:
#        count += 1
#        lines.append(line)
#        if count % chunk_size == 0:
#            write_chunk(count // chunk_size, lines)
#            lines = []
#    # write remainder
#    if len(lines) > 0:
#        write_chunk((count // chunk_size) + 1, lines)