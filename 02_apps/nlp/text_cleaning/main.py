import streamlit as st
import utils


def main():
    st.header("Text Cleaning")
    st.divider()
    st.subheader("Step 1: Type the text")

    txt = utils.get_txt()

    st.divider()
    st.subheader("Step 2: Choose the cleaning methods from left side bar")

    selected = utils.sidebar()

    if st.button('Finish typing and choosing', type="primary"):
        if not selected:
            st.error("No text cleaning methods selected")
            st.stop()

        for step, item in enumerate(selected, 3):
            st.divider()
            st.subheader(f"Step {step}: {item[1]}")
            txt = utils.clean(txt, item[0])
            with st.expander("See result", expanded=True):
                st.write(txt)


if __name__ == "__main__":
    main()
