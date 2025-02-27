import html

def convert_delimiter(s, start_delimiter, end_delimiter, start_html_tag, end_html_tag):
    while True:
        start = s.find(start_delimiter)
        if start == -1:
            break
        end = s.find(end_delimiter, start + len(start_delimiter))
        if end == -1:
            break
        s = f'{s[:start]}{start_html_tag}{s[start + len(start_delimiter):end]}{end_html_tag}{s[end + len(end_delimiter):]}'
    return s

def render_html(response):
    if response is None:
        raise ValueError("Response is None")
    
    response = html.escape(response) # escape html characters

    # convert markdown delimeters to html tags
    response = convert_delimiter(response, '```', '```', '<pre><code>', '</code></pre>')
    response = convert_delimiter(response, '**', '**', '<b>', '</b>')
    response = convert_delimiter(response, '*', '*', '<i>', '</i>')
    response = convert_delimiter(response, '### ', '\n', '<h3>', '</h3>')
    response = convert_delimiter(response, '## ', '\n', '<h2>', '</h2>')
    response = convert_delimiter(response, '# ', '\n', '<h1>', '</h1>')
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
        f.write(render_html(response))

if __name__ == "__main__":
    main()