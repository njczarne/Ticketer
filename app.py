from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

ticket_count = 0        # total number of tickets issued
current_ticket = 0      # ticket currently being served (0 = none)
tickets = []            # list of dicts: {"number": int, "group": int, "completed": bool}


@app.route("/")
def home():
    return render_template("role_select.html")


@app.route("/student")
def student():
    return render_template("student.html", count=ticket_count, current=current_ticket)


@app.route("/professor")
def professor():
    return render_template("professor.html", count=ticket_count, current=current_ticket, tickets=tickets)


@socketio.on("request_ticket")
def handle_ticket_request(data):
    """
    Student requests a ticket. data contains {'group': int}.
    Behavior:
      - Always increment ticket_count and append ticket record.
      - If this is the first ticket ever (current_ticket == 0), set current_ticket = 1.
      - Do NOT auto-advance current_ticket in any other case.
      - Notify the requesting student of their ticket number & group.
      - Broadcast updated count, current ticket (may be unchanged), and dashboard.
    """
    global ticket_count, current_ticket, tickets
    ticket_count += 1
    group_number = data.get("group", None)

    tickets.append({"number": ticket_count, "group": group_number, "completed": False})

    # If no one is currently being served, start serving the first ticket
    if current_ticket == 0:
        current_ticket = 1

    # Send personal ticket back to the requesting student only
    emit("your_ticket", {"ticket_number": ticket_count, "group": group_number})

    # Broadcast updated state to everyone
    emit("update_count", {"count": ticket_count}, broadcast=True)
    emit("update_current_ticket", {"current": current_ticket}, broadcast=True)
    emit("update_dashboard", {"tickets": tickets}, broadcast=True)


@socketio.on("complete_ticket")
def handle_complete_ticket():
    """
    Professor completes the currently served ticket:
      - Mark the ticket with number == current_ticket as completed.
      - If there is a next ticket (current_ticket < ticket_count), advance current_ticket by 1.
      - Broadcast the updated current_ticket and dashboard.
    """
    global current_ticket, ticket_count, tickets

    # No-op if nothing is being served
    if current_ticket == 0:
        return

    # Mark the currently served ticket as completed
    for t in tickets:
        if t["number"] == current_ticket:
            t["completed"] = True
            break

    # Advance to next ticket only if one exists
    if current_ticket < ticket_count:
        current_ticket += 1
    # If current_ticket == ticket_count (last ticket), do NOT increment further.

    # Broadcast the new state
    emit("update_current_ticket", {"current": current_ticket}, broadcast=True)
    emit("update_dashboard", {"tickets": tickets}, broadcast=True)


@socketio.on("reset_system")
def handle_reset_system():
    """
    Reset everything to initial state and notify clients to clear student display too.
    """
    global ticket_count, current_ticket, tickets
    ticket_count = 0
    current_ticket = 0
    tickets = []

    emit("update_count", {"count": ticket_count}, broadcast=True)
    emit("update_current_ticket", {"current": current_ticket}, broadcast=True)
    emit("update_dashboard", {"tickets": tickets}, broadcast=True)
    emit("clear_student_ticket", {}, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
