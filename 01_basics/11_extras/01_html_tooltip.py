import streamlit as st

# Define the documentation text
documentation_text = """
This is the documentation text for the feature. It can be a multi-line string explaining the functionality, usage instructions, 
or any other relevant information.This is the documentation text for the feature. It can be a multi-line string explaining
 the functionality, usage instructions, or any other relevant information.
"""

# Calculate the font size, width, and height based on the length of the text
text_length = len(documentation_text)
width = 400
font_size = 8
height = 400

# Add some custom CSS for the tooltip
tooltip_css = f"""
<style>
.tooltip {{
  position: relative;
  display: inline-block;
}}

.tooltip .tooltiptext {{
  visibility: hidden;
  width: {width}px;
  max-width: {width}px;
  max-height: {height}px;
  background-color: black;
  color: #fff;
  text-align: left;
  border-radius: 6px;
  padding: 5px;
  position: absolute;
  z-index: 1;
  bottom: 150%;
  left: 50%;
  margin-left: -{width//2}px;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: {font_size}px;
  line-height: {font_size}px;
  word-wrap: break-word;
  white-space: pre-wrap;
  overflow-wrap: break-word;
  overflow: auto;
}}

.tooltip:hover .tooltiptext {{
  visibility: visible;
  opacity: 1;
}}
</style>
"""

# Add the info icon and tooltip
with st.container():
    st.markdown(tooltip_css, unsafe_allow_html=True)
    st.markdown("""
                <div class="tooltip">
                    <span style='font-family:sans-serif; color:blue; font-size:20px;'>&#9432;</span>
                    <span class="tooltiptext">{}</span>
                </div>
                """.format(documentation_text), unsafe_allow_html=True)