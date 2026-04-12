### Manual PL/Perl Installation

Source: https://www.postgresql.org/docs/18/xplang-install.html

Example demonstrating the manual registration of the PL/Perl language components.

```sql
CREATE FUNCTION plperl_call_handler() RETURNS language_handler AS
    '$libdir/plperl' LANGUAGE C;
```

```sql
CREATE FUNCTION plperl_inline_handler(internal) RETURNS void AS
    '$libdir/plperl' LANGUAGE C STRICT;

CREATE FUNCTION plperl_validator(oid) RETURNS void AS
    '$libdir/plperl' LANGUAGE C STRICT;
```

```sql
CREATE TRUSTED LANGUAGE plperl
    HANDLER plperl_call_handler
    INLINE plperl_inline_handler
    VALIDATOR plperl_validator;
```

---

### Specify library path for preloading

Source: https://www.postgresql.org/docs/18/runtime-config-client.html

Example syntax for referencing a library within the standard installation directory.

```text
'$libdir/mylib'
```

---

### Set up type and extension for transform example

Source: https://www.postgresql.org/docs/18/sql-createtransform.html

Before creating a transform, ensure the data type and the procedural language extension are created. This example shows the setup for 'hstore' type and 'plpython3u' language.

```sql
CREATE TYPE hstore ...;

CREATE EXTENSION plpython3u;
```

---

### PostgreSQL 18 Build and Install Short Version

Source: https://www.postgresql.org/docs/18/install-meson.html

A concise sequence of commands for building and installing PostgreSQL 18 from source using Meson. This includes setup, compilation, installation, user creation, data directory setup, initialization, starting the server, creating a database, and connecting via psql.

```bash
meson setup build --prefix=/usr/local/pgsql
cd build
ninja
su
ninja install
adduser postgres
mkdir -p /usr/local/pgsql/data
chown postgres /usr/local/pgsql/data
su - postgres
/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
/usr/local/pgsql/bin/pg_ctl -D /usr/local/pgsql/data -l logfile start
/usr/local/pgsql/bin/createdb test
/usr/local/pgsql/bin/psql test
```

---

### Main Function for libpq Example

Source: https://www.postgresql.org/docs/18/libpq-example.html

The main entry point for the libpq program, handling connection setup, query execution, and result processing. It orchestrates the demonstration of parameterized queries.

```c
int
main(int argc, char **argv)
{
    const char *conninfo;
    PGconn     *conn;
    PGresult   *res;
    const char *paramValues[1];
    int         paramLengths[1];
    int         paramFormats[1];
    uint32_t    binaryIntVal;

    /*
     * If the user supplies a parameter on the command line, use it as the
     * conninfo string; otherwise default to setting dbname=postgres and using
     * environment variables or defaults for all other connection parameters.
     */
    if (argc > 1)
        conninfo = argv[1];
    else
        conninfo = "dbname = postgres";

    /* Make a connection to the database */
    conn = PQconnectdb(conninfo);

    /* Check to see that the backend connection was successfully made */
    if (PQstatus(conn) != CONNECTION_OK)
    {
        fprintf(stderr, "%s", PQerrorMessage(conn));
        exit_nicely(conn);
    }

    /* Set always-secure search path, so malicious users can't take control. */
    res = PQexec(conn, "SET search_path = testlibpq3");
    if (PQresultStatus(res) != PGRES_COMMAND_OK)
    {
        fprintf(stderr, "SET failed: %s", PQerrorMessage(conn));
        PQclear(res);
        exit_nicely(conn);
    }
    PQclear(res);

    /*
     * The point of this program is to illustrate use of PQexecParams() with
     * out-of-line parameters, as well as binary transmission of data.
     *
     * This first example transmits the parameters as text, but receives the
     * results in binary format.  By using out-of-line parameters we can avoid
     * a lot of tedious mucking about with quoting and escaping, even though
     * the data is text.  Notice how we don't have to do anything special with
     * the quote mark in the parameter value.
     */

    /* Here is our out-of-line parameter value */
    paramValues[0] = "joe's place";

    res = PQexecParams(conn,
                       "SELECT * FROM test1 WHERE t = $1",
                       1,       /* one param */
                       NULL,    /* let the backend deduce param type */
                       paramValues,
                       NULL,    /* don't need param lengths since text */
                       NULL,    /* default to all text params */
                       1);      /* ask for binary results */

    if (PQresultStatus(res) != PGRES_TUPLES_OK)
    {
        fprintf(stderr, "SELECT failed: %s", PQerrorMessage(conn));
        PQclear(res);
        exit_nicely(conn);
    }

    show_binary_results(res);

    PQclear(res);

    /*
     * In this second example we transmit an integer parameter in binary form,
     * and again retrieve the results in binary form.
     *
     * Although we tell PQexecParams we are letting the backend deduce
     * parameter type, we really force the decision by casting the parameter
     * symbol in the query text.  This is a good safety measure when sending
     * binary parameters.
     */

    /* Convert integer value "2" to network byte order */
    binaryIntVal = htonl((uint32_t) 2);

    /* Set up parameter arrays for PQexecParams */
    paramValues[0] = (char *) &binaryIntVal;
    paramLengths[0] = sizeof(binaryIntVal);
    paramFormats[0] = 1;        /* binary */

    res = PQexecParams(conn,
                       "SELECT * FROM test1 WHERE i = $1::int4",
                       1,       /* one param */
                       NULL,    /* let the backend deduce param type */
                       paramValues,
                       paramLengths,
                       paramFormats,
                       1);      /* ask for binary results */

    if (PQresultStatus(res) != PGRES_TUPLES_OK)
    {
        fprintf(stderr, "SELECT failed: %s", PQerrorMessage(conn));
        PQclear(res);
        exit_nicely(conn);
    }

    show_binary_results(res);

    PQclear(res);

    /* close the connection to the database and cleanup */
    PQfinish(conn);

    return 0;
}
```

---

### Install PostgreSQL Documentation

Source: https://www.postgresql.org/docs/18/install-make.html

Installs HTML and man page documentation.

```bash
make install-docs
```

---

### Variable Initialization Examples

Source: https://www.postgresql.org/docs/18/plpgsql-declarations.html

Examples of initializing variables with default values and constants.

```sql
quantity integer DEFAULT 32;
url varchar := 'http://mysite.com';
transaction_time CONSTANT timestamp with time zone := now();
```

---

### Install PostgreSQL World

Source: https://www.postgresql.org/docs/18/install-make.html

Installs the entire build including documentation.

```bash
make install-world
```

---

### Meson Setup with Custom Prefix

Source: https://www.postgresql.org/docs/18/install-meson.html

Configures the Meson build for PostgreSQL with a custom installation prefix. This allows specifying a non-default location for installed files.

```bash
meson setup build --prefix=/home/user/pg-install
```

---

### Create Publication for Replication

Source: https://www.postgresql.org/docs/18/logical-replication-subscription.html

Initial setup to create a publication that will be used by the replication examples.

```sql
/* pub # */ CREATE PUBLICATION pub1 FOR ALL TABLES;
```

---

### MOVE Command Examples

Source: https://www.postgresql.org/docs/18/plpgsql-cursors.html

Examples demonstrating cursor repositioning using different direction keywords.

```sql
MOVE curs1;
MOVE LAST FROM curs3;
MOVE RELATIVE -2 FROM curs4;
MOVE FORWARD 2 FROM curs4;
```

---

### Start Upgraded PostgreSQL Server

Source: https://www.postgresql.org/docs/18/logical-replication-upgrade.html

Start the newly upgraded PostgreSQL instance.

```bash
pg_ctl -D /opt/PostgreSQL/data1_upgraded start -l logfile
```

```bash
pg_ctl -D /opt/PostgreSQL/data2_upgraded start -l logfile
```

```bash
pg_ctl -D /opt/PostgreSQL/data3_upgraded start -l logfile
```

---

### Default Partition Example

Source: https://www.postgresql.org/docs/18/sql-createtable.html

Example of creating a default partition for a 'cities' table.

````APIDOC
## CREATE TABLE cities_partdef

### Description
Creates a default partition named 'cities_partdef' for the 'cities' table.

### Method
SQL

### Endpoint
N/A

### Parameters
#### Path Parameters
N/A

#### Query Parameters
N/A

#### Request Body
N/A

### Request Example
```sql
CREATE TABLE cities_partdef
    PARTITION OF cities DEFAULT;
````

### Response

#### Success Response (200)

N/A

#### Response Example

N/A

````

--------------------------------

### FETCH Command Examples

Source: https://www.postgresql.org/docs/18/plpgsql-cursors.html

Examples demonstrating various directions and target assignments for the FETCH command.

```sql
FETCH curs1 INTO rowvar;
FETCH curs2 INTO foo, bar, baz;
FETCH LAST FROM curs3 INTO x, y;
FETCH RELATIVE -2 FROM curs4 INTO x;
````

---

### Solaris init.d Script for PostgreSQL

Source: https://www.postgresql.org/docs/18/server-start.html

Example of an init script for Solaris to start the PostgreSQL server. It uses `su` to run `pg_ctl start` as the `postgres` user and specifies log and data directories.

```bash
su - postgres -c "/usr/local/pgsql/bin/pg_ctl start -l logfile -D /usr/local/pgsql/data"
```

---

### Install PostgreSQL World Binaries

Source: https://www.postgresql.org/docs/18/install-make.html

Installs the world build excluding documentation.

```bash
make install-world-bin
```

---

### List Partitioning Example

Source: https://www.postgresql.org/docs/18/sql-createtable.html

Example of creating a partition for a 'cities' table based on a list of values.

````APIDOC
## CREATE TABLE cities_ab

### Description
Creates a partition named 'cities_ab' for the 'cities' table, containing values 'a' and 'b', with a check constraint on 'city_id'.

### Method
SQL

### Endpoint
N/A

### Parameters
#### Path Parameters
N/A

#### Query Parameters
N/A

#### Request Body
N/A

### Request Example
```sql
CREATE TABLE cities_ab
    PARTITION OF cities (
    CONSTRAINT city_id_nonzero CHECK (city_id != 0)
) FOR VALUES IN ('a', 'b');
````

### Response

#### Success Response (200)

N/A

#### Response Example

N/A

````

--------------------------------

### Hash Partitioning Example

Source: https://www.postgresql.org/docs/18/sql-createtable.html

Example of creating partitions for an 'orders' table using hash partitioning.

```APIDOC
## CREATE TABLE orders_p1

### Description
Creates a hash partition 'orders_p1' for the 'orders' table with a modulus of 4 and remainder of 0.

### Method
SQL

### Endpoint
N/A

### Parameters
#### Path Parameters
N/A

#### Query Parameters
N/A

#### Request Body
N/A

### Request Example
```sql
CREATE TABLE orders_p1 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE orders_p2 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE orders_p3 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE orders_p4 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);
````

### Response

#### Success Response (200)

N/A

#### Response Example

N/A

````

--------------------------------

### Prepare a Transaction Example

Source: https://www.postgresql.org/docs/18/sql-prepare-transaction.html

An example of preparing the current transaction using the identifier 'foobar'.

```sql
PREPARE TRANSACTION 'foobar';
````

---

### List Partitioning with Sub-partitioning Example

Source: https://www.postgresql.org/docs/18/sql-createtable.html

Example of creating a list-partitioned table that is further partitioned by range.

````APIDOC
## CREATE TABLE cities_ab_10000_to_100000

### Description
Creates a sub-partition 'cities_ab_10000_to_100000' for the 'cities_ab' table, partitioning by population range from 10000 to 100000.

### Method
SQL

### Endpoint
N/A

### Parameters
#### Path Parameters
N/A

#### Query Parameters
N/A

#### Request Body
N/A

### Request Example
```sql
CREATE TABLE cities_ab
    PARTITION OF cities (
    CONSTRAINT city_id_nonzero CHECK (city_id != 0)
) FOR VALUES IN ('a', 'b') PARTITION BY RANGE (population);

CREATE TABLE cities_ab_10000_to_100000
    PARTITION OF cities_ab FOR VALUES FROM (10000) TO (100000);
````

### Response

#### Success Response (200)

N/A

#### Response Example

N/A

````

--------------------------------

### WHENEVER Action Examples

Source: https://www.postgresql.org/docs/18/ecpg-sql-whenever.html

Various examples of setting actions for different SQL conditions.

```SQL
EXEC SQL WHENEVER NOT FOUND CONTINUE;
EXEC SQL WHENEVER NOT FOUND DO BREAK;
EXEC SQL WHENEVER NOT FOUND DO CONTINUE;
EXEC SQL WHENEVER SQLWARNING SQLPRINT;
EXEC SQL WHENEVER SQLWARNING DO warn();
EXEC SQL WHENEVER SQLERROR sqlprint;
EXEC SQL WHENEVER SQLERROR CALL print2();
EXEC SQL WHENEVER SQLERROR DO handle_error("select");
EXEC SQL WHENEVER SQLERROR DO sqlnotice(NULL, NONO);
EXEC SQL WHENEVER SQLERROR DO sqlprint();
EXEC SQL WHENEVER SQLERROR GOTO error_label;
EXEC SQL WHENEVER SQLERROR STOP;
````

---

### SIMILAR TO Usage Examples

Source: https://www.postgresql.org/docs/18/functions-matching.html

Examples demonstrating pattern matching behavior with SIMILAR TO.

```sql
'abc' SIMILAR TO 'abc'          _true_
'abc' SIMILAR TO 'a'            _false_
'abc' SIMILAR TO '%(b|d)%'      _true_
'abc' SIMILAR TO '(b|c)%'       _false_
'-abc-' SIMILAR TO '%\mabc\M%'  _true_
'xabcy' SIMILAR TO '%\mabc\M%'  _false_
```

---

### Start PostgreSQL Tutorial Session

Source: https://www.postgresql.org/docs/18/tutorial-sql-intro.html

Connect to your 'mydb' database using psql in single-step mode and load the 'basics.sql' tutorial script.

```bash
$ psql -s mydb

mydb=> \i basics.sql
```

---

### Get Execution Context with GET DIAGNOSTICS

Source: https://www.postgresql.org/docs/18/plpgsql-control-structures.html

This example demonstrates how to use the GET DIAGNOSTICS command with the PG_CONTEXT item to retrieve the current call stack information within a PL/pgSQL function.

```plpgsql
CREATE OR REPLACE FUNCTION outer_func() RETURNS integer AS $$
BEGIN
  RETURN inner_func();
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION inner_func() RETURNS integer AS $$
DECLARE
  stack text;
BEGIN
  GET DIAGNOSTICS stack = PG_CONTEXT;
  RAISE NOTICE E'--- Call Stack ---
%', stack;
  RETURN 1;
END;
$$ LANGUAGE plpgsql;

SELECT outer_func();
```

---

### Short Version Installation Procedure

Source: https://www.postgresql.org/docs/18/install-make.html

A quick-start sequence for configuring, building, and initializing a PostgreSQL instance.

```shell
./configure
make
su
make install
adduser postgres
mkdir -p /usr/local/pgsql/data
chown postgres /usr/local/pgsql/data
su - postgres
/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
/usr/local/pgsql/bin/pg_ctl -D /usr/local/pgsql/data -l logfile start
/usr/local/pgsql/bin/createdb test
/usr/local/pgsql/bin/psql test
```

---

### Ignore Harmless sepgsql Installation Notifications

Source: https://www.postgresql.org/docs/18/sepgsql.html

Example of harmless warning messages that may appear during the installation process depending on the SELinux policy version.

```text
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 33 has invalid object type db_blobs
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 36 has invalid object type db_language
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 37 has invalid object type db_language
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 38 has invalid object type db_language
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 39 has invalid object type db_language
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 40 has invalid object type db_language
```

---

### Create a user mapping example

Source: https://www.postgresql.org/docs/18/sql-createusermapping.html

Example of mapping the user 'bob' to the foreign server 'foo' with specific credentials.

```sql
CREATE USER MAPPING FOR bob SERVER foo OPTIONS (user 'bob', password 'secret');
```

---

### Return composite types using array get

Source: https://www.postgresql.org/docs/18/pltcl-functions.html

Example using the Tcl array get command to construct the result list for a composite return type.

```sql
CREATE FUNCTION raise_pay(employee, delta int) RETURNS employee AS $$
    set 1(salary) [expr {$1(salary) + $2}]
    return [array get 1]
$$ LANGUAGE pltcl;
```

---

### PL/pgSQL Exception Handler with GET STACKED DIAGNOSTICS

Source: https://www.postgresql.org/docs/18/plpgsql-control-structures.html

An example of a PL/pgSQL exception handler that uses GET STACKED DIAGNOSTICS to capture the message text, detail, and hint of an exception.

```plpgsql
DECLARE
  text_var1 text;
  text_var2 text;
  text_var3 text;
BEGIN
  -- some processing which might cause an exception
  ...
EXCEPTION WHEN OTHERS THEN
  GET STACKED DIAGNOSTICS text_var1 = MESSAGE_TEXT,
                          text_var2 = PG_EXCEPTION_DETAIL,
                          text_var3 = PG_EXCEPTION_HINT;
END;
```

---

### Example DTrace Script Output

Source: https://www.postgresql.org/docs/18/dynamic-trace.html

This is an example of the output generated when the DTrace script for transaction analysis is executed. It shows the counts for transaction starts, commits, and the total time in nanoseconds.

```text
# ./txn_count.d `pgrep -n postgres` or ./txn_count.d <PID>
^C

Start                                          71
Commit                                         70
Total time (ns)                        2312105013


```

---

### GET /system/views/pg_available_extensions

Source: https://www.postgresql.org/docs/18/view-pg-available-extensions.html

Retrieves a list of all extensions available for installation in the current PostgreSQL database.

```APIDOC
## GET /system/views/pg_available_extensions

### Description
The `pg_available_extensions` view lists the extensions that are available for installation. This view is read-only.

### Method
GET

### Response
#### Success Response (200)
- **name** (name) - Extension name
- **default_version** (text) - Name of default version, or NULL if none is specified
- **installed_version** (text) - Currently installed version of the extension, or NULL if not installed
- **comment** (text) - Comment string from the extension's control file
```

---

### Define Composite Type for Examples

Source: https://www.postgresql.org/docs/18/plpython-data.html

Setup for demonstrating composite type return values.

```sql
CREATE TYPE named_value AS (
  name   text,
  value  integer
);
```

---

### Create a database with default settings

Source: https://www.postgresql.org/docs/18/app-createdb.html

Creates a new database named demo using the default server settings.

```shell
$ **createdb demo**
```

---

### Define Composite Type and Table

Source: https://www.postgresql.org/docs/18/ecpg-variables.html

SQL setup required for the subsequent ECPG examples.

```sql
CREATE TYPE comp_t AS (intval integer, textval varchar(32));
CREATE TABLE t4 (compval comp_t);
INSERT INTO t4 VALUES ( (256, 'PostgreSQL') );
```

---

### Verify Backup with External Manifest

Source: https://www.postgresql.org/docs/18/app-pgverifybackup.html

This example demonstrates creating a base backup, moving its manifest file to a secure location, and then verifying the backup using the external manifest path.

```bash
$ pg_basebackup -h mydbserver -D /usr/local/pgsql/backup1234
```

```bash
$ mv /usr/local/pgsql/backup1234/backup_manifest /my/secure/location/backup_manifest.1234
```

```bash
$ pg_verifybackup -m /my/secure/location/backup_manifest.1234 /usr/local/pgsql/backup1234
```

---

### Start the PostgreSQL Server

Source: https://www.postgresql.org/docs/18/app-pg-ctl.html

Commands to initiate the server process with default or custom configurations.

```bash
$ **pg_ctl start**
```

```bash
$ **pg_ctl -o "-F -p 5433" start**
```

---

### Get Column Name Example

Source: https://www.postgresql.org/docs/18/libpq-exec.html

Illustrates how PQfname and PQfnumber work with different quoting and casing.

```c
PQfname(res, 0)              _foo_
PQfname(res, 1)              _BAR_
PQfnumber(res, "FOO")        _0_
PQfnumber(res, "foo")        _0_
PQfnumber(res, "BAR")        _-1_
PQfnumber(res, "\"BAR\"")    _1_
```

---

### Manage Multiple Database Connections Example

Source: https://www.postgresql.org/docs/18/ecpg-connect.html

An example program demonstrating how to connect to multiple databases, execute queries on specific connections using AT, switch the current connection, and disconnect.

```c
#include <stdio.h>

EXEC SQL BEGIN DECLARE SECTION;
    char dbname[1024];
EXEC SQL END DECLARE SECTION;

int
main()
{
    EXEC SQL CONNECT TO testdb1 AS con1 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL CONNECT TO testdb2 AS con2 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL CONNECT TO testdb3 AS con3 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    /* This query would be executed in the last opened database "testdb3". */
    EXEC SQL SELECT current_database() INTO :dbname;
    printf("current=%s (should be testdb3)\n", dbname);

    /* Using "AT" to run a query in "testdb2" */
    EXEC SQL AT con2 SELECT current_database() INTO :dbname;
    printf("current=%s (should be testdb2)\n", dbname);

    /* Switch the current connection to "testdb1". */
    EXEC SQL SET CONNECTION con1;

    EXEC SQL SELECT current_database() INTO :dbname;
    printf("current=%s (should be testdb1)\n", dbname);

    EXEC SQL DISCONNECT ALL;
    return 0;
}

```

```text
current=testdb3 (should be testdb3)
current=testdb2 (should be testdb2)
current=testdb1 (should be testdb1)


```

---

### Get Library Directory with pg_config

Source: https://www.postgresql.org/docs/18/libpq-build.html

Use pg_config to find the directory where the libpq library is installed.

```bash
$ pg_config --libdir
/usr/local/pgsql/lib

```

---

### Build and Install All Contrib Components

Source: https://www.postgresql.org/docs/18/contrib.html

Run these commands in the 'contrib' directory of a configured source tree to build and install all optional components. Ensure PostgreSQL is running for 'make installcheck'.

```bash
**make**
**make install**
```

---

### Create PostgreSQL Data Directory and Initialize

Source: https://www.postgresql.org/docs/18/creating-cluster.html

This sequence demonstrates creating the parent directory, setting ownership to the postgres user, and then initializing the data directory using initdb.

```bash
root# mkdir /usr/local/pgsql
```

```bash
root# chown postgres /usr/local/pgsql
```

```bash
root# su postgres
```

```bash
postgres$ initdb -D /usr/local/pgsql/data
```

---

### Apply Variable Conflict Resolution in a Function

Source: https://www.postgresql.org/docs/18/plpgsql-implementation.html

Example of setting the variable conflict resolution policy at the start of a function definition.

```sql
CREATE FUNCTION stamp_user(id int, comment text) RETURNS void AS $$
    #variable_conflict use_variable
    DECLARE
        curtime timestamp := now();
    BEGIN
        UPDATE users SET last_modified = curtime, comment = comment
          WHERE users.id = id;
    END;
$$ LANGUAGE plpgsql;
```

---

### Bin Timestamp to 15-Minute Intervals

Source: https://www.postgresql.org/docs/18/functions-datetime.html

Example of using date_bin to bin a timestamp into 15-minute intervals, starting from the origin '2001-01-01'.

```sql
SELECT date_bin('15 minutes', TIMESTAMP '2020-02-11 15:44:17', TIMESTAMP '2001-01-01');
```

---

### Dynamic Domain Transition Example

Source: https://www.postgresql.org/docs/18/sepgsql.html

Demonstrates switching security labels using sepgsql_setcon. Note that transitioning to a smaller privilege set is allowed, while transitioning back to a larger set is denied.

```sql
regression=# select sepgsql_getcon();
                    sepgsql_getcon
-------------------------------------------------------
 unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
(1 row)

regression=# SELECT sepgsql_setcon('unconfined_u:unconfined_r:unconfined_t:s0-s0:c1.c4');
 sepgsql_setcon
----------------
 t
(1 row)

regression=# SELECT sepgsql_setcon('unconfined_u:unconfined_r:unconfined_t:s0-s0:c1.c1023');
ERROR:  SELinux: security policy violation


```

---

### Create and Populate JSON Table

Source: https://www.postgresql.org/docs/18/functions-json.html

Initial setup for the examples, creating a table named my_films and inserting a nested JSON structure.

```sql
CREATE TABLE my_films ( js jsonb );

INSERT INTO my_films VALUES (
'{ "favorites" : [
   { "kind" : "comedy", "films" : [
     { "title" : "Bananas",
       "director" : "Woody Allen"},
     { "title" : "The Dinner Game",
       "director" : "Francis Veber" } ] },
   { "kind" : "horror", "films" : [
     { "title" : "Psycho",
       "director" : "Alfred Hitchcock" } ] },
   { "kind" : "thriller", "films" : [
     { "title" : "Vertigo",
       "director" : "Alfred Hitchcock" } ] },
   { "kind" : "drama", "films" : [
     { "title" : "Yojimbo",
       "director" : "Akira Kurosawa" } ] }
  ] }');
```

---

### Execute a prepared statement with parameters

Source: https://www.postgresql.org/docs/18/ecpg-sql-prepare.html

This example demonstrates preparing a statement with placeholders and then executing it using specific input descriptors.

```c
char *stmt = "SELECT * FROM test1 WHERE a = ? AND b = ?";

EXEC SQL ALLOCATE DESCRIPTOR outdesc;
EXEC SQL PREPARE foo FROM :stmt;

EXEC SQL EXECUTE foo USING SQL DESCRIPTOR indesc INTO SQL DESCRIPTOR outdesc;

```

---

### Forbid DDL commands with an event trigger

Source: https://www.postgresql.org/docs/18/sql-createeventtrigger.html

An example of creating a function and an associated event trigger to block DDL commands at the start of execution.

```sql
CREATE OR REPLACE FUNCTION abort_any_command()
  RETURNS event_trigger
 LANGUAGE plpgsql
  AS $$
BEGIN
  RAISE EXCEPTION 'command % is disabled', tg_tag;
END;
$$;

CREATE EVENT TRIGGER abort_ddl ON ddl_command_start
   EXECUTE FUNCTION abort_any_command();
```

---

### Meson Setup with OpenSSL Support

Source: https://www.postgresql.org/docs/18/install-meson.html

Configures the Meson build for PostgreSQL to include OpenSSL support. This requires the OpenSSL development libraries to be installed.

```bash
meson setup build -Dssl=openssl
```

---

### Get SSL Cipher in PostgreSQL

Source: https://www.postgresql.org/docs/18/sslinfo.html

Obtain the name of the cipher suite used for the SSL connection via the `ssl_cipher()` function. Example output: DHE-RSA-AES256-SHA.

```sql
SELECT ssl_cipher();
```

---

### Get SSL Version in PostgreSQL

Source: https://www.postgresql.org/docs/18/sslinfo.html

Retrieve the SSL protocol version used for the current connection with `ssl_version()`. Examples include TLSv1.0, TLSv1.2, and TLSv1.3.

```sql
SELECT ssl_version();
```

---

### SET CONNECTION Usage Examples

Source: https://www.postgresql.org/docs/18/ecpg-sql-set-connection.html

Demonstrates switching between established database connections using the SET CONNECTION command.

```SQL
EXEC SQL SET CONNECTION TO con2;
EXEC SQL SET CONNECTION = con1;
```

---

### Sample Session with execq Function

Source: https://www.postgresql.org/docs/18/spi-examples.html

Demonstrates various uses of the 'execq' function, including table creation, insertion, selection, and the impact of the row count limit. Also shows data visibility rules.

```sql
=> SELECT execq('CREATE TABLE a (x integer)', 0);
 execq
-------
     0
(1 row)

=> INSERT INTO a VALUES (execq('INSERT INTO a VALUES (0)', 0));
INSERT 0 1
=> SELECT execq('SELECT * FROM a', 0);
INFO:  EXECQ:  0    _-- inserted by execq_
 execq
-------
     2
(1 row)

=> SELECT execq('INSERT INTO a SELECT x + 2 FROM a RETURNING *', 1);
INFO:  EXECQ:  2    _-- returned by execq and inserted by upper INSERT_
 execq
-------
     1
(1 row)

=> SELECT execq('SELECT * FROM a', 10);
INFO:  EXECQ:  0
INFO:  EXECQ:  1
INFO:  EXECQ:  2

 execq
-------
     3              _-- 10 is the max value only, 3 is the real number of rows_
(1 row)

=> SELECT execq('INSERT INTO a SELECT x + 10 FROM a', 1);
 execq
-------
     3              _-- all rows processed; count does not stop it, because nothing is returned_
(1 row)

=> SELECT * FROM a;
 x
----
  0
  1
  2
 10
 11
 12
(6 rows)

=> DELETE FROM a;
DELETE 6
=> INSERT INTO a VALUES (execq('SELECT * FROM a', 0) + 1);
INSERT 0 1
=> SELECT * FROM a;
 x
---
 1                  _-- 0 (no rows in a) + 1_
(1 row)

=> INSERT INTO a VALUES (execq('SELECT * FROM a', 0) + 1);
INFO:  EXECQ:  1
INSERT 0 1
=> SELECT * FROM a;
 x
---
 1
 2                  _-- 1 (there was one row in a) + 1_
(2 rows)

_-- This demonstrates the data changes visibility rule._
_-- execq is called twice and sees different numbers of rows each time:_

=> INSERT INTO a SELECT execq('SELECT * FROM a', 0) * x FROM a;
INFO:  EXECQ:  1    _-- results from first execq_
INFO:  EXECQ:  2
INFO:  EXECQ:  1    _-- results from second execq_
INFO:  EXECQ:  2
INFO:  EXECQ:  2
INSERT 0 2
=> SELECT * FROM a;
 x
---
 1
 2
 2                  _-- 2 rows * 1 (x in first row)_
 6                  _-- 3 rows (2 + 1 just inserted) * 2 (x in second row)_
(4 rows)

```

---

### Get Background Worker PID

Source: https://www.postgresql.org/docs/18/bgworker.html

Polls the status of a background worker using its handle. Returns the PID if the worker is running, or indicates if it has not started or has stopped.

```c
GetBackgroundWorkerPid(_BackgroundWorkerHandle *handle, _pid_t *)

```

---

### Configure extension and library paths together

Source: https://www.postgresql.org/docs/18/runtime-config-client.html

Example of setting both extension and library paths to include nonstandard locations.

```text
extension_control_path = '/usr/local/share/postgresql:$system'
dynamic_library_path = '/usr/local/lib/postgresql:$libdir'
```

---

### Get Backend PIDs and Queries

Source: https://www.postgresql.org/docs/18/monitoring-stats.html

Retrieves the process IDs and current queries for all active backend processes. This example demonstrates using pg_stat_get_backend_idset() to iterate through active backends.

```sql
SELECT pg_stat_get_backend_pid(backendid) AS pid,
       pg_stat_get_backend_activity(backendid) AS query
FROM pg_stat_get_backend_idset() AS backendid;
```

---

### Compile PostgreSQL Tutorial Files

Source: https://www.postgresql.org/docs/18/tutorial-sql-intro.html

Navigate to the tutorial directory in the PostgreSQL source distribution and run 'make' to compile C files and create scripts for user-defined functions and types.

```bash
$ cd _..._/src/tutorial
$ make
```

---

### Get Top 10 Most Frequent Words using ts_stat

Source: https://www.postgresql.org/docs/18/textsearch-features.html

Example query using ts_stat to find the ten most frequent words in a document collection by ordering results by entry count and document count.

```sql
SELECT * FROM ts_stat('SELECT vector FROM apod')
ORDER BY nentry DESC, ndoc DESC, word
LIMIT 10;
```

---

### to_tsquery Usage Examples

Source: https://www.postgresql.org/docs/18/textsearch-controls.html

Examples demonstrating token normalization, weight labels, prefix matching, and thesaurus phrase handling.

```sql
SELECT to_tsquery('english', 'The & Fat & Rats');
  to_tsquery
---------------
 'fat' & 'rat'
```

```sql
SELECT to_tsquery('english', 'Fat | Rats:AB');
    to_tsquery
------------------
 'fat' | 'rat':AB
```

```sql
SELECT to_tsquery('supern:*A & star:A*B');
        to_tsquery
--------------------------
 'supern':*A & 'star':*AB
```

```sql
SELECT to_tsquery('''supernovae stars'' & !crab');
  to_tsquery
---------------
 'sn' & !'crab'
```

---

### Setup Partitioned Tables

Source: https://www.postgresql.org/docs/18/logical-replication-row-filter.html

Creates a partitioned table structure on both publisher and subscriber nodes.

```sql
/* pub # */ CREATE TABLE parent(a int PRIMARY KEY) PARTITION BY RANGE(a);
/* pub # */ CREATE TABLE child PARTITION OF parent DEFAULT;
```

```sql
/* sub # */ CREATE TABLE parent(a int PRIMARY KEY) PARTITION BY RANGE(a);
/* sub # */ CREATE TABLE child PARTITION OF parent DEFAULT;
```

---

### Get Database Object Comment by OID and Catalog in PostgreSQL

Source: https://www.postgresql.org/docs/18/functions-info.html

Retrieves the comment for a database object using its OID and the name of the system catalog it belongs to. Example: obj_description(123456, 'pg_class') retrieves the comment for a table with OID 123456.

```sql
obj_description(oid, name)
```

---

### Install tsm_system_rows Extension

Source: https://www.postgresql.org/docs/18/tsm-system-rows.html

Use this command to install the tsm_system_rows extension. This module is trusted and can be installed by non-superusers with CREATE privilege.

```sql
CREATE EXTENSION tsm_system_rows;
```

---

### Rename PostgreSQL installation directory

Source: https://www.postgresql.org/docs/18/pgupgrade.html

Use this command to move an existing non-version-specific installation directory to prevent interference with a new installation.

```bash
mv /usr/local/pgsql /usr/local/pgsql.old
```

---

### Full Procedure Example

Source: https://www.postgresql.org/docs/18/ecpg-sql-get-descriptor.html

A complete C program demonstrating the lifecycle of a descriptor, including allocation, fetching, and retrieval of result set information.

```C
int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    int  d_count;
    char d_data[1024];
    int  d_returned_octet_length;
EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO testdb AS con1 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL ALLOCATE DESCRIPTOR d;

    /* Declare, open a cursor, and assign a descriptor to the cursor  */
    EXEC SQL DECLARE cur CURSOR FOR SELECT current_database();
    EXEC SQL OPEN cur;
    EXEC SQL FETCH NEXT FROM cur INTO SQL DESCRIPTOR d;

    /* Get a number of total columns */
    EXEC SQL GET DESCRIPTOR d :d_count = COUNT;
    printf("d_count                 = %d\n", d_count);

    /* Get length of a returned column */
    EXEC SQL GET DESCRIPTOR d VALUE 1 :d_returned_octet_length = RETURNED_OCTET_LENGTH;
    printf("d_returned_octet_length = %d\n", d_returned_octet_length);

    /* Fetch the returned column as a string */
    EXEC SQL GET DESCRIPTOR d VALUE 1 :d_data = DATA;
    printf("d_data                  = %s\n", d_data);

    /* Closing */
    EXEC SQL CLOSE cur;
    EXEC SQL COMMIT;

    EXEC SQL DEALLOCATE DESCRIPTOR d;
    EXEC SQL DISCONNECT ALL;

    return 0;
}
```

---

### Create a database with specific connection and template parameters

Source: https://www.postgresql.org/docs/18/app-createdb.html

Creates a database named demo on a specific host and port using a template, displaying the underlying SQL command.

```shell
$ **createdb -p 5000 -h eden -T template0 -e demo**
CREATE DATABASE demo TEMPLATE template0;
```

---

### Using pgtypes Library for Date and Timestamp Calculations in C

Source: https://www.postgresql.org/docs/18/ecpg-pgtypes.html

This example demonstrates how to use the pgtypes library to perform date and timestamp calculations within a C program. It includes declaring date and timestamp variables, getting the current date, selecting data from a table, adding an interval to a timestamp, and converting the result to a string. Remember to free allocated character strings using PGTYPESchar_free.

```c
EXEC SQL BEGIN DECLARE SECTION;
   date date1;
   timestamp ts1, tsout;
   interval iv1;
   char *out;
EXEC SQL END DECLARE SECTION;

PGTYPESdate_today(&date1);
EXEC SQL SELECT started, duration INTO :ts1, :iv1 FROM datetbl WHERE d=:date1;
PGTYPEStimestamp_add_interval(&ts1, &iv1, &tsout);
out = PGTYPEStimestamp_to_asc(&tsout);
printf("Started + duration: %s\n", out);
PGTYPESchar_free(out);


```

---

### Create and Verify Base Backup

Source: https://www.postgresql.org/docs/18/app-pgverifybackup.html

This example first creates a base backup using pg_basebackup and then verifies its integrity using pg_verifybackup.

```bash
$ pg_basebackup -h mydbserver -D /usr/local/pgsql/data
```

```bash
$ pg_verifybackup /usr/local/pgsql/data
```

---

### CLOSE Command Example

Source: https://www.postgresql.org/docs/18/plpgsql-cursors.html

Example of closing a cursor to release resources.

```sql
CLOSE curs1;
```
