from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get input times from the form
        time_entries = request.form.getlist('time_entries')  # Expecting a list of in and out times

        total_time_spent = timedelta()

        for entry in time_entries:
            in_time_str, out_time_str = entry.split(',')

            # Convert the times to datetime objects
            in_time = datetime.strptime(in_time_str.strip(), '%H:%M:%S')
            out_time = datetime.strptime(out_time_str.strip(), '%H:%M:%S')

            # Validate the times
            if out_time < in_time: 
                return jsonify({"error": f"Out time {out_time_str} cannot be earlier than In time {in_time_str}!"})

            # Accumulate the time difference
            total_time_spent += (out_time - in_time)

        # Convert the total timedelta to hours, minutes, and seconds
        total_seconds = total_time_spent.total_seconds()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return jsonify({
            "total_hours": int(hours),
            "total_minutes": int(minutes),
            "total_seconds": int(seconds)
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

# alerting for completing 8 hrs . 


