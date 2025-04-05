from datetime import datetime

def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

response_text = """
TOPIC
-----
South East Asia Population

SUMMARY
-------
Southeast Asia is a region of diverse demographics and rapid population growth...

TOOLS_USED
----------
wikipedia, save_text_to_file
"""

msg = save_to_txt(response_text)
print(msg)

