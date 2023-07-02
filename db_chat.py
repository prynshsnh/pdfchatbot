import databutton as db
import streamlit as st


def check_for_openai_key():
    try:
        key = db.secrets.get("OPENAI_API_KEY")
    except Exception:
        return False

    if len(key) > 10:
        return key

    st.info(
        """This example requires an OpenAI API key to run. Your key will be stored in the Databutton Secrets that 
    that you can find under Configure in the left-hand menu.
    """
    )
    key = st.text_input(
        "Please, type in you OpenAI API key to continue", type="password"
    )
    if key:
        db.secrets.put("OPENAI_API_KEY", key)
        st.experimental_rerun()

    st.stop()
    return 1


def db_dataframe(name):
    df = db.storage.dataframes.get(name)
    df.to_csv(name)
    return name


class user_message:
    def __init__(self, text, user_name="You"):
        self.name = user_name
        self.container = st.empty()
        self.update(text)

    def update(self, text):
        message = f"""<div style='display:flex;align-items:center;justify-content:flex-end;margin-bottom:10px;'>
                     <div style='background-color:{st.get_option("theme.secondaryBackgroundColor")};border-radius:10px;padding:10px;'>
                     <p style='margin:0;font-weight:bold;'>{self.name}</p>
                     <p style='margin:0;color={st.get_option("theme.textColor")}'>{text}</p>
                     </div>
                     <img src='https://i.imgur.com/qxo27Eu.png' style='width:50px;height:50px;border-radius:50%;margin-left:10px;'>
                     </div>
        """
        self.container.write(message, unsafe_allow_html=True)
        return self


class bot_message:
    def __init__(self, text, bot_name="Assistant"):
        self.name = bot_name
        self.container = st.empty()
        self.update(text)

    def update(self, text):
        message = f"""<div style='display:flex;align-items:center;margin-bottom:10px;'>
                    <img src='https://i.imgur.com/rKTnxVN.png' style='width:50px;height:50px;border-radius:50%;margin-right:10px;'>
                    <div style='background-color:st.get_option("theme.backgroundColor");border: 1px solid {st.get_option("theme.secondaryBackgroundColor")};border-radius:10px;padding:10px;'>
                    <p style='margin:0;font-weight:bold;'>{self.name}</p>
                    <p style='margin:0;color={st.get_option("theme.textColor")}'>{text}</p>
                    </div>
                    </div>
        """
        self.container.write(message, unsafe_allow_html=True)
        return self
