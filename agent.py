import os
from dotenv import load_dotenv
from tools import optimize_route, predict_delay

# -------------------------------
# Load env
# -------------------------------
load_dotenv()

# -------------------------------
# SAFE GEMINI INIT (VERY IMPORTANT)
# -------------------------------
client = None

try:
    from google import genai

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        client = genai.Client(api_key=api_key)

except Exception:
    client = None


# -------------------------------
# FALLBACK INTENT DETECTION
# -------------------------------
def detect_intent(user_query):
    query = user_query.lower()

    route_keywords = [
        "route", "path", "optimize", "delivery",
        "shortest", "navigation", "distance"
    ]

    delay_keywords = [
        "delay", "late", "traffic", "time"
    ]

    if any(word in query for word in route_keywords):
        return "route"

    if any(word in query for word in delay_keywords):
        return "delay"

    return "route"  # default


# -------------------------------
# MAIN AGENT
# -------------------------------
def run_agent(user_query, locations=None):

    intent = None

    # -------------------------------
    # TRY GEMINI (ONLY IF AVAILABLE)
    # -------------------------------
    if client:
        try:
            prompt = f"""
            Classify the user intent into ONE word:
            route / delay / general

            Query: {user_query}
            """

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            intent = response.text.strip().lower()

        except Exception:
            intent = None

    # -------------------------------
    # FALLBACK (ALWAYS WORKS)
    # -------------------------------
    if not intent:
        intent = detect_intent(user_query)

    # -------------------------------
    # TOOL EXECUTION (MCP STYLE)
    # -------------------------------
    if "route" in intent:
        if not locations:
            return {"error": "Please provide locations"}

        return {"route": optimize_route(locations)}

    elif "delay" in intent:
        return {"delay": predict_delay("rain", "high")}

    else:
        # -------------------------------
        # GENERAL RESPONSE
        # -------------------------------
        if client:
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=user_query
                )
                return {"message": response.text}
            except Exception:
                pass

        return {"message": "General query (fallback mode)"}