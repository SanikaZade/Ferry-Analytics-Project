import re
with open('dashboard/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = 'st.markdown("""'
end_marker = '""", unsafe_allow_html=True)'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    before = content[:start_idx + len(start_marker)]
    after = content[end_idx:]
    middle = content[start_idx + len(start_marker):end_idx]
    
    # Remove empty lines in the CSS/HTML block
    middle = '\n'.join([line for line in middle.split('\n') if line.strip() != ''])
    
    new_content = before + '\n' + middle + '\n' + after
    
    with open('dashboard/app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('CSS block fixed!')
else:
    print('Markers not found')
