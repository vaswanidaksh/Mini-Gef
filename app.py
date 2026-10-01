import streamlit as st
from transformers import pipeline

# ... (keep the rest of your app.py code in cell [17])

import streamlit as st
from transformers import pipeline

def load_node():
  return pipeline(
    "zero-shot-classification",
    model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0"
    )
  

def score(text, levels, template="For support, {}."):
    probs = choice(text, levels, template)
    value = sum((levels.index(level) + 1) * p for level, p in probs.items())
    return round(value, 2)

def noul(text, yes, no, template="The customer is {}."):
    return choice(text, [yes, no], template)[yes]

# Do NOT paste: !pip lines, print(...) lines, classifier = pipeline(...), THRESHOLD.

# ==================== PASTE FROM COLAB: END ====================

if not all(name in globals() for name in ["choice", "noul", "score"]):
    st.error("Nothing pasted yet (or not all of it). Paste the three COPY THIS cells from Colab into app.py.")
    st.stop()

st.title("Mini-Jev: support inbox triage")
st.caption("A free, weaker imitation of Jev. It only decides, it never writes.")

message = st.text_area(
    "Customer message",
    "I was charged twice this month and nobody is answering."
)
threshold = st.slider("Auto-route only if at least this sure", 0.50, 0.99, 0.80)

if st.button("Decide"):
    route = choice(message, ROUTES)
    top, p = next(iter(route.items()))
    if p >= threshold:
        st.success(f"Auto-route to {top} ({p:.0%} sure)")
    else:
        st.warning(f"Send to a human. Best guess: {top}, only ({p:.0%} sure)")
        st.bar_chart(route)
        angry = noul(message, "angry or frustrated", "calm or happy")
        st.metric("How angry", f"{angry:.0%}")
        st.metric("How urgent (1 to 3)", score(message, URGENCY))
