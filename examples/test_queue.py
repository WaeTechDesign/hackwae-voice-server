from services.queue.manager import queue_manager

job = queue_manager.create(
    text="Halo HackWae",
    voice="putri",
    engine="chatterbox",
)

print(job.id)

print(job.status)

print(queue_manager.get(job.id))

print(queue_manager.next())

print(queue_manager.list())
