# Research Answers

## Question 1: HTTP State Preservation & Session Management

Word count requirement: 150–250 words.

The Hypertext Transfer Protocol (HTTP) is inherently stateless, meaning the web server treats every incoming request as an isolated transaction with no built-in memory of preceding interactions. Modern web applications overcome this limitation using session management mechanisms powered by HTTP cookies and server-side session stores. When a user authenticates by submitting credentials, the server validates them and generates a unique, cryptographically secure session identifier (session ID). This identifier is dispatched to the client's web browser inside a `Set-Cookie` HTTP response header. The browser automatically stores this cookie and attaches it to every subsequent outgoing request header targeted at the same domain. Upon receiving subsequent requests, the web server reads the session ID cookie and references its server-side session store—such as a relational database table like Django's `django_session`, a memory cache like Redis, or an encrypted cookie backend—to look up the corresponding user profile and authentication status. Through this handshake, the application maintains continuous user identity, permission levels, and state across cycles without transmitting sensitive credentials on every request. Security safeguards such as `HttpOnly` flags (preventing client-side JavaScript access to thwart Cross-Site Scripting), `Secure` flags (mandating HTTPS transmission), and `SameSite` attributes (defending against Cross-Site Request Forgery) ensure session cookies remain protected against interception and unauthorized tampering throughout the lifecycle of the user's active browsing session.

Word count: 214 words.

---

## Question 2: Django Database Migrations to MariaDB

Word count requirement: 150–250 words.

Migrating a Django project from the default local SQLite database to a production-grade server database like MariaDB involves a clear, procedural workflow. First, install the appropriate Python database adapter into your virtual environment, typically `mysqlclient` (or alternatively `pymysql`), alongside any necessary system development headers (`libmysqlclient-dev`). Next, connect to the MariaDB server via the administrative command line to provision a dedicated database and user account with explicit permissions: `CREATE DATABASE sticky_notes_db CHARACTER SET utf8mb4;` followed by granting full privileges to a secured user. Before switching database connections, export existing application records from SQLite into a serialized JSON fixture file by executing `python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > datadump.json`. Third, update the `DATABASES` dictionary in `settings.py` by switching `'ENGINE'` to `'django.db.backends.mysql'` and configuring `'NAME'`, `'USER'`, `'PASSWORD'`, `'HOST'`, and `'PORT'`. Once configured, execute `python manage.py makemigrations` to verify schema readiness, followed by `python manage.py migrate` to construct the entire schema—including built-in Django tables and application models—directly inside MariaDB. Finally, restore the preserved data by running `python manage.py loaddata datadump.json`. This completes the transition to a centralized, concurrent relational database system while preserving existing data integrity.

Word count: 188 words.
