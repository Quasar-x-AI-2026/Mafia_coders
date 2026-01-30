import logging
from livekit.agents import function_tool, RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

# -----------------------
# Existing Tools
# -----------------------

@function_tool()
async def get_weather(context: RunContext, city: str) -> str:
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather for {city}: {response.text.strip()}")
            return response.text.strip()
        return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Error retrieving weather for {city}: {e}")
        return f"An error occurred while retrieving weather for {city}."

@function_tool()
async def search_web(context: RunContext, query: str) -> str:
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."

@function_tool()
async def send_email(context: RunContext, to_email: str, subject: str, message: str, cc_email: Optional[str] = None) -> str:
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")

        if not gmail_user or not gmail_password:
            logging.error("Gmail credentials not found")
            return "Email sending failed: Gmail credentials not configured."

        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject
        recipients = [to_email]
        if cc_email:
            msg['Cc'] = cc_email
            recipients.append(cc_email)
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipients, msg.as_string())
        server.quit()

        logging.info(f"Email sent successfully to {to_email}")
        return f"Email sent successfully to {to_email}"

    except smtplib.SMTPAuthenticationError:
        logging.error("Gmail authentication failed")
        return "Email sending failed: Authentication error."
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
        return f"Email sending failed: SMTP error - {str(e)}"
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return f"An error occurred while sending email: {str(e)}"

# -----------------------
# New Real-Time Search Tools
# -----------------------

@function_tool()
async def genmini_search(context: RunContext, query: str) -> str:
    """
    Query GenMini API for real-time results.
    """
    try:
        api_key = os.getenv("GENMINI_API_KEY")
        if not api_key:
            return "GenMini API key not configured."

        response = requests.get(
            "https://api.genmini.ai/search",
            params={"q": query},
            headers={"Authorization": f"Bearer {api_key}"}
        )

        if response.status_code == 200:
            result = response.json().get("answer", "")
            logging.info(f"GenMini result for '{query}': {result}")
            return result or "No result from GenMini."
        return f"GenMini search failed with status {response.status_code}"

    except Exception as e:
        logging.error(f"GenMini search error: {e}")
        return f"GenMini search failed: {str(e)}"

@function_tool()
async def groque_search(context: RunContext, query: str) -> str:
    """
    Query Groque API for real-time results.
    """
    try:
        api_key = os.getenv("GROQUE_API_KEY")
        if not api_key:
            return "Groque API key not configured."

        response = requests.get(
            "https://api.groque.ai/query",
            params={"q": query},
            headers={"Authorization": f"Bearer {api_key}"}
        )

        if response.status_code == 200:
            result = response.json().get("answer", "")
            logging.info(f"Groque result for '{query}': {result}")
            return result or "No result from Groque."
        return f"Groque search failed with status {response.status_code}"

    except Exception as e:
        logging.error(f"Groque search error: {e}")
        return f"Groque search failed: {str(e)}"

@function_tool()
async def search_real_time(context: RunContext, query: str) -> str:
    """
    Perform a meta search using GenMini and Groque, and return the best result.
    """
    try:
        genmini_result = await genmini_search(context, query)
        groque_result = await groque_search(context, query)

        # Simple heuristic: pick the longer, non-empty result
        results = [genmini_result, groque_result]
        results = [r for r in results if r and "failed" not in r.lower()]
        if not results:
            return "No real-time results available."

        best_result = max(results, key=len)
        logging.info(f"Meta search for '{query}': {best_result}")
        return best_result

    except Exception as e:
        logging.error(f"Meta search error: {e}")
        return f"Real-time search failed: {str(e)}"
