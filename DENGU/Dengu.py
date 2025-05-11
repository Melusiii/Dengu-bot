from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import random
import re

app = Flask(__name__)

# 🎯 Rich, specific local Q&A bank
qa_bank = {
    "saving": [
        "📌 Saving Tip: Save at least 10% of any money you get—e.g., $5 from $50. Use Ecocash to store it separately or use a piggy bank. Avoid daily impulse buys like street food or airtime you don’t need.",
        "💡 Try the envelope method: Create 'envelopes' for Transport, Food, Data, etc. Only use money from each for its purpose. That way, you can *visibly track* your spending habits.",
        "✅ Save in USD if possible. It's more stable than bond/RTGS. You can also use Mukuru Smart Save for short-term targets like buying a phone or paying school fees."
    ],
    "side hustle": [
        "🔥 Side Hustle Idea: Buy 2nd-hand clothes from Mbare, clean and resell them at school or online (WhatsApp statuses work!). Capital: $10–$20. Returns can double in 2–3 weeks.",
        "📲 Freelance: Offer Canva poster design for clubs or events, tutor high school kids on Zoom (especially in English or Math), or type CVs and assignments. All you need is bundles and a good phone.",
        "🍰 Bake & Sell: Start small with cupcakes or snacks on campus. $5 can get you enough to start. Partner with someone to split baking and selling tasks."
    ],
    "mobile money": [
        "📱 Use Ecocash to split spending: Have one account for day-to-day use, and another (or a friend you trust) as a savings wallet. Avoid Send Money fees by transferring via Merchant Pay if possible.",
        "⚠️ Avoid borrowing from apps like EcoCash Kashagi unless it’s life-or-death. Their interest adds up fast, and you lose control of your budget.",
        "✅ Link Ecocash to Mukuru: You can save USD separately or receive USD from diaspora family. Transfer only what you need to your main wallet."
    ],
    "invest": [
        "📈 Micro-Investment: Buy airtime bundles in bulk and resell to friends with a 10–20% markup. Easy to start with as little as $2. Keep records so you know your profit.",
        "🌱 Group Saving (Mukando): Start a 5-person group where each saves $5/month. One person gets $25 monthly on rotation. Use it to buy stock or cover emergencies.",
        "🎓 Skills Investment: Use free sites like Coursera or YouTube to learn Canva, Excel, or coding. Use the skill to earn. Invest time now = make money later."
    ],
    "budget": [
        "🧮 Budget Tip: Track all expenses daily. Use a notebook or a free app like 'AndroMoney'. Write even $0.50 for airtime. After 1 week, you’ll see where money leaks.",
        "🎯 50/30/20 Rule: Use 50% of your allowance for needs (food, transport), 30% for wants (data, snacks), and 20% for saving or investing. Adjust based on your exact income.",
        "💵 Always budget in USD if possible. Set limits: $10 for transport, $5 for data per week, etc. Never spend your emergency stash unless it’s *really* needed."
    ],
    "debt": [
        "⚖️ Avoid daily borrowing. If you *must* borrow, do it from trusted peers and keep the amount realistic (under $5) with a deadline. Build financial trust.",
        "❌ Don’t borrow for luxury (e.g., takeout, parties). Borrowing should be for needs—medical, school, transport when stuck. Otherwise, you get trapped.",
        "💬 If you're already in debt: List what you owe, prioritize small quick wins, and avoid taking on new debt while repaying."
    ]
}


# 🧠 Keyword-to-topic matcher
def match_topic(user_msg):
    patterns = {
        "saving": r"\bsave|saving|money|piggy bank\b",
        "side hustle": r"\bhustle|side hustle|extra cash|business|money making\b",
        "mobile money": r"\becocash|mukuru|wallet|transfer|send\b",
        "invest": r"\binvest|investment|profit|return|mukando\b",
        "budget": r"\bbudget|plan|expenses|track\b",
        "debt": r"\bborrow|debt|owe|loan\b"
    }

    for topic, pattern in patterns.items():
        if re.search(pattern, user_msg, re.IGNORECASE):
            return topic
    return None


# 💬 Flask Bot Route
@app.route("/whatsapp", methods=["POST"])
def bot():
    user_msg = request.form.get("Body", "").lower()
    topic = match_topic(user_msg)

    if topic:
        reply = random.choice(qa_bank[topic])
    else:
        reply = (
            "👋 Welcome to DENGU 🇿🇼\n"
            "Ask me about:\n"
            "💰 Saving tips\n"
            "📈 Side hustles\n"
            "📱 Mobile money\n"
            "🌱 Investing\n"
            "🧮 Budgeting\n"
            "⚖️ Handling debt\n"
            "Type something like: 'how can I save money as a student?'"
        )

    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
