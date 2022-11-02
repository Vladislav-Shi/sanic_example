from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "product" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "heading" VARCHAR(256) NOT NULL UNIQUE,
    "description" TEXT,
    "price" INT NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "create_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_product_create__a75639" ON "product" ("create_at");
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(32) NOT NULL UNIQUE,
    "is_admin" BOOL NOT NULL  DEFAULT False,
    "is_active" BOOL NOT NULL  DEFAULT False,
    "password" VARCHAR(256) NOT NULL,
    "create_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_user_create__31859c" ON "user" ("create_at");
CREATE TABLE IF NOT EXISTS "bill" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "balance" INT NOT NULL  DEFAULT 0,
    "create_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_bill_create__d033a2" ON "bill" ("create_at");
CREATE TABLE IF NOT EXISTS "transaction" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "value" INT,
    "after_balance" INT,
    "create_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(32) NOT NULL  DEFAULT 'process',
    "bill_id" INT NOT NULL REFERENCES "bill" ("id") ON DELETE CASCADE,
    "product_id" INT REFERENCES "product" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_transaction_create__c25c53" ON "transaction" ("create_at");
COMMENT ON COLUMN "transaction"."status" IS 'IN_PROCESS: process\nCOMPLETE: complete\nREJECTED: rejected\nERROR: error';
CREATE TABLE IF NOT EXISTS "verification" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "link" VARCHAR(256) NOT NULL,
    "create_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
