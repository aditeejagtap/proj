from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        time_entries = request.form.getlist('time_entries')

        total_time_spent = timedelta()

        for entry in time_entries:
            in_time_str, out_time_str = entry.split(',')

            in_time = datetime.strptime(in_time_str.strip(), '%H:%M:%S')
            out_time = datetime.strptime(out_time_str.strip(), '%H:%M:%S')

            if out_time < in_time: 
                return jsonify({"error": f"Out time {out_time_str} cannot be earlier than In time {in_time_str}!"})

            total_time_spent += (out_time - in_time)

        total_seconds = total_time_spent.total_seconds()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        response = {
            "total_hours": int(hours),
            "total_minutes": int(minutes),
            "total_seconds": int(seconds)
        }

        # Alert if total time reaches 8 hours
        if hours >= 8:
            response["alert"] = "You have completed 8 hours!"

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
