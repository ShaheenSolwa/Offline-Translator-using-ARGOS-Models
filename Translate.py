import argostranslate.package
import argostranslate.translate
import streamlit as st
from streamlit_navigation_bar import st_navbar
import fitz
import os

st.set_page_config(
    page_title="Translate-THOR",
    initial_sidebar_state="collapsed",
    layout="wide"
)

def build_language_translation_index(path_to_models):
    for argosmodel in os.listdir(path_to_models):
        if argosmodel.endswith('argosmodel'):
            model = os.path.join(path_to_models, argosmodel)
            argostranslate.package.install_from_path(str(model))

def build_language_pairs():
    language_index_dict = {
        'sq': 'Albanian', 'ar': 'Arabic', 'az': 'Azerbaijani', 'bn': 'Bengali', 'bg': 'Bulgrian',
        'ca': 'Catalan', 'zt': 'Chinese (Traditional)', 'zh': 'Chinese', 'cs': 'Czech',
        'da': 'Danish', 'nl': 'Dutch', 'en': 'English', 'eo': 'Esperanto', 'et': 'Estonian',
        'fi': 'Finnish', 'fr': 'French', 'de': 'German', 'el': 'Greek', 'hi': 'Hindi',
        'hu': 'Hungarian', 'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian', 'ja': 'Japanese',
        'ko': 'Korean', 'lv': 'Latvian', 'lt': 'Lithuanian', 'ms': 'Malay', 'nb': 'Norwegian',
        'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portugese', 'ro': 'Romanian', 'ru': 'Russian',
        'sk': 'Slovak', 'sl': 'Slovenian', 'es': 'Spanish', 'sv': 'Swedish', 'tl': 'Tagalog',
        'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukranian'
    }

    keys = []
    values = []
    for x, y in language_index_dict.items():
        keys.append(x)
        values.append(y)

    keys.insert(0, '')
    values.insert(0, '')

    return keys, values


def main_text():
    col1, col2, col3 = st.columns(3)

    keys, values = build_language_pairs()

    output = ''
    #text_input = ""
    warning_dict = {}

    with col1:
        language_from = st.selectbox("Select Language", options=values, key='lang_from')
        text_input = st.text_area("Enter Text To Translate...", height=300)

    with col2:
        c1,c2,c3 = st.columns(3)
        with c2:
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")

            button = st.button("TRANSLATE")

            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")

            clear = st.button("CLEAR TEXT")

        if button:
            if 'language_to' in st.session_state and text_input != '':
                l_to = st.session_state['language_to']
                from_index = values.index(language_from)
                l_from = keys[from_index]
                to_index = values.index(l_to)
                l_to = keys[to_index]
                output = argostranslate.translate.translate(str(text_input),
                                                            str(l_from),
                                                            str(l_to))

            else:
                warning_dict["language to"] = "Please choose a language."

        if clear:
            output = " "

    with col3:
        language_to = st.selectbox("Select Language", options=values, key='lang_to')
        st.session_state['language_to'] = language_to

        if 'language to' in warning_dict.keys():
            st.warning(warning_dict["language to"])

        st.text_area(label="Translated Text", value=output, placeholder="Translated Text will Appear Here.", height=300)


def main_document():
    file = st.file_uploader("Upload a document to translate", type=["pdf"])
    keys, values = build_language_pairs()
    text = ''
    language_from = ''
    page_info = {}
    output_dict = {}
    if file is not None:
        with st.spinner("Reading document..."):
            doc = fitz.open(stream=file.read(), filetype='pdf')
            for page in doc:
                text = page.get_text()
                page_str = int(str(page).split(" ")[1]) + 1
                page_info[page_str] = text
            doc.close()

        st.write(page_info)
        language_from = st.selectbox("Select Language", options=values, key='lang_from')
        language_to = st.selectbox("Select Language", options=values, key='lang_to')

        col1,col2,col3,col4,col5,col6,col7 = st.columns(7)
        with col4:
            if st.button("Translate", key='translate_doc'):
                with st.spinner("Translating..."):
                    if language_from != '' and language_to != '':
                        to_index = values.index(language_to)
                        language_to = keys[to_index]

                        from_index = values.index(language_from)
                        language_from = keys[from_index]

                        for page, text in page_info.items():
                            output_dict[page] = argostranslate.translate.translate(str(text),
                                                                                   str(language_from),
                                                                                   str(language_to))
                st.write(output_dict)


if __name__ == "__main__":
    pages = ["Text Translate", "Document Translate"]
    styles = {
        "nav": {
            "background-color": "#FFA500",
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
            "height": "100px"
        },
        "span": {
        },
        "selected": {
            "background-color": "yellow",
            "color": "var(--text-color)",
            "font-weight": "normal",
            "padding": "14px",
        },
    }

    page = st_navbar(
        pages,
        selected="Home",
        # logo_path="",
        # urls=urls,
        styles=styles,
    )

    if page == 'Text Translate':
        st.text("\n")
        st.text("\n")
        st.text("\n")

        main_text()
    elif page == 'Document Translate':
        main_document()