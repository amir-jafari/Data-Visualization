import streamlit as st
# %%--------------------------------------------------------------------------------------------------------------------
st.title("Streamlit App")
st.markdown("""___""")
st.header("Header 1")
st.subheader("header2")
st.divider()
# %%--------------------------------------------------------------------------------------------------------------------
st.write('This is the place you can start writing')
st.divider()
# %%--------------------------------------------------------------------------------------------------------------------
code = """df = pd.DataFrame(
    np.random.randint(low=0, high=100, size=(10, 10)),
    columns=('col %d' % i for i in range(10)))

st.dataframe(df)"""
st.code(code, language="python")

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()
st.latex(r'''
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    ''')

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()

st.markdown("*Streamlit* is **really** ***cool***.")
st.markdown('''
    :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
    :gray[pretty] :rainbow[colors].''')
st.markdown("Here's a bouquet &mdash;\
            :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

# %%--------------------------------------------------------------------------------------------------------------------
st.divider()

md = st.text_area('Type in your markdown string (without outer quotes)',
                  "Happy Streamlit-ing! :balloon:")

st.code(f"""
import streamlit as st

st.markdown('''{md}''')
""")

st.markdown(md)

print('Amir')
