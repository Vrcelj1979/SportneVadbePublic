from flask import Flask

from cron.remove_deleted_users import remove_deleted_users_cron
from handlers.admin import users
from handlers.profile.auth import logout
from handlers.public import business_users as public_business_users
from handlers.public import sports_providers as public_sports_providers
from handlers.public import contact as public_contact
from handlers.public import main as public_main, auth
from handlers.profile import main as profile_main
from tasks.send_email_task import send_email_via_sendgrid
from utils.check_environment import is_local
from utils.fake_data import load_fake_data

app = Flask(__name__)

# PUBLIC URLS
app.add_url_rule(rule="/", endpoint="public.main.index", view_func=public_main.index, methods=["GET"])
app.add_url_rule(rule="/business_users", endpoint="public.business_users.index", view_func=public_business_users.index, methods=["GET"])
app.add_url_rule(rule="/sports_providers", endpoint="public.sports_providers.index", view_func=public_sports_providers.index, methods=["GET"])
app.add_url_rule(rule="/contact", endpoint="public.contact.index", view_func=public_contact.index, methods=["GET"])

# PUBLIC auth
app.add_url_rule(rule="/init", endpoint="public.auth.init", view_func=auth.init, methods=["GET", "POST"])
app.add_url_rule(rule="/register", endpoint="public.auth.register", view_func=auth.register, methods=["GET", "POST"])
app.add_url_rule(rule="/login", endpoint="public.auth.login", view_func=auth.login, methods=["GET", "POST"])
app.add_url_rule(rule="/magic-login-token/<token>", view_func=auth.validate_magic_login_link, methods=["GET"])
app.add_url_rule(rule="/login-password", endpoint="public.auth.login_password", view_func=auth.login,
                 methods=["GET", "POST"])


# PROFILE URLS
app.add_url_rule(rule="/profile", endpoint="profile.main.sessions_list", view_func=profile_main.sessions_list,
                 methods=["GET"])
app.add_url_rule(rule="/profile/session/delete", endpoint="profile.main.session_delete",
                 view_func=profile_main.session_delete, methods=["POST"])

# PROFILE auth
app.add_url_rule(rule="/logout", endpoint="profile.auth.logout", view_func=logout, methods=["POST"])


# ADMIN URLS
app.add_url_rule(rule="/admin/users", endpoint="admin.users.users_list", view_func=users.users_list,
                 methods=["GET", "POST"])
app.add_url_rule(rule="/admin/user/<user_id>", endpoint="admin.users.user_details", view_func=users.user_details,
                 methods=["GET"])

# CRON JOBS
app.add_url_rule(rule="/cron/remove-deleted-users", view_func=remove_deleted_users_cron, methods=["GET"])

# TASKS
app.add_url_rule(rule="/tasks/send-email", endpoint="tasks.send_email_task.send_email_via_sendgrid",
                 view_func=send_email_via_sendgrid, methods=["POST"])

# LOAD FAKE DATA (localhost only!)
if is_local():
    app.add_url_rule(rule="/load-fake-data", view_func=load_fake_data, methods=["GET"])

if __name__ == '__main__':
    if is_local():
        app.run(port=8080, host="localhost", debug=True)  # localhost
    else:
        app.run(debug=False)  # production
