#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>
#include <sqlite3.h>
#include <string.h>

char *concat(char *s1, char *s2)
{
    char *result = malloc( strlen(s1) + strlen(s2) + 1);
    strcpy(result, s1);
    strcat(result, s2);
    return result;
}

static int print_row (void *data, int argc, char **argv, char **azColName) {
    int i;
    printf("%s: ", (char *) data);
    for (i = 0; i < argc; i++) {
        printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
    }
    printf("\n");
    return 0;
}

int main (int argc, char *argv[]) {
    sqlite3 *db;
    char *zErrMsg = 0;
    char *sql;
    int rc;

    struct passwd *pw = getpwuid(getuid());
    char *homedir = pw->pw_dir;
    char *db_path = concat(homedir, "/.chestnut/chestnut/models/chestnut.db");
    const char *data = "Callback function called";

    rc = sqlite3_open(db_path, &db);
    if (rc) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
    } else {
        fprintf(stderr, "Opened database successfully\n");
    }
    sql = "SELECT chestnut_index.id, chestnut_index.path \
           FROM chestnut_index \
           WHERE chestnut_index.path LIKE '\%model\%' \
           ORDER BY length(chestnut_index.path) \
           LIMIT 5";

    rc = sqlite3_exec(db, sql, print_row, "Callback function called", NULL);

    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        fprintf(stdout, "Operation done successfully\n");
    }

    sqlite3_close(db);

    return 0;
}
