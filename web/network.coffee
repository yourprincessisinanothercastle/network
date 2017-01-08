connection = null
method = "ticket"

getConnection = (user, pass) ->
    onchallenge = (session, method, extra) ->
        console.log("onchallenge", method, extra);
        if (method == "ticket")
           return pass;
        else
           throw "don't know how to authenticate using '" + method + "'";


    connection = new autobahn.Connection({
        url: 'ws://127.0.0.1:8080/ws',
        realm: 'realm1',
        authmethods: ["ticket"],
        authid: user,
        onchallenge: onchallenge
    });

    connection.onopen = (session, details) ->
        console.log("connected session with ID " + session.id);
        console.log("authenticated using method '"
          + details.authmethod + "' and provider '"
          + details.authprovider + "'");
        console.log("authenticated with authid '"
          + details.authid + "' and authrole '"
          + details.authrole + "'");

    connection.onclose = (reason, details) ->
        console.log("disconnected", reason, details.reason, details);

    connection.open();

