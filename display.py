import html

def replace_delimiter(s, start_old, end_old, start_new, end_new):
    while True:
        start = s.find(start_old)

        if start == -1:
            return s

        end = s.find(end_old, start + len(start_old))

        if end == -1:
            return s
        
        s = s[:start] + start_new + s[start + len(start_old):end] + end_new + s[end + len(end_old):]

def generate_html(response):
    if response is None:
        raise ValueError("Response is None")
    
    response = html.escape(response) # escape html characters

    # convert markdown delimeters to html tags
    response = replace_delimiter(response, '```', '```', '<pre><code>', '</code></pre>')
    response = replace_delimiter(response, '**', '**', '<b>', '</b>')
    response = replace_delimiter(response, '*', '*', '<i>', '</i>')
    response = replace_delimiter(response, '### ', '\n', '<h3>', '</h3>')
    response = replace_delimiter(response, '## ', '\n', '<h2>', '</h2>')
    response = replace_delimiter(response, '# ', '\n', '<h1>', '</h1>')
    response = response.replace('---', '<hr>')
    response = response.replace('\n\n', '<br>')
    response = response.replace('\n', '<br>')

    # assemble html webpage with script for rendering math expressions
    return f'''
<!DOCTYPE html>
<html>
    <head><title>Response</title></head>
    <body>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <p>
        {response}
        </p>
    </body>
</html>'''

def main():
    from openai_wrapper import Client
    client = Client()
    response = client.create_completion(txt_prompt="this is a test prompt. Your response should contain math expressions, html code blocks, horizontal rules, lists, bold text, italic text, and headings")
    
    with open('response.html', 'w', encoding='utf-8') as f:
        f.write(generate_html(response))

if __name__ == "__main__":
    main()