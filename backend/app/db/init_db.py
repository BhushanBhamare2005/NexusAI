from sqlalchemy import inspect

from app.models.base import Base
from app.db.session import engine
# Import models so metadata registers them
from app.models import (  # noqa: F401
    merchant, customer, transaction, refund, ticket,
    approval, agent_run, audit_event, recovery_opportunity, user, notification_log,
    role_assignment_history,
)

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        columns = await conn.run_sync(
            lambda sync_conn: {
                column["name"]
                for column in inspect(sync_conn).get_columns("agent_runs")
            }
        )
        if "state_data" not in columns:
            await conn.exec_driver_sql(
                "ALTER TABLE agent_runs ADD COLUMN state_data JSON NOT NULL DEFAULT '{}'"
            )
        customer_columns = await conn.run_sync(
            lambda sync_conn: {
                column["name"]
                for column in inspect(sync_conn).get_columns("customers")
            }
        )
        if "sms_opt_in" not in customer_columns:
            await conn.exec_driver_sql(
                "ALTER TABLE customers ADD COLUMN sms_opt_in BOOLEAN NOT NULL DEFAULT FALSE"
            )
        if "sms_consent_source" not in customer_columns:
            await conn.exec_driver_sql(
                "ALTER TABLE customers ADD COLUMN sms_consent_source VARCHAR"
            )
        notification_columns = await conn.run_sync(
            lambda sync_conn: {
                column["name"]
                for column in inspect(sync_conn).get_columns("notification_logs")
            }
        )
        if "customer_id" not in notification_columns:
            await conn.exec_driver_sql(
                "ALTER TABLE notification_logs ADD COLUMN customer_id VARCHAR"
            )
        if "accepted" not in notification_columns:
            await conn.exec_driver_sql(
                "ALTER TABLE notification_logs ADD COLUMN accepted BOOLEAN NOT NULL DEFAULT FALSE"
            )
        user_columns = await conn.run_sync(
            lambda sync_conn: {
                column["name"]
                for column in inspect(sync_conn).get_columns("users")
            }
        )
        if "is_demo" not in user_columns:
            await conn.exec_driver_sql(
                "ALTER TABLE users ADD COLUMN is_demo BOOLEAN NOT NULL DEFAULT FALSE"
            )
        await conn.exec_driver_sql(
            "CREATE INDEX IF NOT EXISTS idx_users_is_demo ON users (is_demo)"
        )
