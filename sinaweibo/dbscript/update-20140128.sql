/* status 新增格式转化和内容扩展相关字段，favorite 新增收藏状态字段。 */

BEGIN;

alter table sinaweibo_status rename to temp_sinaweibo_status;
alter table sinaweibo_favorite rename to temp_sinaweibo_favorite;

CREATE TABLE "sinaweibo_status" (
    "id" bigint NOT NULL PRIMARY KEY,
    "raw_content" varchar(5000) NOT NULL,
    "parse_version" integer NOT NULL,
    "parsed_content" varchar(5000),
    "extra_info" text
);

CREATE TABLE "sinaweibo_favorite" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "sinaweibo_user" ("id"),
    "status_id" bigint NOT NULL REFERENCES "sinaweibo_status" ("id"),
    "tags" varchar(2000) NOT NULL,
    "fav_time" datetime NOT NULL,
    "is_archived" bool NOT NULL,
    "is_destroyed" bool NOT NULL
);

insert into sinaweibo_status(id, raw_content, parse_version) select id, content, 0 from temp_sinaweibo_status;

drop table temp_sinaweibo_status;

insert into sinaweibo_favorite select id, user_id, status_id, tags, fav_time, 0, 0 from temp_sinaweibo_favorite;

drop table temp_sinaweibo_favorite;

COMMIT;
