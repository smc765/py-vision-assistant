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

    # replace markdown delimeters with html tags
    response = replace_delimiter(response, '```', '```', '<pre><code>', '</code></pre>')
    response = replace_delimiter(response, '**', '**', '<b>', '</b>')
    response = replace_delimiter(response, '*', '*', '<i>', '</i>')
    response = replace_delimiter(response, '_', '_', '<i>', '</i>')
    response = replace_delimiter(response, '###### ', '\n', '<h5>', '</h6>')
    response = replace_delimiter(response, '##### ', '\n', '<h5>', '</h5>')
    response = replace_delimiter(response, '#### ', '\n', '<h4>', '</h4>')
    response = replace_delimiter(response, '### ', '\n', '<h3>', '</h3>')
    response = replace_delimiter(response, '## ', '\n', '<h2>', '</h2>')
    response = replace_delimiter(response, '# ', '\n', '<h1>', '</h1>')
    response = response.replace('---\n\n', '<hr>')
    response = response.replace('\n', '<br>')

    # assemble html webpage with script for rendering math expressions
    return f'''
<!DOCTYPE html>
<html>
    <head>
        <title>AI Response</title>
        <style>
            :root {{color-scheme: dark;
            font-family: Arial, Helvetica, sans-serif;}}
        </style>
    </head>
    <body>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <p>
        {response}
        </p>
    </body>
</html>'''

def main():
    # from openai_wrapper import Client
    # client = Client()
    # response = client.create_completion(
    #   txt_prompt="this is a test prompt. Your response should contain math expressions, html code blocks, horizontal rules, lists, bold text, italic text, and headings"
    # )

    # test response
    response = '# Test Response\n\nThis is an example response to the test prompt, demonstrating various formatting elements.\n\n## Mathematical Expressions\n\nLet\'s solve a quadratic equation:\n\n\\[ ax^2 + bx + c = 0 \\]\n\nThe solutions are given by the quadratic formula:\n\n\\[\nx = \\frac{{-b \\pm \\sqrt{{b^2 - 4ac}}}}{2a}\n\\]\n\n---\n\n## HTML Code Block\n\nBelow is an example of an HTML code block that features a simple webpage structure.\n\n```html\n<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta http-equiv="X-UA-Compatible" content="IE=edge">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Test HTML Page</title>\n</head>\n<body>\n    <h1>Welcome to My Webpage</h1>\n    <p>This is a paragraph in my simple HTML page.</p>\n    <ul>\n        <li>Item 1</li>\n        <li>Item 2</li>\n        <li>Item 3</li>\n    </ul>\n</body>\n</html>\n```\n\n---\n\n## Lists\n\nHere is an **unordered list** of fruits:\n\n- Apples\n- Oranges\n- Bananas\n\nHere is an *ordered list* of steps to make tea:\n\n1. Boil water.\n2. Add tea leaves or tea bag.\n3. Steep for 3-5 minutes.\n4. **Enjoy your tea!**\n\n---\n\n### Using Styles for Emphasis\n\n- **Bold text** is often used for emphasis.\n- _Italic text_ can be used for names or foreign words.\n\nThank you for reviewing this example response containing math expressions, HTML code blocks, formatting with horizontal rules, and text styles.'
    
    with open('response.html', 'w', encoding='utf-8') as f:
        f.write(generate_html(response))

if __name__ == "__main__":
    main()