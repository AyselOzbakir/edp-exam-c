from queue import Queue

class Event:
    def __init__(self, payload):
        self.payload = payload

class ApplicationSentEvent(Event):
    def __init__(self, payload):
        super().__init__(payload)

class ApplicationAcceptedEvent(Event):
    def __init__(self, payload):
        super().__init__(payload)

class ApplicationRejectedEvent(Event):
    def __init__(self, payload):
        super().__init__(payload)

class CommunicationQueue:
    def __init__(self):
        self.queue = Queue()

    def send_event(self, event):
        self.queue.put(event)

    def receive_event(self):
        if not self.queue.empty():
            return self.queue.get()
        return None

class Student:
    def __init__(self, name):
        self.name = name
        self.application_status = None

    def apply_to_university(self, university, queue):
        payload = {"student": self.name, "university": university.name}
        event = ApplicationSentEvent(payload)
        queue.send_event(event)
        print(f"{self.name} applied to {university.name}.")

    def receive_response(self, event):
        if isinstance(event, ApplicationAcceptedEvent):
            self.application_status = "Accepted"
            print(f"{self.name} received an acceptance letter from {event.payload['university']}.")
        elif isinstance(event, ApplicationRejectedEvent):
            self.application_status = "Rejected"
            print(f"{self.name} received a rejection letter from {event.payload['university']}.")

class University:
    def __init__(self, name):
        self.name = name

    def process_application(self, queue):
        event = queue.receive_event()
        if event and isinstance(event, ApplicationSentEvent):
            student_name = event.payload["student"]
            decision = "Accepted" if len(student_name) % 2 == 0 else "Rejected"
            if decision == "Accepted":
                response_event = ApplicationAcceptedEvent({"student": student_name, "university": self.name})
            else:
                response_event = ApplicationRejectedEvent({"student": student_name, "university": self.name})
            queue.send_event(response_event)
            print(f"{self.name} processed application for {student_name}. Decision: {decision}")

if __name__ == "__main__":
    queue = CommunicationQueue()

    student = Student("Alice")
    university = University("Tech University")

    student.apply_to_university(university, queue)
    university.process_application(queue)
    response_event = queue.receive_event()
    if response_event:
        student.receive_response(response_event)
