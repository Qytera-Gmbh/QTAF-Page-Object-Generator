import streamlit as st
from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader(searchpath="./templates"),
    autoescape=select_autoescape()
)
template = env.get_template("page_object.jinja")

# Session initialization
if 'po_elements' not in st.session_state:
    st.session_state.po_elements = []
if 'input_element_varname_value' not in st.session_state:
    st.session_state.input_element_varname_value = ""
if 'input_element_name_value' not in st.session_state:
    st.session_state.input_element_name_value = ""
if 'input_element_type' not in st.session_state:
    st.session_state.input_element_type = ""
if 'input_element_selector_value' not in st.session_state:
    st.session_state.input_element_selector_value = ""

def on_name_change():
    st.session_state.input_element_name_value = st.session_state.input_element_name
    st.session_state.input_element_name = ""

def on_varname_change():
    st.session_state.input_element_varname_value = st.session_state.input_element_varname
    st.session_state.input_element_varname = ""

def on_selector_change():
    st.session_state.input_element_selector_value = st.session_state.input_element_selector
    st.session_state.input_element_selector = ""

st.markdown("# QTAF Page Object Generator")
st.markdown("## Page object class")

class_name = st.text_input("Class name")
class_package = st.text_input("Class package")

st.markdown("### Parent element")
root_element_selector = st.text_input("Root element selector")

st.markdown("### New element")

st.text_input("Element Log Name", key="input_element_name", on_change=on_name_change)
st.text(st.session_state.input_element_name_value)

st.text_input("Java Function name", key="input_element_varname", on_change=on_varname_change)
st.text(st.session_state.input_element_varname_value)

st.session_state.input_element_type = st.selectbox(
    "Element Type",
    ["TextElement", "NumberElement", "LinkElement", "DateTextElement", "FormInputElement", "FormSelectElement", "FormCheckboxElement", "ButtonElement"],
)
st.text_input("Selector", key="input_element_selector", on_change=on_selector_change)
st.text(st.session_state.input_element_selector_value)

add_element_button = st.button("Add element")

code = st.code(template.render({
    "po_class": {"name": class_name, "package": class_package},
    "root_element_selector": root_element_selector.replace("\"", "\\\""),
    "elements": st.session_state['po_elements']
}))

if add_element_button:
    st.session_state.po_elements.append({
        "name": st.session_state.input_element_name_value,
        "varname": st.session_state.input_element_varname_value,
        "type": st.session_state.input_element_type,
        "type_function": st.session_state.input_element_type[0].lower() + st.session_state.input_element_type[1:],
        "selector": st.session_state.input_element_selector_value.replace("\"", "\\\"")
    })
    st.session_state.input_element_name_value = ""
    st.session_state.input_element_varname_value = ""
    st.session_state.input_element_type = ""
    st.session_state.input_element_selector_value = ""
    st.rerun()