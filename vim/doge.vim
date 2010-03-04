function! Pydoge_inner()
python << endpython
import vim
import pydoge.main

# init
(row_call, col_call) = vim.current.window.cursor
row_call -= 1
row_current = row_call
cb = vim.current.buffer

# Find closest class or method
while row_current >= 0:
    line = cb[row_current]
    if line.lstrip().startswith('class') \
      or line.lstrip().startswith('def'):
        break
    row_current -= 1

row_stop = row_current + 1 if row_current >= 0 else 1
#vim.command("set rc=%d", row_current)
#ret = vim.eval("&rc")
#ret = vim.eval("3")
#print ret

vim.command("return %d" % row_stop) # return from the Vim function!

#vim.command("return %d" % row_current) # return from the Vim function!
endpython
endfunction



function! Pydoge_object()
python << endpython
import vim
import pydoge.main

# init
(row_call, col_call) = vim.current.window.cursor
row_call -= 1
row_current = row_call
cb = vim.current.buffer

row_begin = int(vim.eval("Pydoge_inner()"))
row_begin -= 1 # python domain
#line_stop = line

row_current = row_begin # start on definition line

# Escape possible multi-line definition
while row_current < len(cb) and not cb[row_current].rstrip().endswith(':'):
    row_current += 1
row_current += 1 # jump to next line
row_content = row_current

# Escape possible empty lines
while row_current < len(cb) and not cb[row_current].strip():
    row_current += 1

# Make sure there is at least one line: row_current < len(cb)
if row_current < len(cb):

    indent = 0
    for c in cb[row_current]:
        if c != ' ':
            break
        indent += 1

    while row_current < len(cb) and (not cb[row_current] or cb[row_current].startswith(indent * ' ')):
        row_current += 1

    row_end = row_current + 1

    print row_begin, row_end #, cb[row_begin], cb[row_end - 1]

    # Update buffer
    buffer = [l + '\n' for l in cb[row_begin:row_end]]

    end = cb[row_end + 1:]
    buffer_new = pydoge.main.handle_buffer(buffer)

    # Delete non necessary empty lines
    # TODO: fix added line when only 'def fct():' in file
    #while buffer_new and buffer_new[0].strip() == '':
    #    del buffer_new[0]

    # Apply update
    del cb[row_begin:]
    for line in buffer_new:
        for subline in line.splitlines():
            cb.append(subline)
    for line in end:
        cb.append(line)

    # Set cursor on object head
    vim.current.window.cursor = (row_content, indent)

endpython
endfunction










function! Pydoge_file()
python << endpython
import vim
import pydoge.main

# init
(row_call, col_call) = vim.current.window.cursor
row_call -= 1
row_current = row_call
cb = vim.current.buffer

row_stop = int(vim.eval("Pydoge_inner()"))
line_stop = cb[row - 1]

# Count identical definitions before this one
row_current -= 1
nb_same = 0
while row_current >= 0:
    line = cb[row_current]
    if line == line_stop:
        nb_same += 1
    row_current -= 1

    
# Update buffer
buffer = [l + '\n' for l in cb]
buffer_new = pydoge.main.handle_buffer(buffer)
del cb[:]
for line in buffer_new:
    for subline in line.splitlines():
        cb.append(subline)


# Find correct line
for index, line in enumerate(cb):
    if line == line_stop:
        row_stop = index + 1
        if nb_same == 0:
            break
        nb_same -= 1

# Set cursor
vim.current.window.cursor = (row_stop, 0)

# Success message
#print "File updated!"
#vim.command("return 1") # return from the Vim function!
endpython
endfunction

"map <silent> ` :call Pydoge_file()<cr>
ab dgf call Pydoge_file()<cr>
ab dgm call Pydoge_object()<cr>
