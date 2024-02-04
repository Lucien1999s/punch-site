import sqlite3
import streamlit as st
from src.core import punch

def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                 (account TEXT UNIQUE, login_password TEXT, company_id TEXT, company_mail TEXT, password TEXT)''')
    conn.close()

def sign_up_page():
    st.image("image/sign up.png", use_column_width=True)
    st.markdown(
        "<h1 style='text-align: center; color: lightblue; font-size: 40px;'>確 認 您 的 身 份</h1>",
        unsafe_allow_html=True,
    )
    account = st.text_input("登入帳號")
    login_password = st.text_input("登入密碼", type="password")
    company_id = st.text_input("公司统一编号")
    company_mail = st.text_input("公司信箱")
    password = st.text_input("公司密碼", type="password")

    if st.button("註冊"):
        if not account or not login_password or not company_id or not company_mail or not password:
            st.error("請填寫以上所有欄位")
        else:
            try:
                conn = sqlite3.connect('users.db')
                conn.execute("INSERT INTO users (account, login_password, company_id, company_mail, password) VALUES (?, ?, ?, ?, ?)",
                             (account, login_password, company_id, company_mail, password))
                conn.commit()
                conn.close()
                st.success("註冊成功")
                st.session_state.show_sign_up = False
                st.session_state.show_login = True
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("該帳號名已存在")
            except Exception as e:
                st.error(f"註冊失敗：{e}")

    if st.button("返回"):
        st.session_state.show_sign_up = False
        st.session_state.show_login = True
        st.rerun()


def login_page():
    st.image("image/login.png", use_column_width=True)
    st.markdown(
        "<h1 style='text-align: center; color: lightblue; font-size: 40px;'>躺 在 家 打 卡 Online</h1>",
        unsafe_allow_html=True,
    )
    account = st.text_input("帳號")
    login_password = st.text_input("密碼", type="password")
    if st.button("登入"):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT account, login_password FROM users WHERE account = ? AND login_password = ?", (account, login_password))
        user = cursor.fetchone()
        conn.close()

        if user:
            st.success("登入成功！")
            st.session_state.logged_in = True
            st.session_state.user_account = account
            st.rerun()
        else:
            st.error("帳號或密碼錯誤")

    if st.button("註冊"):
        st.session_state.show_sign_up = True
        st.rerun()

def main_page():
    st.image("image/main.png", use_column_width=True)
    st.markdown(
        "<h1 style='text-align: center; color: lightblue; font-size: 40px;'>打 卡 神 器 !!</h1>",
        unsafe_allow_html=True,
    )
    if st.session_state.get('load_defaults', False):
        account = st.session_state.user_account
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("SELECT company_id, company_mail, password FROM users WHERE account = ?", (account,))
            info = cursor.fetchone()
            conn.close()
            if info:
                uno_default, mail_default, pwd_default = info
            else:
                st.error("未找到用户信息")
                uno_default, mail_default, pwd_default = '', '', ''
        except Exception as e:
            st.error(f"查詢失敗：{e}")
            uno_default, mail_default, pwd_default = '', '', ''
        st.session_state.load_defaults = False
    else:
        uno_default, mail_default, pwd_default = '', '', ''

    uno = st.text_input("统一编号", value=uno_default, key='uno')
    mail = st.text_input("公司信箱", value=mail_default, key='mail')
    pwd = st.text_input("密碼", type="password", value=pwd_default, key='pwd')

    if st.button("打卡"):
        if uno and mail and pwd:
            try:
                resp_state = punch(int(uno), mail, pwd)
                if resp_state == 200:
                    st.success("打卡成功")
                else:
                    st.error(f"打卡失敗：{resp_state}")
            except Exception as e:
                st.error(f"錯誤：{e}")
        else:
            st.error("請填寫所有資料")

    if st.button("自動填入"):
        st.session_state.load_defaults = True
        if not uno and mail and pwd:
            st.error("請重新點擊")
        else:
            st.write("再點擊一次，以確認資料是否有誤")

    if st.sidebar.button("登出"):
        st.session_state.logged_in = False
        st.session_state.show_sign_up = False
        st.rerun()

def query_users_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    conn.close()

def UI():
    init_db()
    if 'show_sign_up' not in st.session_state:
        st.session_state.show_sign_up = False
    if 'show_login' not in st.session_state:
        st.session_state.show_login = True
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        main_page()
    elif st.session_state.show_sign_up:
        sign_up_page()
    elif st.session_state.show_login:
        login_page()

if __name__ == "__main__":
    UI()
