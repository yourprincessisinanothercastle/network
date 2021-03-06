// Generated by CoffeeScript 1.9.3
var connection, getConnection, method;

connection = null;

method = "ticket";

getConnection = function(user, pass) {
  var onchallenge;
  onchallenge = function(session, method, extra) {
    console.log("onchallenge", method, extra);
    if (method === "ticket") {
      return pass;
    } else {
      throw "don't know how to authenticate using '" + method + "'";
    }
  };
  connection = new autobahn.Connection({
    url: 'ws://127.0.0.1:8080/ws',
    realm: 'realm1',
    authmethods: ["ticket"],
    authid: user,
    onchallenge: onchallenge
  });
  connection.onopen = function(session, details) {
    console.log("connected session with ID " + session.id);
    console.log("authenticated using method '", +details.authmethod + "' and provider '", +details.authprovider + "'");
    return console.log("authenticated with authid '", +details.authid + "' and authrole '", +details.authrole + "'");
  };
  connection.onclose = function(reason, details) {
    return console.log("disconnected", reason, details.reason, details);
  };
  return connection.open();
};

//# sourceMappingURL=network.js.map
