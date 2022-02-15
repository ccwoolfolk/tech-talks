import os

src = './union-types/slides-source.md'
snippet_dir = './union-types/snippets'

# Clear the old snippets
for filename in os.listdir(snippet_dir):
    path = os.path.join(snippet_dir, filename)
    try:
        if os.path.isfile(path) and filename != ".keep":
            os.unlink(path)
    except Exception as e:
        print(e)


# Parse source file
with open(src) as f:
    lines = f.readlines()

is_mid_block = False
snippets = []

for line in lines:
    if "```typescript" in line:
        is_mid_block = True
        snippets.append([])
    elif "```" in line:
        is_mid_block = False
    elif is_mid_block:
        snippets[-1].append(line)

# Write output
for i, snippet in enumerate(snippets):
    file_num = '{:0>2}'.format(i)
    with open(f'{snippet_dir}/code_{file_num}.ts', 'w') as f:
        # Wrap in namespace to prevent confusing VS Code w/ identically named types
        f.write('export namespace n' + str(file_num) + ' {\n')
        for line in snippet:
            f.write(line)
        f.write('}')
