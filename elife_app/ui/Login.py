from nicegui import ui, app
from elife_app.data_access.dao import UserDAO


def create_login_page(user_dao: UserDAO) -> None:
    @ui.page('/')
    def login_page() -> None:
        with ui.column().classes('w-full h-screen items-center justify-center gap-4'):
            with ui.card().classes('w-96 p-6 shadow-lg'):
                ui.label('Login').classes('text-2xl font-bold text-center')

                username_input = ui.input('Username').classes('w-full')
                password_input = ui.input('Password', password=True).classes('w-full')

                def login() -> None:
                    username = username_input.value
                    password = password_input.value

                    user = user_dao.get_by_username(username)
                    if user and user.password == password:
                        app.storage.user['username'] = user.username
                        app.storage.user['user_id'] = user.id
                        ui.navigate.to('/dashboard')
                    else:
                        ui.notify('Wrong username or password', color='negative')

                ui.button('Login', on_click=login).classes('w-full')
