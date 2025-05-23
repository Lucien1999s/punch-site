import streamlit as st
from src.core import punch
from src.settings import SUPER_ACC, SUPER_PWD
from src.pixel import get_pixel_art
from src.notion_db import fetch, create, delete, fetch_user, fetch_2

def sign_up_page():
    st.image("image/sign up.png", use_container_width=True)
    st.markdown(
        "<h1 style='text-align: center; color: orange; font-size: 40px;'>確 認 您 的 身 份</h1>",
        unsafe_allow_html=True,
    )
    account = st.text_input("登入帳號")
    login_password = st.text_input("登入密碼", type="password")
    company_id = st.text_input("公司统一编号")
    company_mail = st.text_input("公司信箱")
    password = st.text_input("公司密碼", type="password")

    if st.button("註冊"):
        if (
            not account
            or not login_password
            or not company_id
            or not company_mail
            or not password
        ):
            st.error("請填寫以上所有欄位")
        else:
            resp = create([account, login_password, company_id, company_mail, password])
            if resp == 200:
                st.success("註冊成功")
                st.session_state.show_sign_up = False
                st.session_state.show_login = True
                st.rerun()
            else:
                st.error("該帳號名已存在")

    if st.sidebar.button("返回登入頁面"):
        st.session_state.show_sign_up = False
        st.session_state.show_login = True
        st.rerun()


def login_page():
    st.image("image/login.png", use_container_width=True)
    st.markdown(
        "<h1 style='text-align: center; color: orange; font-size: 40px;'>躺 在 家 打 卡 Online</h1>",
        unsafe_allow_html=True,
    )
    account = st.text_input("帳號")
    login_password = st.text_input("密碼", type="password")
    if st.button("登入"):
        user = fetch_user(account=account, login_password=login_password)

        if account == SUPER_ACC and login_password == SUPER_PWD:
            st.success("管理員登入成功！")
            st.session_state.logged_in = True
            st.session_state.is_admin = True  # 新增標記以識別管理員用戶
            st.session_state.user_account = account
            st.rerun()
        elif user:
            st.success("登入成功！")
            st.session_state.logged_in = True
            st.session_state.is_admin = False  # 確保非管理員用戶沒有管理員權限
            st.session_state.user_account = account
            st.rerun()
        else:
            st.error("帳號或密碼錯誤")

    if st.sidebar.button("註冊"):
        st.session_state.show_sign_up = True
        st.rerun()
    
    if st.sidebar.button("教學"):
        st.session_state.show_sign_up = False
        st.session_state.show_login = False
        st.session_state.logged_in = False  # 確保用戶在查看教學時不會被認為是已登入狀態
        st.session_state.show_tutor = True  # 新增一個狀態用於控制是否顯示教學頁面
        st.rerun()

def tutor_page():
    st.video("image/punch_tutor.mp4")
    if st.sidebar.button("返回登入頁面"):
        st.session_state.show_sign_up = False
        st.session_state.show_login = True
        st.session_state.logged_in = False  # 確保用戶從教學頁面返回時不會被認為是已登入狀態
        st.rerun()

def main_page():
    st.image("image/main.png", use_container_width=True)
    st.markdown(
        "<h1 style='text-align: center; color: orange; font-size: 40px;'>打 卡 神 器 🫣</h1>",
        unsafe_allow_html=True,
    )
    
    # 在函式開頭定義 account 變量，確保它在所有執行路徑中都有值
    account = st.session_state.user_account
    
    if st.session_state.get("load_defaults", False):
        try:
            info = fetch_2(account=account)
            if info:
                uno_default = info[2]
                mail_default = info[3]
                pwd_default = info[4]
            else:
                st.error("未找到用户信息")
                uno_default, mail_default, pwd_default = "", "", ""
        except Exception as e:
            st.error(f"查詢失敗：{e}")
            uno_default, mail_default, pwd_default = "", "", ""
        st.session_state.load_defaults = False
    else:
        uno_default, mail_default, pwd_default = "", "", ""
    

    svg = get_pixel_art(account)
    # 使用 flex 布局來使圖片和文本並排顯示
    content = f'''
    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="flex-shrink: 0; width: 50px; height: 50px;">{svg}</div>
        <div style="font-size: 25px;">Hello {account}</div>
    </div>
    '''
    st.sidebar.markdown(content, unsafe_allow_html=True)
    st.sidebar.write("")
    st.sidebar.write("")


    if st.session_state.get("logged_in", False) and st.session_state.get(
        "is_admin", False
    ):
        if st.sidebar.button("管理後台"):
            st.session_state.show_console = True  # 使用一個新的 session_state 變量來控制是否顯示管理後台
            st.rerun()

    uno = st.text_input("统一编号", value=uno_default, key="uno")
    mail = st.text_input("公司信箱", value=mail_default, key="mail")
    pwd = st.text_input("密碼", type="password", value=pwd_default, key="pwd")

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

    if st.sidebar.button("自動填入"):
        st.session_state.load_defaults = True
        if not uno and mail and pwd:
            st.error("請重新點擊")
        else:
            st.write("再點擊一次，以確認資料是否有誤")
    account = st.session_state.user_account

    if st.sidebar.button("登出"):
        st.session_state.logged_in = False
        st.session_state.show_sign_up = False
        st.session_state.show_login = True
        st.rerun()

def console():
    st.image("image/console.png", use_container_width=True)
    st.markdown(
        "<h1 style='text-align: center; color: orange; font-size: 40px;'>管 理 員 後 台</h1>",
        unsafe_allow_html=True,
    )
    # data = query_users_db()
    data = fetch()
    st.table(data)
    user_name = st.text_input("欲刪除的使用者")
    if st.button("刪除"):
        if user_name:
            # delete_user(user_name)
            delete(name=user_name)
            st.success("成功刪除")
            st.rerun()
    if st.sidebar.button("返回主頁"):
        st.session_state.show_console = False
        st.session_state.show_login = False
        st.session_state.show_sign_up = False
        st.session_state.logged_in = True
        st.rerun()


def UI():
    # 初始化 session_state 變量
    if "show_sign_up" not in st.session_state:
        st.session_state.show_sign_up = False
    if "show_login" not in st.session_state:
        st.session_state.show_login = True
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "show_console" not in st.session_state:
        st.session_state.show_console = False
    if "show_tutor" not in st.session_state:  # 新增的教學頁面顯示控制
        st.session_state.show_tutor = False

    if st.session_state.logged_in and st.session_state.show_console:
        console()
    elif st.session_state.logged_in:
        main_page()
    elif st.session_state.show_sign_up:
        sign_up_page()
    elif st.session_state.show_login:
        login_page()
    elif st.session_state.show_tutor:  # 新增的條件來顯示教學頁面
        tutor_page()


if __name__ == "__main__":
    UI()
