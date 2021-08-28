<template>
  <div class="home">
    <input v-model="message" placeholder="edit me">
    <button @click.prevent="senddata(message)">Send Message</button>
    <button @click.prevent="sendjson(message)">Send JSON</button>
    <br />
    <button @click.prevent="joinroom()">Join Room</button>
    <button @click.prevent="leaveroom()">Leave Room</button>
    <br />
    <textarea v-model="servermsgs"></textarea>
  </div>
</template>

<script>
// @ is an alias to /src
import io from "socket.io-client";

export default {
  name: 'Home',
  data() {
    return {
      message: "Hello World!",
      socket: null,
      namedsocket: null,
      servermsgs: ""
    }
  },
  created() {
    this.socket = io.connect("http://192.168.1.157:44444");
    this.socket.on("connect", () => {
      //console.log(fetcheddata);
      this.servermsgs = this.servermsgs + "Connected with sid: " + this.socket.id + "\n";
    });

    this.socket.on("connectevent", fetcheddata => {
      //console.log(fetcheddata);
      this.servermsgs = this.servermsgs + fetcheddata['data'] + ": " + fetcheddata['sid'] + "\n";
    });

    this.socket.on("message", fetcheddata => {
      //console.log(fetcheddata);
      this.servermsgs = this.servermsgs + fetcheddata + "\n";
    });


    this.namedsocket = io.connect("http://192.168.1.157:44444/my_namespace");
    this.namedsocket.on("message", fetcheddata => {
      //console.log(fetcheddata);
      this.servermsgs = this.servermsgs + fetcheddata + "\n";
    });
  },
  methods: {
    joinroom(){
      this.socket.emit("join");
    },
    leaveroom() {
      this.socket.emit("leave", {'msg': 'testmsg'});
    },
    senddata(msg) {
      console.log("Sending: " + msg);
      this.socket.send(msg);
    },
    sendjson(msg) {
      console.log("JSONSending: " + msg);
      this.namedsocket.emit('json', msg);
    }
  }
}
</script>
