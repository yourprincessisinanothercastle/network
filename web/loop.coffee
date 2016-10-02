loop_time = 1/60

tick = () ->
    # send collected events
    if events.length != 0
        console.log('sending ' + events.length + ' events')
    for event in events
        send(event)

    events = []

    # process events
    process_incoming()

    setTimeout(tick, loop_time);

# start ticking
tick()