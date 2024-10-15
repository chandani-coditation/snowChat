from typing import Any, Dict

import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.version import VERSION


class SnowflakeConnection:
    """
    This class is used to establish a connection to Snowflake.

    Attributes
    ----------
    connection_parameters : Dict[str, Any]
        A dictionary containing the connection parameters for Snowflake.
    session : snowflake.snowpark.Session
        A Snowflake session object.

    Methods
    -------
    get_session()
        Establishes and returns the Snowflake connection session.

    """

    def __init__(self):
        self.connection_parameters = self._get_connection_parameters_from_env()
        self.session = None

    @staticmethod
    def _get_connection_parameters_from_env() -> Dict[str, Any]:
        connection_parameters = {
            "host": st.secrets["HOST"],
            "account": st.secrets["ACCOUNT"],
            "database": st.secrets["DATABASE"],
            "warehouse": st.secrets["WAREHOUSE"],
            "schema": st.secrets["SCHEMA"],
            "role": st.secrets["ROLE"],
            "authenticator": "oauth",
            "token": SnowflakeConnection._read_oauth_token()
        }
        return connection_parameters

    @staticmethod
    def _read_oauth_token() -> str:
        with open('/snowflake/session/token', 'r') as file:
            return file.read().strip()

    def get_session(self):
        """
        Establishes and returns the Snowflake connection session.
        Returns:
            session: Snowflake connection session.
        """
        if self.session is None:
            self.session = Session.builder.configs(self.connection_parameters).create()
            self.session.sql_simplifier_enabled = True
        return self.session