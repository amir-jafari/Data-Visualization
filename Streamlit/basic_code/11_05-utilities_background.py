import os
import streamlit as st
import base64

st.subheader("***Background***")
st.write('Setup the webpage background.')


with st.echo():
    # @st.cache_data
    @st.cache_data
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()


    @st.cache_data
    def set_png_as_page_bg(png_file):
        bin_str = get_base64_of_bin_file(png_file)
        page_bg_img = '''
        <style>
        .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: scroll; # doesn't work
        }
        </style>
        ''' % bin_str

        st.markdown(page_bg_img, unsafe_allow_html=True)
        return


    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir('..')

    file_name = os.getcwd() + os.path.sep + 'static' + os.path.sep + 'background.webp'
    set_png_as_page_bg(file_name)
