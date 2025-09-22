# 🎟️ Real-Time Ticket Queue System

A **real-time, multi-user ticketing system** built with **Flask + Flask-SocketIO**.
Students can join the queue by entering their group number and taking a ticket. Professors can view the queue, see group numbers, advance the current ticket, and reset the system. All updates propagate instantly to every connected user.

---

## ✨ Features

* 🔄 **Real-time updates** using WebSockets (no page refresh required)
* 🧑‍🎓 **Student view**

  * Enter a group number before taking a ticket
  * See your personal ticket number and the current ticket being served
  * Automatically cleared if professor resets the system
* 👩‍🏫 **Professor view**

  * See total ticket count and current ticket being served
  * Dashboard showing every ticket and its group number
  * Completed tickets turn **red**
  * **Complete Ticket** button advances to the next ticket
  * **Reset System** button clears all tickets and resets counters

---

## 📦 Installation

1. **Clone this repository** or copy the project files to your machine.

2. **Install dependencies**:

```bash
pip install flask flask-socketio
```

---

## ▶️ Running the Server

```bash
python app.py
```

By default, the server runs on port `5000`.

Go to the third IP address displayed. 

This IP address can be accessed by anyone on the same WiFi network as the server.

---

## 🖥️ Usage

### Step 1 — Choose Role

On the homepage, click either:

* **Student** — to access the ticket-taking screen
* **Professor** — to access the dashboard and controls

---

### Step 2 — Student Actions

1. Enter your **group number** in the "Group: \_\_\_" input field.
2. Click **Take Ticket**.
3. You’ll see:

   * Your personal ticket number
   * Total tickets taken so far
   * Current ticket being served

---

### Step 3 — Professor Actions

1. See live **ticket count**, **current ticket**, and dashboard of all tickets.
2. Click **Complete Ticket** to mark the current ticket as served and move to the next one.
3. Click **Reset System** to clear the queue and reset counts (students are notified automatically).

---

## 🔄 How It Works (Behind the Scenes)

* The server tracks:

  * `ticket_count` (total tickets issued)
  * `current_ticket` (ticket currently being served)
  * `tickets[]` (list of `{number, group, completed}` objects)
* Students taking tickets update `ticket_count` and add to the ticket list.
* The first ticket automatically sets `current_ticket = 1` (start serving).
* Professors completing tickets mark them as completed and advance `current_ticket` only if there are more tickets waiting.
* All changes are broadcast via Socket.IO so every connected client stays in sync.

---

## 🧪 Example Workflow

1. Student A (Group 5) takes first ticket → Ticket #1, current ticket = 1
2. Student B (Group 3) takes second ticket → Ticket #2, current ticket stays at 1
3. Professor clicks **Complete Ticket** → Ticket #1 marked red, current ticket = 2
4. Professor clicks **Complete Ticket** again → Ticket #2 marked red, current ticket = 2 (no more tickets left)
5. Student C takes a ticket → Ticket #3, current ticket stays at 2 until professor completes again
6. Professor clicks **Complete Ticket** → current ticket = 3, Ticket #3 now being served

---

## ⚠️ Notes

* Multiple students and professors can be connected at the same time — updates are broadcast to all.
* If the professor resets the system, all students’ ticket numbers are cleared and they must re-enter their group number to get a new ticket.
* This implementation uses in-memory storage (`tickets[]`, counters). If the server restarts, all data is lost — persistent storage can be added later if needed.


