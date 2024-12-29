def solve_part2(input_string):
  on_disk = []
  id = 0
  k = 0

  for char in input_string:
      n = int(char)
      if (k % 2) == 0:
          sid = str(id)
          repeated_sid = n * [sid]
          on_disk.extend(repeated_sid)
          id += 1
      else:
          on_disk.extend(n * ['.'])
      k += 1

  #print(on_disk)

  def swap_positions(s, i, j):
      s[i], s[j] = s[j], s[i]
      return s

  def find_sublist_start(big_list, sublist):
      len_big = len(big_list)
      len_sub = len(sublist)
      for i in range(len_big - len_sub + 1):
          if big_list[i:i + len_sub] == sublist:
              return i
      return -1

  # did not find the proper way to do this ... so let's be silly !

  first_dot=0
  last_number=len(on_disk)

  while True:

    last_number = max((i for i, val in enumerate(on_disk[:last_number]) if val != '.'), default=None)
    if last_number is None:
      break
    j = last_number-1
    while on_disk[j] == on_disk[last_number]:
      j-=1
    l = last_number-j
    #print('last_number',last_number, on_disk[last_number]) 
    #print('l',l) 
    #print('j',j) 

    s = l*['.']
    first_dot = find_sublist_start(on_disk,s)
    print('\rfirst_dot {:< 10d} \t\t, last number {:< 10d}'.format(first_dot, last_number), end='', flush=True)
    if first_dot >= 0:
      very_first_dot = find_sublist_start(on_disk,'.')
      #print('first_dot',first_dot)

      if first_dot < j:

        if first_dot and last_number and last_number > very_first_dot:
          for i in range(first_dot, first_dot+l):
            on_disk = swap_positions(on_disk,i,j+i-first_dot+1)
          #print(on_disk)
        else:
          break

      first_dot = 0

    last_number -= l-1
    #print(last_number*'.'+'^')
    #print('----------------------------------------------------------------')


  def chunked_sum(s, chunk_size=10**6):
      total = 0
      for start in range(0, len(s), chunk_size):
          chunk = s[start:start + chunk_size]
          total += sum(int(char) * (start + i) for i, char in enumerate(chunk))
          #print(total)
      return total

  result = chunked_sum([i.replace('.','0') for i in on_disk])

  print('\n', result)

def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n')
    return lines

# Test
input = '2333133121414131402'
solve_part2(input)

# Real
input = read('data/data09')[0]
solve_part2(input)