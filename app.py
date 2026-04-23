from flask import Flask, render_template, request, redirect
from datetime import datetime
import csv
import os

app = Flask(__name__)

customers = []

@app.route('/')
def home():
    total = len(customers)
    at_risk = sum(1 for c in customers if "At Risk" in c['insight'])
    high_value = sum(1 for c in customers if "High Value" in c['insight'])

    return render_template('index.html', customers=customers,
                           total=total, at_risk=at_risk, high_value=high_value)


@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    days = int(request.form['days'])
    amount = int(request.form['amount'])
    review = request.form['review'].lower()

    # 🔹 Priority (fixed version)
    priority = max(0, amount - (days * 50))

    # 🔹 Behavior Insight + Membership
    if days > 30 and amount < 3000:
        insight = "⚠️ At Risk"
        suggestion = "Send discount offer"
        membership = "None"

    elif amount > 3000:
        insight = "💰 High Value"
        suggestion = "Give VIP rewards"
        membership = "🌟 VIP Member"

    elif days <= 10:
        insight = "🟢 Active"
        suggestion = "Recommend new arrivals"
        membership = "Regular"

    else:
        insight = "🟡 Regular"
        suggestion = "Engage with offers"
        membership = "Regular"

    # 🔹 Review Sentiment + Action (improved)
    if any(word in review for word in ["bad","slow","late","poor","worst"]):
        sentiment = "😡 Negative"
        action = "Call customer / fix issue"

    elif any(word in review for word in ["good","love","excellent","great"]):
        sentiment = "😊 Positive"
        action = "Send thank you message"

    else:
        sentiment = "😐 Neutral"
        action = "Monitor feedback"

    # 🔹 Store in memory
    customers.append({
        'name': name,
        'days': days,
        'amount': amount,
        'insight': insight,
        'sentiment': sentiment,
        'suggestion': suggestion,
        'membership': membership,
        'action': action,
        'priority': priority,
        'time': datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    # 🔹 SAVE TO CSV (correct place)
    file_exists = os.path.isfile('customers.csv')

    with open('customers.csv', 'a', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Name","Days","Amount","Insight","Sentiment","Membership","Action","Priority"])

        writer.writerow([name, days, amount, insight, sentiment, membership, action, priority])

    return redirect('/')


# 🗑 DELETE ROUTE
@app.route('/delete/<int:index>')
def delete(index):
    if index < len(customers):
        customers.pop(index)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)